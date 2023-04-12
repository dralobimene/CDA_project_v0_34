import pygame
import utilitaires
import random


class NPC:

    # static variable
    # le fichier png qui affiche le stair
    png_file = "Save/saveGAME/save_png/output_corridors_1.png"

    # static variable to count number of instances created
    NPC_count = 0

    # static variable to store all attributes of every instances
    # format will be json dictionaries
    NPC_instances = []

    # 2] - stockera les posit° de ttes les rooms
    # associées au stair
    # static variable
    tab_NPC_all_positions_rooms = []

    def __init__(self,
                 name=None,
                 race="unknown",
                 x=0,
                 y=0,
                 health=100,
                 width=5,
                 height=5):

        self.name = name
        self.race = race
        self.x = x
        self.y = y
        self.health = health
        self.color = (0, 0, 0)
        self.radius = 5
        self.speed = 5
        self.width = width
        self.height = height

        # increment counter of instances
        NPC.NPC_count += 1

        # write json dictionnary containing all attributes
        # of this instance
        NPC_attributes = {
            "NPC_count": NPC.NPC_count,
            "name": self.name,
            "race": self.race,
            "color": self.color,
            "x": self.x,
            "y": self.y,
            "health": self.health,
            "speed": self.speed
        }

        # add this json dictionary to the array
        # every attribute of this instance (so every instance created)
        # will be stored into this array
        # to access: (example: from start.py)
        # for <DICTIONARY_NAME> in <NPC.ARRAY_CONTAINING>:
        #   print(f"Position of NPC {position_attributes['NPC_count']}: ({position_attributes['x']}")
        NPC.NPC_instances.append(NPC_attributes)

    def get_center(self):
        """
        Get center of red circle
        """

        center_x = self.x + self.radius
        center_y = self.y + self.radius
        return (center_x, center_y)

    def draw(self,
             surface,
             left_surface_rect):
        """
        Creer 1 pygame surface avec
            - cô coordonnées celles du left_canvas défini ds DungeonGen.py
            - cô coordonnées celles du left_canvas défini ds DungeonGen.py

        Récupère les dimensions grâce à left_surface_rect pr
        les appliquer à cette pygame surface

        Résultat:
            on a 1 surface qui ne contient que les NPC.
            Cx-ci pvent se deplacer sur tte la surface de surface_NPC
            qui est équivalente ()

        Utilité:
            permet de deplacer les cercles rouge qui representent
            les NPCs

        @param: surface:
            Surface left_canvas definie ds DungeonGen.py
        @param: left_surface_rect:
            rectangle invisible qui sert à récupérer les dimens°
            du canvas left_canvas.
            Défini ds DungeonGen.py
        """

        # Create a new surface

        # prend les dimensions du left_canvas_rect defini ds
        # DungeonGen.py
        surface_NPC_width = left_surface_rect.width
        surface_NPC_height = left_surface_rect.height

        # placer la surface aux coordonnées du left_canvas defini
        # ds DungeonGen.py (ou a son rectangle: left_canvas_rect)
        # sert + bas ds la methode de blit
        surface_NPC_x = left_surface_rect.x
        surface_NPC_y = left_surface_rect.y

        # on applique les dimens° et un canal alpha
        surface_NPC = pygame.Surface((surface_NPC_width, surface_NPC_height),
                                     pygame.SRCALPHA)

        # Clear the screen with a transparent surface
        # surface_NPC.fill((0, 0, 0, 50))

        #
        pygame.draw.circle(surface_NPC,
                           self.color,
                           (self.x, self.y),
                           self.radius)

        """
        # dessine 1 pixel noir au centre et sur chacun des pts cardinaux
        # centre
        pygame.draw.circle(surface_NPC, (0, 0, 0), (self.x, self.y), 1)
        # nord
        pygame.draw.circle(surface_NPC, (0, 0, 0), (self.x, self.y + 5), 1)
        # est
        pygame.draw.circle(surface_NPC, (0, 0, 0), (self.x + 5, self.y), 1)
        # sud
        pygame.draw.circle(surface_NPC, (0, 0, 0), (self.x, self.y - 5), 1)
        # ouest
        pygame.draw.circle(surface_NPC, (0, 0, 0), (self.x - 5, self.y), 1)
        """

        # Blit the surface to the screen
        # superpose la surface_NPC au-dessus de la surface
        # (left_canvas defini ds DungeonGen.py)
        surface.blit(surface_NPC, (surface_NPC_x, surface_NPC_y))

        pygame.display.flip()

    """
    def draw_01(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.display.flip()
    """

    # Add any additional methods you need for your game logic,
    # such as movement, interaction, etc.
    def move_left(self):
        print("")

        next_position = (self.x - self.speed, self.y)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file, next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.x -= self.speed

    def move_right(self):
        print("")

        next_position = (self.x + self.speed, self.y)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file, next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.x += self.speed

    def move_up(self):
        print("")

        next_position = (self.x, self.y - self.speed)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file,
                                                                  next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.y -= self.speed

    def move_down(self):
        print("")

        next_position = (self.x, self.y + self.speed)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file,
                                                                  next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.y += self.speed

    def choose_randomly_deplacement(self):
        # Create a list of the available movement methods
        available_moves = [self.move_right, self.move_left, self.move_up, self.move_down]

        # Choose a random method from the list
        chosen_move = random.choice(available_moves)

        # Apply the chosen method
        chosen_move()

    # Getters and setters
    def get_name(self):
        return self.name

    def get_race(self):
        return self.race

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_health(self):
        return self.health

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_position(self):
        return self.x, self.y

    def set_name(self, name):
        self.name = name

    def set_race(self, race):
        set.race = race

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_health(self, health):
        self.health = health

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def show(self,
             surface,
             left_surface_rect,
             showNPCAtStartingGame_pos):
        """
        Utilité:
            permet d'afficher les instances de la class NPC
            lorsqu'on clique sur le bouton START GAME.
            Les instances seront placées ds des room choisies au hasard.

        @param: surface:
            Le param de la methode draw().
            Ds le but de faire du passage de parametre
        @param: left_surface_rect:
            Le param de la methode draw().
            Ds le but de faire du passage de parametre
        @param: showNPCAtStartingGame_pos:
            1 tuple = aux coordoonnées x - y qui va permettre
            de placer les instances au centre de la room qui a été
            choisie au hasard
        """

        print("")
        print("fichier: NPC.py")
        print("method: show()")

        self.x, self.y = showNPCAtStartingGame_pos
        self.draw(surface, left_surface_rect)
        self.tab_NPC_all_positions.append((self.x, self.y))

        print("tableau des positions du NPC: "
              + str(self.tab_NPC_all_positions))

    # toString method
    def __str__(self):
        return f"NPC(name={self.name}\n,\
                        race={self.race}\n,\
                        x={self.x}\n,\
                        y={self.y}\n,\
                        health={self.health}\n,\
                        color={self.color}\n,\
                        radius={self.radius}\n,\
                        speed={self.speed}\n)"

# Helper function to print the NPC_instances array
# in a JSON formatted string
def print_NPC_instances():
    print(json.dumps(NPC.NPC_instances, indent=4))
