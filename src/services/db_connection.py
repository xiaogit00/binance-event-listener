import os
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    logging.info(f"Successfully connected to DB: {os.getenv("DB_NAME")}, user: {os.getenv("DB_USER")}")
    return conn