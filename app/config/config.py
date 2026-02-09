import os
import shutil

from loguru import logger
from dotenv import load_dotenv
import json
from pathlib import Path
from app import __version__
from app.models.host import Hosts
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot

load_dotenv()

# Добавляем лологирование
logger.add(f"app/logs/logger.log",
           format="{time} - {level} - {message}",
           level="INFO", rotation="100 Mb", compression="zip")


class Config:
    BOT_TOKEN: str
    USERS: list[int]
    VERSION: str
    HOSTS: Hosts
    BOT: Bot

    def __init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        if not self.BOT_TOKEN:
            raise ValueError("Telegram токен не установлен в переменных окружения")
        workdir = Path(__file__).parent.absolute()
        config_file = workdir / 'files' / "config.json"
        example_file = workdir / "config.json.example"
        self._ensure_config(config_file, example_file)
        with config_file.open() as file:
            data = json.load(file)
        self.USERS = data.get("users")
        self.VERSION = __version__

        self.HOSTS = Hosts(config_file=config_file)
        self.BOT = Bot(token=self.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

    @staticmethod
    def _ensure_config(config_file: Path, example_file: Path):
        if not config_file.exists():
            if not example_file.exists():
                raise FileNotFoundError(
                    "Не найден ни config.json, ни config.json.example"
                )
            config_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(example_file, config_file)
            logger.info("config.json создан из шаблона")


config = Config()
