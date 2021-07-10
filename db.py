from playhouse.postgres_ext import PostgresqlExtDatabase
from utils import config

pg_db = PostgresqlExtDatabase(database=config.DATABASE,
                              user=config.USER,
                              password=config.PASSWORD,
                              host=config.HOST,
                              port=config.PORT)
