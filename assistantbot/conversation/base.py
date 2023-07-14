from abc import ABC

from telegram.ext import MessageHandler
from telegram.ext.filters import BaseFilter


class ConversationHandler(ABC):
    def __init__(self, type: BaseFilter):
        self._type = type

    def handler(self, *args, **kwargs) -> MessageHandler:
        ...

    def callback(self, *args, **kwargs) -> None:
        ...
