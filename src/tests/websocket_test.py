from src.services import binanceWebsocket
import requests

import unittest
import os
import asyncio


class TestWebsocket(unittest.TestCase):
    def test_get_listen_key(self):
        res = binanceWebsocket.get_listen_key()
        print(res)

if __name__ == '__main__':
    asyncio.run(unittest.main())


