import os

from dotenv import load_dotenv


load_dotenv()

redis_password = os.getenv('REDIS_PASSWORD')