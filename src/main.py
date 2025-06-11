import logging, asyncio
from src.services import binanceWebsocket, binanceREST
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
            db.findByIdAndCancel(parsed_event['order_id'], parsed_event) 

        elif parsed_event['status'] == "NEW": # New Order
            db.insertNewOrderByType(parsed_event["type"] ,parsed_event) 

        elif parsed_event['type'] == "MARKET" and parsed_event['status'] == "FILLED":
            db.findByIdAndUpdateFilledMarketOrder(parsed_event['order_id'], parsed_event)

            new_order_group_id = db.get_group_id_by_order(parsed_event['order_id'])
            if new_order_group_id:
                db.insertNewTrade(new_order_group_id, parsed_event)
            else: # This catches the case where I just insert an MO, for test for instance, which an accompanying order_id is not found 
                logging.info("No group_id found for order, inserting a new entry in order_groups table")
                new_group_id = db.get_latest_group_id()
                new_group_id = 999999999
                db.insertNewOrderGroup(new_group_id, parsed_event)
                db.insertNewTrade(new_group_id, parsed_event)
        elif parsed_event['type'] != "MARKET" and parsed_event['status'] == "FILLED":
            db.findByIdAndUpdateFilledSLTPOrder(parsed_event['order_id'], parsed_event) 
            group_id = db.get_group_id_by_order(parsed_event['order_id'])
            remaining_order = None
            if parsed_event['type'] == "STOP_MARKET":
                remaining_order = "TP"
            else:
                remaining_order = "SL"
            if new_order_group_id:
                db.updateTrade(group_id, parsed_event)
                remaining_order_id = db.find_remaining_order(group_id, remaining_order)
                binanceREST.cancel_orders(remaining_order_id)
            else: # This catches the case where I just insert an SL/TP, for test for instance, which an accompanying order_id is not found 
                logging.info("No group_id found for order, inserting a new entry in order_groups table")
                new_group_id = db.get_latest_group_id()
                new_group_id = new_group_id + 1 if new_group_id else 0
                db.insertNewOrderGroup(new_group_id, parsed_event)




asyncio.run(main())

