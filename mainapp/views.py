from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .utilities import CommonService
from .tasks import fetch_stocks_data_task
from .serializers import StockDataRequestSerializer
from mainapp.openAPI.output_schema import ExtendSchemaStructure


# Create your views here.
class StocksView(APIView):
    authentication_classes = ()
    serializer_class = StockDataRequestSerializer
    api_path = reverse_lazy("stocks")

    @extend_schema(**ExtendSchemaStructure.StockData.value)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            # raise ExtendedValidationError(
            #     serializer.errors, request_id=self.request.request_id
            # )
            # For now, use standard validation error response
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        stocks_list = serializer.validated_data["stocks"]
        
        # Fetch stock data using Celery background task
        stocks_data = fetch_stocks_data_task.delay(stocks_list=stocks_list).get()
        
        response_data = {
            "count": len(stocks_data),
            "stocks": stocks_data
        }

        data = CommonService().default_response(request, response_data, self.api_path)    
        return Response(data, status=status.HTTP_200_OK)
