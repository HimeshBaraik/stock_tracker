from rest_framework import serializers


class StockDataRequestSerializer(serializers.Serializer):
    """
    Serializer for validating stock data request
    """
    stocks = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        help_text="List of stock symbols (e.g., ['RELIANCE.NS', 'TCS.NS'])"
    )
    
    def validate_stocks(self, value):
        """
        Validate that stocks list is not empty and contains valid symbols
        """
        if not value:
            raise serializers.ValidationError("Stocks list cannot be empty.")
        
        if len(value) > 100:
            raise serializers.ValidationError("Maximum 100 stocks allowed per request.")
        
        # Validate each stock symbol format (basic validation)
        for stock in value:
            if not isinstance(stock, str) or not stock.strip():
                raise serializers.ValidationError(f"Invalid stock symbol: {stock}")
        
        return value

