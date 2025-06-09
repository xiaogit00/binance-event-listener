import os
import psycopg2
from dotenv import load_dotenv
from src.services.db_connection import get_connection
from src.utils.supabase_client import get_supabase_client
import logging


from datetime import datetime

load_dotenv()
supabase = get_supabase_client()

def get_one_order(order_id):
    """Gets one order"""
    try:
        res = (
            supabase.table("orders")
            .select("*")
            .eq("order_id", order_id)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue getting one order from supabase: ", e)

def get_orders():
    """Get all orders"""
    try:
        res = (
            supabase.table("orders")
            .select("*")
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue getting supabase table: ", e)

def delete_orders():
    """Get all orders"""
    try:
        res = (
            supabase.table("orders")
            .delete()
            .neq("order_id", 0)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue updating supabase table: ", e)

def insertNewOrderByType(order_type, order_data):
    logging.info("Attempting to insert new order into DB...")
    try:
        newOrder = {
            "order_id":order_data["order_id"],
            "status":order_data["status"],
            "direction":order_data["direction"],
            "symbol":order_data["symbol"],
            "order_type":order_data["type"],
            "ask_price":None if order_data["type"] == "MARKET" else order_data["ask_price"], # Ask Price is none,
            "filled_price":None, # Filled Price Price is none
            "side":order_data["side"],
            "created_at": str(datetime.fromtimestamp(order_data["created_at"]/1000)),
            "updated_at": None,
        }
        res = (
            supabase.table("orders")
            .insert(newOrder)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue updating supabase table: ", e)

        
def findByIdAndUpdateFilledMarketOrder(order_id, order_data):
    logging.info(f"Attempting to UPDATE order {order_id} to FILLED")
    try:
        updated_market_order = {
            "status":order_data["status"],
            "ask_price":order_data['ask_price'],
            "filled_price":order_data['filled_price'],
            "updated_at": str(datetime.fromtimestamp(order_data["updated_at"]/1000)),
        }
        res = (
            supabase.table("orders")
            .update(updated_market_order)
            .eq("order_id", order_id)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue updating supabase table: ", e)

def findByIdAndUpdateFilledSLTPOrder(order_id, order_data):
    logging.info(f"Attempting to UPDATE order {order_id} to FILLED")
    try:
        updated_sltp_order = {
            "status":order_data["status"],
            "filled_price":order_data['filled_price'],
            "updated_at": str(datetime.fromtimestamp(order_data["updated_at"]/1000)),
        }
        res = (
            supabase.table("orders")
            .update(updated_sltp_order)
            .eq("order_id", order_id)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue updating supabase table: ", e)


def findByIdAndCancel(order_id, order_data):
    '''
    Updates the status of the order to be cancelled
    '''
    print(f"Attempting to UPDATE order {order_id} to CANCELED")
    try:
        res = (
            supabase.table("orders")
            .update({"status": order_data['status'], "updated_at": str(datetime.fromtimestamp(order_data["updated_at"]/1000))})
            .eq("order_id", order_id)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue updating supabase table: ", e)

def insertNewTrade(group_id, order_data):
    logging.info("Attempting to insert new trade into DB...")
    try:
        newTrade = {
            "group_id": group_id,
            "symbol": order_data["symbol"],
            "direction":order_data["direction"],
            "entry_time": str(datetime.fromtimestamp(order_data["updated_at"]/1000)),
            "exit_time": None, # This is entered only upon exit
            "entry_price":order_data["filled_price"], 
            "exit_price":None, # This is entered only upon exit
            "qty": order_data["qty"],
            "realized_pnl": None,# This is entered only upon exit
            "is_closed": False 
        }
        res = (
            supabase.table("trades")
            .insert(newTrade)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue updating supabase table: ", e)

def get_entry_price_for_trade(group_id):
    try:
        res = (
            supabase.table("trades")
            .select("*")
            .eq("group_id", group_id)
            .execute()
        )
        if not res.data:
            return None
        return res.data[0]['entry_price']
    except Exception as e: 
        print("There's an issue getting one order from supabase: ", e)

def updateTrade(group_id, order_data):
    logging.info("Attempting to update trade...")
    try:
        entry_price = get_entry_price_for_trade(group_id)
        updated_trade = {
            "exit_time":str(datetime.fromtimestamp(order_data["updated_at"]/1000)),
            "exit_price":order_data['filled_price'],
            "realized_pnl":round((float(order_data['filled_price']) - entry_price)/entry_price, 3),
            "is_closed": True,
        }
        res = (
            supabase.table("trades")
            .update(updated_trade)
            .eq("group_id", group_id)
            .execute()
        )
        return res
    except Exception as e: 
        print("There's an issue updating supabase table: ", e)


def get_latest_group_id() -> int:
    """Makes connection to orders table and gets the latest group ID of the orders."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            logging.info("Fetching latest group_id from orders table")
            cur.execute("SELECT group_id FROM orders ORDER BY created_at DESC LIMIT 1;")
            res = cur.fetchall()
            if not res:
                logging.info("No latest_group_id found, returning id 0")
                return 0
            else:
                logging.info(f"Latest group_id found from orders table: {res[0][0]}")
                return res[0][0]
    finally:
        conn.close()
    

def get_group_id_by_order(order_id):
    try:
        res = (
            supabase.table("order_groups")
            .select("*")
            .eq("order_id", order_id)
            .execute()
        )
        if not res.data:
            return None
        return res.data[0]['group_id']
    except Exception as e: 
        print("There's an issue getting one order from supabase: ", e)