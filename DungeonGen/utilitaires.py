import pygame
import string
import random
import cairosvg
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps
from PIL import Image
import psutil
import time

from classes.Player import Player
from classes.Item import Item
from classes.Sword import Sword
from classes.Helmet import Helmet
from classes.NPC import NPC


def get_cpu_usage():
    while True:
        cpu_percent = psutil.cpu_percent(interval=10)
        print(f"CPU usage: {cpu_percent}%")


def get_usage_memory():
    while True:
        # Get the current RAM usage
        ram_usage = psutil.virtual_memory()

        # Print the RAM usage information
        print(f"Total memory: {ram_usage.total / (1024 * 1024):.2f} MB")
        print(f"Available memory: {ram_usage.available / (1024 * 1024):.2f} MB")
        print(f"Used memory: {ram_usage.used / (1024 * 1024):.2f} MB")

        # Wait for 10 seconds before printing again
        time.sleep(10)


def get_pixel_color_from_image(image_path,
                               pos):
    """
    Retourne la RGB d'1 pixel sur 1 image

    Args:
        image_path (str):
            le chemin de l'image

        pos:
            posit° de la souris au click
    """

    try:
        with Image.open(image_path) as image:
            image = Image.open(image_path)
            return image.getpixel(pos)
    except IndexError:
        print("")
        print("Warning from utilitaires.py")
        print("method: get_pixel_color_from_image()")
        print("Warning: Attempted to access a pixel outside the image bounds.")
        print("")
        return None


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except OSError:
        print(f"Error: Creating directory {directory}")
        return False


def generate_random_string(length):
    """
    return a random string with 20 characters

    Args: length (int):
        number of characters to compose the string

    Returns:
        the random string
    """

    # Define the possible characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate a random string by randomly choosing characters from the pool
    random_string = ''.join(random.choice(characters) for i in range(length))

    return random_string


def folder_exists(folder_path):
    """
    Check if folder exists

    Args:
        folder_path (str):
            Path of folder to check

    Returns:
        bool:
            True if folder exists, False otherwise
    """

    if os.path.exists(folder_path):
        return True
    else:
        return False


def count_files_in_folder(folder_path):
    """
    count number of file(s) into the folder param

    Args:
        folder_path (str): Path of folder to check

    Returns:
        -1: folder does not exist
        int: number of files into the param folder
    """

    if not os.path.isdir(folder_path):
        # folder does not exist
        return -1
    else:
        print("il y a: " +
              str(len([f for f in os.listdir(folder_path)])) +
              "fichier(s)")

        return len([f for f in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, f))])


def store_pixels_with_color(color,
                            canvas):
    """
    Given a color and a canvas, store the x,y coordinates of every pixel
    drawn with the given color.

    Parameters:
        color (tuple):
            The RGB values of the color to look for, in the format (R, G, B).
        canvas (pygame.Surface):
            The canvas on which to search for pixels.

    Returns:
        List[Tuple[int,int]]:
            A list of tuples containing the x,y coordinates
            of pixels drawn with the given color.
    """

    pixels_with_color = []
    for x in range(canvas.get_width()):
        for y in range(canvas.get_height()):
            if canvas.get_at((x, y)) == color:
                pixels_with_color.append((x, y))
    return pixels_with_color


def delete_all_files_in_folder(folder_path):
    """
    Delete all files in the specified folder.

    Args:
        folder_path (str):
            path of the folder to check

    Returns:
        bool
    """

    if not os.path.exists(folder_path):
        print(f"{folder_path} does not exist.")
        return False

    if not os.listdir(folder_path):
        print(f"{folder_path} is already empty.")
        return True
    else:
        try:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"File {file_path} deleted.")
            return True
        except Exception as e:
            print(f"Error deleting files in {folder_path}: {e}")
            return False


def write_dict_to_json(data_dict,
                       filename):
    """
    Write json file

    Args:
        data_dict (json dictionary):
            json dictionary

        filename (str):
            path and name to write json file

    """

    with open(filename, "w") as f:
        json.dump(data_dict,
                  f,
                  indent=4)

    # print("utilitaires.py")
    # print("write_dict_to_json()")
    # print("Data written to", filename)


def read_and_draw_file(filename,
                       old_canvas,
                       color):
    """
    travaille avec des fichier .npy
    """

    #
    canvas = create_new_canvas(old_canvas,
                               color)

    # Load the file using NumPy
    data = np.load(filename)

    # Draw the data onto the old_canvas
    for point in data:
        color = (0, 0, 255)
        pygame.draw.rect(old_canvas,
                         (color),
                         pygame.Rect(point[0], point[1], 10, 10))


def create_new_canvas(old_canvas,
                      color):
    """
    Create new canvas

    Args:
        old_canvas (canvas):
            canvas model to get same dimensions

        color (str):
            color defined with constant defined to start.py
    """

    # Get the dimensions of the old canvas
    width = old_canvas.get_width()
    height = old_canvas.get_height()

    # Create a new canvas with the same dimensions
    # and coordinates as the old canvas
    new_canvas = pygame.Surface((width, height))

    # Set the color key to black
    new_canvas.set_colorkey((0, 0, 0))

    # Set the alpha value to fully opaque
    new_canvas.set_alpha(255)

    # Fill the new canvas with blue color
    new_canvas.fill(color)

    # Return the new canvas
    return new_canvas


def ask_yes_no_question(question,
                        screen,
                        canvas,
                        color01,
                        color02):
    """
    Ask a question, displaying it onto a surface

    Args:
        question (str):
            the question you want to ask

        screen (screen):
            the screen

        canvas (canvas):
            canvas to display the surface

        color01 (color):
            color defined by constant defined into start.py

        color02 (color):
            color defined by constant defined to start.py
    """

    # Initialize font for question text
    font = pygame.font.SysFont('Arial', 20)

    # Render the question text
    question_text = font.render(question, True, color01)

    # Display the question text on the right canvas
    canvas.fill(color02)
    canvas.blit(question_text, (10, 10))

    # Blit the right canvas onto the main screen
    screen.blit(canvas, (0, 0))

    pygame.display.update()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False
                else:
                    return False


def display_message(message):
    print(message)


def write_text_file(content,
                    filename):
    """
    Create a new text file and write content

    Args:
        content (str):
            The text content to write to the file.

        filename (str):
            The name of the file to create.
    """

    try:
        with open(filename, 'w') as f:
            f.write(str(content))
        print(f"File '{filename}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating file {filename}: {e}")


def write_binary_file(content,
                      filename):
    """
    Create a new binary file with the given filename and write the
    content to the file.

    Args:
        content ():
            The content to write to the file.

        filename (str):
            The name of the file to create.
    """

    content = np.array(content)
    try:
        np.save(filename, content)
        # print(f"File '{filename}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating file {filename}: {e}")


def compare_npy_files(file1,
                      file2):
    """
    Loads and compares two npy files.
    liste les pixels qui ne st pas les 1 au-dessus des autres
    PROBLEME

    Args:
        file1 (str): Path to the first npy file.
        file2 (str): Path to the second npy file.

    Returns:
        list of tuples: A list of coordinates of non-overlapping pixels.
    """
    # Load the npy files
    array1 = np.load(file1)
    array2 = np.load(file2)

    # Find the non-overlapping pixels
    diff = np.where(array1 != array2)

    # Convert the coordinates to tuples and return as a list
    return list(zip(diff[0], diff[1]))


def compare_npy_filesV2(file1,
                        file2):
    """
    Loads and compares two npy files.
    liste les pixels qui ne st pas les 1 au-dessus des autres

    Args:
        file1 (str): Path to the first npy file.
        file2 (str): Path to the second npy file.

    Returns:
        list of tuples: A list of coordinates of non-overlapping pixels.
    """

    # Check if the input files are valid npy files
    if not is_valid_npy_file(file1) or not is_valid_npy_file(file2):
        print("probleme de validité d'1 des 2 fichiers")
        return []

    # Load the npy files
    array1 = np.load(file1)
    array2 = np.load(file2)

    # Check if one or both of the input arrays are empty
    if array1.size == 0:
        print("array01 empty")
        return []
    else:
        print("01: " + str(len(array1)))

    if array2.size == 0:
        print("array02 empty")
        return []
    else:
        print("02: " + str(len(array2)))

    # Find the non-overlapping pixels
    diff = np.setdiff1d(array1.view(dtype=[('f0', int), ('f1', int)]),
                        array2.view(dtype=[('f0', int), ('f1', int)]),
                        assume_unique=True)

    # Convert the result back to the original format
    diff_coordinates = diff.view(dtype=int).reshape(-1, 2)

    # Print shapes and contents of the arrays for debugging
    print("Array1 shape:", array1.shape)
    print("Array1 contents:\n", array1)

    print("Array2 shape:", array2.shape)
    print("Array2 contents:\n", array2)

    # Print diff for debugging
    print("Diff:", diff)

    # Return the list of non-overlapping coordinates
    # return diff_coordinates.tolist()
    return [tuple(coord) for coord in diff_coordinates]


def compare_npy_filesV3(file1,
                        file2):
    """
    compare 2 npy files and return a list of
    non overlapping pixels

    Args:
        file1 (str):
            path to file1

        file2 (str):
            path to file2

    Returns: list (of tuples or not?)
    """

    # Load the npy files
    array1 = np.load(file1)
    array2 = np.load(file2)

    # Define gray and red colors as tuples
    gray = (128, 128, 128)
    red = (255, 0, 0)

    # Find gray pixels in array1
    gray_pixels_array1 = set(tuple(coord) for coord in array1)

    # Find red pixels in array2
    red_pixels_array2 = set(tuple(coord) for coord in array2)

    # Find non-overlapping gray pixels not covered by red pixels
    non_overlapping_gray_pixels = gray_pixels_array1.difference(red_pixels_array2)

    return list(non_overlapping_gray_pixels)


def compare_npy_filesV4(file1,
                        left_canvas):

    # Load the npy files
    array1 = np.load(file1)

    # Find gray pixels in array1
    gray_pixels_array1 = set(tuple(coord) for coord in array1)

    # Define the white color
    white = (255, 255, 255)

    # Find white pixels on left_canvas
    white_pixels_left_canvas = {(x, y) for x in range(left_canvas.get_width()) for y in range(left_canvas.get_height()) if left_canvas.get_at((x, y))[:3] == white}

    # Find gray pixels overlapping with white pixels on left_canvas
    non_overlapping_gray_white_pixels = gray_pixels_array1.difference(white_pixels_left_canvas)

    return list(non_overlapping_gray_white_pixels)


def find_overlap_pixels(file1,
                        file2):
    """
    Trouve les pixels qui st les 1 au-dessus des autres

    Args:
        file1 (str):
            le chemin du 1° fichier

        file2 (str):
            le chemin du 2° fichier
    """
    try:
        # load the files
        arr1 = np.load(file1)
        arr2 = np.load(file2)

        # compare the files
        overlap = np.intersect1d(arr1, arr2)

        # find the coordinates of the overlapping pixels
        coords1 = np.argwhere(np.isin(arr1, overlap))
        coords2 = np.argwhere(np.isin(arr2, overlap))

        # return the list of overlapping pixel coordinates
        return coords1.tolist() + coords2.tolist()
    except Exception as e:
        print(f"An error occurred while comparing files {file1} and {file2}: {e}")
        return []


def getAllRoomsDatas(data):
    """
    retourne ttes les infos de ttes les rooms
    definies ds ce data (data = le fichier json
                         passé en parametre)

    @param: data:
        1 fichier json

    @return: rooms:
        retourne 1 liste des rooms issues du json
    """

    print("")
    print("fichier utilitaires.py")
    print("methode: getAllRoomsDatas()")

    #
    with open(data, 'r') as file:
        data = json.load(file)

    # Get a list of all the rooms
    rooms = list(data["rooms"].values())

    return rooms


def knowingNameRoomClicked(data,
                           mousePos):
    """
    Affiche le nom de la room cliquée

    @param: data
        le fichier json qui est chargé
    @param: mousePos
        la posit° de la souris au moment du clik
    """

    print("fichier: utilitaires.py")
    print("methode: knowingNameRoomClicked()")

    print("pos de la souris: " + str(mousePos))

    rooms = getAllRoomsDatas(data)
    # print("rooms de knowingNameRoomClicked: " +
          # str(rooms))

    # Check if the clicked point is inside a room
    # display room name
    for room in rooms:
        if (room['x'] <= mousePos[0] <= room['x'] + room['width'] and
                room['y'] <= mousePos[1] <= room['y'] + room['height']):
            print('click over', room['name'])


def getAllCorridorsDatas(data):
    """
    retourne ttes les infos de ts les corridors
    definis ds ce data (data = le fichier json
                         passé en parametre)

    @param: data:
        1 fichier json

    @return: corridors:
        retourne 1 liste des corridors issus du json
    """

    print("")
    print("fichier utilitaires.py")
    print("methode: getAllCorridorsDatas()")

    # Get a list of all the rooms
    corridors = list(data["corridors"].values())

    return corridors


def knowingNameCorridorClicked(data,
                               mousePos):
    """
    Affiche le nom du corridor cliquée

    @param: data
        le fichier json qui est chargé
    @param: mousePos
        la posit° de la souris au moment du clik
    """

    print("fichier: utilitaires.py")
    print("methode: knowingNameCorridorClicked()")

    print("pos de la souris: " + str(mousePos))

    corridors = getAllCorridorsDatas(data)
    # print("corridors de knowingNameCorridorClicked: " +
          # str(corridors))

    # Check if the clicked point is inside a corridor
    # display corridor name
    for corridor in corridors:
        if (corridor['x'] <= mousePos[0] <= corridor['x'] + corridor['width'] and corridor['y'] <= mousePos[1] <= corridor['y'] + corridor['height']):
            print('Player is inside corridor', corridor['name'])


def setCenterForRandomChosenRoom(data):
    """
    choose a random room from a list
    calculate its center

    @param data: json loaded when pygame init() occurs

    return center of a random chosen room (which is a tuple)
    """

    # print("")
    # print("fichier: utilitaires.py")
    # print("method: setCenterForRandomChosenRoom()")

    # Get a list of all the rooms
    rooms = list(data["rooms"].values())

    # print("valeur de rooms (data)")
    # print(list(data["rooms"].values()))

    # Choose a random room
    chosen_room = random.choice(rooms)
    # print("valeur de chosen_room: " +
          # str(chosen_room))

    # Calculate the center of the room
    center_x = chosen_room["x"] + chosen_room["width"] // 2
    # print("valeur de center_x: " +
          # str(center_x))
    center_y = chosen_room["y"] + chosen_room["height"] // 2
    # print("valeur de center_y: " +
          # str(center_y))
    # print("")

    return center_x, center_y


def read_json_file(file_path):
    """
    Lit 1 fichier json et le renvoie en intégralité

    Args:
        file_path (str):
    """

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    return json_data


def is_valid_npy_file(file_path):
    """
    Checks if the given file path points to a valid npy file.

    Args:
        file_path (str): Path to the npy file.

    Returns:
        bool: True if the file is a valid npy file, False otherwise.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        return False

    # Check if the file has a .npy extension
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() != ".npy":
        return False

    return True


def load_and_display_npy(file_path):
    """
    load a .npy file and display its contents in the console
    """
    try:
        # Load the .npy file using NumPy's load function
        data = np.load(file_path)

        # Display the contents of the loaded .npy file in the console
        # print("Content of the .npy file:")
        print(data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while loading the .npy file: {e}")


def find_common_tuples_from_2_lists(list1,
                                    list2):
    """
    Trouve les tuples communs entre 2 listes

    Args:
        list1 ():
            Liste 1

        list2 ():
            Liste2
    """

    # Check if both inputs are non-empty lists
    if not (isinstance(list1, list) and isinstance(list2, list)) or (len(list1) == 0 or len(list2) == 0):
        print("Error: Both inputs must be non-empty lists.")
        return []

    # Check if both lists contain only tuples
    if not (all(isinstance(item, tuple)
                for item in list1)
            and all(isinstance(item, tuple)
                    for item in list2)):
        print("Error: Both lists must contain only tuples.")

        return []

    # Use list comprehension to find common tuples in both lists
    common = [t for t in list1 if t in list2]

    return common


def get_color_at_position(liste,
                          source):
    """

    """

    for point in liste:
        x, y = point
        # Check if the coordinates are within
        # the bounds of the left_canvas Surface
        if 0 <= x < source.get_width() and 0 <= y < source.get_height():
            color = source.get_at((x, y))
            # print(f"Point: {point}, Color: {color}")
        else:
            print(f"Point: {point}, Out of bounds")
    """
    # Check if the coordinates are within the bounds of the left_canvas array
    for i in range(len(list)):
        print(list[i])
        color = source[list[i]]
        print(color)
    """


def circle_rect_overlap(circle_center,
                        circle_radius,
                        rect):
    """
    checks if a circle overlaps with a rectangle.

    Args:
        circle_center ():


        circle_radius ():


        rect (rect):


    Utilité:
    """

    rect_x, rect_y, rect_w, rect_h = rect
    circle_distance_x = abs(circle_center[0] - rect_x - rect_w / 2)
    circle_distance_y = abs(circle_center[1] - rect_y - rect_h / 2)

    if circle_distance_x > (rect_w / 2 + circle_radius):
        return False
    if circle_distance_y > (rect_h / 2 + circle_radius):
        return False

    if circle_distance_x <= (rect_w / 2):
        return True
    if circle_distance_y <= (rect_h / 2):
        return True

    corner_distance_sq = (circle_distance_x - rect_w / 2) ** 2 + (circle_distance_y - rect_h / 2) ** 2

    return corner_distance_sq <= (circle_radius ** 2)


def rectangles_intersect(rect1,
                         rect2):
    """
    determine the intersection between red rectangles and other rectangles
    """

    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
        x_intersect = max(x1, x2)
        y_intersect = max(y1, y2)
        return x_intersect, y_intersect

    return None


def subtract_rectangles(rect1,
                        rect2):
    """
    a way to not draw parts of other rectangles
    overlap red rectangles_intersect
    """

    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if not (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2):

        return [rect1]

    new_rects = []

    if y1 < y2:
        new_rects.append((x1,
                          y1,
                          w1,
                          y2 - y1))

        y1 = y2
        h1 = h1 - (y2 - y1)

    if x1 < x2:
        new_rects.append((x1,
                          y1,
                          x2 - x1,
                          h1))

        w1 = w1 - (x2 - x1)
        x1 = x2

    if x1 + w1 > x2 + w2:
        new_rects.append((x2 + w2,
                          y1,
                          (x1 + w1) - (x2 + w2),
                          h1))

        w1 = w2

    if y1 + h1 > y2 + h2:
        new_rects.append((x1,
                          y2 + h2,
                          w1,
                          (y1 + h1) - (y2 + h2)))

    return new_rects


def loadRoomsDatasFromJsonFile(jsonFile):
    """
    Charge 1 des fichier json qui décrit 1 stair
    Methode qui récupere les infos de ttes les rooms

    Args:
        jsonFile (str):
            chemin et nom du fichier json à charger
    """

    #
    jsonFile = read_json_file(jsonFile)

    # Extract the rooms data
    rooms_data = jsonFile["rooms"]

    """
    #
    print(rooms_data)
    print(rooms_data["Room_1"])
    print(rooms_data["Room_1"]["width"])
    """

    #
    return rooms_data


def loadCorridorsDatasFromJsonFile(jsonFile):
    """
    Charge 1 des fichier json qui décrit 1 stair
    Methode qui récupere les infos de ts les corridors

    Args:
        jsonFile (str):
            chemin et nom du fichier json à charger
    """

    #
    jsonFile = read_json_file(jsonFile)

    # Extract the rooms data
    corridors_data = jsonFile["corridors"]

    """
    #
    print(corridors_data)
    print(corridors_data["yellow_rect_1"])
    print(corridors_data["yellow_rect_1"]["width"])
    """

    #
    return corridors_data


def draw_rooms(rooms_data,
               canvas_destination,
               color):
    """
    Dessine des rectangles depuis 1 json
    """

    for room_name, room_info in rooms_data.items():
        x, y, width, height = room_info['x'],\
                              room_info['y'],\
                              room_info['width'],\
                              room_info['height']

        pygame.draw.rect(canvas_destination,
                         color, pygame.Rect(x, y, width, height))


def has_identical_values(array):
    """
    check if there are 2 or more identical
    values in an array of dictionaries
    """

    unique_values = []

    for item in array:
        if item in unique_values:
            return True
        unique_values.append(item)

    return False


def draw_rectangles_contained_into_array(rectangles_list,
                                         canvas,
                                         color):
    """
    Draw rectangles from a list that contains
    dictionaries of rectangles
    """

    for rect in rectangles_list:
        if 'x' in rect and 'y' in rect and 'w' in rect and 'h' in rect:
            x = rect['x']
            y = rect['y']
            w = rect['w']
            h = rect['h']
            pygame.draw.rect((x, y, w, h), canvas, color)


def count_calls(func):
    """
    Compte le nbre de x ou 1 methode est executée.

    Args:
        func (str):
            le nom de la methode

    Utilise 1 wrapper
    Définit° d'1 wrapper:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1

        # print(f"{func.__name__} has been \
                # called {wrapper.call_count} times----")

        return func(*args, **kwargs)

    wrapper.call_count = 0

    return wrapper


def get_rectangles_from_png(p_img,
                            color):
    """
    obtient ts les pixels d'1 image selon la couleur

    Args:
        p_img (str):
            path or file

        color (color):
            la couleur dt il faut récupérer chaque pixel
            ds l'image

    Utilité:
    """

    # open the PNG file
    img01 = Image.open(p_img)

    # convert the image to RGB mode (if it's not already)
    img01 = img01.convert('RGB')

    # list to store yellow rectangles
    rectangles = []

    # iterate over all pixels in the image
    for x in range(img01.width):
        for y in range(img01.height):
            # get the color of the pixel
            r, g, b = img01.getpixel((x, y))
            # check if the pixel is yellow
            if (r, g, b) == color:
                # check if this is the first pixel of a yellow rectangle
                if not any(rectangle['x'] == x
                           and rectangle['y'] == y
                           for rectangle in rectangles):

                    # find the dimensions of the rectangle
                    width = 0
                    height = 0

                    while img01.getpixel((x + width, y)) == color:
                        width += 1

                    while img01.getpixel((x, y + height)) == color:
                        height += 1

                    # add the yellow rectangle to the list
                    rectangles.append({'x': x,
                                       'y': y,
                                       'width': width,
                                       'height': height})

    return rectangles


def draw_rectangles(surface,
                    rectangles,
                    color):
    """
    Draws rectangles on a Pygame surface based on a list of rectangle data.
    Each element of the list should be a dictionary containing the keys
    'x', 'y', 'width', and 'height'.

    Args:
        surface ():


        rectangles ():


        color (color):


    Utilité:
    """
    for rectangle in rectangles:
        x = rectangle['x']
        y = rectangle['y']
        width = rectangle['width']
        height = rectangle['height']
        pygame.draw.rect(surface,
                         color,
                         pygame.Rect(x, y, width, height))


def display_png_on_canvas(canvas,
                          file_path):
    """
    Affiche 1 png sur 1 canvas
    """

    # Load the PNG image
    image = pygame.image.load(file_path)

    # Get the size of the canvas
    canvas_width = canvas.get_width()
    canvas_height = canvas.get_height()

    # Scale the image to fit the canvas
    image = pygame.transform.scale(image,
                                   (canvas_width, canvas_height))

    # Display the image on the canvas
    canvas.blit(image, (0, 0))

    # Update the canvas display
    pygame.display.update()


def check_overlap_between_player_and_NPCs(player: Player,
                                          NPC: NPC) -> bool:
    """
    checks if both parameters overlap
    using their respective positions and dimensions

    Args:
        player (Player):
            instance of the player

        npc (NPC):
            instance of a NPC
    """

    #
    player_x, player_y = player.get_position()
    player_radius = player.radius

    #
    NPC_x, NPC_y = NPC.get_position()
    NPC_width = NPC.get_width()
    NPC_height = NPC.get_height()

    #
    player_left = player_x - player_radius
    player_right = player_x + player_radius
    player_top = player_y - player_radius
    player_bottom = player_y + player_radius

    NPC_left = NPC_x
    NPC_right = NPC_x + NPC_width
    NPC_top = NPC_y
    NPC_bottom = NPC_y + NPC_height

    # Check if there's an overlap
    if (player_left < NPC_right) and (player_right > NPC_left) and (player_top < NPC_bottom) and (player_bottom > NPC_top):
        return True

    return False


def check_overlap_between_player_and_items(player: Player,
                                           item: Item) -> bool:
    """
    checks if both parameters overlap
    using their respective positions and dimensions

    Args:
        player (Player):
            instance of the player

        item (Item):
            instance of a item
    """

    #
    player_x, player_y = player.get_position()
    player_radius = player.radius

    #
    item_x, item_y = item.get_position()
    item_width = item.get_width()
    item_height = item.get_height()

    #
    player_left = player_x - player_radius
    player_right = player_x + player_radius
    player_top = player_y - player_radius
    player_bottom = player_y + player_radius

    item_left = item_x
    item_right = item_x + item_width
    item_top = item_y
    item_bottom = item_y + item_height

    # Check if there's an overlap
    if (player_left < item_right) and (player_right > item_left) and (player_top < item_bottom) and (player_bottom > item_top):
        return True

    return False


def createPlayer(name):
    player = Player(name)
    return player


def placePlayer(name,
                data,
                surface,
                surface_rect):
    """
    Créer 1 instance de la classe Player,
    Définir 1 point au centre d'1 room choisie au hasard
    Affiche l'instance de Player

    Args:
        name (str):
            name of the player instance

        data ():

        surface (canvas):
            le canvas qui doit contenir
            le dessin de l'instance de Player

        surface_rect (rectangle):
            le rect qui est superposé au canvas pr obtenir
            les dimens° du canvas
    """

    #
    player = createPlayer(name)

    # definit° du point d'ancrage du joueur
    # (ou celui-ci doit apparaitre qd on lance le jeu)
    # represente 1 tuple
    bornPointPlayer = setCenterForRandomChosenRoom(data)

    # permet de placer l'instance de player (cercle vert)
    # au centre d'1 room choisie au hasard
    player.show(surface,
                surface_rect,
                bornPointPlayer)

    return player


def draw_strip_around_rect(rect):
    """
    Définit 4 rectangles superposés au bord ms à 
    l'intèrieur des
    rectangles représentant les rooms. On ne place
    pas d'instance ds ces rectangles (strips), permet
    de ne pas afficher les instances de Item chevauchant
    les bords des rectangles représentant les rooms

    Args:
        rect (rectangle):
            1 rectangle de ref auquel on va ajouter les 4
            rectangles definis ci-dessous appelées les strips.

    """

    # Draw strip at top of rectangle
    # le strip (rectangle) sur le bord sup du rect de la room
    strip_rect = pygame.Rect(rect.left, rect.top, rect.width, 10)
    # pygame.draw.rect(win, (255, 255, 0), strip_rect)

    # Draw strip at bottom of rectangle
    # le strip (rectangle) sur le bord inf du rect de la room
    strip_rect = pygame.Rect(rect.left, rect.bottom - 10, rect.width, 10)
    # pygame.draw.rect(win, (255, 255, 0), strip_rect)

    # Draw strip at left of rectangle
    # le strip (rectangle) sur le bord gauche du rect de la room
    strip_rect = pygame.Rect(rect.left, rect.top, 10, rect.height)
    # pygame.draw.rect(win, (255, 255, 0), strip_rect)

    # Draw strip at right of rectangle
    # le strip (rectangle) sur le bord droit du rect de la room
    strip_rect = pygame.Rect(rect.right - 10, rect.top, 10, rect.height)
    # pygame.draw.rect(win, (255, 255, 0), strip_rect)


def create_NPC(file,
                surface,
                surface_rect):
    """
    creer et placer des instances de NPC ds des rooms
    au hasard

    Args:
        file (str):
            path & name of the json file

        surface (surface):

        surface_rect (surface_rect):
    """

    #
    file = "Save/saveGAME/save_json/file_level_1.json"

    #
    datas_of_rooms = getAllRoomsDatas(file)

    #
    number_of_NPCs = random.randint(2, 10)

    #
    placed_NPCs = []

    #
    for NPCs_a_placer in range(number_of_NPCs):

        # Instantiate the NPC class (from NPC.py)
        NPC_instance = NPC()

        #
        room_to_place_NPC = random.choice(datas_of_rooms)
        room_x = room_to_place_NPC['x']
        room_y = room_to_place_NPC['y']
        room_width = room_to_place_NPC['width']
        room_height = room_to_place_NPC['height']

        #
        room_rect = pygame.Rect(room_x, room_y, room_width, room_height)

        # definit des rectangles ds chaque rectangle representant
        # des rooms. Ces 4 rectangles st DEDANS les rectangles des
        # rooms, en haut a droite, en bas et a gauche. On ne place
        # pas d'instances ds ces rectangles. on s'assure cô ça de ne
        # pas placer d'inatnces de Item qui pourraient chevaucher
        # ou apparaitre en partie à l'exterieur d'1 room
        draw_strip_around_rect(room_rect)

        # largeur des strips
        strip_width = 10

        # Définit dc les rectangles ou l'on peut placer des
        # instances de NPC
        NPC_placement_rect = pygame.Rect(
            room_x + strip_width,
            room_y + strip_width,
            room_width - 2 * strip_width,
            room_height - 2 * strip_width
        )

        #
        random_x = random.randint(NPC_placement_rect.left,
                                  NPC_placement_rect.right)
        random_y = random.randint(NPC_placement_rect.top,
                                  NPC_placement_rect.bottom)

        # Update the NPC instance's position with the random coordinates
        NPC_instance.set_x(random_x)
        NPC_instance.set_y(random_y)

        # Add the placed NPC instance to the placed_NPCs list
        placed_NPCs.append(NPC_instance)

        # Draw the NPC instance on the surface
        NPC_instance.draw(surface, surface_rect)

    return placed_NPCs


def create_item(file,
                surface,
                surface_rect):
    """
    creer et placer des instances de Item ds des rooms
    au hasard

    Args:
        file (str):
            path & name of the json file

        surface (surface):

        surface_rect (surface_rect):
    """

    #
    file = "Save/saveGAME/save_json/file_level_1.json"

    #
    datas_of_rooms = getAllRoomsDatas(file)

    #
    number_of_items = random.randint(2, 10)

    #
    placed_items = []

    #
    for items_a_placer in range(number_of_items):
        # Choose a random item class (Sword or Helmet)
        item_class = random.choice([Sword, Helmet])

        # Create an instance of the chosen item class
        item_instance = item_class()

        #
        room_to_place_item = random.choice(datas_of_rooms)
        room_x = room_to_place_item['x']
        room_y = room_to_place_item['y']
        room_width = room_to_place_item['width']
        room_height = room_to_place_item['height']

        #
        room_rect = pygame.Rect(room_x, room_y, room_width, room_height)

        # definit des rectangles ds chaque rectangle representant
        # des rooms. Ces 4 rectangles st DEDANS les rectangles des
        # rooms, en haut a droite, en bas et a gauche. On ne place
        # pas d'instances ds ces rectangles. on s'assure cô ça de ne
        # pas placer d'inatnces de Item qui pourraient chevaucher
        # ou apparaitre en partie à l'exterieur d'1 room
        draw_strip_around_rect(room_rect)

        # largeur des strips
        strip_width = 10

        # Définit dc les rectangles ou l'on peut placer des
        # instances de Item
        item_placement_rect = pygame.Rect(
            room_x + strip_width,
            room_y + strip_width,
            room_width - 2 * strip_width,
            room_height - 2 * strip_width
        )

        # Generate random coordinates for the NPC placement
        random_x = random.randint(item_placement_rect.left,
                                  item_placement_rect.right)
        random_y = random.randint(item_placement_rect.top,
                                  item_placement_rect.bottom)

        # Update the item instance's position with the random coordinates
        item_instance.set_x(random_x)
        item_instance.set_y(random_y)

        # Update the corresponding dictionary entry in item_instances
        # MAJ des attributs x et y ds le json dict.
        # On peut recuperer les attributs x et y de chaque item placé
        for item_attributes in Item.item_instances:
            if item_attributes["item_count"] == item_instance.item_count:
                item_attributes['x'] = random_x
                item_attributes['y'] = random_y
                break

        # Add the placed item instance to the placed_items list
        placed_items.append(item_instance)

        # Draw the item instance on the surface
        item_instance.draw(surface, surface_rect)

    return placed_items


def startGame(name,
              left_canvas,
              left_canvas_rect,
              right_canvas,
              GREY):
    """
    Démarre le jeu qd on clique sur le bouton start game

    Args:
        name (str):
            le nom de joueur que l'on crée

        left_canvas (canvas):
            le canvas de gauche qui dessine

        left_canvas_rect (rect):
            le rectangle superposée au canvas de gauche pr
            obtenir les dims du canvas

        right_canvas (canvas):
            le canvas de droite qui représente le menu

        GREY (color):
            la couleur de remplissage pr le canvas de droite
    """

    # Redraw the right canvas after the start button is pressed
    redrawRightCanvasAfterStartButtonPressed(right_canvas, GREY)

    # Read the JSON data
    lvl = read_json_file("Save/saveGAME/save_json/file_level_1.json")

    # Create & Place the player
    # name:
    # lvl:
    # left_canvas:
    # left_canvas_rect:
    player = placePlayer(name,
                         lvl,
                         left_canvas,
                         left_canvas_rect)

    # Call create_item() and get the list of placed items
    # lvl:
    # left_canvas:
    # left_canvas_rect:
    items_list = create_item(lvl,
                             left_canvas,
                             left_canvas_rect)

    # Call create_NPC() and get the list of placed NPCs
    # lvl:
    # left_canvas:
    # left_canvas_rect:
    NPCs_list = create_NPC(lvl,
                             left_canvas,
                             left_canvas_rect)

    return player, items_list, NPCs_list


def redrawRightCanvasAfterStartButtonPressed(canvas,
                                             color):
    """
    Redessine le canvas de droite 1 x que le bouton
    start game a été presse
    Contenu: VIDE

    Args:
        canvas (canvas):
            le canvas que l'on redessine

        color (color):
            la couleur de remplissage
    """

    canvas.fill(color)
