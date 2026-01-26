from django.urls import path, include
from .views import StocksView, websocket_test_view

urlpatterns = [
    path('stocks/', StocksView.as_view(), name='stocks'),
    path('ws-test/', websocket_test_view, name='websocket_test'),
]