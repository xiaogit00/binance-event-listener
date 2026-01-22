import logging, asyncio
from src.services import binanceAPI, binanceWebsocket
import src.event_handler as EventHandler
from src.utils.logger import init_logger
from src.utils.calcs import calculateTrailingValue
from src.services import db
from dotenv import load_dotenv
import os
import time

async def main():
    load_dotenv()
    env = os.getenv("ENV")

    init_logger()
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

        elif parsed_event['status'] == "NEW" and parsed_event['type'] == "MARKET": # New Market Order
            order_exists = db.get_one_order(parsed_event['order_id']).data
            if not order_exists:
                db.insertNewOrderByType(parsed_event["type"] ,parsed_event) 
                #INSERTING INTO ORDER_GROUPS DB
                time.sleep(5) # Catch case: Binance latency in MO OR DB latency, which results in candle data not being inserted
                candle_data = db.getCandleData(parsed_event['order_id']) if env == 'prod' else db.getCandleData(2222)
                group_id = int(candle_data['group_id'])
                order_groups_data = {
                    "group_id": group_id,
                    "order_id": parsed_event['order_id'],
                    "type": parsed_event['type'],
                    "direction": parsed_event['direction'],
                    "current_stop_loss": None,
                    "trailing_value": None,
                    "trailing_price": None,
                    "next_stoploss_price": None
                }
                db.insertNewOrderGroup(group_id, order_groups_data) 
        
        elif parsed_event['status'] == "NEW" and parsed_event['type'] == "STOP_MARKET": # New Market Order
            order_exists = db.get_one_order(parsed_event['order_id']).data
            if not order_exists:
                db.insertNewOrderByType(parsed_event["type"] ,parsed_event) 
                time.sleep(5)
                actual_entry_price = parsed_event['ask_price'] # because it's an SL order, the ask price will be equal to its filled price
                candle_data = db.getCandleData(parsed_event['order_id']) if env == 'prod' else db.getCandleData(2222)
                group_id = int(candle_data['group_id'])
                current_stop_loss, trailing_value, trailing_price, next_stoploss_price = calculateTrailingValue(candle_data,parsed_event['direction'] , float(actual_entry_price))
                order_groups_data = {
                    "group_id": group_id,
                    "order_id": parsed_event['order_id'],
                    "type": parsed_event['type'],
                    "direction": parsed_event['direction'],
                    "current_stop_loss": current_stop_loss,
                    "trailing_value": trailing_value,
                    "trailing_price": trailing_price,
                    "next_stoploss_price": next_stoploss_price
                }
                db.insertNewOrderGroup(group_id, order_groups_data) # INSERTING ORDER GROUP HERE ON NEW SL ORDER BECAUSE ACTUAL ENTRY PRICE CAN BE DERIVED; in contrast, MO's actual entry price is only emitted in FILLED event. 

        elif parsed_event['type'] == "MARKET" and parsed_event['status'] == "FILLED": # Filled MO
            db.findByIdAndUpdateFilledMarketOrder(parsed_event['order_id'], parsed_event)
            db.insertNewTrade(group_id, parsed_event)

        elif parsed_event['type'] == "STOP_MARKET" and parsed_event['status'] == "FILLED": 
            db.findByIdAndUpdateFilledSLOrder(parsed_event['order_id'], parsed_event) 
            db.updateTrade(group_id, parsed_event)

asyncio.run(main())

