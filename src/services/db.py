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

    # conn = get_connection()
    # try:
    #     with conn.cursor() as cur:
    #         cur.execute("""
    #                         UPDATE orders
    #                         SET status = %s, filled_price = %s, updated_at = %s
    #                         WHERE order_id = %s
    #                         RETURNING *;
    #                     """, (
    #             order_data['status'],
    #             order_data['filled_price'],
    #             datetime.fromtimestamp(order_data["updated_at"]/1000),
    #             order_id,
    #         ))
    #         new_order = cur.fetchone()
    #         conn.commit()
    #         logging.info(f"Successfully updated Market Order {order_id} with FILLED info: {new_order}")
    #         return new_order
    # finally:
    #     conn.close()

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



def add_new_order(res, ask_price):
    """Inserts a new order in orders table."""
    logging.info("Attempting to insert new order into DB...")
    order_id = res["orderId"]
    symbol = res["symbol"]
    order_type = res["type"]
    side = res["side"]
    created_at = str(datetime.fromtimestamp(round(res["updateTime"]/1000, 0)))
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO orders (order_id, symbol, order_type, ask_price, filled_price, side, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                order_id,
                symbol,
                order_type,
                ask_price,
                0, 
                side,
                created_at
            ))
            new_order = cur.fetchone()
            conn.commit()
            logging.info(f"Successfully inserted new order into DB, response: {new_order}")
            return new_order
    finally:
        conn.close()

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