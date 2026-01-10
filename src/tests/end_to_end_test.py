from src.services import db
from src.tests import event_samples
import unittest
import asyncio
from src.utils import logger
from src.services import binanceAPI 
import logging
logging.basicConfig(level=logging.INFO)

class TestE2E(unittest.TestCase):
    '''This test does the following: 
        1. Execute a MO - see it fill
        2. Execute an SL see it fill
        3. Execute an SL and cancel it
    '''
    # def test_can_execute_MO_and_reflected_in_db(self):
    #     res = binanceAPI.execute_market_order("SOLUSDT", 0.04)
        
    #     # DB should at least have that executed market order record 
    #     # Sleep for 10 seconds
    #     # Check that the Order is filled - 
    #     print(res)
    def test_can_execute_SL_and_reflected_in_db(self):
        res = binanceAPI.execute_stop_loss_order("SOLUSDT", 136.53, 0.04)
        
        # DB should at least have that executed market order record 
        # Sleep for 10 seconds
        # Check that the Order is filled - 
        print(res)

if __name__ == '__main__':
    asyncio.run(unittest.main())


