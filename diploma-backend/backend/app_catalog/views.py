from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.core.paginator import Paginator
from shopapp.models import Category, Product
from shopapp.serializers import ProductSerializer

class CategoryAPIView(APIView):
    """
    Класс отвечающий за вывод категорий и подкатегорий товаров
    на кнопку "All Departments"
    """

    def get(self, request):
        categories = Category.objects.only('id', 'title', 'image')
        categories_data = []
        for category in categories:
            subcategories = category.subcategory_set.prefetch_related(
                'product_set'
            ).only('id', 'title', 'image')
            subcategories_data = []
            for subcategory in subcategories:
                data_sub = {
                    "id": subcategory.pk,
                    "title": subcategory.title,
                    "image": subcategory.get_image(),
                }
                subcategories_data.append(data_sub)
            data_cat = {
                "id": category.pk,
                "title": category.title,
                "image": category.get_image(),
                "subcategories": subcategories_data,
            }
            categories_data.append(data_cat)
        return JsonResponse(categories_data, safe=False)


class CatalogAPIView(APIView):
    """
    Класс отвечающий за вывод каталога товаров с фильтрацией и сортировкой.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'price': ['gte', 'lte'],
        'free_delivery': ['exact'],
        'count': ['gt'],
        'title': ['icontains'],
        'tags__name': ['exact'],
    }
    ordering_fields = [
        'id',
        'category__id',
        'price',
        'count',
        'date',
        'title',
        'free_delivery',
        'rating',
    ]

    def filter_queryset(self, products):
        category_id = self.request.GET.get('category')
        min_price = float(self.request.GET.get('filter[minPrice]', 0))
        max_price = float(self.request.GET.get('filter[maxPrice]', float('inf')))
        free_delivery = self.request.GET.get('filter[free_delivery]', '').lower() == 'true'
        available = self.request.GET.get('filter[available]', '').lower() == 'true'
        name = self.request.GET.get('filter[name]', '').strip()
        tags = self.request.GET.getlist('tags[]')
        sort_field = self.request.GET.get('sort', 'id')
        sort_type = self.request.GET.get('sortType', 'inc')

        if category_id:
            products = products.filter(category__id=category_id)
        products = products.filter(price__gte=min_price, price__lte=max_price)
        if free_delivery:
            products = products.filter(free_delivery=True)
        if available:
            products = products.filter(count__gt=0)
        if name:
            products = products.filter(title__icontains=name)
        for tag in tags:
            products = products.filter(tags__name=tag)
        if sort_type == 'inc':
            products = products.order_by(sort_field)
        else:
            products = products.order_by('-' + sort_field)

        return products

    def get(self, request):
        products = Product.objects.only('id', 'title', 'price', 'count', 'free_delivery', 'rating', 'category__id') \
            .select_related('category') \
            .prefetch_related('tags')
        filtered_products = self.filter_queryset(products)
        page_number = int(request.GET.get('currentPage', 1))
        limit = int(request.GET.get('limit', 20))
        paginator = Paginator(filtered_products, limit)
        page = paginator.get_page(page_number)
        products_list = []
        for product in page:
            products_list.append(ProductSerializer(product).data)
        catalog_data = {
            "items": products_list,
            "currentPage": page_number,
            "lastPage": paginator.num_pages
        }
        return Response(catalog_data)
