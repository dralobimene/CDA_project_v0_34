# -*- coding: UTF-8 -*-

import sys
import pygame
import random
import os
from datetime import datetime
import json

from bsp.bsp_moj import dungeon
import utilitaires
from classes.Item import Item
from classes.NPC import NPC

# u may call the helper
from classes.Item import print_item_instances

from pygame.locals import *


# definit° de constantes

# colors
TRANSPARENT = pygame.Color(0, 0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)
RED = pygame.Color(255, 0, 0)
GREY = pygame.Color(128, 128, 128)

ROOM_COL = GREY
CORR_COL = BLACK

# les dossiers de sauvegarde
LES_ARRAY = "Save/saveGAME/save_array"
LES_JSON = "Save/saveGAME/save_json"
LES_SVG = "Save/saveGAME/save_svg"
LES_PNG = "Save/saveGAME/save_png"


@utilitaires.count_calls
def generate_dungeon():

    #
    seed = None

    # Increment the count each time generate_dungeon is called
    generate_dungeon.count += 1

    # Print the value of the count variable
    print(f"generate_dungeon has been called {generate_dungeon.count} times.")
    print("")

    #
    dung = dungeon(left_canvas_width,
                   left_canvas_height,
                   seed)

    # ======================================================

    # definit° de nveaux attributs pr le dongeon

    # le nom du dongeon généré
    dung.name = utilitaires.generate_random_string(20)

    # generation date
    now = datetime.now()
    dung.generation_date = now.strftime("%Y-%m-%d_%H-%M-%S")

    # permet de numéroter chacune des rooms
    # de manière incrémentale
    index_numero_room = 0


    # print("")
    # print("impress° des attributs du dongeon généré pr verif")
    # print("valeur de dung.name: " + str(dung.name))
    # print("valeur de dung.generation_date: " + str(dung.generation_date))

    # ecrit le dictionnaire json de ce stair
    # partie 01
    stair_data = {
        'stair_name': dung.name,
        'stair_date_generation': dung.generation_date,
    }

    # ======================================================

    # create an empty dictionary to store
    # datas for each room defined into this stair
    rooms_data = {}

    # loop to define rooms of this stair
    for piece in dung:

        # print("")
        # print("info de la piece (ou room)")
        # print("valeur de piece: " + str(piece))
        # print(" "*piece.depth + str(piece.packit()))

        if piece.leftBIS is None and piece.r is None:

            # increment variable to give a number for each room
            index_numero_room += 1

            # define color of the room
            nROOM_COL = ROOM_COL

            # draw each room
            # pygame.draw.rect(left_canvas, nROOM_COL, piece.room.packit())
            pygame.draw.rect(left_canvas, RED, piece.room.packit())
            # print("packit: --" + str(piece.room.packit()))
            # print("packit01: " + str(piece.room.packit()[0]))
            # print("packit01: " + str(piece.room.packit()[1]))
            # print("packit01: " + str(piece.room.packit()[2]))
            # print("packit01: " + str(piece.room.packit()[3]))

            x_rect = piece.room.packit()[0]
            y_rect = piece.room.packit()[1]
            width_rect = piece.room.packit()[2]
            height_rect = piece.room.packit()[3]

            #
            red_rectangles.append((x_rect, y_rect, width_rect, height_rect))
            # print("contenu de la list red_rectangles")
            # print(red_rectangles)

            center_rect = (x_rect + width_rect / 2, y_rect + height_rect / 2)

            # pygame.draw.circle(left_canvas, BLUE, center_rect, 5)

            # give a name to the room with variable incremented
            piece.room.name = f"Room_{index_numero_room}"

            # print("-- valeur de piece.room.name: " +
                  # str(piece.room.name))
            # print("-- valeur de piece.room.x: " +
                  # str(piece.room.x))
            # print("-- valeur de piece.room.y: " +
                  # str(piece.room.y))
            # print("-- valeur de piece.room.width: " +
                  # str(piece.room.width))
            # print("-- valeur de piece.room.height: " +
                  # str(piece.room.height))
            # print("-- valeur de piece.room.center: " +
                  # str(piece.room.center))

            #
            connect_rooms(dung.tree)

            print("")

            # ecrit le dictionnaire json qui contient
            # les attributs de chacune des rooms de ce stair
            # partie 02
            room_data = {
                "name": piece.room.name,
                "x": piece.room.x,
                "y": piece.room.y,
                "width": piece.room.width,
                "height": piece.room.height,
                "center": piece.room.center,
            }

            # print("Information de la piece (room_data): " +
            # str(room_data))

            # add the room data to the dictionary
            rooms_data[piece.room.name] = room_data

    # combiner les différents dictionnaires json de ce stair
    # pr les ecrire ds le meme fichier json
    stair_dictionaries = {**stair_data, "rooms": rooms_data}


    #
    connect_secret_rooms(dung.tree.leftBIS,
                         dung.tree.r,
                         dung.tree.split_orientation)


    # ecrire le fichier json
    utilitaires.write_dict_to_json(stair_dictionaries,
                                   str(LES_JSON) +
                                   "/file_level_" +
                                   str(generate_dungeon.count) +
                                   ".json")

    # stocke chaque tuple de pixels de chaque room de ce stair
    # les pixels des rooms st de couleur rouge
    content_pixels_rooms = utilitaires.store_pixels_with_color(RED,
                                                               left_canvas)

    """
    #
    print("")
    print("sortie console: content_pixels_rooms: ")
    print(content_pixels_rooms)
    print("")
    """

    """
    # ecrit le contenu de content_pixels_rooms ds 1 fichier numpy
    utilitaires.write_binary_file(content_pixels_rooms,
                                  str(LES_ARRAY) +
                                  "/file_level_" +
                                  str(generate_dungeon.count) + ".npy")
    """

    """
    #
    print("")
    print("sortie console: contenu du fichier qui doit contenir")
    print("file_level_1.npy")

    utilitaires.load_and_display_npy("Save/saveGAME/save_array/file_level_1.npy")
    """

    # stocke chaque tuple de pixels de chaque corridor de ce stair
    # les pixels des corridors st de couleur jaune
    content_pixels_corridors = utilitaires.store_pixels_with_color(YELLOW,
                                                               left_canvas)
    """
    #
    print("")
    print("sortie console: content_pixels_corridors: ")
    print(content_pixels_corridors)
    print("")
    """

    """
    # ecrit le contenu de content_pixels_corridors ds 1 fichier numpy
    utilitaires.write_binary_file(content_pixels_corridors,
                                  str(LES_ARRAY) +
                                  "/file_level_" +
                                  str(generate_dungeon.count + 1) + ".npy")
    """

    """
    #
    print("")
    print("sortie console: contenu du fichier qui doit contenir")
    print("file_level_2.npy")

    utilitaires.load_and_display_npy("Save/saveGAME/save_array/file_level_2.npy")
    """

    """
    #
    print("")
    print("sortie console:")
    print("Affiche la couleur de chaque pixels de content_pixels_rooms")
    """
    utilitaires.get_color_at_position(content_pixels_rooms, left_canvas)
    print("")

    #
    # print("")
    # print("sortie console:")
    # print("Affiche la couleur de chaque pixels de content_pixels_corridors")

    utilitaires.get_color_at_position(content_pixels_corridors, left_canvas)
    print("")



    """
    #
    print("")
    print("sortie console: list03")
    list03 = utilitaires.find_common_tuples_from_2_lists(content_pixels_rooms,
                                                         content_pixels_corridors)
    print(list03)
    print("")
    """

    """
    #
    rendu = utilitaires.find_overlap_pixels(
            "Save/saveGAME/save_array/file_level_1.npy",
            "Save/saveGAME/save_array/file_level_2.npy")

    print("")
    print("sortie console: rendu")
    print(rendu)
    print("")


    utilitaires.write_binary_file(rendu,
                                  str(LES_ARRAY) +
                                  "/file_level_" +
                                  str(generate_dungeon.count + 2) + ".npy")

    print("")
    print("sortie console: contenu du fichier qui doit contenir")
    print("file_level3.npy")
    utilitaires.load_and_display_npy("Save/saveGAME/save_array/file_level_3.npy")
    print("")
    """

    # enregistre 1 png du stair
    # que l'on va afficher
    pygame.image.save(left_canvas, "Save/saveGAME/save_png/output_corridors_1.png")

    # remplit le canvas d'1 nvelle couche de blanc
    # pr effacer le precedent stair
    left_canvas.fill(WHITE)

    # Affiche le png du stair
    utilitaires.display_png_on_canvas(left_canvas,
                                      "Save/saveGAME/save_png/output_corridors_1.png")

    # imprime ts les tuples qui affichent des rectangles jaunes
    # print(tab_corridors)

    return dung


@utilitaires.count_calls
def connect_rooms_between_rooms(room1,
                                room2,
                                CORR_WIDTH=10,
                                nCORR_COL=GREY):
    px = room1.room.x + room1.room.width/2
    py = room1.room.y + room1.room.height/2
    kx = room2.room.x + room2.room.width/2
    ky = room2.room.y + room2.room.height/2

    if px < kx:
        # Check if the corridor overlaps with room1
        if py + CORR_WIDTH > room1.room.y + room1.room.height:
            # start_y = (room1.room.y + room1.room.height) / 2
            start_y = (room1.room.y + room1.room.height) + 1
        else:
            start_y = py

        # Check if the corridor overlaps with room2
        if ky - CORR_WIDTH < room2.room.y:
            # end_y = (room2.room.y / 2)
            end_y = (room2.room.y - 1)
        else:
            end_y = ky

        # pygame.draw.rect(left_canvas, nCORR_COL, (px, start_y, CORR_WIDTH,
                                                  # end_y-start_y))
    elif px > kx:
        # Check if the corridor overlaps with room1
        if py + CORR_WIDTH > room1.room.y + room1.room.height:
            # start_y = (room1.room.y + room1.room.height) / 2
            start_y = (room1.room.y + room1.room.height) + 1
        else:
            start_y = py

        # Check if the corridor overlaps with room2
        if ky - CORR_WIDTH < room2.room.y:
            # end_y = room2.room.y / 2
            end_y = (room2.room.y - 1)
        else:
            end_y = ky

        # pygame.draw.rect(left_canvas, nCORR_COL, (kx, start_y, CORR_WIDTH,
                                                  # end_y-start_y))
    elif py < ky:
        # Check if the corridor overlaps with room1
        if px + CORR_WIDTH > room1.room.x + room1.room.width:
            # start_x = (room1.room.x + room1.room.width) / 2
            start_x = (room1.room.x + room1.room.width) + 1
        else:
            start_x = px

        # Check if the corridor overlaps with room2
        if kx - CORR_WIDTH < room2.room.x:
            # end_x = room2.room.x
            end_x = room2.room.x - 1
        else:
            end_x = kx

        # pygame.draw.rect(left_canvas, nCORR_COL, (start_x, py, end_x-start_x,
                                                  # CORR_WIDTH))
    else:
        # Check if the corridor overlaps with room1
        if px + CORR_WIDTH > room1.room.x + room1.room.width:
            # start_x = (room1.room.x + room1.room.width) / 2
            start_x = (room1.room.x + room1.room.width) + 1
        else:
            start_x = px

        # Check if the corridor overlaps with room2
        if kx - CORR_WIDTH < room2.room.x:
            # end_x = room2.room.x
            end_x = room2.room.x - 1
        else:
            end_x = kx

        # pygame.draw.rect(left_canvas, nCORR_COL, (start_x, ky, end_x-start_x,
                                                  # CORR_WIDTH))


@utilitaires.count_calls
def connect_rooms(node, CORR_WIDTH=10, nCORR_COL=GREY):
    left = node.leftBIS
    right = node.r

    if left.leftBIS is not None:
        connect_rooms(left, CORR_WIDTH, nCORR_COL)
    if right.leftBIS is not None:
        connect_rooms(right, CORR_WIDTH, nCORR_COL)

    # Call the draw_corr function instead of connect_rooms_between_rooms
    px, py, kx, ky, pos = draw_corr(left, right, CORR_WIDTH, nCORR_COL)

    # Determine the position of the current node's
    # room based on the child rooms
    if px < kx:
        node.room.x = int(px)
        node.room.y = int(ky)
    else:
        node.room.x = int(kx)
        node.room.y = int(py)

    node.room.width = 0
    node.room.height = 0


@utilitaires.count_calls
def draw_corr(left,
              right,
              CORR_WIDTH=10,
              nCORR_COL=RED):

    px = left.room.x + left.room.width/2
    py = left.room.y + left.room.height/2
    kx = right.room.x + right.room.width/2
    ky = right.room.y + right.room.height/2

    code = determine_pos((left.room.x+left.room.width/2,
                          left.room.y+left.room.height/2),
                         (right.room.x+right.room.width/2,
                          right.room.y+right.room.height/2))

    # print(" "*(left.depth-1) + str(left.room.packit()))
    # print(" "*(right.depth-1) + str(right.room.packit()))

    #
    pos = random.choice((0, 1))

    #
    rectangles = []
    circles = []
    other_rectangles = []

    if code == 10:
        # bottom right
        if pos == 0:
            # down, then right
            # corridors
            """
            rect1 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     py,
                                     CORR_WIDTH,
                                     ky-py + CORR_WIDTH))

            other_rectangles.append((rect1.x,
                                     rect1.y,
                                     rect1.width,
                                     rect1.height))

            """

            # keep rect1 but do not draw it
            rect1 = (px, py, CORR_WIDTH, ky-py + CORR_WIDTH)

            # add rect1 inside other_rectangles array
            other_rectangles.append(rect1)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            """
            rect2 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     ky,
                                     kx - px + CORR_WIDTH,
                                     CORR_WIDTH))

            other_rectangles.append((rect2.x,
                                     rect2.y,
                                     rect2.width,
                                     rect2.height))
            """

            # keep rect2 but do not draw it
            rect2 = (px, ky, kx - px + CORR_WIDTH, CORR_WIDTH)

            # add rect2 inside other_rectangles array
            other_rectangles.append(rect2)


            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            rectangles.extend([rect1, rect2])

            circle1 = (px, py), 5
            circle2 = (kx, ky), 5
            circles.extend([circle1, circle2])

        else:
            # right, then down
            # corridors

            """
            rect1 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     py,
                                     kx - px + CORR_WIDTH,
                                     CORR_WIDTH))

            other_rectangles.append((rect1.x,
                                     rect1.y,
                                     rect1.width,
                                     rect1.height))
            """

            # keep rect1 but do not draw it
            rect1 = (px, py, kx - px + CORR_WIDTH, CORR_WIDTH)

            # add rect1 inside other_rectangles array
            other_rectangles.append(rect1)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            """
            rect2 = pygame.draw.rect(left_canvas, nCORR_COL, (kx,
                                     py,
                                     CORR_WIDTH,
                                     ky - py + CORR_WIDTH))

            other_rectangles.append((rect2.x,
                                     rect2.y,
                                     rect2.width,
                                     rect2.height))
            """

            # keep rect2 but do not draw it
            rect2 = (kx, py, CORR_WIDTH, ky - py + CORR_WIDTH)

            # add rect2 inside other_rectangles array
            other_rectangles.append(rect2)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            rectangles.extend([rect1, rect2])

            circle1 = (px, py), 5
            circle2 = (kx, ky), 5
            circles.extend([circle1, circle2])

    elif code == 9:
        # top right
        # corridors
        if pos == 0:

            """
            rect1 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     py,
                                     CORR_WIDTH,
                                     ky - py + CORR_WIDTH))

            other_rectangles.append((rect1.x,
                                     rect1.y,
                                     rect1.width,
                                     rect1.height))
            """

            # keep rect1 but do not draw it
            rect1 = (px, py, CORR_WIDTH, ky - py + CORR_WIDTH)

            # add rect1 inside other_rectangles array
            other_rectangles.append(rect1)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            """
            rect2 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     ky,
                                     kx - px + CORR_WIDTH,
                                     CORR_WIDTH))

            other_rectangles.append((rect2.x,
                                     rect2.y,
                                     rect2.width,
                                     rect2.height))
            """

            # keep rect2 but do not draw it
            rect2 = (px, ky, kx - px + CORR_WIDTH, CORR_WIDTH)

            # add rect2 inside other_rectangles array
            other_rectangles.append(rect2)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            rectangles.extend([rect1, rect2])

            circle1 = (px, py), 5
            circle2 = (kx, ky), 5
            circles.extend([circle1, circle2])

        else:
            # corridors
            """
            rect1 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     py,
                                     kx - px + CORR_WIDTH,
                                     CORR_WIDTH))

            other_rectangles.append((rect1.x,
                                     rect1.y,
                                     rect1.width,
                                     rect1.height))
            """

            # keep rect1 but do not draw it
            rect1 = (px, py, kx - px + CORR_WIDTH, CORR_WIDTH)

            # add rect1 inside other_rectangles array
            other_rectangles.append(rect1)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            """
            rect2 = pygame.draw.rect(left_canvas, nCORR_COL, (kx,
                                     py,
                                     CORR_WIDTH,
                                     ky - py + CORR_WIDTH))

            other_rectangles.append((rect2.x,
                                     rect2.y,
                                     rect2.width,
                                     rect2.height))
            """

            # keep rect2 but do not draw it
            rect2 = (kx, py, CORR_WIDTH, ky - py + CORR_WIDTH)

            # add rect2 inside other_rectangles array
            other_rectangles.append(rect2)


            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            rectangles.extend([rect1, rect2])

            circle1 = (px, py), 5
            circle2 = (kx, ky), 5
            circles.extend([circle1, circle2])

    elif code == 6:
        # bottom left
        # corridors
        if pos == 0:

            """
            rect1 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     py,
                                     CORR_WIDTH,
                                     ky - py + CORR_WIDTH))

            other_rectangles.append((rect1.x,
                                     rect1.y,
                                     rect1.width,
                                     rect1.height))
            """

            # keep rect1 but do not draw it
            rect1 = (px, py, CORR_WIDTH, ky - py + CORR_WIDTH)

            # add rect1 inside other_rectangles array
            other_rectangles.append(rect1)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            """
            rect2 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                             ky,
                             kx - px + CORR_WIDTH,
                             CORR_WIDTH))
            other_rectangles.append((rect2.x,
                                     rect2.y,
                                     rect2.width,
                                     rect2.height))
            """

            # keep rect2 but do not draw it
            rect2 = (px, ky, kx - px + CORR_WIDTH, CORR_WIDTH)

            # add rect2 inside other_rectangles array
            other_rectangles.append(rect2)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            rectangles.extend([rect1, rect2])

            circle1 = (px, py), 5
            circle2 = (kx, ky), 5
            circles.extend([circle1, circle2])

        else:
            # corridors

            """
            rect1 = pygame.draw.rect(left_canvas, nCORR_COL, (px,
                                     py,
                                     kx - px + CORR_WIDTH,
                                     CORR_WIDTH))

            other_rectangles.append((rect1.x,
                                     rect1.y,
                                     rect1.width,
                                     rect1.height))
            """

            # keep rect1 but do not draw it
            rect1 = (px, py, kx - px + CORR_WIDTH, CORR_WIDTH)

            # add rect1 inside other_rectangles array
            other_rectangles.append(rect1)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            """
            rect2 = pygame.draw.rect(left_canvas, nCORR_COL, (kx,
                                     py,
                                     CORR_WIDTH,
                                     ky - py + CORR_WIDTH))

            other_rectangles.append((rect2.x,
                                     rect2.y,
                                     rect2.width,
                                     rect2.height))
            """

            # keep rect2 but do not draw it
            rect2 = (kx, py, CORR_WIDTH, ky - py + CORR_WIDTH)

            # add rect2 inside other_rectangles array
            other_rectangles.append(rect2)

            # print("contenu de la liste other_rectangles")
            # print(other_rectangles)

            rectangles.extend([rect1, rect2])

            circle1 = (px, py), 5
            circle2 = (kx, ky), 5
            circles.extend([circle1, circle2])

    # Draw circles at the beginning and the end of the rectangles
    circle_color = BLUE
    circle_radius = 5

    # Check for overlaps between blue circles and red rectangles
    for rect in rectangles:
        x, y, width, height = rect
        if width > height:
            rect_type = "horizontal"
        elif height > width:
            rect_type = "vertical"
        else:
            rect_type = "square"

        # print(f"The {rect_type} red rectangle: {rect}")

        for circle_center, circle_radius in circles:
            if utilitaires.circle_rect_overlap(circle_center,
                                               circle_radius,
                                               rect):
                # print("A blue circle overlaps with a red rectangle.")

                # Draw circles at the beginning and the end of the rectangles
                # pygame.draw.circle(left_canvas,
                                   # GREEN,
                                   # (int(px), int(py)), circle_radius)

                # pygame.draw.circle(left_canvas,
                                   # circle_color,
                                   # (int(kx), int(ky)), circle_radius)
                break
                # pass

    for red_rect in red_rectangles:
        for other_rect in other_rectangles:
            intersection = utilitaires.rectangles_intersect(red_rect,
                                                            other_rect)
            if intersection:
                # print(f"Red rectangle {red_rect} intersects with other")
                # print(f"rectangle {other_rect} at point {intersection}.")

                # pygame.draw.circle(left_canvas, BLACK, (intersection), 5)
                pass

    # Subtract overlapping parts of other rectangles
    for red_rect in red_rectangles:
        # les rectangles qui overlappent les rooms
        new_other_rectangles = []
        for other_rect in other_rectangles:
            new_other_rectangles.extend(utilitaires.subtract_rectangles(other_rect, red_rect))
        other_rectangles = new_other_rectangles

    # Draw the remaining parts of other rectangles
    for other_rect in other_rectangles:
        x, y, w, h = other_rect

        #
        index_empty_json = 1

        if w > h:

            # print("The yellow rectangle is horizontal.")
            # print("width: " + str(w))
            # print("height: " + str(h))

            if w < 10 or h < 10:

                # pygame.draw.rect(left_canvas, BLACK, (x, y, w, h))

                pass
            else:
                if 0 <= x and 0 <= y and x + w <= left_canvas_rect.width and y + h <= left_canvas_rect.height:
                    # print("The rectangle is entirely drawn
                    # within the canvas.")
                    pygame.draw.rect(left_canvas, YELLOW, (x, y, w, h))

                    # ajoute au tableau
                    tab_corridors.append((x, y, width, height))

                    # ======================================================
                    # open corridors.json & append each other_rect

                    # This code checks if the file "corridors.json"
                    # located in the directory "Save/saveGAME/test"self
                    # has a size of 0 bytes.
                    # if the file is empty or doesn't exist,
                    # the condition will evaluate to True, and the code
                    # inside the if statement will be executed.
                    # If the file has some content, the condition will
                    # evaluate to False, and the code inside the
                    # if statement will be skipped
                    if os.path.getsize("Save/saveGAME/test/corridors.json") == 0:
                        corridors_data = {"corridors": {}}
                    else:
                        with open("Save/saveGAME/test/corridors.json", "r") as f:
                            corridors_data = json.load(f)

                    corridors_index = len(corridors_data["corridors"]) + 1
                    corridors_key = f"corridors_{corridors_index}"

                    corridors_data["corridors"][corridors_key] = {
                        "name": corridors_key,
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h
                    }

                    with open("Save/saveGAME/test/corridors.json", "w") as f:
                        json.dump(corridors_data, f, indent=4)
                    # ======================================================
                else:
                    # print("The rectangle is not entirely drawn within the canvas.")
                    # print("do not draw")
                    pass

        elif w < h:
            # print("01: The yellow rectangle is vertical.")
            # print("width: " + str(w))
            # print("height: " + str(h))
            if w < 10 or h < 10:
                # pygame.draw.rect(left_canvas, BLACK, (x, y, w, h))
                pass
            else:
                if 0 <= x and 0 <= y and x + w <= left_canvas_rect.width and y + h <= left_canvas_rect.height:
                        # print("The rectangle is entirely drawn within the canvas.")
                        pygame.draw.rect(left_canvas, YELLOW, (x, y, w, h))

                        # a priori on a pas besoin de ce qui suit,
                        # ca a l'air d'ê intégré ds la précédente condit°
                        """
                        # ajoute au tableau
                        tab_corridors.append((x, y, width, height))

                        # ======================================================
                        # open corridors.json & append each other_rect

                        # This code checks if the file "corridors.json"
                        # located in the directory "Save/saveGAME/test"self
                        # has a size of 0 bytes.
                        # if the file is empty or doesn't exist,
                        # the condition will evaluate to True, and the code
                        # inside the if statement will be executed.
                        # If the file has some content, the condition will
                        # evaluate to False, and the code inside the
                        # if statement will be skipped
                        if os.path.getsize("Save/saveGAME/test/corridors.json") == 0:
                            corridors_data = {"corridors": {}}
                        else:
                            with open("Save/saveGAME/test/corridors.json", "r") as f:
                                corridors_data = json.load(f)

                        corridors_index = len(corridors_data["corridors"]) + 1
                        corridors_key = f"corridors_{corridors_index}"

                        corridors_data["corridors"][corridors_key] = {
                            "name": corridors_key,
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h
                        }

                        with open("Save/saveGAME/test/corridors.json", "w") as f:
                            json.dump(corridors_data, f, indent=4)
                        # ======================================================
                        """

                else:
                    # print("The rectangle is not entirely drawn within the canvas.")
                    # print("do not draw")
                    pass
        else:
            # print("the yellow rectangle is a square.")
            # print("width: " + str(w))
            # print("height: " + str(h))
            if w < 10 or h < 10:
                # pygame.draw.rect(left_canvas, BLACK, (x, y, w, h))
                pass
            else:
                if 0 <= x and 0 <= y and x + w <= left_canvas_rect.width and y + h <= left_canvas_rect.height:
                        # print("The rectangle is entirely drawn within the canvas.")
                        pygame.draw.rect(left_canvas, YELLOW, (x, y, w, h))

                        # a priori on a pas besoin de ce qui suit,
                        # ca a l'air d'ê intégré ds la précédente condit°
                        """
                        # ajoute au tableau
                        tab_corridors.append((x, y, width, height))

                        # ======================================================
                        # open corridors.json & append each other_rect

                        # This code checks if the file "corridors.json"
                        # located in the directory "Save/saveGAME/test"self
                        # has a size of 0 bytes.
                        # if the file is empty or doesn't exist,
                        # the condition will evaluate to True, and the code
                        # inside the if statement will be executed.
                        # If the file has some content, the condition will
                        # evaluate to False, and the code inside the
                        # if statement will be skipped
                        if os.path.getsize("Save/saveGAME/test/corridors.json") == 0:
                            corridors_data = {"corridors": {}}
                        else:
                            with open("Save/saveGAME/test/corridors.json", "r") as f:
                                corridors_data = json.load(f)

                        corridors_index = len(corridors_data["corridors"]) + 1
                        corridors_key = f"corridors_{corridors_index}"

                        corridors_data["corridors"][corridors_key] = {
                            "name": corridors_key,
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h
                        }

                        with open("Save/saveGAME/test/corridors.json", "w") as f:
                            json.dump(corridors_data, f, indent=4)
                        # ======================================================
                        """

                else:
                    # print("The rectangle is not entirely drawn within the canvas.")
                    # print("do not draw")
                    pass

    #
    return px, py, kx, ky, pos


def determine_pos(a, b):

    ax, ay = a
    bx, by = b

    # using a modification of Cohen-Sutherland clipping algorithm
    code = 0  # 0000
    top = 1  # 0001
    bottom = 2  # 0010
    left = 4  # 0100
    right = 8  # 1000

    if ax >= bx:
        code = code | left
    else:
        code = code | right

    if ay >= by:
        code = code | top
    else:
        code = code | bottom
    # print("code is", code)
    return code


def connect_secret_rooms(left,
                         right,
                         split_orientation):
    SEC_CORR_WIDTH = 10
    SEC_CORR_COL = CORR_COL

    # split_orientation is 0 if vertical, 1 if horizontal
    l_list = find_left_candidates(left, split_orientation)
    r_list = find_right_candidates(right, split_orientation)

    halfl = int(len(l_list)/2)
    halfr = int(len(r_list)/2)

    # for l_list[1,2,3,4] and r_list[1,2,3,4,5,6,7,8,9]
    # result is [(1,1), (2,2), (4,9), (3,8)]. The order is not important,
    # grouping is.
    cand_list = list(zip(l_list[:halfl], r_list[:halfr]))
    cand_list.extend(zip(reversed(l_list[halfl:]), reversed(r_list[halfr:])))
    for room1, room2 in cand_list:
        if random.randint(0, 100) < 75:
            draw_corr(room1, room2, SEC_CORR_WIDTH, GREY)
        else:
            draw_corr(room1, room2, SEC_CORR_WIDTH, GREY)


def find_left_candidates(left, so):
    cand_list = []
    if left.leftBIS is None:
        if left.depth > 2:
            cand_list.append(left)
    elif left.split_orientation == 1:
        if so == 1:
            cand_list.extend(find_left_candidates(left.r, 1))
        else:
            cand_list.extend(find_left_candidates(left.leftBIS, 0))
            cand_list.extend(find_left_candidates(left.r, 0))
    else:
        if so == 1:
            cand_list.extend(find_left_candidates(left.leftBIS, 1))
            cand_list.extend(find_left_candidates(left.r, 1))
        else:
            cand_list.extend(find_left_candidates(left.r, 0))
    return cand_list


def find_right_candidates(right, so):
    cand_list = []
    if right.leftBIS is None:
        if right.depth > 2:
            cand_list.append(right)
    elif right.split_orientation == 1:
        if so == 1:
            cand_list.extend(find_right_candidates(right.leftBIS, 1))
        else:
            cand_list.extend(find_right_candidates(right.leftBIS, 0))
            cand_list.extend(find_right_candidates(right.r, 0))
    else:
        if so == 1:
            cand_list.extend(find_right_candidates(right.leftBIS, 1))
            cand_list.extend(find_right_candidates(right.r, 1))
        else:
            cand_list.extend(find_right_candidates(right.leftBIS, 0))
    return cand_list

# ============================================================================
# ============================================================================

pygame.init()

# Define a static variable to count the number of
# times generate_dungeon is called
generate_dungeon.count = 0

# =============================================================================
# Définitions de variables

# definit° de variables a None pr affichage de canvas tests
canvas_test01 = None

#
red_rectangles = []

#
tab_corridors = []

# Define an empty dictionary
data = {}

# Create a new file called corridors.json
# chargé de stocker les datas de chacun des corridors
# ensuite on placera le contenu a la suite du fichier
# json officiel
if not os.path.exists("Save/saveGAME/test/corridors.json"):
    os.makedirs(os.path.dirname("Save/saveGAME/test/corridors.json"), exist_ok=True)
    with open('Save/saveGAME/test/corridors.json', 'w') as f:
        pass
else:
    print("File already exists.")

#
p01 = None
player_created = False

# =============================================================================

# dictionnaire touche clavier
# pr les touches directionnelles
# servent a diriger le joueur
# Key state dictionary
key_states = {
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False
}


# les methodes qui agissent sur les touches de fct°

#
def handle_F1():
    print("")
    print("F1 is pressed")

    rooms = utilitaires.loadRoomsDatasFromJsonFile("Save/saveGAME/save_json/file_level_1.json")

    print("")
    print("le contenu de file_level_1.json")
    print(rooms)
    print("")

    utilitaires.draw_rooms(rooms, left_canvas, RED)


#
def handle_F2():
    print("")
    print("F2 is pressed")
    print("")

    left_canvas.fill(WHITE)


#
def handle_F3():
    print("")
    print("F3 is pressed")


#
def handle_F4():
    print("")
    print("F4 is pressed")

    print("")
    print("affiche le contenu de tab_corridors")
    print(str(tab_corridors))
    print("")


#
def handle_F5():
    print("")
    print("F5 is pressed")

    print("")
    print("affiche le contenu du fichier")
    print("corridors.json")
    print("")

    # Load the JSON data from the file
    corr = utilitaires.loadCorridorsDatasFromJsonFile("Save/saveGAME/test/corridors.json")

    print(corr)
    print("")

    # Draw the rectangles
    # DESSINE UNIQUEMENT DES COULOIRS HORIZONTAUX
    # ET EN +, ILS NE CORRESPONDENT PAS
    utilitaires.draw_rooms(corr, left_canvas, BLACK)


#
def handle_F6():
    print("")
    print("F6 is pressed")

    print("")
    print("enregistre 1 png")
    print("")
    pygame.image.save(left_canvas, "Save/saveGAME/save_svg/output01.png")


#
def handle_F7():
    print("")
    print("F7 is pressed")

    # LES CORRIDORS ST BLEUS ET ONT L'AIR BIEN SUPERPOSÉS AUX
    # AUX CORRIDORS JAUNES

    # left_canvas.fill(WHITE)

    corridors_from_png = utilitaires.get_rectangles_from_png("Save/saveGAME/save_png/output_corridors_1.png", YELLOW)

    print("")
    print("affiche le contenu de corridors_from_png")
    print(corridors_from_png)
    print("")

    utilitaires.draw_rectangles(left_canvas, corridors_from_png, BLUE)


#
def handle_F8():
    print("")
    print("F8 is pressed")
    print("")


#
def handle_F9():
    print("")
    print("F9 is pressed")
    print("")

    """
    print("")
    print("ts les attributs de chaque instance de Item")
    print("de la class Item")
    for item_attributes in Item.item_instances:
        print(f"item_count {item_attributes['item_count']}:\n,\
          ({item_attributes['wordToDescribe']}\n,\
           {item_attributes['price']}\n,\
           {item_attributes['mayContain']}\n,\
           {item_attributes['color']}\n,\
           {item_attributes['isTransportable']}\n,\
           {item_attributes['isDeplacable']}\n,\
           {item_attributes['x']}\n,\
           {item_attributes['y']}\n,\
           {item_attributes['width']}\n,\
           {item_attributes['height']})")
    """

    print("")
    print("ts les attributs de chaque instance de NPC")
    print("de la class NPC")
    for NPC_attributes in NPC.NPC_instances:
        print(f"NPC_count {NPC_attributes['NPC_count']}:\n,\
          ({NPC_attributes['name']}\n,\
           {NPC_attributes['race']}\n,\
           {NPC_attributes['x']}\n,\
           {NPC_attributes['y']}\n,\
           {NPC_attributes['health']}\n,\
           {NPC_attributes['color']}\n,\
           {NPC_attributes['speed']})")

    print("")


#
def handle_F10():
    print("")
    print("F10 is pressed")
    print("")


#
def handle_F11():
    print("")
    print("F11 is pressed")
    print("")


#
def handle_F12():
    print("")
    print("F12 is pressed")
    print("")

    utilitaires.get_cpu_usage()
    utilitaires.get_usage_memory()


# dictionnaire des methodes pr les touches
# de fonct°
func_key_methods = {
    pygame.K_F1: handle_F1,
    pygame.K_F2: handle_F2,
    pygame.K_F3: handle_F3,
    pygame.K_F4: handle_F4,
    pygame.K_F5: handle_F5,
    pygame.K_F6: handle_F6,
    pygame.K_F7: handle_F7,
    pygame.K_F8: handle_F8,
    pygame.K_F9: handle_F9,
    pygame.K_F10: handle_F10,
    pygame.K_F11: handle_F11,
    pygame.K_F12: handle_F12
}

# ========================================================================

# font initialization for mouse coords
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)

#
window_info = pygame.display.Info()
windowWidth = 1000
windowHeight = 600

#
screen = pygame.display.set_mode((windowWidth, windowHeight), 0)

#
left_canvas_width = 800
left_canvas_height = 600
left_canvas = pygame.Surface((left_canvas_width, left_canvas_height),
                             pygame.SRCALPHA)

#
left_canvas.convert_alpha()
left_canvas.fill(WHITE)

# rectangle qui prend les posit° du left_canvas
left_canvas_rect = left_canvas.get_rect()

# Set the position of the left_canvas_rect
left_canvas_rect.topleft = (0, 0)

#
right_canvas_width = 200
right_canvas_height = 600
right_canvas = pygame.Surface((right_canvas_width, right_canvas_height),
                              pygame.SRCALPHA)

#
right_canvas.convert_alpha()
right_canvas.fill(GREY)

# rectangle qui prend les posit° du right_canvas
right_canvas_rect = right_canvas.get_rect()

# Set the position of the right_canvas_rect
right_canvas_rect.topleft = (left_canvas_width, 0)

# ============================================================================

# bouton Start game
# Define button properties
button_width = 150
button_height = 50
button_x = 25
button_y = 25
button_color = BLUE
button_text = "Start Game"
text_color = WHITE

# surface qui superposée au bouton Start Game
# Create button surface
button_surface = pygame.Surface((button_width, button_height))
button_surface.fill(button_color)
button_text_surface = myfont.render(button_text, True, text_color)
text_x = button_width // 2 - button_text_surface.get_width() // 2
text_y = button_height // 2 - button_text_surface.get_height() // 2
button_surface.blit(button_text_surface, (text_x, text_y))

# aire clickable superposée au bouton Start Game
# Define button area
button_area = pygame.Rect((left_canvas_width + button_x),
                          button_y,
                          button_width,
                          button_height)

# Add button Start Game to right canvas
right_canvas.blit(button_surface,
                  (button_x, button_y))

# ============================================================================

# fill the screen with white
screen.fill(WHITE)

# ============================================================================

# teste si les differents dossiers de sauvegarde existent
json_folder = utilitaires.folder_exists(LES_JSON)

if json_folder:
    print("le dossier de sauvegarde json existe")
    print("on peut continuer")
else:
    utilitaires.create_folder("Save/saveGAME/save_json/")
    print("le dossier json n'existe pas, il faut le creer")
    print("creation du dossier de sauvegarde json")

array_folder = utilitaires.folder_exists(LES_ARRAY)

if array_folder:
    print("le dossier de sauvegarde array existe")
    print("on peut continuer")
else:
    utilitaires.create_folder("Save/saveGAME/save_array/")
    print("le dossier array n'existe pas, il faut le creer")
    print("creation du dossier de sauvegarde array")

svg_folder = utilitaires.folder_exists(LES_SVG)

if svg_folder:
    print("le dossier de sauvegarde svg existe")
    print("on peut continuer")
else:
    utilitaires.create_folder("Save/saveGAME/save_svg/")
    print("le dossier svg n'existe pas, il faut le creer")
    print("creation du dossier de sauvegarde svg")

png_folder = utilitaires.folder_exists(LES_PNG)

if png_folder:
    print("le dossier de sauvegarde png existe")
    print("on peut continuer")
else:
    utilitaires.create_folder("Save/saveGAME/save_png/")
    print("le dossier png n'existe pas, il faut le creer")
    print("creation du dossier de sauvegarde png")

# ============================================================================

# compte le nbre de fichiers présent(s) ds
# chacun des dossiers ci-dessus
count_json_files_number = utilitaires.count_files_in_folder(LES_JSON)
count_array_files_number = utilitaires.count_files_in_folder(LES_ARRAY)
count_svg_files_number = utilitaires.count_files_in_folder(LES_SVG)
count_png_files_number = utilitaires.count_files_in_folder(LES_PNG)

# s'il n'y a pas de fichier ds le dossier de sauvegarde json
if count_json_files_number == 0:
    print("Aucun fichier déjà présent ds le dossier json, normal")
    print("on peut continuer")
else:
    utilitaires.delete_all_files_in_folder("Save/SaveGAME/save_json/")
    print("on efface les fichiers deja presents")

# s'il n'y a pas de fichier ds le dossier de sauvegarde svg
if count_svg_files_number == 0:
    print("Aucun fichier déjà présent ds le dossier svg, normal")
    print("on peut continuer")

else:
    utilitaires.delete_all_files_in_folder("Save/SaveGAME/save_json/")
    print("on efface les fichiers deja presents")

# s'il n'y a pas de fichier ds le dossier de sauvegarde array
if count_array_files_number == 0:
    print("Aucun fichier déjà présent ds le dossier array, normal")
    print("on peut continuer")
else:
    utilitaires.delete_all_files_in_folder("Save/SaveGAME/save_json/")
    print("on efface les fichiers deja presents")

# s'il n'y a pas de fichier ds le dossier de sauvegarde png
if count_png_files_number == 0:
    print("Aucun fichier déjà présent ds le dossier png, normal")
    print("on peut continuer")
else:
    utilitaires.delete_all_files_in_folder("Save/SaveGAME/save_json/")
    print("on efface les fichiers deja presents")

# ============================================================================

for i in range(1, 2):
    print("================================")
    print("boucle :" + str(i))

    dung = generate_dungeon()

    print("Fin de la boucle: " + str(i))
    print("================================")

    #
    for leaf_BIS in dung.tree.leaves():
        leaf_BIS.name = "Room " + str(leaf_BIS)

    #
    seedsurf = myfont.render(str(dung.seed), False, RED, BLACK)

# ============================================================================

# affichage de la seed en bas a gauche de la
# fenetre
right_canvas.blit(seedsurf, (10, left_canvas_height-20))

# ============================================================================

while True:
    # mouse coords
    textsurface = myfont.render(str(pygame.mouse.get_pos()), False, RED, BLACK)

    # Affichage des coordonnées de la souris
    # en haut a gauche de la fenetre
    right_canvas.blit(textsurface, (10, 0))

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)

        # en rapport avec le dictionnaire de methodes défini
        # ds le pygame init pr les touches de fct°
        if event.type == pygame.KEYDOWN:
            if event.key in func_key_methods:
                func_key_methods[event.key]()

        # ================================================================

        # qd les boutons souris st relachés
        if event.type == pygame.MOUSEBUTTONUP:
            # qd le bouton gauche de la souris est relaché
            # imprime les coordonnées de la souris
            # et de chacun des rooms
            if event.button == 1:  # left mouse button
                mouse_pos = pygame.mouse.get_pos()

                # si on relache la souris au-dessus du canvas de gauche
                if left_canvas_rect.collidepoint(mouse_pos):
                    print("")
                    print("Mouse over left_canvas")
                    print("Mouse in the screen's coordinate system clicked at:", mouse_pos)
                    local_pos = (mouse_pos[0] - left_canvas_rect.x, mouse_pos[1] - left_canvas_rect.y)
                    print("Mouse in the surface's coordinate system: " + str(local_pos))
                    print("(coordonnées locales)")
                    print("")
                    print("couleur au clic: " + str(left_canvas.get_at(local_pos)))

                    if str(left_canvas.get_at(local_pos)) == str((255, 0, 0, 255)):
                        print("click sur 1 room")
                        utilitaires.knowingNameRoomClicked(utilitaires.read_json_file("Save/saveGAME/save_json/file_level_1.json"),mouse_pos)

                    if str(left_canvas.get_at(local_pos)) == str((255, 255, 0, 255)):
                        print("click sur 1 corridor")
                        utilitaires.knowingNameCorridorClicked(utilitaires.read_json_file("Save/saveGAME/test/corridors.json"),mouse_pos)

                    if str(left_canvas.get_at(local_pos)) == str((255, 255, 255, 255)):
                        print("click sur 1 autre couleur")
                        print("soit blanc (en dehors du dongeon)")
                        print("soit sur 1 couleur qu'on a pas encore defini")

                    """
                    pixelColorFromPNG = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", mouse_pos)
                    print("couleur du pixel cliqué sur le png:")
                    print(pixelColorFromPNG)
                    """

                # si on relache la souris au-dessus du canvas de droite
                elif right_canvas_rect.collidepoint(mouse_pos):
                    print("")
                    print("Mouse over right_canvas")
                    print("")
                    # when "start" button is pressed
                    if button_area.collidepoint(mouse_pos):
                        # on verifie apres si le joueur a deja été crée,
                        # normalement non

                        """
                        print("")
                        print("Contenu de red_rectangles[]")
                        print("doit representer les coordonnées des rooms")
                        # [(40, 8, 75, 75), (473, 481, 217, 74)]
                        print("defini ds le pygame init")
                        print(red_rectangles)
                        print("")

                        print("")
                        print("Contenu de tab_corridors[]")
                        print("doit representer les coordonnées des corridors")
                        # [(115, 45.5, 10, 43.0), (247, 363.0, 362.5, 10)]
                        print("defini ds le pygame init")
                        print(tab_corridors)
                        print("")

                        print("")
                        print("Contenu de data{}, vide")
                        print("qu'est ce que cela represente?")
                        print(data)
                        print("")

                        print("")
                        print("Contenu de Save/saveGAME/save_json/file_level_1.json")
                        print(utilitaires.read_json_file("Save/saveGAME/save_json/file_level_1.json"))
                        print("")
                        """

                        if not player_created:

                            # ON CLIQUE SUR LE BOUTON
                            # START GAME
                            # 1 - le nom du joueur crée
                            # 2 - le canvas de destination
                            # 3 - le rectangle qui prend les dims du canvas
                            # 4 - le canvas de droite que l'on redessine qd
                            # on appuie sur le bouton start game
                            # 5 - la couleur de remplissage qd on redessine
                            # le canvas de droite

                            # p01 = instance de Player = le joueur
                            # items_list = 1 tableau qui contient
                            # 1 certain nbre d'instance d'Item
                            # NPCs_list = 1 tableau qui contient
                            # 1 certain nbre d'instances de NPC
                            p01, items_list, NPCs_list = utilitaires.startGame("Sabrino",
                                                                               left_canvas,
                                                                               left_canvas_rect,
                                                                               right_canvas,
                                                                               GREY)

                            #
                            player_created = True

                            # retourne la methode de classe de Item
                            # Affiche la liste des rooms. Cette liste ne doit
                            # ê imprimée qu'1 seule x indépendemment du nbre
                            # d'instances de la classe Item créees. Elle ne
                            # doit contenir qu'1 seule x la liste des rooms
                            # Item.init_rooms_data()


                            # Print the attributes of all Item instances
                            print("")
                            print("ts les attributs de chaque instance")
                            print("de la class Item")
                            for item_attributes in Item.item_instances:
                                print(f"item_count {item_attributes['item_count']}:\n,\
                                  ({item_attributes['wordToDescribe']}\n,\
                                   {item_attributes['price']}\n,\
                                   {item_attributes['mayContain']}\n,\
                                   {item_attributes['color']}\n,\
                                   {item_attributes['isTransportable']}\n,\
                                   {item_attributes['isDeplacable']}\n,\
                                   {item_attributes['x']}\n,\
                                   {item_attributes['y']}\n,\
                                   {item_attributes['width']}\n,\
                                   {item_attributes['height']})")
                            print("")


                            """
                            #
                            print("")
                            print("attributs de p01")
                            print(str(p01))
                            print("")

                            #
                            print("")
                            print("le nom du joueur seulement")
                            print(str(p01.name))
                            print("")

                            #
                            print("")
                            print("attributs de item1 avec la toString")
                            print(str(item1))
                            print("")
                            print("attributs de ts les items")
                            print("avec le helper json defini ds classes/Item")
                            print_item_instances()
                            """

            # qd le bouton droit de la souris est relaché
            # imprime 1 message
            elif event.button == 3:  # right mouse button
                print("")
                print("Right button clicked")
                print("")

    # ========================================================================

    # en rapport avec le dictionnaires touches defini
    # ds le pygame init, pr les touches directionnelles

    # Get the current state of all keys
    # following dictionary defined into pygame init()
    key_states = pygame.key.get_pressed()

    # Perform actions based on key states
    if key_states[pygame.K_UP]:
        print("Up key is active")
        if p01:
            print("")
            print("p01 exists")
            print("player to the up")
            print("")

            next_position = (p01.x, p01.y - p01.speed - 3)
            print("next position: " + str(next_position))
            next_pixel_color = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", next_position)

            if next_pixel_color is not None:
                print("")
                print("next pixel color: " + str(next_pixel_color))
                print("")

                if next_pixel_color != (255, 255, 255, 255):

                    #
                    p01.move_up()

                    # redessine le canvas avec le png
                    utilitaires.display_png_on_canvas(left_canvas,
                                      "Save/saveGAME/save_png/output_corridors_1.png")

                    # Loop through the items_list and call the draw()
                    # method for each item
                    # permet de redessiner ts les items a chaque press°
                    # d'1 touche
                    for item in items_list:
                        item.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_items(p01, item):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{item.get_wordToDescribe()}")
                            print(f"{item.get_price()}")
                            print(f"{item.get_mayContain()}")
                            print(f"{item.get_color()}")
                            print(f"{item.get_isTransportable()}")
                            print(f"{item.get_isDeplacable()}")
                            print(f"{item.get_x()}")
                            print(f"{item.get_y()}")
                            print(f"{item.get_width()}")
                            print(f"{item.get_height()}")
                            print(f"{item.get_position()}")

                    # boucle a travers la liste des NPC et les dessine
                    for npc in NPCs_list:
                        npc.choose_randomly_deplacement()
                        npc.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_NPCs(p01, npc):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{npc.get_name()}")
                            print(f"{npc.get_race()}")
                            print(f"{npc.get_health()}")
                            print(f"{npc.get_x()}")
                            print(f"{npc.get_y()}")
                            print(f"{npc.get_width()}")
                            print(f"{npc.get_height()}")
                            print(f"{npc.get_position()}")

                    #
                    p01_center = (p01.x, p01.y)

                    # redessine le joueur
                    p01.draw(left_canvas, left_canvas_rect)

                    p01_center_pixel = pygame.draw.circle(left_canvas, (0, 0, 0), p01_center, 1)

                    color_current_pixel = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", p01_center)

                    print("p01_center: " + str(p01_center))
                    print("color_current_pixel: " + str(color_current_pixel))

                    color_current_pixel_auDessus_seven = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png",(p01_center[0], p01_center[1]+7))
                    print("couleur du pixel qui se trouve à 7 px au-dessus")
                    print(color_current_pixel_auDessus_seven)
            else:
                print("")
                print("Exception from:")
                print("file: start.py")
                print("if key_states[pygame.K_UP]")
                print("The next position is outside the image bounds.")
                print("")

        else:
            print("")
            print("le joueur n'existe pas")
            print("")

    if key_states[pygame.K_DOWN]:
        print("Down key is active")
        if p01:
            print("")
            print("p01 exists")
            print("player to the down")
            print("")

            next_position = (p01.x, p01.y + p01.speed + 3)
            print("next position: " + str(next_position))
            next_pixel_color = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", next_position)

            if next_pixel_color is not None:
                print("")
                print("next pixel color: " + str(next_pixel_color))
                print("")

                if next_pixel_color != (255, 255, 255, 255):

                    #
                    p01.move_down()

                    # redessine le canvas avec le png
                    utilitaires.display_png_on_canvas(left_canvas,
                                      "Save/saveGAME/save_png/output_corridors_1.png")

                    # Loop through the items_list and call the draw()
                    # method for each item
                    # permet de redessiner ts les items a chaque press°
                    # d'1 touche
                    for item in items_list:
                        item.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_items(p01, item):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{item.get_wordToDescribe()}")
                            print(f"{item.get_price()}")
                            print(f"{item.get_mayContain()}")
                            print(f"{item.get_color()}")
                            print(f"{item.get_isTransportable()}")
                            print(f"{item.get_isDeplacable()}")
                            print(f"{item.get_x()}")
                            print(f"{item.get_y()}")
                            print(f"{item.get_width()}")
                            print(f"{item.get_height()}")
                            print(f"{item.get_position()}")

                    # boucle a travers la liste des NPC et les dessine
                    for npc in NPCs_list:
                        npc.choose_randomly_deplacement()
                        npc.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_NPCs(p01, npc):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{npc.get_name()}")
                            print(f"{npc.get_race()}")
                            print(f"{npc.get_health()}")
                            print(f"{npc.get_x()}")
                            print(f"{npc.get_y()}")
                            print(f"{npc.get_width()}")
                            print(f"{npc.get_height()}")
                            print(f"{npc.get_position()}")

                    #
                    p01_center = (p01.x, p01.y)

                    # dessine le joueur
                    p01.draw(left_canvas, left_canvas_rect)

                    p01_center_pixel = pygame.draw.circle(left_canvas, (0, 0, 0), p01_center, 1)

                    color_current_pixel = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", p01_center)

                    print("p01_center: " + str(p01_center))
                    print("color_current_pixel: " + str(color_current_pixel))

                    color_current_pixel_auDessous_seven = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png",(p01_center[0], p01_center[1]-7))
                    print("couleur du pixel qui se trouve à 7 px au-dessous")
                    print(color_current_pixel_auDessous_seven)

            else:
                print("")
                print("Exception from:")
                print("file: start.py")
                print("if key_states[pygame.K_DOWN]")
                print("The next position is outside the image bounds.")
                print("")

        else:
            print("")
            print("le joueur n'existe pas")
            print("")

    if key_states[pygame.K_LEFT]:
        print("Left key is active")
        if p01:
            print("")
            print("p01 exists")
            print("player to the left")
            print("")

            next_position = (p01.x - p01.speed - 3, p01.y)
            print("next position: " + str(next_position))
            next_pixel_color = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", next_position)

            if next_pixel_color is not None:
                print("")
                print("next pixel color: " + str(next_pixel_color))
                print("")

                if next_pixel_color != (255, 255, 255, 255):

                    #
                    p01.move_left()

                    # redessine le canvas avec le png
                    utilitaires.display_png_on_canvas(left_canvas,
                                      "Save/saveGAME/save_png/output_corridors_1.png")

                    # Loop through the items_list and call the draw()
                    # method for each item
                    # permet de redessiner ts les items a chaque press°
                    # d'1 touche
                    for item in items_list:
                        item.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_items(p01, item):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{item.get_wordToDescribe()}")
                            print(f"{item.get_price()}")
                            print(f"{item.get_mayContain()}")
                            print(f"{item.get_color()}")
                            print(f"{item.get_isTransportable()}")
                            print(f"{item.get_isDeplacable()}")
                            print(f"{item.get_x()}")
                            print(f"{item.get_y()}")
                            print(f"{item.get_width()}")
                            print(f"{item.get_height()}")
                            print(f"{item.get_position()}")

                    # boucle a travers la liste des NPC et les dessine
                    for npc in NPCs_list:
                        npc.choose_randomly_deplacement()
                        npc.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_NPCs(p01, npc):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{npc.get_name()}")
                            print(f"{npc.get_race()}")
                            print(f"{npc.get_health()}")
                            print(f"{npc.get_x()}")
                            print(f"{npc.get_y()}")
                            print(f"{npc.get_width()}")
                            print(f"{npc.get_height()}")
                            print(f"{npc.get_position()}")

                    #
                    p01_center = (p01.x, p01.y)

                    # redessine le joueur
                    p01.draw(left_canvas, left_canvas_rect)

                    p01_center_pixel = pygame.draw.circle(left_canvas, (0, 0, 0), p01_center, 1)

                    color_current_pixel = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", p01_center)

                    print("p01_center: " + str(p01_center))
                    print("color_current_pixel: " + str(color_current_pixel))

                    color_current_pixel_minus_seven = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png",(p01_center[0]-7, p01_center[1]))
                    print("couleur du pixel qui se trouve à 7 px à gauche")
                    print(color_current_pixel_minus_seven)

            else:
                print("")
                print("Exception from:")
                print("file: start.py")
                print("if key_states[pygame.K_LEFT]")
                print("The next position is outside the image bounds.")
                print("")

        else:
            print("")
            print("le joueur n'existe pas")
            print("")

    if key_states[pygame.K_RIGHT]:
        print("Right key is active")
        if p01:
            print("")
            print("p01 exists")
            print("player to the right")
            print("")

            next_position = (p01.x + p01.speed + 2, p01.y)
            print("next position: " + str(next_position))
            next_pixel_color = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", next_position)

            if next_pixel_color is not None:
                print("")
                print("next pixel color: " + str(next_pixel_color))
                print("")

                if next_pixel_color != (255, 255, 255, 255):

                    #
                    p01.move_right()

                    # redessine le canvas avec le png
                    utilitaires.display_png_on_canvas(left_canvas,
                                      "Save/saveGAME/save_png/output_corridors_1.png")

                    # Loop through the items_list and call the draw()
                    # method for each item
                    # permet de redessiner ts les items a chaque press°
                    # d'1 touche
                    for item in items_list:
                        item.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_items(p01, item):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{item.get_wordToDescribe()}")
                            print(f"{item.get_price()}")
                            print(f"{item.get_mayContain()}")
                            print(f"{item.get_color()}")
                            print(f"{item.get_isTransportable()}")
                            print(f"{item.get_isDeplacable()}")
                            print(f"{item.get_x()}")
                            print(f"{item.get_y()}")
                            print(f"{item.get_width()}")
                            print(f"{item.get_height()}")
                            print(f"{item.get_position()}")

                    # boucle a travers la liste des NPC et les dessine
                    for npc in NPCs_list:
                        npc.choose_randomly_deplacement()
                        npc.draw(left_canvas, left_canvas_rect)
                        if utilitaires.check_overlap_between_player_and_NPCs(p01, npc):
                            print(f"{p01.name} has overlapped with:")
                            print(f"{npc.get_name()}")
                            print(f"{npc.get_race()}")
                            print(f"{npc.get_health()}")
                            print(f"{npc.get_x()}")
                            print(f"{npc.get_y()}")
                            print(f"{npc.get_width()}")
                            print(f"{npc.get_height()}")
                            print(f"{npc.get_position()}")

                    #
                    p01_center = (p01.x, p01.y)

                    # redessine le joueur
                    p01.draw(left_canvas, left_canvas_rect)

                    p01_center_pixel = pygame.draw.circle(left_canvas, (0, 0, 0), p01_center, 1)

                    color_current_pixel = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png", p01_center)

                    print("p01_center: " + str(p01_center))
                    print("color_current_pixel: " + str(color_current_pixel))

                    color_current_pixel_plus_seven = utilitaires.get_pixel_color_from_image("Save/saveGAME/save_png/output_corridors_1.png",(p01_center[0]+7, p01_center[1]))
                    print("couleur du pixel qui se trouve à 7 px à droite")
                    print(color_current_pixel_plus_seven)
            else:
                print("")
                print("Exception from:")
                print("file: start.py")
                print("if key_states[pygame.K_LEFT]")
                print("The next position is outside the image bounds.")
                print("")

        else:
                print("")
                print("le joueur n'existe pas")
                print("")

    # draw left & right canvases
    screen.blit(left_canvas, (0, 0))
    screen.blit(right_canvas, (left_canvas_width, 0))

    # Blit the new canvases onto the screen, if it exists
    if canvas_test01 is not None:
        screen.blit(canvas_test01, (0, 0))

    pygame.display.update()

# quit pygame
pygame.quit()
