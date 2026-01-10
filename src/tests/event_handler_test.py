import src.event_handler as EventHandler
import src.tests.event_samples as EventSamples
import requests

import unittest
import os
import asyncio
import logging
logging.basicConfig(level=logging.INFO)

class TestEventHandler(unittest.TestCase):
    # def test_trade_lite(self):
    #     res = EventHandler.event_parser(EventSamples.newTradeLite())
    #     logging.info("res=%s", res)
    #     self.assertEqual(res, None)
    # def test_new_mo_order_trade_update(self):
    #     res = EventHandler.event_parser(EventSamples.newMarketOrder())
    #     logging.info("res=%s", res)
    #     parsed_mo = {'order_id': 121058809222, 'status': 'NEW', 'symbol': 'SOLUSDT', 'side': 'BUY', 'type': 'MARKET', 'qty': '0.09', 'direction': 'LONG', 'created_at': 1749013292798}
    #     self.assertEqual(res, parsed_mo)
    # def test_canceled_order(self):
    #     res = EventHandler.event_parser(EventSamples.newCanceledSLOrder())
    #     logging.info("res=%s", res)
    #     parsed_canceled_order = {'order_id': 1000000332992900, 'status': 'CANCELED', 'symbol': 'SOLUSDT', 'side': 'SELL', 'type': 'STOP_MARKET', 'qty': '0.05', 'direction': 'LONG', 'updated_at': 1768014907127}
    #     self.assertEqual(res, parsed_canceled_order)
    def test_new_SL_order(self):
        res = EventHandler.event_parser(EventSamples.newAlgoSLOrder())
        logging.info("res=%s", res)
        parsed_new_SL_order = {'order_id': 1000000333505502, 'status': 'NEW', 'symbol': 'SOLUSDT', 'side': 'SELL', 'type': 'STOP_MARKET', 'qty': '0.04', 'direction': 'LONG', 'created_at': 1768015698681, 'ask_price': '136.12'}
        self.assertEqual(res, parsed_new_SL_order)

if __name__ == '__main__':
    asyncio.run(unittest.main())


