from src.services import db
from src.tests import event_samples
import unittest
import asyncio


class TestDB(unittest.TestCase):
    # def test_get_orders(self):
    #     res = db.get_orders()
    #     print(res)
    # def test_insert_new_market_order(self):
    #     db.delete_orders()
    #     res = db.insertNewOrderByType("MARKET", event_samples.newParsedMarketOrder())
    #     print(res)
    # def test_update_filled_market_order(self):
    #     db.delete_orders()
    #     db.insertNewOrderByType("MARKET", event_samples.newParsedMarketOrder())
    #     db.findByIdAndUpdateFilledMarketOrder("121058809222", event_samples.newParsedFilledMarketOrder())
    # def test_insert_new_SL_order(self):
    #     db.delete_orders()
    #     res = db.insertNewOrderByType("STOP_MARKET", event_samples.newParsedSLOrder())
    #     print(res)
    # def test_insert_new_SL_order(self):
        # db.delete_orders()
        # db.insertNewOrderByType("STOP_MARKET", event_samples.newParsedSLOrder())
    #     db.findByIdAndUpdateFilledSLTPOrder("121112646034", event_samples.newParsedFilledSLOrder())
    # def test_find_order_and_cancel(self):
    #     db.delete_orders()
    #     db.insertNewOrderByType("STOP_MARKET", event_samples.newParsedSLOrder())
    #     db.findByIdAndCancel(121112646034, event_samples.newParsedCancelOrder())
    def test_get_one_order(self):
        res = db.get_one_order('12143509663')
        print(res)

if __name__ == '__main__':
    asyncio.run(unittest.main())


