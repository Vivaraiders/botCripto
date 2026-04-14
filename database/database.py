import mysql.connector
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_HOST= getenv('DB_HOST')
DB_USER=getenv('DB_USER')
DB_PASSWORD=getenv('DB_PASSWORD')
DB_DATABASE=getenv('DB_DATABASE')

def get_connection():
    try:
        conn = mysql.connector.connect(
            host= DB_HOST,
            user= DB_USER,
            password= DB_PASSWORD,
            database=DB_DATABASE
        )
    
        print('conexão estabelecida!')
        return conn
    
    except mysql.connector.Error as err:
        print(f'erro na conexão: {err}')
        return None
 