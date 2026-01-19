from src.services import db
from src.tests import event_samples
import unittest
import asyncio
from src.utils import logger
from src.utils.calcs import calculateTrailingValue

class TestCalcs(unittest.TestCase):

    def test_calcs(self):
        candle_data = {'order_id': 188999740044, 'candle_data': '{"open": "139.10", "high": "149.10", "low": "129.10", "close": "138.10"}', 'trade_metadata': '{"risk_amount": 10, "fee": 0.1, "portfolio_threshold": 20, "rv_period": 2, "ema_period": 9, "rv_threshold": 2.8, "trailing_percentage": 0.7}', 'created_at': '2026-01-13T10:49:06.448679+00:00'}
        print(calculateTrailingValue(candle_data, "123"))

if __name__ == '__main__':
    asyncio.run(unittest.main())


