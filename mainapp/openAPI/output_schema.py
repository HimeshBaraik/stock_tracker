from enum import Enum
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from .utils import *


class ExtendSchemaStructure(Enum):
    StockData = {
        "methods": ["POST"],
        "request": {
            "application/json": {
                "type": "object",
                "properties": {
                    "stocks": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "default": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"],
                        "description": "List of stock ticker symbols with .NS suffix for NSE stocks",
                        "example": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS"]
                    }
                },
                "required": ["stocks"]
            }
        },
        "responses": {
            200: OpenApiResponse(
                response=200,
                description="Stock data fetched successfully",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value=openAPIExamples.StockDataSuccess.value
                    ),
                    OpenApiExample(
                        "Partial Success (Some stocks failed)",
                        value=openAPIExamples.StockDataFetchError.value
                    )
                ]
            ),
            400: OpenApiResponse(
                response=400,
                description="Invalid request data or validation failed",
                examples=[
                    OpenApiExample(
                        "Validation Error - Missing Field",
                        value=openAPIExamples.StockDataValidationError.value
                    ),
                    OpenApiExample(
                        "Validation Error - Empty List",
                        value=openAPIExamples.StockDataEmptyListError.value
                    ),
                    OpenApiExample(
                        "Validation Error - Max Limit Exceeded",
                        value=openAPIExamples.StockDataMaxLimitError.value
                    )
                ]
            ),
        },
        "description": OpenAPIDescription.StockDataDescription.value
    }

