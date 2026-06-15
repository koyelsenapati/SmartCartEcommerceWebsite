import os
import mysql.connector
from dotenv import load_dotenv


# Load .env file
load_dotenv()


def get_connection():

    try:

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        return connection

    except mysql.connector.Error as error:

        print("Database Connection Error:", error)

        return None