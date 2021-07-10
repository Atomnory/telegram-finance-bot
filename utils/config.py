""" Store all environment variables. """
import os

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN_PB')
ACCESS_USER_ID = os.getenv('TELEGRAM_ACCESS_USER_ID')

DATABASE = os.getenv('DB_POSTGRES_TB_PEEWEE_NAME')
USER = os.getenv('DB_POSTGRES_USER')
PASSWORD = os.getenv('DB_POSTGRES_USER_PASSWORD')
HOST = os.getenv('DB_POSTGRES_HOST')
PORT = os.getenv('DB_POSTGRES_PORT')
