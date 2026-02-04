import os
from loguru import logger
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

# Добавляем лологирование
logger.add(f"app/logs/logger.log",
           format="{time} - {level} - {message}",
           level="INFO", rotation="100 Mb", compression="zip")


class Config:
    BOT_TOKEN: str
    USERS: list[int]

    def __init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        workdir = Path(__file__).parent.absolute()
        with (workdir / 'config.json').open() as file:
            data = json.load(file)
        self.USERS = data.get("users")


config = Config()
