from django.urls import path

from apps.product.views import ProductDetailView, ShopMenListView, ShopWomenListView, NewArrivalsListView, \
    BestProductsListView, AddToCartView, ProductDeleteView, OrderListView

urlpatterns = [
    path('detail/<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('shop-men/', ShopMenListView.as_view(), name='shop-men'),
    path('shop-women/', ShopWomenListView.as_view(), name='shop-women'),
    path('new-arrivals/', NewArrivalsListView.as_view(), name='new-arrivals'),
    path('best-products/', BestProductsListView.as_view(), name='best-products'),
    path('add-to-cart/<slug:slug>', AddToCartView.as_view(), name='add-to-cart'),
    path('delete-product/<slug:slug>', ProductDeleteView.as_view(), name='delete-product'),
    path('ordering/', OrderListView.as_view(), name='ordering'),
]