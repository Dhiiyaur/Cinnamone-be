from django.urls import path
from .views import (
    ProductList,
    ProductDetail,
    addToCart,
    removeFromCart,
    UserCart,
    Checkout

)

# urlpatterns = [
    
#     path('product-list/', ProductList.as_view(), name = 'product-list'),
#     path('product-detail/', ProductDetail.as_view(), name = 'product-detail'),
#     path('user-cart/', UserCart.as_view(), name = 'user-cart'),
#     path('add-to-cart/', addToCart.as_view(), name = 'add-to-cart'),
#     path('update-cart-item/', removeFromCart.as_view(), name = 'update-cart-item'),
#     path('checkout/', Checkout.as_view(), name = 'checkout'),
# ]



urlpatterns = [
    
    path('product-list/', ProductList.as_view(), name = 'product-list'),
    path('product/', ProductDetail.as_view(), name = 'product-detail'),
    path('user-cart/', UserCart.as_view(), name = 'user-cart'),
    path('add-item/', addToCart.as_view(), name = 'add-to-cart'),
    path('remove-item/', removeFromCart.as_view(), name = 'update-cart-item'),
    path('checkout/', Checkout.as_view(), name = 'checkout'),
    
]
