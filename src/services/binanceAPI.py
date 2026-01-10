import time
import hmac
import hashlib
import requests
import logging 
import os 
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://fapi.binance.com'
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

def _sign(params):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def cancel_orders(symbol, orderid):
    url = f"{BASE_URL}/fapi/v1/order"
    headers = {
        'X-MBX-APIKEY': api_key
    }

    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol.upper(),
        'orderId': orderid,
        'timestamp': timestamp
    }
    params['signature'] = _sign(params)

    try: 
        response = requests.delete(url, headers=headers, params=params)
        if response.status_code == 200: 
            logging.info(f"✅ Stop loss order {orderid} for {symbol} canceled.")
            return response.json()
        else:
            logging.warning(f"❌ Error canceling Stop loss order: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.error(f"⚠️ Request exception: {e}")

def cancel_algo_orders(symbol, algoId):
    url = f"{BASE_URL}/fapi/v1/algoOrder"
    headers = {
        'X-MBX-APIKEY': api_key
    }

    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol.upper(),
        'algoid': algoId,
        'timestamp': timestamp
    }
    params['signature'] = _sign(params)

    try: 
        response = requests.delete(url, headers=headers, params=params)
        if response.status_code == 200: 
            logging.info(f"✅ Stop loss order {algoId} for {symbol} canceled.")
            return response.json()
        else:
            logging.warning(f"❌ Error canceling Stop loss order: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.error(f"⚠️ Request exception: {e}")

def execute_stop_loss_order(symbol, trigger_price, qty):
    url = f"{BASE_URL}/fapi/v1/algoOrder"

    headers = {
        'X-MBX-APIKEY': api_key
    }
    timestamp = int(time.time() * 1000)
    params = {
        'algoType': "CONDITIONAL",
        'symbol': symbol,
        'side': 'SELL', # BUY / SELL
        'reduceOnly': "true", # This prevents the case of a 'naked' stop loss order, where in the case of an already closed position, Binance will open a Short position on SL trigger.
        # 'positionSide': 'LONG', # (Optional) Default BOTH for One-way Mode ; LONG or SHORT for Hedge Mode. It must be sent in Hedge Mode.
        'type': 'STOP_MARKET',
        'triggerPrice': trigger_price,
        'quantity': qty,
        'timestamp': timestamp
    }
    params['signature'] = _sign(params)

    try: 
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 200: 
            logging.info(f"✅ Stop loss order {response} created.")
            return response.json()
        else:
            logging.warning(f"❌ Error making Stop loss order: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.error(f"⚠️ Request exception: {e}")

def execute_market_order(symbol, qty):
    url = f"{BASE_URL}/fapi/v1/order"

    headers = {
        'X-MBX-APIKEY': api_key
    }
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': 'BUY', # BUY / SELL
        # 'positionSide': 'LONG', # (Optional) Default BOTH for One-way Mode ; LONG or SHORT for Hedge Mode. It must be sent in Hedge Mode.
        'type': 'MARKET',
        'quantity': qty,
        'timestamp': timestamp
    }
    params['signature'] = _sign(params)

    try: 
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 200: 
            logging.info(f"✅ Market order {response} created.")
            return response.json()
        else:
            logging.warning(f"❌ Error making market order: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.error(f"⚠️ Request exception: {e}")