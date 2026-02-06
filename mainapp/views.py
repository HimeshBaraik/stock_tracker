from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .utilities import CommonService, StockDataService
from .serializers import StockDataRequestSerializer
from mainapp.openAPI.output_schema import ExtendSchemaStructure
from django.conf import settings
from pathlib import Path


# Create your views here.
class StocksView(APIView):
    authentication_classes = ()
    serializer_class = StockDataRequestSerializer
    api_path = reverse_lazy("stocks")

    @extend_schema(**ExtendSchemaStructure.StockData.value)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        stocks_list = serializer.validated_data["stocks"]
        stocks_data = StockDataService.fetch_stocks_data(stocks_list)
        
        response_data = {
            "count": len(stocks_data),
            "stocks": stocks_data
        }

        data = CommonService().default_response(request, response_data, self.api_path)    
        return Response(data, status=status.HTTP_200_OK)


def websocket_test_view(request):
    """Simple view to serve the WebSocket test page"""
    test_file = Path(settings.BASE_DIR) / 'websocket_test.html'
    with open(test_file, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/html')
