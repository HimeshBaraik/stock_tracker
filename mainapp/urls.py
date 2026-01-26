from django.urls import path, include
from .views import StocksView

urlpatterns = [
    path('stocks/', StocksView.as_view(), name='stocks'),
]