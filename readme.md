## Stock Tracker (Django + DRF + Celery + Channels)

This project provides:
- A **REST API** to fetch stock data on-demand via Yahoo Finance (`yfinance`)
- A **WebSocket** stream that pushes stock updates to connected clients
- A **Celery Beat** schedule that periodically fetches stock data and broadcasts it over WebSockets

### High-level flow
- **REST (on-demand)**:
  - Client calls `POST /stocks/` with a list of tickers
  - `mainapp.utilities.StockDataService` fetches data (parallelized with `ThreadPoolExecutor`)
  - API returns a formatted JSON response
- **WebSocket (push updates)**:
  - Client connects to `ws://127.0.0.1:8000/ws/stock/`
  - `mainapp.consumers.StockConsumer` joins the `stock_updates` group
  - Celery Beat triggers `mainapp.tasks.fetch_stocks_data_task` every **10 seconds** (configured in `stock_tracker/celery.py`)
  - Celery worker fetches stock data and broadcasts it to the `stock_updates` group via **Redis channel layer**
  - All connected WebSocket clients receive `{ "type": "stock_update", "data": [...] }`

### Prerequisites
- **Python** (recommended 3.10+)
- **Redis** running locally on `127.0.0.1:6379`
  - Used as **Celery broker** and **Channels (WebSocket) channel layer**

### Setup
Create + activate a virtualenv, install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run migrations (required for Django + `django-celery-results` + `django-celery-beat` tables):

```bash
python manage.py migrate
```

### Run (local development)
You need **4 things** running: Redis, Django server, Celery worker, Celery beat.

#### 1) Start Redis
- If you have Docker:

```bash
docker run --rm -p 6379:6379 redis
```

#### 2) Start Django (HTTP + ASGI/WebSockets)

```bash
python manage.py runserver
```

#### 3) Start Celery worker (Windows: use `--pool=solo`)

```bash
celery -A stock_tracker.celery worker --pool=solo -l info
```

#### 4) Start Celery beat (scheduler)

```bash
celery -A stock_tracker.celery beat -l info
```

### Useful URLs
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **OpenAPI schema**: `http://127.0.0.1:8000/api/schema/`
- **Stocks API**: `POST http://127.0.0.1:8000/stocks/`
- **WebSocket**: `ws://127.0.0.1:8000/ws/stock/`

### Quick test
#### REST

PowerShell:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/stocks/" `
  -ContentType "application/json" `
  -Body '{"stocks":["RELIANCE.NS","TCS.NS","HDFCBANK.NS"]}'
```

Windows CMD (optional):

```bat
curl -X POST http://127.0.0.1:8000/stocks/ ^
  -H "Content-Type: application/json" ^
  -d "{\"stocks\": [\"RELIANCE.NS\", \"TCS.NS\", \"HDFCBANK.NS\"]}"
```

#### WebSocket
Connect to `ws://127.0.0.1:8000/ws/stock/` and wait for updates (every ~10 seconds).

> Note: The route `/ws-test/` exists, but it expects a `websocket_test.html` file at the project root; if the file is missing you’ll get a server error.

### Configuration notes
- **Tickers + interval** are currently hardcoded in `stock_tracker/celery.py` (`beat_schedule` runs every 10 seconds).
- Redis endpoints are configured in `stock_tracker/settings.py`:
  - `CELERY_BROKER_URL = redis://localhost:6379`
  - `CHANNEL_LAYERS` uses `127.0.0.1:6379`
