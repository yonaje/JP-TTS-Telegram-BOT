TOKEN = '5439586795:AAFDliDfwPsAQikxtHRVuQsU0gpH4WilYLg'

import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile


from voicevox import Client
from googletrans import Translator