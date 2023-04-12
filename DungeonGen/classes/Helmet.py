# -*- coding: UTF-8 -*-

from .Item import Item


class Helmet(Item):
    def __init__(self,
                 wordToDescribe: str = "Helmet",
                 price: int = 0,
                 mayContain: bool = False,
                 color: tuple = (0, 0, 0),
                 isTransportable: bool = True,
                 isDeplacable: bool = True,
                 x: int = 0,
                 y: int = 0,
                 width: int = 5,
                 height: int = 5,
                 defense_power: int = 10):

        super().__init__(wordToDescribe,
                         price,
                         mayContain,
                         color,
                         isTransportable,
                         isDeplacable,
                         x,
                         y,
                         width,
                         height)

        self.__defense_power = defense_power

    def get_defense_power(self) -> int:
        return self.__defense_power

    def set_defense_power(self, defense_power: int) -> None:
        self.__defense_power = defense_power

    # Override the __str__ method
    def __str__(self) -> str:
        return f"Helmet(item_count={Item.item_count}\n,\
                wordToDescribe={self.get_wordToDescribe()}\n,\
                price={self.get_price()}\n,\
                mayContain={self.get_mayContain()}\n,\
                color={self.get_color()}\n,\
                isTransportable={self.get_isTransportable()}\n,\
                isDeplacable={self.get_isDeplacable()}\n,\
                x={self.get_x()}\n,\
                y={self.get_y()}\n,\
                position={self.get_position()}\n,\
                width={self.get_width()}\n,\
                height={self.get_height()},\n\
                defense_power={self.__defense_power})"
