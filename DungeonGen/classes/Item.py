# -*- coding: UTF-8 -*-

import pygame
import json


class Item:
    """
    Use double underscores to make the attributes private
    """

    # le fichier png qui affiche le stair
    png_file = "Save/saveGAME/save_png/output_corridors_1.png"

    # le fichier json qui contient ttes les infos du stair
    json_file = "Save/saveGAME/save_json/file_level_1.json"

    # static variable to count number of instances created
    item_count = 0

    # static variable to store all attributes of every instances
    # format will be json dictionaries
    item_instances = []

    """
    chatGPT
    keeping the tab_Item_all_positions_rooms variable allows you to store
    the room positions data in the Item class, which can be useful if you
    want to use this data in other parts of your code where the Item class
    is used. If you don't use this variable, you won't be able
    to store this data directly in the Item class.
    """
    # variable pr contenir les datas de ttes les rooms
    tab_Item_all_positions_rooms = []

    """
    chatGPT
    To store the data only once, you can use a class method
    to initialize the tab_Item_all_positions_rooms array when
    the class is loaded. By using the class method init_rooms_data
    and calling it outside the class, you ensure that
    the tab_Item_all_positions_rooms array is populated only once
    when the class is loaded, regardless of how many Item objects
    are created.

    how to call this method:
    into start.py: example:
        Item.init_rooms_data()
    """
    @classmethod
    def init_rooms_data(cls):

        # local import to minimize circular imports problems
        # Using a SOLID pattern implementat° is better approach
        from utilitaires import getAllRoomsDatas

        # cls = param pr accéder à la variable statique
        cls.tab_Item_all_positions_rooms = getAllRoomsDatas(cls.json_file)

        print("")
        print("fichier: Item.py")
        print("methode de classe: init_rooms_data()")
        print("contenu de cls.tab_Item_all_positions_rooms")
        print(cls.tab_Item_all_positions_rooms)
        print("")

    def __init__(self,
                 wordToDescribe: str,
                 price: int = 1,
                 mayContain: bool = False,
                 color: tuple = (1, 0, 0),
                 isTransportable: bool = False,
                 isDeplacable: bool = True,
                 x: int = 1,
                 y: int = 1,
                 width: int = 6,
                 height: int = 6):

        self.__wordToDescribe = wordToDescribe
        self.__price = price
        self.__mayContain = mayContain
        self.__color = color
        self.__isTransportable = isTransportable
        self.__isDeplacable = isDeplacable
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

        # increment counter of instances
        Item.item_count += 1

        # write json dictionnary containing all attributes
        # of this instance
        item_attributes = {
            "item_count": Item.item_count,
            "wordToDescribe": self.__wordToDescribe,
            "price": self.__price,
            "mayContain": self.__mayContain,
            "color": self.__color,
            "isTransportable": self.__isTransportable,
            "isDeplacable": self.__isDeplacable,
            "x": self.__x,
            "y": self.__y,
            "width": self.__width,
            "height": self.__height
        }

        # add this json dictionary to the array
        # every attribute of this instance (so every instance created)
        # will be stored into this array
        # to access: (example: from start.py)
        # for <DICTIONARY_NAME> in <Item.ARRAY_CONTAINING>:
        #   print(f"Position of Item {position_attributes['item_count']}: ({position_attributes['x']}")
        Item.item_instances.append(item_attributes)

    def get_wordToDescribe(self) -> str:
        return self.__wordToDescribe

    def get_price(self) -> int:
        return self.__price

    def get_mayContain(self) -> bool:
        return self.__mayContain

    def get_color(self) -> tuple:
        return self.__color

    def get_isTransportable(self) -> bool:
        return self.__isTransportable

    def get_isDeplacable(self) -> bool:
        return self.__isDeplacable

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_position(self):
        return (self.__x, self.__y)

    def set_wordToDescribe(self, wordToDescribe: str) -> None:
        self.__wordToDescribe = wordToDescribe

    def set_price(self, price: int) -> None:
        self.__price = price

    def set_mayContain(self, mayContain: bool) -> None:
        self.__mayContain = mayContain

    def set_color(self, color: tuple) -> None:
        self.__color = color

    def set_isTransportable(self, isTransportable: bool) -> None:
        self.__isTransportable = isTransportable

    def set_isDeplacable(self, isDeplacable: bool) -> None:
        self.__isDeplacable = isDeplacable

    def set_x(self, x: int) -> None:
        self.__x = x

    def set_y(self, y: int) -> None:
        self.__y = y

    def set_width(self, width: int) -> None:
        self.__width = width

    def set_height(self, height: int) -> None:
        self.__height = height

    def set_position(self, x, y):
        self.__x = x
        self.__y = y

    def draw(self, surface, left_surface_rect):
        surface_item_width = left_surface_rect.width
        surface_item_height = left_surface_rect.height
        surface_item_x = left_surface_rect.x
        surface_item_y = left_surface_rect.y
        surface_item = pygame.Surface((surface_item_width, surface_item_height),
                                      pygame.SRCALPHA)

        rect = pygame.Rect(self.get_x(),
                           self.get_y(),
                           self.get_width(),
                           self.get_height())

        # print(f"Drawing rect: {rect}")

        pygame.draw.rect(surface_item,
                         self.get_color(),
                         rect)

        surface.blit(surface_item,
                     (surface_item_x, surface_item_y))

        pygame.display.flip()

    def show(self,
             surface,
             left_surface_rect,
             showItemAtStartingGame_pos):

        """
        Utilité:
            permet d'afficher 1 instance de la class Item
            lorsqu'on clique sur le bouton START GAME.
            L'instance sera placée au centre d'1 room choisie au hasard.

        @param: surface:
            Le param de la methode draw().
            Ds le but de faire du passage de parametre
        @param: left_surface_rect:
            Le param de la methode draw().
            Ds le but de faire du passage de parametre
        @param: showPlayerAtStartingGame_pos:
            1 tuple = aux coordoonnées x - y qui va permettre
            de placer l'instance au centre de la room qui a été
            choisie au hasard
        """

        print("")
        print("fichier: Item.py")
        print("method: show()")
        self.x, self.y = showItemAtStartingGame_pos
        self.draw(surface, left_surface_rect)

    # toString method
    def __str__(self) -> str:
        return f"Item(item_count={Item.item_count}\n,\
                wordToDescribe={self.__wordToDescribe}\n,\
                price={self.__price}\n,\
                mayContain={self.__mayContain}\n,\
                color={self.__color}\n,\
                isTransportable={self.__isTransportable}\n,\
                isDeplacable={self.__isDeplacable}\n,\
                x={self.__x}\n,\
                y={self.__y}\n,\
                position={self.get_position()}\n,\
                width={self.__width}\n,\
                height={self.__height})"


# Helper function to print the item_instances array
# in a JSON formatted string
def print_item_instances():
    print(json.dumps(Item.item_instances, indent=4))
