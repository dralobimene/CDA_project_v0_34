# -*- coding: UTF-8 -*-

from .Item import Item


class Sword(Item):
    def __init__(self,
                 wordToDescribe: str = "Sword",
                 price: int = 0,
                 mayContain: bool = False,
                 color: tuple = (0, 0, 0),
                 isTransportable: bool = True,
                 isDeplacable: bool = True,
                 x: int = 0,
                 y: int = 0,
                 width: int = 5,
                 height: int = 5,
                 attack_power: int = 10):

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

        self.__attack_power = attack_power

    def get_attack_power(self) -> int:
        return self.__attack_power

    def set_attack_power(self, attack_power: int) -> None:
        self.__attack_power = attack_power

    # Override the __str__ method
    def __str__(self) -> str:
        return f"Sword(item_count={Item.item_count}\n,\
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
                attack_power={self.__attack_power})"
