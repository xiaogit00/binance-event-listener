from dotenv import load_dotenv
import requests, os, asyncio, logging, websockets, json
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
baseUrl = 'https://fapi.binance.com'
listen_key = None

load_dotenv()

def get_listen_key():
    url = f"{baseUrl}/fapi/v1/listenKey"
    headers = {'X-MBX-APIKEY': os.getenv("BINANCE_API_KEY")}
    response = requests.post(url, headers=headers)
    try:
        response.raise_for_status()
    except Exception as e:
        print(e)
    listen_key = response.json()['listenKey']
    return listen_key

async def websocket_binance_event_listener(binance_event_queue: asyncio.Queue):
    listen_key = get_listen_key()
    ws_url = f"wss://fstream.binance.com/ws/{listen_key}"
    logging.info(f"Connecting to {ws_url}")

    while True:
        try:
            async with websockets.connect(ws_url) as ws:
                logging.info(f"✅ Connected to Binance event listening websocket")
                while True:
                    try:
                        message = await ws.recv()
                        print("event connection websocket is running in the background")
                        event = json.loads(message)
                        await binance_event_queue.put(event)
                    except asyncio.TimeoutError:
                        logging.warning("⏱️ No message in 60 seconds. Sending ping...")
                        try:
                            pong = await ws.ping()
                            await asyncio.wait_for(pong, timeout=10)
                        except asyncio.TimeoutError:
                            logging.warning("⚠️ Ping timed out. Reconnecting...")
                            break  # Exit to reconnect

        except (ConnectionClosedError, ConnectionClosedOK) as e:
            logging.info(f"🔌 Binance event websocket closed: {e}. Reconnecting...")
        except Exception as e:
            logging.critical(f"🔥 Unexpected WebSocket error for Binance event websocket: {e}", exc_info=True)
        await asyncio.sleep(2)  # Optional: prevent rapid reconnect loop