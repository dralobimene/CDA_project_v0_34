import pygame
import utilitaires


class Player:

    # static variable
    # le fichier png qui affiche le stair
    png_file = "Save/saveGAME/save_png/output_corridors_1.png"

    # static variable
    #  Define an empty list to hold the positions of all players
    tab_player_all_positions = []

    # bouton "start game" pressé:
    # 1] - stockera le fichier
    # json associé au stair ou se trouve actuellement
    # cette instance
    # static variable
    tab_player_all_datas_from_this_dungeon = []

    # 2] - stockera les posit° de ttes les rooms
    # associées au stair
    # static variable
    tab_player_all_positions_rooms = []

    def __init__(self, name, health=100, x=0, y=0):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.radius = 5
        self.speed = 5
        self.tab_player_all_positions.append((self.x, self.y))

    def get_center(self):
        """
        Get center of green circle
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
            on a 1 surface qui ne contient que le joueur.
            Celui-ci peut se deplacer sur tte la surface de surface_player
            qui est équivalente ()

        Utilité:
            permet de deplacer le cercle vert qui represente
            le player

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
        surface_player_width = left_surface_rect.width
        surface_player_height = left_surface_rect.height

        # placer la surface aux coordonnées du left_canvas defini
        # ds DungeonGen.py (ou a sonrectangle: left_canvas_rect)
        # sert + bas ds la methode de blit
        surface_player_x = left_surface_rect.x
        surface_player_y = left_surface_rect.y

        # on applique les dimens° et un canal alpha
        surface_player = pygame.Surface((surface_player_width, surface_player_height),
                                        pygame.SRCALPHA)

        # Clear the screen with a transparent surface
        # surface_player.fill((0, 0, 0, 50))

        #
        pygame.draw.circle(surface_player,
                           self.color,
                           (self.x, self.y),
                           self.radius)

        """
        # dessine 1 pixel noir au centre et sur chacun des pts cardinaux
        # centre
        pygame.draw.circle(surface_player, (0, 0, 0), (self.x, self.y), 1)
        # nord
        pygame.draw.circle(surface_player, (0, 0, 0), (self.x, self.y + 5), 1)
        # est
        pygame.draw.circle(surface_player, (0, 0, 0), (self.x + 5, self.y), 1)
        # sud
        pygame.draw.circle(surface_player, (0, 0, 0), (self.x, self.y - 5), 1)
        # ouest
        pygame.draw.circle(surface_player, (0, 0, 0), (self.x - 5, self.y), 1)
        """

        # Blit the surface to the screen
        # superpose la surface_player au-dessus de la surface
        # (left_canvas defini ds DungeonGen.py)
        surface.blit(surface_player, (surface_player_x, surface_player_y))

        pygame.display.flip()

    def move_left(self):
        print("")

        next_position = (self.x - self.speed, self.y)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file, next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.x -= self.speed
            self.tab_player_all_positions.append((self.x, self.y))

        print("")
        print("tableau des positions du joueur: "
              + str(self.tab_player_all_positions))
        print("")

    def move_right(self):
        print("")

        next_position = (self.x + self.speed, self.y)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file, next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.x += self.speed
            self.tab_player_all_positions.append((self.x, self.y))

        print("")
        print("tableau des positions du joueur: "
              + str(self.tab_player_all_positions))
        print("")

    def move_up(self):
        print("")

        next_position = (self.x, self.y - self.speed)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file,
                                                                  next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.y -= self.speed
            self.tab_player_all_positions.append((self.x, self.y))

        print("")
        print("tableau des positions du joueur: "
              + str(self.tab_player_all_positions))
        print("")

    def move_down(self):
        print("")

        next_position = (self.x, self.y + self.speed)
        next_pixel_color = utilitaires.get_pixel_color_from_image(self.png_file,
                                                                  next_position)

        if next_pixel_color != (255, 255, 255, 255):
            self.y += self.speed
            self.tab_player_all_positions.append((self.x, self.y))

        print("")
        print("tableau des positions du joueur: "
              + str(self.tab_player_all_positions))
        print("")

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def set_name(self, name):
        self.name = name

    def set_health(self, health):
        self.health = health

    def get_position(self):
        return (self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def show(self,
             surface,
             left_surface_rect,
             showPlayerAtStartingGame_pos):
        """
        Utilité:
            permet d'afficher l'instance de la class Player
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
        print("fichier: Player.py")
        print("method: show()")

        self.x, self.y = showPlayerAtStartingGame_pos
        self.draw(surface, left_surface_rect)
        self.tab_player_all_positions.append((self.x, self.y))

        print("tableau des positions du joueur: "
              + str(self.tab_player_all_positions))

    # toString method
    def __str__(self):
        return f"Player(name={self.name}\n,\
                        health={self.health}\n,\
                        x={self.x}\n,\
                        y={self.y}\n,\
                        color={self.color}\n,\
                        radius={self.radius}\n,\
                        actual_position={self.tab_player_all_positions}\n,\
                        speed={self.speed}\n)"
