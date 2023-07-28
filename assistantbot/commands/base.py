from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import ContextTypes


class BaseCommand(ABC):
    def __init__(self):
        self._command = None

    @abstractmethod
    async def command_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        ...

    @abstractmethod
    def command_handler(self, *args, **kwargs):
        ...
