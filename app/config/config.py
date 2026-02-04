import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# Добавляем лологирование
logger.add(f"app/logs/logger.log",
           format="{time} - {level} - {message}",
           level="INFO", rotation="100 Mb", compression="zip")


class Config:
    BOT_TOKEN: str

    def __init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")


config = Config()
