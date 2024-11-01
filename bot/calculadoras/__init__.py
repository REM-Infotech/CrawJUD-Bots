from typing import Union
from .tjdft import tjdft

Hints = Union[tjdft]


class calculadoras:

    bots = {"tjdf": tjdft}

    def __init__(self, **kwrgs):
        self.__dict__.update(kwrgs)
        try:

            self.Bot.execution()

        except Exception as e:
            raise e

    @property
    def Bot(self) -> Hints:

        rb = self.bots.get(self.bot)
        if not rb:
            raise AttributeError("Robô não encontrado!!")

        return rb(self.app, self.argv, self.pid)
