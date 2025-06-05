import logging, asyncio
from src.services import binanceWebsocket 
import src.event_handler as EventHandler
from src.utils.logger import init_logger
import event_handler as EventHandler
from src.services import db

async def main():
    init_logger()
    binance_event_queue = asyncio.Queue()
    asyncio.create_task(binanceWebsocket.websocket_binance_event_listener(binance_event_queue)) # Creates a background task. 
    while True:
        new_binance_event = await binance_event_queue.get()
        logging.info("🔴 Awaiting next event in queue from Binance event websocket...")
        logging.info(f"😱 Received new Binance event! Event: {new_binance_event}")
        event_type = new_binance_event['e']

        if event_type != "ORDER_TRADE_UPDATE": # Ignoring all other event types
            continue

        parsed_event = EventHandler.event_parser(new_binance_event)

        if parsed_event['status'] == "CANCELED": # UPDATE CANCELLED FIRST
            db.findByIdAndCancel(parsed_event['order_id'], parsed_event) # TO-DO
        if parsed_event['status'] == "NEW": # New Market Order
            db.insertNewOrderByType(parsed_event["type"] ,parsed_event) 
        if parsed_event['type'] == "MARKET" and parsed_event['status'] == "FILLED":
            db.findByIdAndUpdateFilledMarketOrder(parsed_event['order_id'], parsed_event) # TO-DO
        if parsed_event['type'] != "MARKET" and parsed_event['status'] == "FILLED":
            db.findByIdAndUpdateFilledSLTPOrder(parsed_event['order_id'], parsed_event) # TO-DO




asyncio.run(main())

