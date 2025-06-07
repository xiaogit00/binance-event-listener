import src.event_handler as EventHandler
import src.tests.event_samples as EventSamples
import requests

import unittest
import os
import asyncio

class TestEventHandler(unittest.TestCase):
    def test_event_cleaner(self):
        res = EventHandler.event_parser(EventSamples.newSLOrder())
        print(res)

if __name__ == '__main__':
    asyncio.run(unittest.main())


