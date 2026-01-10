from src.services import binanceAPI 
import requests

import unittest
import os
import asyncio

# print(hmac.new(os.getenv("LEI_BINANCE_API_SECRET").encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest())

class TestBinanceAPI(unittest.TestCase):
    # def test_execute_market_order(self):
    #     res = binanceAPI.execute_market_order("SOLUSDT", "LONG", 0.09, 155.5, 5)
    #     print(res)
    def test_execute_stop_loss_order(self):
        res = binanceAPI.execute_stop_loss_order("SOLUSDT", 136.12, 0.04)
        print(res)
    # def test_cancel_orders(self):
    #     res = binanceAPI.cancel_algo_orders("SOLUSDT", "1000000332992900")
    #     print(res)
    # def test_execute_take_profit_order(self):
    #    binanceAPI.execute_take_profit_order("SOLUSDT", "LONG", 156.10, 0.09, 1)
    # async def test_fetch_candle_ws(self):
    #     res = await binanceAPI.fetch_last_candle_ws("SOLUSDT")
    #     # print(res)
    # def test_open_positions(self):
    #    res = binanceAPI.get_futures_positions()
    #    print(res)
    # def test_open_orders(self):
    #    res = binanceAPI.get_open_orders("SOLUSDT")
    #    print(res)
    # def test_listen_key(self):
    #     res = binanceAPI.get_listen_key()
    #     print(res)
       

if __name__ == '__main__':
    asyncio.run(unittest.main())


