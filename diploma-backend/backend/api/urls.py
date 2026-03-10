from django.urls import path


from app_users.views import (
    SignInAPIView,
    SingOutAPIView,
    SignUpAPIView,
    ProfileAPIView,
    AvatarUpdateAPIView,
    ChangePasswordAPIView,
)

from app_catalog.views import CatalogAPIView, CategoryAPIView
from app_banners.views import BannerListAPIView
from app_products.views import PopularListAPIView, LimitedListAPIView
from app_reviews.views import ProductDetailsRetrieveAPIView, ProductReviewAPIView
from app_basket.views import BasketItemsAPIView
from app_orders.views import OrdersAPIView, OrderRegistrationAPIView, PaymentAPIView
from shopapp.views import TagListAPIView, SalesListAPIView


urlpatterns = [
    path("sign-in/", SignInAPIView.as_view()),
    path("sign-up/", SignUpAPIView.as_view()),
    path("sign-out", SingOutAPIView.as_view()),

    path("profile/", ProfileAPIView.as_view()),
    path('profile/avatar', AvatarUpdateAPIView.as_view(), name='avatar-update'),
    path('profile/password', ChangePasswordAPIView.as_view(), name='change-password'),

    path("categories", CategoryAPIView.as_view()),
    path("catalog", CatalogAPIView.as_view()),
    path('banners', BannerListAPIView.as_view()),

    path('products/popular', PopularListAPIView.as_view()),
    path('products/limited', LimitedListAPIView.as_view()),
    path('product/<int:id>', ProductDetailsRetrieveAPIView.as_view()),
    path('product/<int:id>/reviews', ProductReviewAPIView.as_view()),

    path('tags', TagListAPIView.as_view()),
    path('sales', SalesListAPIView.as_view()),
    path('basket', BasketItemsAPIView.as_view()),

    path('orders/', OrdersAPIView.as_view()),
    path('order/<int:order_id>', OrderRegistrationAPIView.as_view()),
    path('payment/<int:order_id>', PaymentAPIView.as_view()),

]