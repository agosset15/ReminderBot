from aiogram import Bot
from pydantic import BaseSettings, SecretStr
from aiogram.fsm.state import State, StatesGroup


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
bot = Bot(token=config.bot_token.get_secret_value())


class Ad(StatesGroup):
    text = State()
    timedate = State()
    conf = State()
