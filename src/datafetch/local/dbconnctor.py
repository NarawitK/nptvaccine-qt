import os
import mariadb
from dotenv import load_dotenv

load_dotenv()

class MariaDBConnector:
    def __init__(self):
        self.__conn = None

    def getInstance(self):
        try:
            self.__conn = mariadb.connect(
            user = os.getenv('DB_USERNAME'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_ADDRESS'),
            port = int(os.getenv('DB_PORT')),
            database = os.getenv('DB_NAME')
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        return self.__conn

    def close_connection(self):
        self.__conn.close()
