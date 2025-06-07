import os
import psycopg2
from dotenv import load_dotenv
from src.services.db_connection import get_connection
import logging

from datetime import datetime

load_dotenv()

def get_one_order(order_id):
    """Gets one order"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE order_id=%s;", [order_id])
            db_res = cur.fetchall()
            if len(db_res):
                print("THERE IS AN ORDER ID EXISTING")
            return db_res
    finally:
        conn.close()

def get_orders():
    """Get all orders"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders;")
            return cur.fetchall()
    finally:
        conn.close()

def delete_orders():
    """Get all orders"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM orders;")
            conn.commit()
    finally:
        conn.close()

def insertNewOrderByType(order_type, order_data):
    logging.info("Attempting to insert new order into DB...")
    '''
    order_data (MO):
        {
        "order_id": 121058809222,
        "status": "NEW",
        "symbol": "SOLUSDT",
        "side": "BUY",
        "type": "MARKET",
        "qty": "0.09",
        "direction": "LONG",
        "created_at": 1749013292798
        }
    order_data (SL):
        {
            "order_id": 121112646034,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "qty": "0", # FOR SL, qty will be 0, as by default im set for "closePosition to be True "
            "direction": "LONG",
            "created_at": 1749037471697,
            "ask_price": "155.7"
        }
    '''
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE order_id=%s;", [order_data['order_id']])
            db_res = cur.fetchall()
            if len(db_res):
                logging.info(f"Existing order ID found for {order_data['order_id']}, skipping adding 'NEW' order to DB.")
                return
            cur.execute("""
                INSERT INTO orders (order_id, status, direction, symbol, order_type, ask_price, filled_price, side, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                order_data["order_id"],
                order_data["status"],
                order_data["direction"],
                order_data["symbol"],
                order_data["type"],
                None if order_data["type"] == "MARKET" else order_data["ask_price"], # Ask Price is none
                None, # Filled Price Price is none
                order_data["side"],
                datetime.fromtimestamp(order_data["created_at"]/1000),
                None
            ))
            new_order = cur.fetchone()
            conn.commit()
            logging.info(f"Successfully inserted new order into DB, response: {new_order}")
            return new_order
    finally:
        conn.close()
        
def findByIdAndUpdateFilledMarketOrder(order_id, order_data):
    logging.info(f"Attempting to UPDATE order {order_id} to FILLED")
    '''
        {
        "order_id": 121058809222,
        "status": "FILLED",
        "symbol": "SOLUSDT",
        "side": "BUY",
        "type": "MARKET",
        "qty": "0.09",
        "direction": "LONG",
        "ask_price": "156.5",
        "filled_price": "156.5",
        "updated_at": 1749013292798
        }
    '''
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                            UPDATE orders
                            SET status = %s, ask_price = %s, filled_price = %s, updated_at = %s
                            WHERE order_id = %s
                            RETURNING *;
                        """, (
                order_data['status'], 
                order_data['ask_price'],
                order_data['filled_price'],
                datetime.fromtimestamp(order_data["updated_at"]/1000),
                order_data['order_id'],
            ))
            new_order = cur.fetchone()
            conn.commit()
            logging.info(f"Successfully updated Market Order {order_data['order_id']} with FILLED info: {new_order}")
            return new_order
    finally:
        conn.close()

def findByIdAndUpdateFilledSLTPOrder(order_id, order_data):
    logging.info(f"Attempting to UPDATE order {order_id} to FILLED")
    '''
        {
            "order_id": 121115517313,
            "group_id": "3",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "qty": "0.09",
            "direction": "LONG",
            "filled_price": "156.02",
            "updated_at": 1749038674248
}
    '''
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                            UPDATE orders
                            SET status = %s, filled_price = %s, updated_at = %s
                            WHERE order_id = %s
                            RETURNING *;
                        """, (
                order_data['status'],
                order_data['filled_price'],
                datetime.fromtimestamp(order_data["updated_at"]/1000),
                order_id,
            ))
            new_order = cur.fetchone()
            conn.commit()
            logging.info(f"Successfully updated Market Order {order_id} with FILLED info: {new_order}")
            return new_order
    finally:
        conn.close()

def findByIdAndCancel(order_id, order_data):
    '''
    Updates the status of the order to be cancelled
    '''
    logging.info(f"Attempting to UPDATE order {order_id} to CANCELED")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                            UPDATE orders
                            SET status = %s, updated_at = %s
                            WHERE order_id = %s
                            RETURNING *;
                        """, (
                order_data['status'],
                datetime.fromtimestamp(order_data["updated_at"]/1000),
                order_id,
            ))
            new_order = cur.fetchone()
            conn.commit()
            logging.info(f"Successfully updated Market Order {order_id} to cancelled {new_order}")
            return new_order
    finally:
        conn.close()


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