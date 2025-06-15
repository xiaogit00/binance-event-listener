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

    while True: 
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

        time.sleep(5)
