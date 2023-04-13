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
- Facultatif: creer et executer 1 environnement virtuel pour installer les
librairies additionnelles nécessaires.
- Se placer ds le repertoire qui contient le script shell pip_install.
Executer le script shell pip_install par la commande suivante:<br>
    ./pip_install<br>
- Effacer le fichier DungeonGen/Save/saveGAME/test/corridors.json
si ce dernier existe.
Il faut effacer ce fichier a chaque execution du fichier start.py  


Exécuter le générateur de dongeons.
Se placer ds le répertoire DungeonGen.
Executer le fichier start.py par la commande suivante:<br>
    python3 start.py<br>

DESCRIPTION:
Le projet repose sur 1 RPG qui se joue au tour par tour.
- 1 partie en python qui est le client lourd.
- 1 site qui permet aux utilisateurs (visiteurs inscrits) de poster des
  commentaires avec affichage de type fils de discussion.
- autres à préciser.

Déroulement d'1 partie:
L'utilisateur clique le bouton "Start Game", son personnage est placé au
centre d'1 pièce. Des items et des NPC (Non Player Characters) st également
placés dans des pièces au hasard.
A chaque pression d'1 touche directionnelle, le programme éxécute différentes
actions.
- Le déplacement du joueur.
- Le déplacement des NPCs.

Fonctionnalités:
- génération d'1 dongeon de manière totalement aléatoire.
algorithme utilisé: Binary Space Partition (BSP).
Principe de fonctionnement:
algorithme de partitionnement d'espace utilisé principalement dans les
domaines de la génération procédurale. Il divise récursivement l'espace
en deux parties en utilisant des plans de partitionnement (appelés noeuds)
jusqu'à ce que chaque sous-espace atteigne une certaine condition prédéfinie
(ici, la taille).

Comment foncionne ce BSP.
Condition d'arrêt de la récursivité: la taille de chaque rectangle.
Ds 1 1° temps, l'algorithme place des rectangles qui représentent des pièces.
Une fois que les pièces sont créées, il connecte les pièces qui se trouvent
dans un meme noeud. Le BSP connecte en suite les noeuds entre eux.

Il connecte par des corridors (d'autres rectangles) les pièces qui se trouvent
dans le même noeud puis définit les corridors pour connecter les noeuds entre
eux.

Le bsp définit pour chaque pièce son centre puis connecte 2 centres entre eux.
Ceci entraine 1 probleme de positionnement du joueur qui peut donc être à la
fois dans une pièce mais en même temps ds un corridor qui se trouve dans cette
même pièce.

SOLUTION:
Travail au niveau pixel.

1 x le donjon généré, on en prend 1 png qui sera affiché. On travaillera
désormais au niveau des couleurs des pixels.

Le joueur est défini grâce à 1 classe Player qui définit
- certains attributs.
- 1 surface de dessin superposée au canvas de gauche (chargé l'affichage
du donjon).
- des methodes de deplacement grâce aux touches directionnelles.
    la methode show() pour montrer la joueur lorsqu'on lance le jeu.
    la methode draw() qui redessine le joueur a chaque pression de touche.

A chaque pression d'1 touche directionnelle, on verifie la couleur des
prochains pixels qui st dans la continuité de cette direction.
    - pixel rouge, on reste ds la salle, le deplacement est effectué.
    - pixel jaune, on passe ds 1 corridor, le deplacement est effectué.
    - pixel blanc, on sort du donjon, le deplacement n'est pas effectué.

Le joueur est placé aléatoirement au centre d'1 pièce.

Placement les items (Item, Helmet et Sword).
On désire placer des items ds les salles. On ne peut pas placer ces Items
en chevauchement des murs des pièces (ou meme qques x à l'extèrieur).
 SOLUTION:
 ON dessine des strips (bandes rectangulaires de 10px) sur chaque bord de
 chaque pièce (tout en restant à l'intèrieur des pièces). On récupère
 les pixels qui ne st pas définis à l'interieur de ces strips.
 On choisit alors 1 px au hasard et on y place l'item.

Placement des NPC:
Même technique.
A chaque x que l'on déplace le joueur, il y a 1 methode de déplacement
du NPC qui choisit 1 direct° au hasard et deplace le NPC.

Enfin, il existe une méthode qui permet de détecter si les pixels
du joueur chevauchent des pixels d'item et ou de NPC.
Si cela arrive, on affiche les caractéristiques de l'item ou du NPC.
