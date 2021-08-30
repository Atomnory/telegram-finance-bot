""" Store all environment variables. """
import os

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN_PB')
ACCESS_USER_ID = os.getenv('TELEGRAM_ACCESS_USER_ID')
DATABASE_URL = os.environ.get('DATABASE_URL')
