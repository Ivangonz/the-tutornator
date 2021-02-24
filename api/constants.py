import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
SQL_ALCHEMY_DATABASE_URI = os.getenv('SQL_ALCHEMY_DATABASE_URI')
