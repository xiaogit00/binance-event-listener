import logging, asyncio
from src.services import binanceAPI, binanceWebsocket
import src.event_handler as EventHandler
from src.utils.logger import init_logger
from src.services import db

async def main():
    init_logger()
    new_group_id = -1
    binance_event_queue = asyncio.Queue()
    asyncio.create_task(binanceWebsocket.websocket_binance_event_listener(binance_event_queue)) # Creates a background task. 
    asyncio.create_task(binanceWebsocket.keep_listen_key_alive())
    while True:
        new_binance_event = await binance_event_queue.get()
        logging.info("🔴 Awaiting next event in queue from Binance event websocket...")
        logging.info(f"😱 Received new Binance event! Event: {new_binance_event}")

        parsed_event = EventHandler.event_parser(new_binance_event)
        if not parsed_event: continue # For skipped events
        
        # The following are all DB updates based on event triggered
        if parsed_event['status'] == "CANCELED": # UPDATE CANCELLED FIRST
            db.findByIdAndCancel(parsed_event['order_id'], parsed_event) 

        elif parsed_event['status'] == "NEW": # New Order
            order_exists = db.get_one_order(parsed_event['order_id']).data
            if not order_exists:
                db.insertNewOrderByType(parsed_event["type"] ,parsed_event) 

        elif parsed_event['type'] == "MARKET" and parsed_event['status'] == "FILLED": # Filled MO
            db.findByIdAndUpdateFilledMarketOrder(parsed_event['order_id'], parsed_event)
            await asyncio.sleep(5)
            new_order_group_id = db.get_group_id_by_order(parsed_event['order_id'])
            if new_order_group_id:
                db.insertNewTrade(new_order_group_id, parsed_event)
            else: # This catches the case where I just insert an MO, for test for instance, which an accompanying order_id is not found 
                logging.info(f"No group_id found for order, inserting a new order_groups with group_id = {new_group_id}")
                db.insertNewOrderGroup(new_group_id, parsed_event)
                db.insertNewTrade(new_group_id, parsed_event)
                new_group_id -= 1
        elif parsed_event['type'] == "STOP_MARKET" and parsed_event['status'] == "FILLED": 
            db.findByIdAndUpdateFilledSLOrder(parsed_event['order_id'], parsed_event) 
            group_id = db.get_group_id_by_order(parsed_event['order_id'])
            if not group_id:
                logging.critical("Fatal: no group_id found, stopping program.") # Insert notif here.
                raise
            db.updateTrade(group_id, parsed_event)

asyncio.run(main())

