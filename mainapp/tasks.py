from celery import shared_task
from .utilities import StockDataService


@shared_task(bind=True)
def fetch_stocks_data_task(self, stocks_list):
    """
    Background task to fetch stock data for a list of stock tickers
    
    Args:
        self: Task instance (from bind=True)
        stocks_list: List of stock ticker symbols (e.g., ['RELIANCE.NS', 'TCS.NS'])
        
    Returns:
        list: List of stock data dictionaries, sorted by symbol
    """
    try:
        stocks_data = StockDataService.fetch_stocks_data(stocks_list)
        return stocks_data
    except Exception as e:
        # Log the error and re-raise so Celery can handle retries
        raise Exception(f"Error fetching stock data: {str(e)}")
