""" Store all environment variables. """
import os

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN_PB')
ACCESS_USER_ID = os.getenv('TELEGRAM_ACCESS_USER_ID')

database = os.getenv('DB_POSTGRES_TB_NAME')
database_peewee = os.getenv('DB_POSTGRES_TB_PEEWEE_NAME')
user = os.getenv('DB_POSTGRES_USER')
password = os.getenv('DB_POSTGRES_USER_PASSWORD')
host = os.getenv('DB_POSTGRES_HOST')
port = os.getenv('DB_POSTGRES_PORT')
