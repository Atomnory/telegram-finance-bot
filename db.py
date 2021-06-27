from playhouse.postgres_ext import PostgresqlExtDatabase
from utils import config

pg_db = PostgresqlExtDatabase(database=config.database_peewee,
                              user=config.user,
                              password=config.password,
                              host=config.host,
                              port=config.port)
