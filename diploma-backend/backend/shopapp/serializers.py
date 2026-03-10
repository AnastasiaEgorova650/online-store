from rest_framework import serializers

from .models import (
    Product, Review, Tag, Specification, BasketItem, Order
)


class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        reviews = Review.objects.filter(product_id=instance.id).values_list(
            "rate", flat=True
        )
        tags = Tag.objects.filter(tags__id=instance.id)
        if reviews.count() == 0:
            rating = "Пока нет отзывов"
        else:
            rating = sum(reviews) / reviews.count()
        rep['title'] = instance.title
        rep['price'] = instance.price
        rep['images'] = instance.get_image()
        rep['tags'] = [{"id": tag.pk, "name": tag.name} for tag in tags]
        rep['reviews'] = reviews.count()
        rep['rating'] = rating

        rep['id'] = instance.pk
        rep["category"] = instance.category.pk
        rep['count'] = instance.count
        rep['date'] = instance.date.strftime("%Y.%m.%d %H:%M")
        rep['description'] = instance.description
        rep['freeDelivery'] = instance.free_delivery
        return rep


class DetailsSerializer(ProductSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        specifications = Specification.objects.filter(pk=instance.id)
        reviews = Review.objects.filter(product_id=instance.id)

        rep['specifications'] = [{'name': spec.name, 'value': spec.value} for spec in specifications]
        rep['reviews'] = [
            {
                'author': f'{review.author.name} {review.author.surname}',
                'email': review.author.email,
                'text': review.text,
                'rate': review.rate,
                'date': review.date.strftime("%Y.%m.%d %H:%M"),
            }
            for review in reviews
        ]
        return rep


class TagSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="name")

    class Meta:
        model = Tag
        fields = "__all__"


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = "__all__"

    def to_representation(self, instance):
        data = ProductSerializer(instance.product).data
        data['count'] = instance.quantity
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        profile = instance.full_name
        products = instance.basket.baskets.all()
        data = {
            "id": instance.pk,
            "createdAt": instance.created_at.strftime("%Y.%m.%d %H:%M"),
            "fullName": f"{profile.surname} {profile.name} {profile.patronymic}",
            "email": profile.email,
            "phone": profile.phone,
            "deliveryType": instance.delivery_type,
            "paymentType": instance.payment_type,
            "totalCost": instance.total_cost,
            "status": instance.status,
            "city": instance.city,
            "address": instance.delivery_address,
            "products": [{
                "id": item.product.pk,
                "category": item.product.category.pk,
                "price": item.product.price,
                "count": item.product.count_of_orders,
                "data": item.product.date.strftime("%Y.%m.%d %H:%M"),
                "title": item.product.title,
                "description": item.product.description[:100],
                "freeDelivery": item.product.free_delivery,
                "images": item.product.get_image(),
                "tags": [{"id": tag.pk, "name": tag.name} for tag in item.product.tags.all()],
                "reviews": Review.objects.filter(product_id=item.product.id).count(),
                "rating": float(item.product.rating),
            } for item in products],
        }
        return data
