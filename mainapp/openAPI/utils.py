from enum import Enum


class openAPIExamples(Enum):
    """
    OpenAPI response examples
    """
    StockDataSuccess = {
        "status": "success",
        "data": {
            "count": 3,
            "stocks": [
                {
                    "symbol": "RELIANCE",
                    "ticker": "RELIANCE.NS",
                    "name": "Reliance Industries Ltd",
                    "current_price": 2450.50,
                    "previous_close": 2440.00,
                    "open": 2445.00,
                    "day_high": 2460.00,
                    "day_low": 2435.00,
                    "volume": 5000000,
                    "average_volume": 4500000,
                    "market_cap": 16500000000000,
                    "52_week_high": 2800.00,
                    "52_week_low": 2100.00,
                    "pe_ratio": 25.50,
                    "dividend_yield": 0.45,
                    "beta": 1.15,
                    "change": 10.50,
                    "change_percent": 0.43
                },
                {
                    "symbol": "TCS",
                    "ticker": "TCS.NS",
                    "name": "Tata Consultancy Services Ltd",
                    "current_price": 3850.75,
                    "previous_close": 3840.00,
                    "open": 3845.00,
                    "day_high": 3860.00,
                    "day_low": 3830.00,
                    "volume": 2000000,
                    "average_volume": 1800000,
                    "market_cap": 14000000000000,
                    "52_week_high": 4200.00,
                    "52_week_low": 3200.00,
                    "pe_ratio": 30.25,
                    "dividend_yield": 1.20,
                    "beta": 0.95,
                    "change": 10.75,
                    "change_percent": 0.28
                },
                {
                    "symbol": "HDFCBANK",
                    "ticker": "HDFCBANK.NS",
                    "name": "HDFC Bank Ltd",
                    "current_price": 1650.25,
                    "previous_close": 1645.00,
                    "open": 1648.00,
                    "day_high": 1660.00,
                    "day_low": 1640.00,
                    "volume": 8000000,
                    "average_volume": 7500000,
                    "market_cap": 12000000000000,
                    "52_week_high": 1800.00,
                    "52_week_low": 1500.00,
                    "pe_ratio": 18.50,
                    "dividend_yield": 0.80,
                    "beta": 1.05,
                    "change": 5.25,
                    "change_percent": 0.32
                }
            ]
        },
        "meta": {
            "timestamp": "2025-12-29T10:30:45.123456Z",
            "request_id": "a1b2c3d4e5f6g7h8i9j0",
            "version": "v1",
            "path": "localhost:8000/"
        }
    }

    StockDataValidationError = {
        "error": {
            "stocks": [
                "This field is required."
            ]
        }
    }

    StockDataEmptyListError = {
        "error": {
            "stocks": [
                "Stocks list cannot be empty."
            ]
        }
    }

    StockDataMaxLimitError = {
        "error": {
            "stocks": [
                "Maximum 100 stocks allowed per request."
            ]
        }
    }

    StockDataFetchError = {
        "status": "success",
        "data": {
            "count": 2,
            "stocks": [
                {
                    "symbol": "RELIANCE",
                    "ticker": "RELIANCE.NS",
                    "name": "Reliance Industries Ltd",
                    "current_price": 2450.50,
                    "previous_close": 2440.00,
                    "open": 2445.00,
                    "day_high": 2460.00,
                    "day_low": 2435.00,
                    "volume": 5000000,
                    "average_volume": 4500000,
                    "market_cap": 16500000000000,
                    "52_week_high": 2800.00,
                    "52_week_low": 2100.00,
                    "pe_ratio": 25.50,
                    "dividend_yield": 0.45,
                    "beta": 1.15,
                    "change": 10.50,
                    "change_percent": 0.43
                },
                {
                    "symbol": "INVALID",
                    "ticker": "INVALID.NS",
                    "error": "No data found for symbol INVALID"
                }
            ]
        },
        "meta": {
            "timestamp": "2025-12-29T10:30:45.123456Z",
            "request_id": "a1b2c3d4e5f6g7h8i9j0",
            "version": "v1",
            "path": "localhost:8000/"
        }
    }


class OpenAPIDescription(Enum):
    """
    OpenAPI endpoint descriptions
    """
    StockDataDescription = """
    Fetch real-time stock data for a list of NSE (National Stock Exchange) stocks using Yahoo Finance.
    
    This endpoint accepts a list of stock ticker symbols (with .NS suffix for NSE stocks) and returns 
    comprehensive stock information including:
    - Current price and previous close
    - Day's high/low and open price
    - Trading volume and average volume
    - Market capitalization
    - 52-week high/low
    - P/E ratio, dividend yield, and beta
    - Price change and percentage change
    
    **Note:** 
    - Maximum 100 stocks can be requested per API call
    - Stock symbols must include the .NS suffix (e.g., RELIANCE.NS, TCS.NS)
    - If a stock symbol is invalid or data is unavailable, an error will be included in the response for that specific stock
    - All stock data is fetched in parallel for optimal performance
    """

