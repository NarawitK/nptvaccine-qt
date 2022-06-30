import os
from mysql.connector import connect, Error
from dotenv import load_dotenv

load_dotenv()


class MariaDBConnector:
    @staticmethod
    def get_instance():
        try:
            return connect(
            user = os.getenv('DB_USERNAME'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_ADDRESS'),
            port = int(os.getenv('DB_PORT')),
            database = os.getenv('DB_NAME'),
            )
        except Error as e:
            print(f"Error connecting to Database Platform: {e}")
