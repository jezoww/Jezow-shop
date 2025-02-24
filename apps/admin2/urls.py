from django.urls import path

from apps.admin2.views import OperatorPageListView, ChangeStatusOrderView, ChangeLocationOrderView

urlpatterns = [
    path('cnasdfhiuherfcrnfesrcfsdcfkjsadmfiowae/', OperatorPageListView.as_view(), name='operator'),
    path('change-status-order/<int:pk>', ChangeStatusOrderView.as_view(), name='change-status-order'),
    path('change-locaton-rder/<int:pk>', ChangeLocationOrderView.as_view(), name='change-location-order'),
]