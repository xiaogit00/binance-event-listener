from src.services import db
from src.tests import event_samples
import unittest
import asyncio
from src.utils import logger

class TestDB(unittest.TestCase):
    # def test_delete_orders(self):
    #     res = db.delete_orders()
    #     print(res)
    # def test_get_orders(self):
    #     res = db.get_orders()
    #     print(res)
    # def test_insert_new_market_order(self):
    #     res = db.insertNewOrderByType("MARKET", event_samples.newParsedMarketOrder())
    #     print(res)
    # def test_update_filled_market_order(self):
    #     db.insertNewOrderByType("MARKET", event_samples.newParsedMarketOrder())
    #     db.findByIdAndUpdateFilledMarketOrder("5", event_samples.newParsedFilledMarketOrder())
    # def test_insert_new_SL_order(self):
    #     db.delete_orders()
    #     res = db.insertNewOrderByType("STOP_MARKET", event_samples.newParsedSLOrder())
    #     print(res)
    # def test_insert_new_SL_order(self):
    #     db.insertNewOrderByType("STOP_MARKET", event_samples.newParsedSLOrder())
    #     db.findByIdAndUpdateFilledSLTPOrder("6", event_samples.newParsedFilledSLOrder())
    # def test_find_order_and_cancel(self):
    #     db.findByIdAndCancel(2, event_samples.newParsedCancelOrder())
    # def test_get_one_order(self):
    #     res = db.get_one_order('6')
    #     print(res)
    # def test_get_group_id_by_order(self):
    #     logger.init_logger()
    #     res = db.get_group_id_by_order(123504619285)
    #     print(res == True)
    def test_insert_new_trade(self):
        res = db.insertNewTrade(-3, event_samples.newParsedFilledMarketOrder())
        print(res)
    # def test_get_entry_price_for_trade(self):
    #     res = db.get_entry_price_for_trade(1)
    #     print(res)
    # def test_update_trade(self):
    #     res = db.updateTrade(-3, event_samples.newParsedFilledSLOrder())
    #     print(res)
    # def test_get_latest_group_id(self):
    #     res = db.get_latest_group_id()
    #     print(res)
    # def test_insert_new_group_order(self):
    #     res = db.insertNewOrderGroup(000, event_samples.newParsedFilledMarketOrder())
    #     print(res)
    # def test_find_remaining_order(self):
    #     res = db.find_remaining_order(0,"SL")
    #     print(res)
    # def test_does_BE_exist_for_order_group(self):
    #     res = db.does_BE_exist_for_order_group(100)
    #     print(res)
    def test_remaining_orders_logic(self):
        is_stop_market = False
        BE_exists = True
        remaining_order = "TP" if is_stop_market else ("BE" if BE_exists else "SL") 
        print(remaining_order)

if __name__ == '__main__':
    asyncio.run(unittest.main())


