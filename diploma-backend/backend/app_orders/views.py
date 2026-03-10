import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from shopapp.models import Order, DeliveryPrices, Product, BasketItem, Basket, Payment
from shopapp.serializers import OrderSerializer
from app_users.models import UserProfile


class OrdersAPIView(APIView):
    """
    Класс обрабатывающий создание заказа. Вывод истории заказов.
    """
    def get(self, request):
        """
        Данный метод отвечает за вывод истории заказов в меню профиля пользователя
        """
        orders = Order.objects.filter(archived=True).select_related(
            'full_name',
            'basket'
        ).only('id', 'total_cost', 'full_name__user__username', 'basket__id')

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Создается заказ из находящихся в корзине товаров, либо передается номер
        незакрытого заказа, для завершения оформления.
        """
        try:
            delivery_price = DeliveryPrices.objects.get(id=1)
            basket = request.user.basket
            profile = UserProfile.objects.get(user=request.user)
            basket_items = BasketItem.objects.filter(basket__user=request.user).select_related(
                'product'
            ).only('product__price', 'product__id', 'quantity')

            total_cost = 0
            active_order = Order.objects.filter(archived=False).first()
            if not active_order:
                order = Order.objects.create(full_name=profile, basket=basket)
                for item in basket_items:
                    product = item.product
                    product.count_of_orders = item.quantity
                    total_cost += item.product.price * item.quantity
                    product.save()
                if total_cost > delivery_price.delivery_free_minimum_cost:
                    order.total_cost = total_cost
                else:
                    order.total_cost = total_cost + delivery_price.delivery_cost
                order.save()
                response_data = {"orderId": order.pk}
                return JsonResponse(response_data)
            else:
                return JsonResponse({"orderId": active_order.pk})
        except Basket.DoesNotExist:
            error_data = {"error": "У данного пользователя пока нет 'корзины'"}
            return JsonResponse(error_data)


class OrderRegistrationAPIView(APIView):
    """
    Класс, обрабатывающий оформление заказа. Доставка. Оплата.
    """
    def get(self, request, order_id):
        order = Order.objects.select_related("full_name", "basket").prefetch_related("products").get(pk=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, order_id):
        order = get_object_or_404(
            Order.objects.select_related("full_name", "basket"),
            id=order_id
        )
        delivery_type = request.data["deliveryType"]
        payment_type = request.data["paymentType"]
        city = request.data["city"]
        address = request.data["address"]
        status_order = "подтвержден"
        print(delivery_type)
        if delivery_type == "express":
            delivery_price = DeliveryPrices.objects.only("delivery_express_cost").get(id=1)
            order.total_cost += delivery_price.delivery_express_cost
            order.save()

        order.delivery_type = delivery_type
        order.payment_type = payment_type
        order.city = city
        order.address = address
        order.status = status_order
        order.save()
        response_data = {"orderId": order.id}
        return Response(response_data, status=200)


class PaymentAPIView(APIView):
    """
    Класс, отвечающий за оплату заказа
    """
    def post(self, request, order_id):
        data = request.data
        card_number = data['number']
        expiration_month = data['month']
        expiration_year = data['year']
        current_year = datetime.datetime.now().year % 100

        if int(expiration_year) < current_year or (
                int(expiration_year == current_year) and
                int(expiration_month) < datetime.datetime.now().month):
            order = Order.objects.only("id").get(id=order_id)
            order.payment_error = "Payment expired"
            order.save()
            print("payment expired")
            return JsonResponse({"error": "Payment expired"})

        if not (len(card_number.strip()) <= 8 and int(card_number) % 2 == 0):
            print("card number invalid")
            return JsonResponse({"error": "Неверный номер банковской карты"})
        res_date = f"{expiration_month}.{expiration_year}"
        order = Order.objects.only("id").get(id=order_id)
        payment = Payment.objects.create(order=order, card_number=card_number, validity_period=res_date)
        order.status = 'оплачено'
        order.archived = True
        order.save()
        basket = Basket.objects.select_related("user").get(user=request.user)
        basket_items = BasketItem.objects.select_related("product").filter(basket=basket)
        for basket_item in basket_items:
            product = Product.objects.get(pk=basket_item.product.pk)
            product.count -= basket_item.quantity
            payment.success = True
            payment.save()
        basket_items.delete()
        return HttpResponse(status=200)
