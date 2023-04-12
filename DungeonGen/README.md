README.md

French:
Projet pr répondre à la certif, Simplon de la formation CDA (Concepteur
Développeur d'Applications).

Sujets:
01:
Produire 1 Jeu de rôles avec génération de dongeons totalement aléatoire.

Techno:
Python3.9

Déploiement:
Facultatif: creer et executer 1 environnement virtuel pour installer les
librairies additionnelles nécessaires.
Se placer ds le repertoire qui contient le script shell pip_install.
Executer le fichier shell pip_install par la commande suivante:
    ./pip_install

Exécuter le générateur de dongeons.
Se placer ds le répertoire DungeonGen.
Executer le fichier start.py par la commande suivante:
    python3 start.py

Structure des dossiers - fichiers:
.
├── bsp
│   ├── bsp_moj.py
│   ├── __init__.py
│   └── __pycache__
│       ├── bsp_moj.cpython-39.pyc
│       ├── __init__.cpython-39.pyc
│       └── Room.cpython-39.pyc
├── classes
│   ├── Helmet.py
│   ├── __init__.py
│   ├── Item.py
│   ├── NPC.py
│   ├── Player.py
│   ├── __pycache__
│   │   ├── Helmet.cpython-39.pyc
│   │   ├── __init__.cpython-39.pyc
│   │   ├── Item.cpython-39.pyc
│   │   ├── NPC.cpython-39.pyc
│   │   ├── Player.cpython-39.pyc
│   │   ├── Room.cpython-39.pyc
│   │   └── Sword.cpython-39.pyc
│   ├── Room.py
│   ├── Sword.py
│   
├── __init__.py
├── __pycache__
│   ├── COMMUNICATION.cpython-39.pyc
│   ├── utilitaires.cpython-39.pyc
│   └── VARIABLES_CONSTANTS.cpython-39.pyc
├── raccourcis_clavier.txt
├── README.md
├── Save
│   ├── __pycache__
│   │   └── Save01.cpython-39.pyc
│   ├── Save01.py
│   ├── Save01.py~
│   └── saveGAME
│       ├── save_array
│       │   ├── file_level_1.npy
│       │   └── file_level_2.npy
│       ├── save_json
│       │   └── file_level_1.json
│       ├── save_png
│       │   └── output_corridors_1.png
│       ├── save_svg
│       └── test
│           └── corridors.json
├── start.py
├── test.txt
├── TODOs.txt
├── utilitaires.py
