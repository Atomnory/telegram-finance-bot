from playhouse.db_url import connect
from utils import config

pg_db = connect(config.DATABASE_URL)
