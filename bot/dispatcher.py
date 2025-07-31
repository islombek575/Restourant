from os import getenv

from aiogram import Dispatcher
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")

dp = Dispatcher()

