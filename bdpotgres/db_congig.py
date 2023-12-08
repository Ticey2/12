import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import settings


connection = psycopg2.connect(user=settings.user, password=settings.password)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor()
sql_create_database = cursor.execute(
    "CREATE DATABASE test03 ENCODING = 'UTF-8' LC_COLLATE='ru_RU.UTF-8' LC_CTYPE='ru_RU.UTF-8' TEMPLATE template0;")

cursor.close()
connection.close()