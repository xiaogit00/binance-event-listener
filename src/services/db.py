import os
import psycopg2
from dotenv import load_dotenv
from src.services.db_connection import get_connection
import logging

from datetime import datetime

load_dotenv()


def get_orders():
    """Get all orders"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders;")
            return cur.fetchall()
    finally:
        conn.close()

def insertNewOrderByType(order_type, order_data):
    logging.info("Attempting to insert new order into DB...")
    '''
    order_data (MO):
        {
        "order_id": 121058809222,
        "group_id": "fOPYqvypuFM2LKJ3ihzKFZ",
        "status": "NEW",
        "symbol": "SOLUSDT",
        "side": "BUY",
        "type": "MARKET",
        "qty": "0.09",
        "direction": "LONG",
        "created_at": 1749013292798
        }
    '''
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO orders (order_id, group_id, direction, symbol, order_type, ask_price, filled_price, side, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                order_data["order_id"],
                order_data["group_id"],
                order_data["direction"],
                order_data["symbol"],
                order_data["type"],
                None,
                None,
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
        

def add_new_order(res, group_id, ask_price):
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
                INSERT INTO orders (order_id, group_id, symbol, order_type, ask_price, filled_price, side, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                order_id,
                group_id,
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