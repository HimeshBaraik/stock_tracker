from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .utilities import StockDataService


@shared_task(bind=True)
def fetch_stocks_data_task(self, stocks_list):
    """
    Background task to fetch stock data for a list of stock tickers
    and broadcast it to connected WebSocket clients
    
    Args:
        self: Task instance (from bind=True)
        stocks_list: List of stock ticker symbols (e.g., ['RELIANCE.NS', 'TCS.NS'])
        
    Returns:
        list: List of stock data dictionaries, sorted by symbol
    """
    try:
        stocks_data = StockDataService.fetch_stocks_data(stocks_list)
        
        # Broadcast stock data to connected WebSocket clients
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "stock_updates",
                {
                    "type": "stock_update",
                    "stock_data": stocks_data
                }
            )
        
        return stocks_data
    except Exception as e:
        # Log the error and re-raise so Celery can handle retries
        raise Exception(f"Error fetching stock data: {str(e)}")
