import logging
from logging.handlers import RotatingFileHandler
from settings import settings

"""
Настраивает логирование и создает логгер.
- Запись логов в файл
- Вывод логов в консоль
- По умолчанию логирование INFO
- Логирование для стороних библиотек ERROR
"""
logging.basicConfig(
    format="[%(asctime)s]:[%(name)s]:[%(levelname)s] - %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler(
            settings.bot_workdir / "IMEICheckerBot.log",
            maxBytes=(1024 * 1024 * 5),
            backupCount=10,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

logging.getLogger("aiogram").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

LOGS = logging.getLogger("IMEICheckerBot")
