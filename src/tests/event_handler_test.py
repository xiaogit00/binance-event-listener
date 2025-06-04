import src.event_handler as EventHandler
import requests

import unittest
import os
import asyncio

trade_event = {
    "e": "ORDER_TRADE_UPDATE",
    "T": 1749037542410,
    "E": 1749037542410,
    "o": {
        "s": "SOLUSDT",
        "c": "g4MptWkQzp3uWetiZUUUJj",
        "S": "SELL",
        "o": "TAKE_PROFIT",
        "f": "GTC",
        "q": "0.09",
        "p": "155.97",
        "ap": "0",
        "sp": "155.99",
        "x": "CANCELED",
        "X": "CANCELED",
        "i": 121112161969,
        "l": "0",
        "z": "0",
        "L": "0",
        "n": "0",
        "N": "USDT",
        "T": 1749037542410,
        "t": 0,
        "b": "0",
        "a": "0",
        "m": False,
        "R": False,
        "wt": "CONTRACT_PRICE",
        "ot": "TAKE_PROFIT",
        "ps": "BOTH",
        "cp": False,
        "rp": "0",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}
class TestEventHandler(unittest.TestCase):
    def test_event_cleaner(self):
        res = EventHandler.event_parser(trade_event)
        print(res)

if __name__ == '__main__':
    asyncio.run(unittest.main())


