import pygame
import json
import os


class Save01:
    """
    Class to implement save & restore functionallity
    """

    def print():
        print("Save class invoked")

    def check_if_directory_to_save_created(directoryToSaveGame):
        """
        Checks if the specified directory to save the game data exists.

        Args:
            directoryToSaveGame: The directory to check.

        Returns:
            None.
        """

        print("Save01.py, def check_if_directory_to_save_created")
        if os.path.isdir(directoryToSaveGame):
            print("Directory exists")
        else:
            print("directory does not exist")

    def check_if_file_to_save_created(fileToSaveGame):
        """
        Checks if the specified file to save the game data exists.

        Args:
            fileToSaveGame: The file to check.

        Returns:
            None.
        """

        print("Save01.py, def check_if_file_to_save_created")
        if os.path.isfile(fileToSaveGame):
            print("file to save game exists")
        else:
            print("file to save game does not exist")

    def saveDungeon(directoryToSaveGame, fileToSaveGame):
        print("Save01.py, def saveDungeon")

        if Save01.check_if_file_to_save_created("Save/saveGAME/fileToSaveGame.json"):
            os.remove("Save/saveGAME/fileToSaveGame.json")

        print("we are ready to run saving process")
        print("re affichage de room_names depuis le fichier")
        print("Save01.py")
        print(VARIABLES_CONSTANTS.room_names)

        dungeon_dict = {
                'dungeon_name': VARIABLES_CONSTANTS.dungs_name[-1],
                'generation_date': VARIABLES_CONSTANTS.dung_generation_date,
                'dungeon_level': VARIABLES_CONSTANTS.dung_level_dungeon,
                'number_of_rooms': len(VARIABLES_CONSTANTS.room_names)
                }

        # Write the dictionary to a JSON file
        with open(fileToSaveGame, 'w') as f:
            json.dump(dungeon_dict, f, indent=1)
            f.close()

    def saveDungeon02():
        """
        Saves the dungeon data to a JSON file.

        Args:
            None.

        Returns:
            None.
        """

        print("Save01.py, def saveDungeon02")

        if not Save01.saveDungeon02.has_run:
            print("Function has not been run yet")
            print("First execution")
            Save01.saveDungeon02.has_run = True
            if os.path.exists("Save/saveGAME/fileToSaveGame.json"):
                print("file already exists, deletion")
                print("in order to create an empty file")
                os.remove("Save/saveGAME/fileToSaveGame.json")
                # Open a new file in write mode
                open("Save/saveGAME/fileToSaveGame.json", "w").close()
                print("we create an empty file to save game")
                print("execution method to add datas")
                Save01.addDatas()
                print("closing file from Save01.addDatas() method")

            else:
                print("file does not exist")
                print("Save/saveGAME/fileToSaveGame.json creation")
                # Open a new file in write mode
                open("Save/saveGAME/fileToSaveGame.json", "w").close()
                print("execution method to add datas")
                Save01.addDatas()
                print("closing file from Save01.addDatas() method")

        else:
            print("Function has already been run")
            print("file to save game should already exists")
            print("checking...")
            if os.path.exists("Save/saveGAME/fileToSaveGame.json"):
                print("as expected, file already exists")
                print("execution method to add datas")
                Save01.addDatas()
                print("closing file from Save01.addDatas() method")

            else:
                print("unexpected problem, file does not exist")
                print("problem: Save01pyProblem01")
                print("where to check error:")
                print("file: Save01.py")
                print("method: Save01.py")

    def addDatas():
        print("file: Save01.py")
        print("method: addDatas")

        # M02C: write the json file, where to save
        # datas to redraw stairs
        # previous step: M02B to DungeonGen.py file

        dungeon_dict = {
            'dungeon_name': VARIABLES_CONSTANTS.dungs_name[-1],
            'generation_date': VARIABLES_CONSTANTS.dung_generation_date,
            'dungeon_level': VARIABLES_CONSTANTS.dung_level_dungeon,
            'stairs_number': VARIABLES_CONSTANTS.dung_stairs_number,
        }

        print("SAUVEGARDE")
        print("dungeon_name: " +
              str(VARIABLES_CONSTANTS.dungs_name[-1]))
        print("generation_date: " +
              str(VARIABLES_CONSTANTS.dung_generation_date))
        print("dungeon_level: " +
              str(VARIABLES_CONSTANTS.dung_level_dungeon))
        print("stairs_number:" +
              str(VARIABLES_CONSTANTS.dung_stairs_number))

        # Convert the Python object back to JSON
        json_dungeon_dict = json.dumps(dungeon_dict,
                                       indent=4,
                                       ensure_ascii=False)
        # Add a newline character after the last closing bracket
        json_dungeon_dict += '\n'

        # Open the JSON file for writing
        with open("Save/saveGAME/fileToSaveGame.json", "a") as f:
            # Write the updated JSON data to the file
            f.write(json_dungeon_dict)

        # Close the JSON file
        f.close()

        # clear variables to re-use
        VARIABLES_CONSTANTS.dungs_name.clear()
        VARIABLES_CONSTANTS.dung_generation_date = ""
        VARIABLES_CONSTANTS.dung_level_dungeon = ""

Save01.saveDungeon02.has_run = False
