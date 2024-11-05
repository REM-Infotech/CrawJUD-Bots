from typing import Union

from bot.pje.pauta import pauta

Hints = Union[pauta]


class pje:

    def __init__(self, **kwrgs):
        self.kwrgs = kwrgs
        self.__dict__.update(kwrgs)
        try:

            self.Bot.execution()

        except Exception as e:
            raise e

    @property
    def Bot(self) -> Hints:

        rb = self.bots.get(self.typebot)
        if not rb:
            raise AttributeError("Robô não encontrado!!")

        return rb(**self.kwrgs)
