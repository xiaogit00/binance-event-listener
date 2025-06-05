from src.services import db
from src.tests import event_samples
import unittest
import asyncio


class TestDB(unittest.TestCase):
    # def test_get_orders(self):
    #     res = db.get_orders()
    #     print(res)
    def test_insert_new_market_order(self):
        res = db.insertNewOrderByType("MARKET", event_samples.newParsedMarketOrder())
        print(res)

if __name__ == '__main__':
    asyncio.run(unittest.main())


