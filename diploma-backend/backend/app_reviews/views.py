from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from app_users.models import UserProfile
from shopapp.models import Product, Review
from shopapp.serializers import DetailsSerializer


class ProductDetailsRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DetailsSerializer
    lookup_url_kwarg = "id"

class ProductReviewAPIView(ProductDetailsRetrieveAPIView):
    """
    Класс, обрабатывающий оставление пользователями отзывов о товаре
    """
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            product = Product.objects.get(pk=kwargs['id'])
            author = profile
            text = request.data['text']
            rate = request.data['rate']

            review = Review.objects.create(
                author=author,
                text=text,
                rate=rate,
                product=product,
            )
            review.save()
            return Response(status=200)
        return Response(status=403)
