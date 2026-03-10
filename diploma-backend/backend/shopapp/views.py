import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from .models import (
    Category,
    Product,
    Review, Tag,
    Sale,
    Basket,
    BasketItem,
    Order,
    Payment,
    DeliveryPrices,
)
from .serializers import (
    ProductSerializer,
    DetailsSerializer,
    TagSerializer,
    BasketItemSerializer, OrderSerializer,

)

from app_users.models import UserProfile




class TagListAPIView(ListAPIView):
    """
    Класс отвечающий за вывод тегов к товару
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all().distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SalesListAPIView(APIView):
    """
    Класс обрабатывающий товары, попадающие под распродажу
    """
    def get(self, request):
        page_number = int(request.GET.get('currentPage', 1))
        limit = int(request.GET.get('limit', 20))
        obj_list = []
        for obj in Sale.objects.all():
            obj_list.append(obj)
        paginator = Paginator(obj_list, limit)
        page = paginator.get_page(page_number)
        serialized_data = []

        for sale in page:
            serialized_data.append({
                "id": sale.product.id,
                "price": sale.product.price,
                "salePrice": sale.product.price - sale.discount,
                "dateFrom": sale.date_from,
                "dateTo": sale.date_to,
                "title": sale.product.title,
                "images": [
                    {
                        "src": settings.MEDIA_URL + str(image.image),
                        "alt": sale.product.title,
                    }
                    for image in
                    sale.product.images.all()],
            })
        response_data = {
            "items": serialized_data,
            "currentPage": page_number,
            "lastPage": paginator.num_pages
        }
        return Response(response_data)








