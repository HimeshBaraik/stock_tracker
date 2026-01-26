import calendar
import pytz
from datetime import datetime, date
from django.utils import timezone
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed


class TimeUtility:
    """
    Utility class for time-related operations
    """
    
    @classmethod
    def time_in_IST(cls):
        """
        Returns time in IST
        """
        return timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def current_time(cls):
        """
        Returns current timezone-aware datetime
        """
        try:
            current_time = timezone.now()
        except Exception as error:
            print(error)
            current_time = None
        return current_time

    @classmethod
    def current_date(cls):
        """
        Returns current date
        """
        try:
            current_time = timezone.now().date()
        except Exception as error:
            print(error)
            current_time = None
        return current_time

    def get_current_datetime_endwith_z(self):
        """
        Method to get UTC date time in zulu format
        Returns: str - Current datetime in format 'YYYY-MM-DDTHH:MM:SSZ'
        """
        current_time = datetime.utcnow()
        utc_tz = pytz.timezone("UTC")
        current_time = utc_tz.localize(current_time)
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return formatted_time


class StockDataService:
    """
    Service class for fetching stock data
    """
    
    @staticmethod
    def fetch_stock_data(ticker):
        """Fetch stock data for a single ticker"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1d")
            
            # Get current price from history or info
            current_price = None
            if not hist.empty:
                current_price = float(hist['Close'].iloc[-1])
            elif 'currentPrice' in info:
                current_price = info.get('currentPrice')
            elif 'regularMarketPrice' in info:
                current_price = info.get('regularMarketPrice')
            
            stock_data = {
                "symbol": ticker.replace('.NS', ''),
                "ticker": ticker,
                "name": info.get('longName') or info.get('shortName', 'N/A'),
                "current_price": round(current_price, 2) if current_price else None,
                "previous_close": round(info.get('previousClose', 0), 2) if info.get('previousClose') else None,
                "open": round(info.get('open', 0), 2) if info.get('open') else None,
                "day_high": round(info.get('dayHigh', 0), 2) if info.get('dayHigh') else None,
                "day_low": round(info.get('dayLow', 0), 2) if info.get('dayLow') else None,
                "volume": info.get('volume', 0),
                "average_volume": info.get('averageVolume', 0),
                "market_cap": info.get('marketCap', 0),
                "52_week_high": round(info.get('fiftyTwoWeekHigh', 0), 2) if info.get('fiftyTwoWeekHigh') else None,
                "52_week_low": round(info.get('fiftyTwoWeekLow', 0), 2) if info.get('fiftyTwoWeekLow') else None,
                "pe_ratio": round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else None,
                "dividend_yield": round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else None,
                "beta": round(info.get('beta', 0), 2) if info.get('beta') else None,
                "change": round(current_price - info.get('previousClose', 0), 2) if current_price and info.get('previousClose') else None,
                "change_percent": round(((current_price - info.get('previousClose', 0)) / info.get('previousClose', 1)) * 100, 2) if current_price and info.get('previousClose') else None,
            }
            return stock_data
        except Exception as e:
            return {
                "symbol": ticker.replace('.NS', ''),
                "ticker": ticker,
                "error": str(e)
            }
    
    @staticmethod
    def fetch_stocks_data(stocks_list):
        """
        Fetch stock data for a list of stock tickers
        
        Args:
            stocks_list: List of stock ticker symbols (e.g., ['RELIANCE.NS', 'TCS.NS'])
            
        Returns:
            list: List of stock data dictionaries, sorted by symbol
        """
        # Fetch data for all requested stocks in parallel for better performance
        stocks_data = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ticker = {executor.submit(StockDataService.fetch_stock_data, ticker): ticker for ticker in stocks_list}
            for future in as_completed(future_to_ticker):
                stock_data = future.result()
                stocks_data.append(stock_data)
        
        # Sort by symbol for consistent ordering
        stocks_data.sort(key=lambda x: x.get('symbol', ''))
        
        return stocks_data


class CommonService:
    """
    Common service class for shared functionality
    """
    
    def default_response(self, request, message, path):
        """
        Custom Response
        
        Args:
            request: Django request object
            message: Response data/message
            path: API path
            
        Returns:
            dict: Formatted response with status, data, and meta information
        """
        output = {
            "status": "success",
            "data": message,
            "meta": {
                "timestamp": TimeUtility().get_current_datetime_endwith_z(),
                "request_id": getattr(request, 'request_id', None),
                "version": "v1",
                "path": str(request.get_host()) + str(path),
            },
        }
        return output

