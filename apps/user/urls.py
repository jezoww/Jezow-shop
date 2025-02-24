from django.urls import path

from apps.user.views import IndexListView, RegisterCreateView, LoginFormView, AboutUsTemplateView, CartListView, \
    ProfileTemplateView, LogoutView, ProfileFormView, ChangeAddressView, HistoryListView, CreateOrderView, OrderView

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('about/', AboutUsTemplateView.as_view(), name='about'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('profile/', ProfileTemplateView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-data/', ProfileFormView.as_view(), name='update-profile'),
    path('update-address/', ChangeAddressView.as_view(), name='update-address'),
    path('history/', HistoryListView.as_view(), name='history'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('order/details/<int:pk>/', OrderView.as_view(), name='order-detail')
]