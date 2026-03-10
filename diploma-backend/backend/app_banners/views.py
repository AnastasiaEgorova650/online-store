from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from shopapp.serializers import ProductSerializer
from shopapp.models import Product

class BannerListAPIView(ListAPIView):
    """
    Класс, отвечающий за вывод трех баннеров с продуктов с самым высоким рейтингом
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        return (
            Product.objects
            .filter(rating__gt=0)
            .order_by('-rating')[:3]
            .only(
                'id', 'title', 'price', 'rating', 'category__title', 'subcategory__title'
            )
            .select_related('category', 'subcategory')
            .prefetch_related('images')
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

