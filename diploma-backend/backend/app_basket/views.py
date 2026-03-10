from rest_framework.response import Response
from rest_framework.views import APIView
from shopapp.models import BasketItem, Product, Basket
from shopapp.serializers import BasketItemSerializer
from django.shortcuts import get_object_or_404

class BasketItemsAPIView(APIView):
    def get(self, request):
        """
        Вывод информации о товарах в корзине
        """
        if request.user.is_anonymous:
            session_cart = request.session.get('cart', {})
            if not session_cart:
                return Response({'message': 'Корзина пуста'}, status=200)

            items = []
            for pid, qty in session_cart.items():
                product = get_object_or_404(Product.objects.only('id', 'title', 'price'), id=pid)
                item = BasketItem(
                    product=product,
                    quantity=qty
                )
                items.append(item)

            serializer = BasketItemSerializer(items, many=True)
            return Response(serializer.data)

        queryset = BasketItem.objects.select_related('product').only(
            'product__id', 'product__title', 'product__price', 'quantity'
        ).filter(basket__user=request.user)

        if not queryset:
            return Response({'message': 'Корзина пуста'}, status=200)

        serializer = BasketItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            product_id = int(request.data.get('id'))
            count = int(request.data.get('count'))
        except (TypeError, ValueError):
            return Response({'error': 'Неверные данные'}, status=400)

        if request.user.is_anonymous:
            cart = request.session.get('cart', {})
            cart[str(product_id)] = cart.get(str(product_id), 0) + count
            request.session['cart'] = cart
            request.session.modified = True

            items = []
            for pid, qty in cart.items():
                product = get_object_or_404(Product.objects.only('id', 'title', 'price'), id=pid)
                item = BasketItem(
                    product=product,
                    quantity=qty
                )
                items.append(item)

            serializer = BasketItemSerializer(items, many=True)
            return Response(serializer.data, status=201)

        product = get_object_or_404(Product.objects.only('id', 'price', 'title'), id=product_id)
        basket, _ = Basket.objects.get_or_create(user=request.user)
        basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

        if not created:
            basket_item.quantity += count
            basket_item.save()

        basket_items = BasketItem.objects.select_related('product').only(
            'product__id', 'product__title', 'product__price', 'quantity'
        ).filter(basket=basket)

        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, status=201)

    def delete(self, request):
        try:
            product_id = int(request.data.get('id'))
            count = int(request.data.get('count'))
        except (TypeError, ValueError):
            return Response({'error': 'Неверные данные'}, status=400)

        if request.user.is_anonymous:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                if cart[str(product_id)] > count:
                    cart[str(product_id)] -= count
                else:
                    del cart[str(product_id)]
                request.session['cart'] = cart
                request.session.modified = True

            items = []
            for pid, qty in cart.items():
                product = get_object_or_404(Product.objects.only('id', 'title', 'price'), id=pid)
                item = BasketItem(
                    product=product,
                    quantity=qty
                )
                items.append(item)

            serializer = BasketItemSerializer(items, many=True)
            return Response(serializer.data)

        basket = get_object_or_404(Basket, user=request.user)
        try:
            basket_item = BasketItem.objects.get(basket=basket, product_id=product_id)
        except BasketItem.DoesNotExist:
            return Response({'error': 'Товар не найден в корзине'}, status=404)

        if basket_item.quantity > count:
            basket_item.quantity -= count
            basket_item.save()
        else:
            basket_item.delete()

        basket_items = BasketItem.objects.select_related('product').only(
            'product__id', 'product__title', 'product__price', 'quantity'
        ).filter(basket=basket)

        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data)











