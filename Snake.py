###############################################################################
#                              Pré-Projet : Snake                             #
#                         Jeu Snake aux Noms Multiples                        #
#                                    v1.0                                     #
#                     Valentin Bernier - Alain Coserariu                      #
###############################################################################


import fltk
from time import sleep, time
from random import randint, randrange

taille_case = 32
largeur_plateau = 40
hauteur_plateau = 30


###############################################################################
#                                  Affichage                                  #
###############################################################################


def case_vers_pixel(case):
    """
    Fonction recevant les coordonnées d'une case du plateau et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case
    Utilisation de la variable globale taille_case

    :param case: Couple de coordonées à convertir
    :return: Couples des coordonées converties

    >>> case_vers_pixel((16, 7))
    (528.0, 240.0)

    >>> case_vers_pixel((10, 12))
    (336.0, 400.0)
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affichage():
    """
    Affiche tous les éléments du jeu à l'écran
    """
    fltk.efface_tout()

    afficheFond(fond)

    # Elements du jeu

    affiche_pommes(pommes)
    affiche_serpent(serpent, "joueur")

    if choixMode == "deuxJoueur" or choixMode == "duel":
        affiche_serpent(serpent2, "ennemi")

    if choixMode == "contreOrdinateur":
        for serpents in serpentEnnemi:
            affiche_serpent(serpents, "ennemi")

    if opt_obstacles:
        affiche_obstacles(obstacles)

    if opt_nuit:
        fltk.image(largeurEcran // 2, hauteurEcran // 2,
                   f"image/obscurite/nuit{image_nuit}.png")

    if opt_obscurite and choixMode != "deuxJoueur":
        fltk.image(obscurite[0], obscurite[1], im_obscu)

    # Interface utilisateur

    fltk.image(0, 0, "image/menu/ATH.png", ancrage="nw")

    fltk.image(1489, 125, f"image/menu/logo{nb_titre}.png")

    fltk.texte(1489, 293, "{:0>6d}".format(meilleur_score), taille=50,
               ancrage="center")

    fltk.texte(1489, 468, "{:0>6d}".format(score), taille=50,
               ancrage="center")

    fltk.texte(1489, 593, "{:0>2d}:{:0>2d}".format(chrono // 60, chrono % 60),
               taille=50, ancrage="center")

    fltk.texte(1489, 768, "{:0>6d}".format(nb_pommes), taille=50,
               ancrage="center")

    fltk.texte(1489, 893, "{:0>6d}".format(nb_kills), taille=50,
               ancrage="center")

    if fps:
        fltk.texte(1696, 10, f"{ips} FPS", ancrage="ne", taille=15)

    fltk.mise_a_jour()


def titre_aleatoire():
    """
    Défini une valeur aléatoire correspondant à un titre du jeu

    >>> from random import seed
    >>> seed(42)
    >>> niveau = 4
    >>> titre_aleatoire()
    1

    >>> niveau = 12
    >>> titre_aleatoire()
    1
    """
    return randint(1, min(6, niveau))


###############################################################################
#                                Serpent                                      #
###############################################################################


# - - - - - - - Affichage - - - - - - - #


def affiche_serpent(serpent, couleur):
    """
    Appelle les fonction qui affichent le serpent

    :param serpent: Liste des coordonnées de chaque parties du serpent
    :param couleur: Serpent a afficher (joueur ou ennemi)
    """
    afficher_tete_serpent(serpent, couleur)
    afficher_corps_serpent(serpent, couleur)
    afficher_queu_serpent(serpent, couleur)


def afficher_tete_serpent(serpent, color):
    """
    Affiche la tête du serpent classique ou personnalisée

    :param serpent: Liste des coordonnées de chaque parties du serpent
    :param color: Serpent a afficher (joueur ou ennemi)
    """
    x, y = case_vers_pixel(serpent[0])
    # Coordonnées du second élément du serpent :
    xApres, yApres = case_vers_pixel(serpent[1])

    # Joueur avec texture classique ou serpent ennemi
    if not opt_paint or color == 'ennemi' or \
            coordonneesDessinSerpents is None:
        if xApres + taille_case == x or \
                xApres - largeurEcran + taille_case == x:
            fltk.image(x, y, f'image/serpent/serpentTete_{color}.png')
        elif xApres - taille_case == x or \
                xApres + largeurEcran - taille_case == x:
            fltk.image(x, y, f'image/serpent/serpentTeteGauche_{color}.png')
        elif yApres + taille_case == y or \
                yApres - hauteurEcran + taille_case == y:
            fltk.image(x, y, f'image/serpent/serpentTeteBas_{color}.png')
        elif yApres - taille_case == y or \
                yApres + hauteurEcran - taille_case == y:
            fltk.image(x, y, f'image/serpent/serpentTeteHaut_{color}.png')
    # Joueur avec texture moddifiée
    else:
        afficherDessinSerpentTete(x, y, xApres, yApres)


def afficher_corps_serpent(serpent, color):
    """
    Affiche le corps du serpent

    :param serpent: Liste des coordonnées de chaque parties du serpent
    :param color: Serpent a afficher (joueur ou ennemi)
    """
    for i in range(1, len(serpent) - 1):
        # Compare la position de chaque élément du corps du serpent avec la
        # position du précédent et du suivant afin de trouver l'orientation de
        # l'image a afficher
        x, y = case_vers_pixel(serpent[i])
        xAvant, yAvant = case_vers_pixel(serpent[i - 1])
        xApres, yApres = case_vers_pixel(serpent[i + 1])

        if yAvant == y == yApres:
            fltk.image(x, y, f'image/serpent/serpentCorp_{color}.png', )
        elif xAvant == x == xApres:
            fltk.image(x, y, f'image/serpent/serpentCorpVertical_{color}.png')

        elif (xApres - taille_case == x or
              xApres + largeurEcran - taille_case == x) and \
                (yAvant - taille_case == y or
                 yAvant + hauteurEcran - taille_case == y) or \
                (yApres - taille_case == y or
                 yApres + hauteurEcran - taille_case == y) and \
                (xAvant - taille_case == x or
                 xAvant + largeurEcran - taille_case == x):
            fltk.image(x, y, f'image/serpent/serpentCorp4_{color}.png')

        elif (xApres + taille_case == x or
              xApres - largeurEcran + taille_case == x) and \
                (yAvant - taille_case == y or
                 yAvant + hauteurEcran - taille_case == y) or \
                (yApres - taille_case == y or
                 yApres + hauteurEcran - taille_case == y) and \
                (xAvant + taille_case == x or
                 xAvant - largeurEcran + taille_case == x):
            fltk.image(x, y, f'image/serpent/serpentCorp3_{color}.png')

        elif (xApres - taille_case == x or
              xApres + largeurEcran - taille_case == x) and \
                (yAvant + taille_case == y or
                 yAvant - hauteurEcran + taille_case == y) or \
                (xAvant - taille_case == x or
                 xAvant + largeurEcran - taille_case == x) and \
                (yApres + taille_case == y or
                 yApres - hauteurEcran + taille_case == y):
            fltk.image(x, y, f'image/serpent/serpentCorp1_{color}.png')

        elif (xApres + taille_case == x or
              xApres - largeurEcran + taille_case == x) and \
                (yAvant + taille_case == y or
                 yAvant - hauteurEcran + taille_case == y) or \
                (xAvant + taille_case == x or
                 xAvant - largeurEcran + taille_case == x) and \
                (yApres + taille_case == y or
                 yApres - hauteurEcran + taille_case == y):
            fltk.image(x, y, f'image/serpent/serpentCorp2_{color}.png')


def afficher_queu_serpent(serpent, color):
    """
    Affiche la queue du serpent

    :param serpent: Liste des coordonnées de chaque parties du serpent
    :param color: Serpent a afficher (joueur ou ennemi)
    """
    x, y = case_vers_pixel(serpent[-1])
    xAvant, yAvant = case_vers_pixel(serpent[-2])
    if xAvant - taille_case == x or xAvant + largeurEcran - taille_case == x:
        fltk.image(x, y, f'image/serpent/serpentQueueDroite_{color}.png')
    elif xAvant + taille_case == x or xAvant - largeurEcran + taille_case == x:
        fltk.image(x, y, f'image/serpent/serpentQueueGauche_{color}.png')
    elif yAvant - taille_case == y or yAvant + hauteurEcran - taille_case == y:
        fltk.image(x, y, f'image/serpent/serpentQueueBas_{color}.png')
    elif yAvant + taille_case == y or yAvant - hauteurEcran + taille_case == y:
        fltk.image(x, y, f'image/serpent/serpentQueueHaut_{color}.png')


# - - - - - - - Déplacement - - - - - - - #


def change_direction(direction, touche, opt_deplacement, joueur):
    """
    Appelle les fonctions qui gèrent l'orientation

    :param direction: Couple de la direction du serpent
    :param touche: Touche pressée
    :param opt_deplacement: Booléen indiquant le type de déplacement
    :param joueur: Joueur 1 ou Joueur 2
    :return: Couple de la direction

    >>> change_direction((0, 1), "Right", True, "j1")
    (-1, 0)

    >>> change_direction((1, 0), "z", False, "j2")
    (0, -1)
    """
    if joueur == "j1":
        if opt_deplacement:
            return deplacement_rotation(direction, touche, "Left", "Right")
        else:
            return deplacement_direction(direction, touche, "Up", "Down",
                                         "Left", "Right")
    elif joueur == "j2":
        if opt_deplacement:
            return deplacement_rotation(direction, touche, "q", "d")
        else:
            return deplacement_direction(direction, touche, "z", "s", "q", "d")


def deplacement_rotation(direction, touche, gauche, droite):
    """
    Rotation du serpent de 90° avec deux touches (Droite et Gauche)

    :param direction: Couple de la direction du serpent
    :param touche: Touche pressée
    :param gauche: Touche pour aller a gauche (Left ou q)
    :param droite: Touche pour aller a droite (Right ou d)
    :return: Couple de la direction

    >>> deplacement_rotation((1, 0), "Left", "Left", "Right")
    (0, -1)

    >>> deplacement_rotation((0, -1), "d", "q", "d")
    (1, 0)
    """
    if (direction == (0, -1) and touche == gauche) or \
            (direction == (0, 1) and touche == droite):
        return -1, 0
    elif (direction == (-1, 0) and touche == gauche) or \
            (direction == (1, 0) and touche == droite):
        return 0, 1
    elif (direction == (0, 1) and touche == gauche) or \
            (direction == (0, -1) and touche == droite):
        return 1, 0
    elif (direction == (1, 0) and touche == gauche) or \
            (direction == (-1, 0) and touche == droite):
        return 0, -1
    else:
        return direction


def deplacement_direction(direction, touche, haut, bas, gauche, droite):
    """
    Changement de direction en fonction de la touche pressée (4 touches)

    :param direction: Couple de la direction du serpent
    :param touche: Touche pressée
    :param bas: Touche pour aller en bas (Down ou s)
    :param haut: Touche pour aller en haut (Up ou z)
    :param gauche: Touche pour aller a gauche (Left ou q)
    :param droite: Touche pour aller a droite (Right ou d)
    :return: Couple de la direction

    >>> deplacement_direction((-1, 0), "Down", "Up", "Down", "Left", "Right")
    (0, 1)

    >>> deplacement_direction((0, 1), "q", "z", "s", "q", "d")
    (0, 1)
    """
    if touche == haut and direction != (0, 1):
        return 0, -1
    elif touche == bas and direction != (0, -1):
        return 0, 1
    elif touche == gauche and direction != (1, 0):
        return -1, 0
    elif touche == droite and direction != (-1, 0):
        return 1, 0
    else:
        return direction


def deplacement_serpent(serpent, direction, opt_obscurite=False,
                        obscurite=None):
    """
    Met à jours les coordonnées des parties du serpent

    :param serpent: Liste des couples de coordonées du corps du serpent
    :param direction: Couple de la direction du serpent
    :param opt_obscurite: Booléen de l'option obscurité
    :param obscurite: Coordonnées du centre du cercle du champs de vision
    :return: Nouvelles coordonnées du serpent et coordonnées obscurité

    >>> deplacement_serpent([(3, 1), (2, 1) ,(1, 1)], (1, 0))
    ([(4, 1), (3, 1) ,(2, 1)], None)

    >>> deplacement_serpent([(1, 3), (1, 2) ,(1, 1)], (0, 1), True, (1, 3))
    ([(1, 4), (1, 3) ,(1, 2)], (1, 4))
    """
    # Retrait du dernier élément du serpent (queue)
    serpent.pop(-1)
    # Ajout en premiere positions des coordonnées de la tête après déplacement
    serpent.insert(0, (serpent[0][0] + direction[0],
                       serpent[0][1] + direction[1]))
    if opt_obscurite and obscurite is not None:
        obscurite = (obscurite[0] + taille_case * direction[0],
                     obscurite[1] + taille_case * direction[1])
    return serpent, obscurite


# - - - - - - - Intéractions - - - - - - - #


def collision_serpent(serpent, obstacles, ennemiSerpent,
                      opt_torique, serpent2):
    """
    Verifie les collision du serpent avec des éléments qui provoquent sa mort

    :param serpent: Liste des couples de coordonées du corps du serpent
    :param obstacles: Liste des couples de coordonées des obstacles
    :param ennemiSerpent: Liste qui contient des serpents (voir plus haut)
    :param opt_torique: Booléen de l'option d'arène torique
    :param serpent2: Liste des couples de coordonées du second serpent
    :return: Booleen, True si il y a collision, False sinon

    >>> collision_serpent([(3, 1), (2, 1) ,(1, 1)], [(3, 1)], [], False, [])
    True

    >>> collision_serpent([(3, 1), (2, 1) ,(1, 1)], [], [], False, [])
    False
    """
    # Bords de la zone
    if bord_zone(serpent, opt_torique):
        return True

    # Obstacles (arbres)
    if serpent[0] in obstacles:
        return True

    # Lui même
    if serpent[0] in serpent[1:]:  # De l'élément 1 à la fin de la liste
        return True

    # L'autre serpent
    if serpent[0] in serpent2:
        return True

    # Serpents de la horde
    for j in ennemiSerpent:
        if serpent[0] in j:
            return True

    return False


def bord_zone(serpent, opt_torique):
    """
    Détecte les collision du serpent avec les bords de la zone de jeu

    :param serpent: Liste des couples de coordonées du corps du serpent
    :param opt_torique: Booléen de l'option d'arène torique
    :return: True si collision

    >>> bord_zone([(-1, 1), (0, 1) ,(1, 1)], False)
    True
    """
    # Mode Normal
    if (serpent[0][0] < 0 or serpent[0][0] > largeur_plateau - 1 or
        serpent[0][1] < 0 or serpent[0][1] > hauteur_plateau - 1) \
            and not opt_torique:
        return True

    # Avec Arène Torique
    else:
        if serpent[0][0] < 0:
            serpent[0] = (largeur_plateau - 1, serpent[0][1])
        elif serpent[0][0] > largeur_plateau - 1:
            serpent[0] = (0, serpent[0][1])
        elif serpent[0][1] < 0:
            serpent[0] = (serpent[0][0], hauteur_plateau - 1)
        elif serpent[0][1] > hauteur_plateau - 1:
            serpent[0] = (serpent[0][0], 0)


def detection_evenement(ev, ty, choixMode, direction, opt_deplacement,
                        joueur="j1"):
    """
    Réalise des actions si le joueur quitte ou appuie sur une touche

    :param ev: Evenement détecté par fltk
    :param ty: Type de cet événement
    :param choixMode: Mode de jeu sélectionné
    :param direction: Couple de la direction du serpent
    :param opt_deplacement: Booléen de l'option de déplacement
    :param joueur: Joueur 1 ou joueur 2
    :return: Mode de jeu, Direction du serpent

    >>> detection_evenement("", "Quitte", "jouer", (0, 1), True, "j2")
    ("menu", (0, 1))

    >>> detection_evenement("Up", "Touche", "contreOrdinateur", (1, 0), False)
    ("contreOrdinateur", (0, -1))
    """
    if ty == 'Quitte':
        choixMode = 'menu'
    elif ty == 'Touche':
        direction = change_direction(direction, fltk.touche(ev),
                                     opt_deplacement, joueur)
    return choixMode, direction


###############################################################################
#                                 Mode Paint                                  #
###############################################################################


def dessinerSerpent():
    """
    Permet a l'utilisateur de dessiner la tête de son serpent

    :return: liste des coordonnées des pixel de la tête du serpent en format
        32 par 32 pixel ; choix du mode pour retourner au menu
    """
    fltk.ferme_fenetre()
    fltk.cree_fenetre(taille_case * 24 + 10, taille_case * 24 + 100)

    # Reset l'ancien dessin du joueur
    coordonneesCouleur = []

    # Limite zone de dessin
    fltk.rectangle(0, 0, taille_case * 24 + 10, taille_case * 20 + 20,
                   epaisseur=5)

    # Dessin carrée retour au menu
    fltk.image(5, 5, "image/menu/retourMenu.png", ancrage="nw")

    # Affichage des carrées pour choisir sa couleur
    fltk.rectangle((taille_case * 24 + 10) / 6,
                   taille_case * 24 + 25,
                   (taille_case * 24 + 10) / 6 + 50,
                   taille_case * 24 + 25 + 50, remplissage="red")
    fltk.texte((taille_case * 24 + 10) / 6, taille_case * 24 + 25, "a")
    fltk.rectangle((taille_case * 24 + 10) / 6 + 100,
                   taille_case * 24 + 25,
                   (taille_case * 24 + 10) / 6 + 50 + 100,
                   taille_case * 24 + 25 + 50, remplissage="green")
    fltk.texte((taille_case * 24 + 10) / 6 + 100, taille_case * 24 + 25, "z")
    fltk.rectangle((taille_case * 24 + 10) / 6 + 200,
                   taille_case * 24 + 25,
                   (taille_case * 24 + 10) / 6 + 50 + 200,
                   taille_case * 24 + 25 + 50, remplissage="yellow")
    fltk.texte((taille_case * 24 + 10) / 6 + 200, taille_case * 24 + 25, "e")
    fltk.rectangle((taille_case * 24 + 10) / 6 + 300,
                   taille_case * 24 + 25,
                   (taille_case * 24 + 10) / 6 + 50 + 300,
                   taille_case * 24 + 25 + 50, remplissage="blue")
    fltk.texte((taille_case * 24 + 10) / 6 + 300, taille_case * 24 + 25, "r")
    fltk.rectangle((taille_case * 24 + 10) / 6 + 400,
                   taille_case * 24 + 25,
                   (taille_case * 24 + 10) / 6 + 50 + 400,
                   taille_case * 24 + 25 + 50, remplissage="black")
    fltk.texte((taille_case * 24 + 10) / 6 + 400, taille_case * 24 + 25, "t",
               couleur="white")
    fltk.rectangle((taille_case * 24 + 10) / 6 + 500,
                   taille_case * 24 + 25,
                   (taille_case * 24 + 10) / 6 + 50 + 500,
                   taille_case * 24 + 25 + 50, remplissage="white")
    fltk.texte((taille_case * 24 + 10) / 6 + 500, taille_case * 24 + 25, "y")

    # Dessin du cou qui sert de référence
    for i in range(6):
        fltk.rectangle(i * 20, 20 * 11, i * 20 + 20, 20 * 12,
                       remplissage="black")
    for i in range(6):
        fltk.rectangle(i * 20, 20 * 20, i * 20 + 20, 20 * 21,
                       remplissage="black")

    couleur = "black"
    bord = ""

    retourMenu = False
    while not retourMenu:

        # Attend une entré de touche et l'enregistre
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)
        touche = fltk.touche(evenement)

        if dansRectangle(evenement, type_evenement, 5, 5, 105, 105):
            retourMenu = True

        abscisseClic = fltk.abscisse(evenement)
        ordonneeClic = fltk.ordonnee(evenement)

        # Changer de couleur
        couleur, bord = detectionToucheCouleur(touche, couleur, bord)

        # Conversion des coordonnées vers case
        hautCarreX = int(abscisseClic // 20) * 20
        hautCarreY = int(ordonneeClic // 20) * 20
        basCarreX = int(abscisseClic // 20) * 20 + 20
        basCarreY = int(ordonneeClic // 20) * 20 + 20

        # Dessine le carre sur la position de la souris si il y a un ClicGauche
        if type_evenement == "ClicGauche" and abscisseClic > 20 * 6 \
                and taille_case * 20 + 20 > ordonneeClic > 10:
            fltk.rectangle(hautCarreX, hautCarreY, basCarreX, basCarreY,
                           remplissage=couleur, couleur=bord,
                           tag="carre")
            coordonneesCouleur.append([hautCarreX // 20 - 6, hautCarreY // 20,
                                       couleur])
        # Efface le tableau si il y a un ClicDroit
        elif type_evenement == "ClicDroit" and abscisseClic > taille_case * 4 \
                and taille_case * 20 + 10 > ordonneeClic > 10:
            fltk.efface("carre")
            coordonneesCouleur = []

        fltk.mise_a_jour()

    # Cree les 3 autres rotations de l'image
    coordonneesCouleurBas = rotationDessin(coordonneesCouleur)
    coordonneesCouleurGauche = rotationDessin(coordonneesCouleurBas)
    coordonneesCouleurHaut = rotationDessin(coordonneesCouleurGauche)

    fltk.ferme_fenetre()

    return (coordonneesCouleur, coordonneesCouleurBas,
            coordonneesCouleurGauche, coordonneesCouleurHaut)


def detectionToucheCouleur(touche, couleur, bord):
    """
    Change la couleur du pinceau en fonction de la touche pressé

    :param touche: Touche pressé
    :param couleur: couleur du piceau
    :param bord: couleur des bord des rectangle égal à cel du pinceau
    :return: couleur ; bord

    >>> detectionToucheCouleur("z", "blue", "blue")
    ("green", "green")
    """
    if touche == "a":
        couleur = "red"
        bord = "red"
        return couleur, bord
    elif touche == 'z':
        couleur = "green"
        bord = "green"
        return couleur, bord
    elif touche == "e":
        couleur = "yellow"
        bord = "yellow"
        return couleur, bord
    elif touche == "r":
        couleur = "blue"
        bord = "blue"
        return couleur, bord
    elif touche == "t":
        couleur = "black"
        bord = "black"
        return couleur, bord
    elif touche == "y":
        couleur = "white"
        bord = "white"
        return couleur, bord
    return couleur, bord


def afficherDessinSerpentTete(x, y, xApres, yApres):
    """
    affiche le dessin du joueur à la place de la tête du serpent
    """
    if xApres + taille_case == x or xApres - largeurEcran + taille_case == x:
        for k in coordonneesDessinSerpents[0]:
            fltk.rectangle(k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           couleur=k[2])
    elif yApres + taille_case == y or yApres - hauteurEcran + taille_case == y:
        for k in coordonneesDessinSerpents[1]:
            fltk.rectangle(k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           couleur=k[2])
    elif xApres - taille_case == x or xApres + largeurEcran - taille_case == x:
        for k in coordonneesDessinSerpents[2]:
            fltk.rectangle(k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           couleur=k[2])
    elif yApres - taille_case == y or yApres + hauteurEcran - taille_case == y:
        for k in coordonneesDessinSerpents[3]:
            fltk.rectangle(k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           k[0] + serpent[0][0] * 32,
                           k[1] + serpent[0][1] * 32,
                           couleur=k[2])


def rotationDessin(dessinSerpent):
    """
    Effectue une rotation de 90° sens horaire du dessin du serpent pour avoir
    pouvoir afficher le serpent dans toutes les directions

    :param dessinSerpent: Listes des coordonnées des pixels de la tête
        du serpent

    >>> rotationDessin([(0, 0, "black"), (16, 16, "red")])
    [(32, 0, "black"), (16, 16, "red")]
    """
    nouveauDessin = []
    for k in dessinSerpent:
        nouveauDessin.append([32 - k[1], k[0], k[2]])
    return nouveauDessin


###############################################################################
#                            Gestion des pommes                               #
###############################################################################


# - - - - - - - Affichage - - - - - - - #


def affiche_pommes(pommes):
    """
    Affiche les pommes

    :param pommes: Liste des couples de coordonées des pommes
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        fltk.image(x, y, 'image/divers/pomme.png')


# - - - - - - - Création - - - - - - - #


def creation_pommes(pommes, serpent, opt_pommes, obstacles, nb_joueur,
                    serpent2=[]):
    """
    Appelle les fonctions de génération de pommes en fonction de l'option
    de génération choisie

    :param pommes: Liste des couples de coordonées des pommes
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param opt_pommes: Booléen de l'option de génération de pommes
    :param obstacles: Liste des couples de coordonées des obstacles
    :param nb_joueur: Nombre de joueur (1 ou 2)
    :param serpent2: Liste des couples de coordonées du second serpent
    :return: Liste des couples de coordonées des pommes
    """
    if opt_pommes:
        pommes = pommes_multi(pommes, serpent, obstacles, serpent2, nb_joueur)
    else:
        pommes = pommes_unique(pommes, serpent, obstacles, serpent2)
    return pommes


def pommes_multi(pommes, serpent, obstacles, serpent2, nb_joueur):
    """
    Génère des pommes à des moments et des endroits aléatoires

    :param pommes: Liste des couples de coordonées des pommes
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param obstacles: Liste des couples de coordonées des obstacles
    :return: Liste des couples de coordonées des pommes
    :param serpent2: Liste des couples de coordonées du second serpent
    :param nb_joueur: Nombre de joueur (1 ou 2)

    >>> from random import seed
    >>> seed(42)
    >>> pommes_multi([], [(3, 1), (2, 1) ,(1, 1)], [], [], 1)
    [(8, 1)]
    """
    # Les valeurs pour l'aléatoire sont définies afin que plus il y a de pommes
    # présentes, plus il est rare qu'une nouvelle se génère
    if randint(0, 20 // nb_joueur + 5 * len(pommes)) == 0:
        pommeX = randint(1, largeur_plateau - 1)
        pommeY = randint(1, hauteur_plateau - 1)
        # Pour empêcher la génération d'un objet dans un autre :
        if (pommeX, pommeY) not in serpent and (pommeX, pommeY) not in pommes \
                and (pommeX, pommeY) not in obstacles and (pommeX, pommeY) \
                not in serpent2:
            pommes.append((pommeX, pommeY))
    return pommes


def pommes_unique(pommes, serpent, obstacles, serpent2):
    """
    Génère une pomme à un endroit aléatoire si et seulement si il n'y a
    aucune pomme déjà présente


    :param pommes: Liste des couples de coordonées des pommes
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param obstacles: Liste des couples de coordonées des obstacles
    :param serpent2: Liste des couples de coordonées du second serpent
    :return: Liste des couples de coordonées des pommes

    >>> from random import seed
    >>> seed(42)
    >>> pommes_unique([], [(3, 1), (2, 1) ,(1, 1)], [(3, 16)], [], 1)
    [(8, 1)]

    >>> pommes_unique([(13, 24)], [(3, 1), (2, 1) ,(1, 1)], [(3, 16)], [])
    [(13, 24)]
    """
    if len(pommes) == 0:
        pommeX = randint(1, largeur_plateau - 1)
        pommeY = randint(1, hauteur_plateau - 1)
        while (pommeX, pommeY) in serpent or (pommeX, pommeY) in obstacles or \
                (pommeX, pommeY) in serpent2:
            pommeX = randint(1, largeur_plateau - 1)
            pommeY = randint(1, hauteur_plateau - 1)
        pommes.append((pommeX, pommeY))
    return pommes


# - - - - - - - Collisions - - - - - - - #


def collision_pommes(pommes, serpent, nb_pommes, pommes_attente, score=None,
                     im_obscu=None):
    """
    Detecte la collision entre la tête du serpent et une pomme

    :param pommes: Liste des couples de coordonées des pommes
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param nb_pommes: Nombre de pommes mangées
    :param pommes_attente: Liste des coordonnées des pommes mangées
    :param score: Score du joueur (défaut : None)
    :param im_obscu: Coorodonées de l'image de l'option obscurité
    :return: Couple contenant les coordonnées de la pomme mangée et la longeur
        du serpent ; Nombre de pommes ; Score du joueur

    >>> collision_pommes([(3, 1)], [(3, 1), (2, 1) ,(1, 1)], 0, [], 3)
    ([((3, 1), 3)], 1, 8, None)
    """
    for e in pommes:
        if serpent[0] == e:
            if score is not None:  # Si c'est le joueur qui mange la pomme
                pommes_attente.append((e, len(serpent)))
                nb_pommes += 1
                score += nb_pommes * 5
                if im_obscu is not None:
                    im_obscu = "image/obscurite/cercleObscuriteGrand.png"
            pommes.remove(e)  # Retrait de la pomme mangée de la liste

    if score is not None:
        return pommes_attente, nb_pommes, score, im_obscu


def grandir_serpent(serpent, pommes_attente, image_obscurite):
    """
    Agrandi le serpent en fonction de ce qu'il mange

    :param serpent: Liste des couples de coordonées du corps du serpent
    :param pommes_attente: Liste des coordonnées des pommes mangées
    :param image_obscurite: Coorodonées de l'image de l'option obscurité
    :return: serpent ; pommes_attente ; image_obscurite

    >>> grandir_serpent([(5, 1), (4, 1) ,(3, 1)], [((2, 1), 0)], None)
    ([(5, 1), (4, 1) ,(3, 1), (2, 1)], [],\
    "image/obscurite/cercleObscuritePetit.png")
    """
    for i in range(len(pommes_attente)):

        # Si la queue vient de dépasser les coordonnées de la pomme mangée :
        if pommes_attente[i][1] == 0:
            # Agrandissement du serpent à la position de la pomme mangée :
            serpent.append(pommes_attente[i][0])
            pommes_attente[i] = -1
            image_obscurite = "image/obscurite/cercleObscuritePetit.png"
        else:
            a, b = pommes_attente[i]
            b -= 1  # Réduction de la longeur du serpent restante
            pommes_attente[i] = (a, b)

    while -1 in pommes_attente:  # Supression des pommes digérées
        pommes_attente.remove(-1)
    return serpent, pommes_attente, image_obscurite


###############################################################################
#                         Gestion des obstables                               #
###############################################################################


def affiche_obstacles(obstacles):
    """
    Affiche les obstacles

    :param obstacles: Liste des couples de coordonées des obstacles
    """
    for obstacle in obstacles:
        if fond == "fondHerbe":
            fltk.image(obstacle[0] * 32 + 16, obstacle[1] * 32 + 16,
                       'image/divers/arbre.png')
        elif fond == "fondDesert":
            fltk.image(obstacle[0] * 32 + 16, obstacle[1] * 32 + 16,
                       'image/divers/cactus.png')
        else:
            fltk.image(obstacle[0] * 32 + 16, obstacle[1] * 32 + 16,
                       'image/divers/trouGlace.png')


def creation_obstacles(obstacles, serpent, pommes, opt_obstacles,
                       serpent2=[]):
    """
    Appelle les fonctions de génération d'obstacles si l'option obstacle
    a été choisie


    :param obstacles: Liste des couples de coordonées des obstacles
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param pommes: Liste des couples de coordonées des pommes
    :param opt_obstacles: Booléen de l'option obstacles
    :param serpent2: Liste des couples de coordonées du second serpent
    :return: Liste des couples de coordonées des obstacles

    >>> from random import seed
    >>> seed(42)
    >>> creation_obstacles([], [(5, 1), (4, 1) ,(3, 1)], [], True)
    [(8, 1)]

    >>> creation_obstacles([(5, 6)], [(5, 1), (4, 1) ,(3, 1)], [(3, 8)], False)
    [(5, 6)]
    """
    if opt_obstacles:
        x = randint(0, 30 + 2 * len(obstacles))
        if x == 0:
            obstacleX = randint(1, largeur_plateau - 1)
            obstacleY = randint(1, hauteur_plateau - 1)
            if (obstacleX, obstacleY) not in serpent and \
                    (obstacleX, obstacleY) not in obstacles and \
                    (obstacleX, obstacleY) not in pommes and \
                    (obstacleX, obstacleY) not in serpent2:
                obstacles.append((obstacleX, obstacleY))
    return obstacles


###############################################################################
#                     Gestion des serpents ennemis                            #
###############################################################################


def creation_ennemi(serpentEnnemi):
    """
    Crée des serpent ennemis

    :param serpentEnnemi: Liste des serpents ennemis
        (serpents = listes de couples de coordonnées)
    :return: Liste des serpents ennemis

    >>> from random import randint
    >>> seed(2)
    >>> creation_ennemi([])
    [[(5, 30), (5, 31), (5, 32), (5, 33), (5, 34)]]
    """
    if randint(1, 10) == 1:

        if randint(1, 2) == 1:  # Apparition à la verticale
            positionEnnemiX = randint(0, largeur_plateau)
            if randint(1, 2) == 1:  # Apparition en haut
                taille = randint(3, 10)
                serpents = []
                # Création du serpent en fonction de sa taille, sa position et
                # son orientation :
                for i in range(1, taille + 1):
                    serpents.append((positionEnnemiX, -i))
                serpentEnnemi.append(serpents)
            else:  # Apparition en bas
                taille = randint(3, 10)
                serpents = []
                for i in range(hauteur_plateau, hauteur_plateau + taille):
                    serpents.append((positionEnnemiX, i))
                serpentEnnemi.append(serpents)

        else:  # Apparition à l'horizontale
            positionEnnemiY = randint(0, hauteur_plateau)
            if randint(1, 2) == 1:  # Apparition à gauche
                taille = randint(3, 6)
                serpents = []
                for i in range(1, taille + 1):
                    serpents.append((-i, positionEnnemiY))
                serpentEnnemi.append(serpents)
            else:  # Apparition à droite
                taille = randint(3, 6)
                serpents = []
                for i in range(largeur_plateau, largeur_plateau + taille):
                    serpents.append((i, positionEnnemiY))
                serpentEnnemi.append(serpents)
    return serpentEnnemi


def evenements_ennemis(serpent, serpentEnnemi, score, pommes_attente, nb_kill):
    """
    Gère les événements des serpents ennemis (déplacement, collisions)

    :param nb_kill:
    :param pommes_attente:
    :param serpent: Liste des couples de coordonnées du serpent
    :param serpentEnnemi: Liste des serpents ennemis
        (serpents = listes de couples de coordonnées)
    :param score: Score du joueur
    :pommes_attente: Liste des coordonnées des pommes mangées
    :return: Liste des serpents ennemis ; Score du joueur

    >>> evenements_ennemis([(3, 1), (2, 1), (1, 1)],\
    [[(5, 30), (5, 31), (5, 32), (5, 33), (5, 34)]], 2000, 0, 5)
    [[(5, 29), (5, 30), (5, 31), (5, 32), (5, 33)]], 2000, 5
    """
    for serpents in serpentEnnemi:

        # Déplacement des serpents
        if serpents[0][0] > serpents[1][0]:
            serpents = deplacement_serpent(serpents, (1, 0), taille_case)[0]
        elif serpents[0][0] < serpents[1][0]:
            serpents = deplacement_serpent(serpents, (-1, 0), taille_case)[0]
        elif serpents[0][1] > serpents[1][1]:
            serpents = deplacement_serpent(serpents, (0, 1), taille_case)[0]
        elif serpents[0][1] < serpents[1][1]:
            serpents = deplacement_serpent(serpents, (0, -1), taille_case)[0]

        # Collisions avec les bords du terrain
        if serpents[-1][0] < -3 or serpents[-1][0] > largeurEcran + 3 or \
                serpents[-1][1] < -3 or serpents[-1][1] > hauteurEcran + 3:
            serpentEnnemi.remove(serpents)

        # Collision avec le joueur
        if serpents[0] in serpent:
            serpentEnnemi.remove(serpents)
            score += 100
            nb_kill += 1

        collision_pommes(pommes, serpents, nb_pommes, pommes_attente)

    return serpentEnnemi, score, nb_kill


###############################################################################
#                            Cycle Jour Nuit                                  #
###############################################################################


def cycle_jn(temps_nuit, image_nuit, cycle_nuit, prog_nuit, opt_nuit):
    """
    Définit le taux de luminosité en fonction du temps

    :param temps_nuit: Compteur de temps d'une période de la journée
    :param image_nuit: ID de l'image associée à l'heure (midi, minuit...)
    :param cycle_nuit: Période de la journée (nuit, jour, crépuscule...)
    :param prog_nuit: Compteur de temps pendant une transition jour-nuit
    :param opt_nuit: Booléen de l'option du cycle jour-nuit
    :return: temps_nuit, image_nuit, cycle_nuit, prog_nuit

    >>> cycle_jn(15, 19, "nuit-jour", 0, True)
    (0, 0, "jour", 0)
    """
    if opt_nuit:
        if temps_nuit == 15 and cycle_nuit == "jour":
            cycle_nuit = "jour-nuit"
            image_nuit = 0
            temps_nuit = 0
            prog_nuit = 0
        elif temps_nuit == 15 and cycle_nuit == "jour-nuit":
            cycle_nuit = "nuit"
            image_nuit = 95
            temps_nuit = 0
            prog_nuit = 0
        elif temps_nuit == 15 and cycle_nuit == "nuit":
            cycle_nuit = "nuit-jour"
            image_nuit = 95
            temps_nuit = 0
            prog_nuit = 0
        elif temps_nuit == 15 and cycle_nuit == "nuit-jour":
            cycle_nuit = "jour"
            image_nuit = 0
            temps_nuit = 0
            prog_nuit = 0

        elif temps_nuit < 15 and cycle_nuit == "jour-nuit":
            if prog_nuit == 3:
                image_nuit += 19
                prog_nuit = 0
        elif temps_nuit < 15 and cycle_nuit == "nuit-jour":
            if prog_nuit == 3:
                image_nuit -= 19
                prog_nuit = 0
    return temps_nuit, image_nuit, cycle_nuit, prog_nuit


###############################################################################
#                        Score, Niveau et Temps                               #
###############################################################################


def gestion_framerate():
    """
    Gère le framerate du jeu (accélération, temps de pause entre deux images)
    """
    global framerate, score, opt_acceleration, temps_debut, temps_fin, \
        temps_intervalle, ips

    # Accélération
    if opt_acceleration and framerate < 60:
        framerate = acceleration(score)

    # Temps de pause entre deux images
    temps_fin = time()
    temps_intervalle = temps_fin - temps_debut

    ips = int(min(1 / temps_intervalle, framerate))

    if temps_intervalle < 1 / framerate:
        sleep(1 / framerate - temps_intervalle)


def acceleration(chrono):
    """
    Acceleration du jeu si l'option acceleration a été choisie

    :param chrono: Temps depuis le début de la partie (en secondes)
    :return: Framerate mis à jour

    >>> acceleration(10)
    10

    >>> acceleration(500)
    12
    """
    return 10 + chrono // 250


def temps(chrono, progression, ips, score, temps_nuit, prog_nuit,
          opt_nuit):
    """
    Compte les secondes depuis le début de la partie
    (mise à jour du chrono et du score)

    :param chrono: Temps de la partie (en secondes)
    :param progression: Nombre de frames depuis la dernière seconde passée
    :param score: Score du joueur
    :param ips: Fréquence d'images par secondes
    :param prog_nuit: Compteur de temps pendant une transition jour-nuit
    :param temps_nuit: Compteur de temps d'une période de la journée
    :param opt_nuit: Booléen de l'option du cycle jour-nuit
    :return: chrono ; progression ; score ; temps_nuit ; prog_nuit

    >>> temps(0, 0, 10, 0, 0, 0, False)
    (0, 1, 0, 0, 0)

    >>> temps(10, 9, 10, 10, 10, 10, True)
    (11, 0, 11, 11, 11)
    """
    progression += 1
    if progression >= ips:
        chrono += 1
        score += 1
        progression = 0
        if opt_nuit:
            temps_nuit += 1
            prog_nuit += 1
    return chrono, progression, score, temps_nuit, prog_nuit


def level(niveau, xp, score):
    """
    Fonction qui met à jour le niveau et l'xp à la fin d'une partie

    :param niveau: Niveau du joueur
    :param xp: Points d'expérience du joueur
    :param score: Score du joueur (en fin de partie)
    :return: niveau ; expérience

    >>> level(1, 900, 100)
    (2, 0)

    >>> level(10, 666, 42)
    (10, 708)
    """
    xp += score
    while xp >= niveau ** 2 * 1000:  # Experience requise pour level up
        xp -= niveau ** 2 * 1000
        niveau += 1
    return niveau, xp


def meilleur(meilleur_score, score):
    """
    Met à jour le meilleur score

    :param meilleur_score: Meilleur Score
    :param score: Score
    :return: Meilleur Score

    >>> meilleur(1000, 2000)
    2000

    >>> meilleur(2000, 1000)
    2000
    """
    if score > meilleur_score:
        return score
    return meilleur_score


###############################################################################
#                            Gestion des menus                                #
###############################################################################


# - - - - - - - Général - - - - - - - #


def dansRectangle(evenement, typeEvenement, rectangleAX, rectangleAY,
                  rectangleBX, rectangleBY):
    """
    Détecte un clic dans un rectangle

    :param evenement: Evenement de fltk
    :param typeEvenement: Type de l'événement
    :param rectangleAX: Coordonnées coin supérieur gauche X
    :param rectangleAY: Coordonnées coin supérieur gauche Y
    :param rectangleBX: Coordonnées coin inférieur droit X
    :param rectangleBY: Coordonnées coin inférieur droit Y
    :return: True si le clic est dans le rectangle, False sinon

    >>> dansRectangle(<ButtonPress event num=1 x=100 y=100>, "ClicGauche",\
        0, 0, 200, 200)
    True

    >>> dansRectangle(<ButtonPress event num=1 x=100 y=100>, "ClicGauche",\
        200, 200, 400, 400)
    False
    """
    if typeEvenement == "ClicGauche" \
            and rectangleAX < fltk.abscisse(evenement) < rectangleBX \
            and rectangleAY < fltk.ordonnee(evenement) < rectangleBY:
        return True
    return False


def bouton(niveau):
    global boutonPommes, boutonObstacles, boutonAcceleration, bouton2Joueurs, \
        boutonDeplacement, boutonTorique, boutonNuit, boutonContreOrdi, \
        boutonPaint
    boutonPommes = "VER"
    boutonObstacles = "VER"
    boutonAcceleration = "VER"
    bouton2Joueurs = "VER"
    boutonDeplacement = "VER"
    boutonTorique = "VER"
    boutonNuit = "VER"
    boutonPaint = "VER"
    boutonContreOrdi = "VER"
    if niveau >= 2:
        boutonPommes = "DEB"
    if niveau >= 3:
        boutonObstacles = "DEB"
    if niveau >= 4:
        boutonAcceleration = "DEB"
    if niveau >= 5:
        bouton2Joueurs = "DEB"
    if niveau >= 6:
        boutonDeplacement = "DEB"
    if niveau >= 7:
        boutonTorique = "DEB"
    if niveau >= 8:
        boutonNuit = "DEB"
    if niveau >= 9:
        boutonPaint = "DEB"
    if niveau >= 10:
        boutonContreOrdi = "DEB"


def fin_jeu(serpent, choixMode, obstacles, ennemiSerpent, opt_torique,
            serpent2=[], id_serpent=1):
    """
    Déclenche la fin de la partie quand le joueur perd


    :param serpent: Liste des couples de coordonées du corps du serpent
    :param choixMode: Mode de jeu selectionné
    :param obstacles: Liste des couples de coordonées des obstacles
    :param ennemiSerpent: Liste qui contient des serpents (voir plus haut)
    :param opt_torique: Booléen de l'option arène torique
    :param serpent2: Liste des couples de coordonées du second serpent
    :param id_serpent: Joueur associé à serpent (1 ou 2)
    :return: un mode de jeu, le mode de jeu actuel, le joueur qui gagne en
        multijoueur (ou 3 pour egalite)

    >>> fin_jeu([(5, 1), (4, 1) ,(3, 1)], "jouer", [(5, 1)], [], False)
    ("finJeu", "jouer", 0)

    >>> fin_jeu([(5, 5), (4, 5) ,(3, 5)], "deuxJoueur", [],\
        [(5, 4), (5, 5) ,(5, 6)], False, 1)
    ("finJeu", "deuxJoueur", 2)
    """
    if collision_serpent(serpent, obstacles, ennemiSerpent, opt_torique,
                         serpent2):

        if choixMode == "deuxJoueur" or choixMode == "duel":
            if collision_serpent(serpent2, obstacles, ennemiSerpent,
                                 opt_torique, serpent):
                gain = 3
            else:
                if id_serpent == 1:
                    gain = 2
                elif id_serpent == 2:
                    gain = 1
        else:
            gain = 0

        return "finJeu", choixMode, gain
    return choixMode, choixMode, 0  # Le jeu continue


# - - - - - - - Menu Principal - - - - - - - #


def menu(niveau, xp, fps):
    """
    Gère le menu principal du jeu

    :param fps:
    :param niveau: Niveau du joueur
    :param xp: Expérience du joueur
    :return: Mode de jeu choisi ; Niveau ; Expérience

    >>> menu(4, 2000, False)
    (jouer, 4, 2000, False, 1)
    """

    # -----Affichages des éléments qui n'ont pas besoin d'être actualisé-------

    fltk.image(0, 0, "image/menu/fond.png", ancrage="nw")

    # Titre
    nb_titre = titre_aleatoire()
    fltk.image((largeurEcran + 426) // 2, hauteurEcran // 4,
               f"image/menu/nom{nb_titre}.png")

    # Affichage meilleur score
    fltk.image(largeurEcran + 421, 5, "image/menu/meilleurScore.png",
               ancrage="ne")
    fltk.texte(largeurEcran + 392, 10, "{:0>6d}".format(meilleur_score),
               taille=45, ancrage="ne")

    # Affichage bouton de jeu unique
    fltk.image((largeurEcran + 426) // 2, 475,
               "image/menu/boutonJouer.png")
    fltk.image((largeurEcran + 426) // 2 - 275, 775,
               "image/menu/boutonOptions.png")
    fltk.image((largeurEcran + 426) // 2 + 275, 775,
               "image/menu/boutonQuitter.png")

    while True:

        fltk.efface("reset")

        # Affichage barre d'expérience
        fltk.image(5, 5, "image/menu/barreXP.png", ancrage="nw", tag="reset")
        fltk.image(5, 49, "image/menu/niveau.png", ancrage="nw", tag="reset")
        fltk.rectangle(12, 12, 12 + xp * 400 // (niveau ** 2 * 1000), 42,
                       couleur="red", remplissage="red", tag="reset")
        # Affichage niveau
        fltk.texte(145, 45, str(niveau), taille=31, tag="reset")
        fltk.texte(207, 27, f"{xp}/{niveau ** 2 * 1000}", taille=20,
                   ancrage="center", tag="reset")

        if fps:  # Affiche ou non les fps
            fltk.texte(1696, 80, f"{ips} FPS", ancrage="ne", taille=15,
                       tag="reset")

        bouton(niveau)

        # Affiche les bouttons bloqués par le niveau
        fltk.image((largeurEcran + 426) // 2 - 275, 625,
                   f"image/menu/bouton2Joueurs{bouton2Joueurs}.png",
                   tag="reset")
        fltk.image((largeurEcran + 426) // 2 + 275, 625,
                   f"image/menu/boutonContreOrdi{boutonContreOrdi}.png",
                   tag="reset")

        fltk.mise_a_jour()

        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)

        # ----------------------Choix du mode de jeu---------------------------
        if dansRectangle(evenement, type_evenement, 353, 425, 1353, 525):
            return 'jouer', niveau, xp, fps, titre_aleatoire()

        elif niveau >= 5 and dansRectangle(evenement, type_evenement, 353, 575,
                                           803, 675):
            return "deuxJoueur", niveau, xp, fps, titre_aleatoire()

        elif niveau >= 10 and dansRectangle(evenement, type_evenement, 903,
                                            575, 1353, 675):
            choixMode = menu_contre_ordi()
            return choixMode, niveau, xp, fps, titre_aleatoire()

        elif dansRectangle(evenement, type_evenement, 353, 725, 803, 825):
            return 'option', niveau, xp, fps, titre_aleatoire()

        elif dansRectangle(evenement, type_evenement, 903, 725, 1353, 825):
            return "quitte", niveau, xp, fps, titre_aleatoire()

        # Mode développeur pour modifier le niveau du joueur et afficher fps
        niveau, xp, fps = mode_developpeur(evenement, niveau, xp, fps)


def mode_developpeur(evenement, niveau, xp, fps):
    """
    Permet de modifier le niveau ou d'afficher les fps à sa guise

    :param evenement: evenement fltk
    :param niveau: niveau joueur
    :param xp: expérience joueur
    :param fps: booléen qui dit si il faut afficher ou non les images par
        secondes
    :return: niveau ; xp ; fps
    """
    if fltk.touche(evenement) == "p":
        xp = 0
        niveau += 1

    elif fltk.touche(evenement) == "o" and niveau != 1:
        xp = 0
        niveau -= 1
        reset_options()

    elif fltk.touche(evenement) == "i":
        fps = not fps
    return niveau, xp, fps


# - - - - - - - Menu Mode Contre l'Ordinateur - - - - - - - #


def menu_contre_ordi():
    """
    Petit menu pour choisir entre le mode horde, duel ou retourner au menu

    :return: Mode de jeu choisi
    """
    fltk.efface_tout()
    fltk.image(0, 0, "image/menu/fond.png", ancrage="nw")
    fltk.image(578, 380, "image/menu/boutonHorde.png")
    fltk.image(1128, 380, "image/menu/boutonDuel.png")
    fltk.image(853, 580, "image/options/boutonMenu.png")

    while True:
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)

        if dansRectangle(evenement, type_evenement, 353, 330, 803, 430):
            return "contreOrdinateur"
        elif dansRectangle(evenement, type_evenement, 903, 330, 1353, 430):
            return "duel"
        elif dansRectangle(evenement, type_evenement, 353, 530, 1353, 630):
            return "menu"


# - - - - - - - Menu Options - - - - - - - #


def menu_options(choixMode):
    """
    Menu de choix des options

    :param choixMode: choix du mode de jeu
    :return: choix du mode de jeu

    >>> menu_options("option")
    "menu"
    """

    while choixMode == "option":

        # Affichage
        fltk.efface_tout()

        bouton(niveau)

        fltk.image(0, 0, "image/menu/fond.png", ancrage="nw")

        # ----------------Affichage des bouttons-------------------------------
        fltk.image(353, 125,
                   f"image/options/boutonPommes{boutonPommes}{opt_pommes}.png",
                   ancrage="nw")

        fltk.image(903, 125, f"image/options/boutonObstacles{boutonObstacles}"
                             f"{opt_obstacles}.png", ancrage="nw")

        fltk.image(353, 275, f"image/options/boutonAcceleration"
                             f"{boutonAcceleration}{opt_acceleration}.png",
                   ancrage="nw")

        fltk.image(903, 275, f"image/options/boutonDeplacement"
                             f"{boutonDeplacement}{opt_deplacement}.png",
                   ancrage="nw")

        fltk.image(353, 425, f"image/options/boutonTorique{boutonTorique}"
                             f"{opt_torique}.png", ancrage="nw")

        fltk.image(903, 425, f"image/options/boutonObscurite{boutonNuit}"
                             f"{opt_obscurite}.png", ancrage="nw")

        fltk.image(353, 575, f"image/options/boutonNuit{boutonNuit}"
                             f"{opt_nuit}.png", ancrage="nw")

        fltk.image(903, 575, f"image/options/boutonPaint{boutonPaint}"
                             f"{opt_paint}.png", ancrage="nw")

        fltk.image(353, 725, "image/options/boutonMenu.png", ancrage="nw")

        fltk.mise_a_jour()

        choixMode = detection_boutons_options()

        if choixMode == "menu":
            return choixMode

    return choixMode


def detection_boutons_options():
    """
    Detecte si le joueur clique sur une des options et la modifie si il a
    le niveau requis

    :return:
    """
    global opt_pommes, opt_obstacles, opt_acceleration, opt_deplacement, \
        opt_torique, opt_obscurite, opt_nuit, opt_paint

    evenement = fltk.attend_ev()
    type_evenement = fltk.type_ev(evenement)

    if niveau >= 2 and dansRectangle(evenement, type_evenement, 353, 125,
                                     803, 225):
        opt_pommes = not opt_pommes

    if niveau >= 3 and dansRectangle(evenement, type_evenement, 903, 125,
                                     1353, 225):
        opt_obstacles = not opt_obstacles

    if niveau >= 4 and dansRectangle(evenement, type_evenement, 353, 275,
                                     803, 375):
        opt_acceleration = not opt_acceleration

    if niveau >= 6 and dansRectangle(evenement, type_evenement, 903, 275,
                                     1353, 375):
        opt_deplacement = not opt_deplacement

    if niveau >= 7 and dansRectangle(evenement, type_evenement, 353, 425,
                                     803, 525):
        opt_torique = not opt_torique
        opt_obscurite = False

    if niveau >= 8 and dansRectangle(evenement, type_evenement, 903, 425,
                                     1353, 525):
        opt_obscurite = not opt_obscurite
        opt_torique = False

    if niveau >= 8 and dansRectangle(evenement, type_evenement, 353, 575,
                                     803, 675):
        opt_nuit = not opt_nuit

    if niveau >= 9 and dansRectangle(evenement, type_evenement, 903, 575,
                                     1128, 675):
        opt_paint = not opt_paint

    bouton_paint(evenement, type_evenement)

    if dansRectangle(evenement, type_evenement, 353, 725, 1353, 825):
        return "menu"

    return choixMode


def bouton_paint(evenement, type_evenement):
    """
    Detecte si le joueur appuis sur le bouton qui mène sur le menu de dessin

    :param evenement: evenement fltk
    :param type_evenement: type evenement fltk (touche, clic souris...)
    """

    global coordonneesDessinSerpents
    if niveau >= 9 and dansRectangle(evenement, type_evenement, 1128, 575,
                                     1353, 675):
        dessinerSerpents = dessinerSerpent()
        coordonneesDessinSerpents = dessinerSerpents
        fltk.cree_fenetre(largeurEcran + 426, hauteurEcran)


# - - - - - - - Tableau des Scores - - - - - - - #


def tableau_score(choixMode, modeTemp, gain):
    """
    Gère l'affichage de fin de partie (score, victoire du joueur 1 ou 2...)

    :param choixMode: Mode de jeu actuel
    :param modeTemp: Mode de jeu joué avant la fin de partie
    :param gain: Joueur ayant gagné (0 si solo, 3 si égalité)
    :return: Si appellée en fin de partie : mode de jeu "menu ; mode de jeu
        avant la fin de partie
    """
    if choixMode == "finJeu":
        fltk.efface_tout()

        if gain == 0:
            fltk.image(0, 0, "image/menu/finJeu.png", ancrage="nw")

            fltk.texte(1078, 400, "{:0>6d}".format(score), taille=50,
                       ancrage="center")

            fltk.texte(628, 400,
                       "{:0>2d}:{:0>2d}".format(chrono // 60, chrono % 60),
                       taille=50, ancrage="center")

            fltk.texte(628, 600, "{:0>6d}".format(nb_pommes), taille=50,
                       ancrage="center")

            fltk.texte(1078, 600, "{:0>6d}".format(nb_kills), taille=50,
                       ancrage="center")

        elif gain == 1:
            fltk.image(0, 0, "image/menu/finVert.png", ancrage="nw")

        elif gain == 2:
            fltk.image(0, 0, "image/menu/finRouge.png", ancrage="nw")

        elif gain == 3:
            fltk.image(0, 0, "image/menu/finEgalite.png", ancrage="nw")

        while True:

            evenement = fltk.attend_ev()
            type_evenement = fltk.type_ev(evenement)

            if dansRectangle(evenement, type_evenement, 453, 750, 803, 850):
                return "menu", modeTemp

            if dansRectangle(evenement, type_evenement, 903, 750, 1253, 850):
                return "menu", "menu"
    return choixMode, modeTemp


###############################################################################
#                                Gestion des fonds                            #
###############################################################################


def afficheFond(fond):
    """
    Affiche le fond du jeu

    :param fond: String contenant le type de fond à utiliser
    """
    fltk.image(largeurEcran / 2, hauteurEcran / 2, f"image/fond/{fond}.png")


def choixFond(niveau):
    """
    Sélectionne un fond aléatoire (nouveau fond débloqué au niveau 3 et 6)

    :param niveau: Niveau du joueur
    :return: String contenant le type de fond à utiliser

    >>> from random import seed
    >>> seed(42)
    >>> choixFond(1)
    1

    >>> choixFond(10)
    1
    """
    x = randint(1, min(niveau // 3 + 1, 3))
    if x == 1:
        return "fondHerbe"
    elif x == 2:
        return "fondDesert"
    elif x == 3:
        return "fondGlace"


###############################################################################
#                     Algorithme Adversaire Mode Duel                         #
###############################################################################


def ia(direction2, joueur, ordinateur, pommes, obstacles):
    """
    Appelle les fonctions qui gèrent le serpent controlé par l'ordinateur

    :param direction2: Direction du serpent de l'ordinateur
    :param joueur: Serpent du joueur
    :param ordinateur: Serpent de l'ordinateur
    :param pommes: Liste des Pommes
    :param obstacles: Liste des Obstacles
    :return: Direction du serpent de l'ordinateur
    """
    ordi = ordinateur[:]
    x, y = ordi[0]

    # Détection des pommes
    conditions, direction2 = ia_pommes(direction2, joueur, x, y, pommes,
                                       obstacles)
    if conditions:
        return direction2
    else:
        # Déplacement aléatoire
        direction2 = ia_aleatoire(direction2, joueur, x, y, obstacles)
        # Evitement des obstacles
        direction2 = ia_obstacles(direction2, joueur, ordinateur, obstacles)

    return direction2


def ia_pommes(direction2, joueur, x, y, pommes, obstacles):
    """
    Détecte la présence de pommes dans un rayon de 2 cases autour de la tête
    du serpent de l'ordinateur. Si il y en a une et qu'il n'y a pas d'obstacle
    sur le chemin pour y aller, change la direction du serpent de l'ordinateur

    :param direction2: Direction du serpent de l'ordinateur
    :param joueur: Serpent du joueur
    :param x: Coordonnée x de la tête du serpent de l'ordinateur
    :param y: Coordonnée y de la tête du serpent de l'ordinateur
    :param pommes: Liste des Pommes
    :param obstacles: Liste des Obstacles
    :return: True si pomme trouvée (False sinon) ; Direction pour aller
        chercher la pomme

    >>> ia_pommes((-1, 0), [(25, 1), (24, 1) ,(23, 1)], 5, 5, (5, 3), [])
    (True, (0, -1))
    """
    # Detection d'une pomme à 1 case de distance
    if (x, y + 1) in pommes and direction2 != (0, -1):
        return True, (0, 1)
    elif (x, y - 1) in pommes and direction2 != (0, 1):
        return True, (0, -1)
    elif (x + 1, y) in pommes and direction2 != (-1, 0):
        return True, (1, 0)
    elif (x - 1, y) in pommes and direction2 != (1, 0):
        return True, (-1, 0)

    # Detection d'une pomme à 2 cases de distance
    if (x, y + 2) in pommes and not collision_serpent([(x, y + 1)], obstacles,
                                                      [], opt_torique, joueur)\
            and direction2 != (0, -1):
        return True, (0, 1)
    elif (x, y - 2) in pommes and not collision_serpent([(x, y - 1)],
                                                        obstacles, [],
                                                        opt_torique, joueur)\
            and direction2 != (0, 1):
        return True, (0, -1)
    elif (x + 2, y) in pommes and not collision_serpent([(x + 1, y)],
                                                        obstacles, [],
                                                        opt_torique, joueur) \
            and direction2 != (-1, 0):
        return True, (1, 0)
    elif (x - 2, y) in pommes and not collision_serpent([(x - 1, y)],
                                                        obstacles, [],
                                                        opt_torique, joueur) \
            and direction2 != (1, 0):
        return True, (-1, 0)
    return False, direction2


def ia_aleatoire(direction2, joueur, x, y, obstacles):
    """
    Réalise une rotation aléatoire à un moment aléatoire

    :param direction2: Direction du serpent de l'ordinateur
    :param joueur: Serpent du joueur
    :param x: Coordonnée x de la tête du serpent de l'ordinateur
    :param y: Coordonnée y de la tête du serpent de l'ordinateur
    :param obstacles: Liste des Obstacles
    :return: Direction du serpent de l'ordinateur

    >>> from random import seed
    >>> seed(266)
    >>> ia_aleatoire((-1, 0), [(25, 1), (24, 1) ,(23, 1)], 5, 5, [])
    (0, -1)
    """
    if randint(1, 7) == 1:
        nb_random = randrange(-1, 2, 2)

        if (direction2 == (-1, 0) or direction2 == (1, 0)) and not \
                collision_serpent([(x, y + nb_random)], obstacles, [],
                                  opt_torique, joueur):
            return 0, nb_random

        elif (direction2 == (0, -1) or direction2 == (0, 1)) and not \
                collision_serpent([(x + nb_random, y)], obstacles, [],
                                  opt_torique, joueur):
            return nb_random, 0
    return direction2


def ia_obstacles(direction2, joueur, ordinateur, obstacles):
    """
    Permet à l'ordinateur d'éviter un obstacle en face de lui

    :param direction2: Direction du serpent de l'ordinateur
    :param joueur: Serpent du joueur
    :param ordinateur: Serpent de l'ordinateur
    :param obstacles: Liste des Obstacles
    :return: Direction du serpent de l'ordinateur
    """
    cmpt = 0
    possible = False
    while not possible:

        cmpt += 1
        ordi = ordinateur[:]

        x, y = ordi[0]
        x += direction2[0]
        y += direction2[1]
        ordi[0] = (x, y)

        # Detection d'un obstacle devant le serpent
        if collision_serpent(ordi, obstacles, [], opt_torique, joueur):
            if direction2 == (-1, 0):
                direction2 = (0, randrange(-1, 2, 2))
            elif direction2 == (1, 0):
                direction2 = (0, randrange(-1, 2, 2))
            elif direction2 == (0, -1):
                direction2 = (randrange(-1, 2, 2), 0)
            elif direction2 == (0, 1):
                direction2 = (randrange(-1, 2, 2), 0)

        # Evalue la présence d'obtacles vers la nouvelle direction
        for i in range(5):
            x, y = ordi[0]
            x += direction2[0]
            y += direction2[1]
            ordi[0] = (x, y)

            if collision_serpent(ordi, obstacles, [], opt_torique, joueur) and\
                    cmpt < 10:
                possible = False
                if randint(0, i) == 0:
                    break
            else:
                possible = True

    return direction2


###############################################################################
#                                Sauvegarde                                   #
###############################################################################


# - - - - - - - Sauvegarde - - - - - - - #


def sauvegarde(meilleur_score, niveau, xp):
    """
    Sauvegarde dans un fichier txt le meilleur score, le niveau et l'expérience

    :param meilleur_score: Meilleur score du joueur
    :param niveau: Niveau du joueur
    :param xp: Expérience du joueur
    """
    with open("save.txt", "w") as save:
        save.write(f"{meilleur_score} {niveau} {xp}")


def chargement():
    """
    Charge le meilleur score, le niveau et l'expérience depuis fichier txt

    :return: Meilleur score ; Niveau ; Expérience
    """
    try:
        with open("save.txt", "r") as save:  # Charge les données de sauvegarde
            donnees = save.read()
            meilleur_score, niveau, xp = donnees.split()
            meilleur_score = int(meilleur_score)
            niveau, xp = int(niveau), int(xp)
    except ValueError:  # En cas d'erreur de valeur, réinitialise les valeurs
        meilleur_score = 0
        niveau = 1
        xp = 0
        sauvegarde(meilleur_score, niveau, xp)
    return meilleur_score, niveau, xp


# - - - - - - - Reinitialisation Variables - - - - - - - #


def reset_variables():
    """
    Initialise ou réinitialise les variables globales en fin de partie
    """
    global framerate, chrono, progres_chrono, nb_pommes, score, direction, \
        pommes, pommes_attente, serpentEnnemi, obstacles, serpent, obscurite, \
        im_obscu, image_nuit, temps_nuit, cycle_nuit, prog_nuit, ips, \
        nb_kills, serpent2, pommes_att2, direction2
    framerate = 10
    ips = 10
    chrono = 0
    progres_chrono = 0
    nb_pommes = 0
    nb_kills = 0
    score = 0
    direction = (1, 0)
    pommes = []
    pommes_attente = []
    serpentEnnemi = []
    obstacles = []
    serpent = [(5, 3), (4, 3), (3, 3)]
    serpent2 = [(34, 26), (35, 26), (36, 26)]
    pommes_att2 = []
    direction2 = (-1, 0)
    obscurite = case_vers_pixel(serpent[0])
    im_obscu = "image/obscurite/cercleObscuritePetit.png"
    image_nuit = 0
    temps_nuit = 0
    cycle_nuit = "jour"
    prog_nuit = 0


def reset_options():
    """
    Initialise ou réinitialise les options de jeu
    """
    global opt_pommes, opt_acceleration, opt_obstacles, opt_deplacement, \
        opt_obscurite, opt_nuit, opt_torique, opt_paint
    opt_pommes = False
    opt_acceleration = False
    opt_obstacles = False
    opt_deplacement = False
    opt_obscurite = False
    opt_nuit = False
    opt_torique = False
    opt_paint = False


###############################################################################
#                                 Principal                                   #
###############################################################################


if __name__ == "__main__":

    # Chargement de la sauvegarde et initialisation des variables
    meilleur_score, niveau, xp = chargement()
    reset_variables()
    fps = False
    modeTemp = "menu"

    # Création de la fenêtre du jeu
    largeurEcran = taille_case * largeur_plateau
    hauteurEcran = taille_case * hauteur_plateau
    fltk.cree_fenetre(largeurEcran + 426, hauteurEcran)

    # Initialisation des options du jeu
    reset_options()
    coordonneesDessinSerpents = None
    gain = 0

    # Boucle principale
    choixMode = "menu"
    while choixMode == "menu":

        # Reinitialisation de la fenêtre
        fltk.efface_tout()

        # Sauvegarde des données
        niveau, xp = level(niveau, xp, score)
        meilleur_score = meilleur(meilleur_score, score)
        sauvegarde(meilleur_score, niveau, xp)

        # Reinitialisation des variables
        reset_variables()

        choixMode = modeTemp

        # Démarrage du menu
        if modeTemp == "menu":
            choixMode, niveau, xp, fps, nb_titre = menu(niveau, xp, fps)

        # Choix du fond
        fond = choixFond(niveau)

        # - - - - - - - Mode de Jeu : Classique - - - - - - - #

        while choixMode == "jouer":
            temps_debut = time()

            affichage()

            # Détection d'un événement avec fltk
            ev = fltk.donne_ev()
            ty = fltk.type_ev(ev)
            choixMode, direction = detection_evenement(ev, ty, choixMode,
                                                       direction,
                                                       opt_deplacement)

            # Création des objets (serpent, pommes, obstacles)
            pommes = creation_pommes(pommes, serpent, opt_pommes, obstacles, 1)
            serpent, obscurite = deplacement_serpent(serpent, direction,
                                                     opt_obscurite, obscurite)

            obstacles = creation_obstacles(obstacles, serpent, pommes,
                                           opt_obstacles)

            # Détection de la défaite du joueur
            choixMode, modeTemp, gain = fin_jeu(serpent, choixMode, obstacles,
                                                serpentEnnemi, opt_torique)

            # Détection de la collision entre la tête du serpent et les pommes
            pommes_attente, nb_pommes, score, im_obscu = collision_pommes(
                pommes, serpent, nb_pommes, pommes_attente, score, im_obscu)

            # Gestion de la taille du serpent
            serpent, pommes_attente, im_obscu = grandir_serpent(serpent,
                                                                pommes_attente,
                                                                im_obscu)

            temps_nuit, image_nuit, cycle_nuit, prog_nuit = cycle_jn(
                temps_nuit, image_nuit, cycle_nuit, prog_nuit, opt_nuit)

            # Chronométrage de la partie en secondes
            chrono, progres_chrono, score, temps_nuit, prog_nuit = temps(
                chrono, progres_chrono, framerate, score, temps_nuit,
                prog_nuit, opt_nuit)

            gestion_framerate()

        # - - - - - - - Mode de Jeu : Deux Joueurs - - - - - - - #

        while choixMode == "deuxJoueur":
            temps_debut = time()

            affichage()

            # Détection d'un événement avec fltk
            ev = fltk.donne_ev()
            ty = fltk.type_ev(ev)
            choixMode, direction = detection_evenement(ev, ty, choixMode,
                                                       direction,
                                                       opt_deplacement,
                                                       joueur="j1")
            choixMode, direction2 = detection_evenement(ev, ty, choixMode,
                                                        direction2,
                                                        opt_deplacement,
                                                        joueur="j2")

            # Création des objets (serpent, pommes, obstacles)
            pommes = creation_pommes(pommes, serpent, opt_pommes, obstacles, 2,
                                     serpent2)

            serpent = deplacement_serpent(serpent, direction)[0]
            serpent2 = deplacement_serpent(serpent2, direction2)[0]

            obstacles = creation_obstacles(obstacles, serpent, pommes,
                                           opt_obstacles, serpent2)

            # Détection de la défaite du joueur
            choixMode, modeTemp, gain = fin_jeu(serpent, choixMode,  obstacles,
                                                serpentEnnemi, opt_torique,
                                                serpent2, 1)

            if choixMode != "finJeu":
                choixMode, modeTemp, gain = fin_jeu(serpent2, choixMode,
                                                    obstacles, serpentEnnemi,
                                                    opt_torique, serpent, 2)

            # Détection de la collision entre la tête du serpent et les pommes
            pommes_attente, nb_pommes, score, im_obscu = collision_pommes(
                pommes, serpent, nb_pommes, pommes_attente, score, im_obscu)

            pommes_att2, nb_pommes, score, im_obscu = collision_pommes(
                pommes, serpent2, nb_pommes, pommes_att2, score, im_obscu)

            # Gestion de la taille du serpent
            serpent, pommes_attente, im_obscu = grandir_serpent(serpent,
                                                                pommes_attente,
                                                                im_obscu)

            serpent2, pommes_att2, im_obscu = grandir_serpent(serpent2,
                                                              pommes_att2,
                                                              im_obscu)

            temps_nuit, image_nuit, cycle_nuit, prog_nuit = cycle_jn(
                temps_nuit, image_nuit, cycle_nuit, prog_nuit, opt_nuit)

            # Chronométrage de la partie en secondes
            chrono, progres_chrono, score, temps_nuit, prog_nuit = temps(
                chrono, progres_chrono, framerate, score, temps_nuit,
                prog_nuit, opt_nuit)

            gestion_framerate()

        # - - - - - - - Mode de Jeu : Duel Contre l'Ordinateur - - - - - - - #

        while choixMode == "duel":

            temps_debut = time()

            affichage()

            # Détection d'un événement avec fltk
            ev = fltk.donne_ev()
            ty = fltk.type_ev(ev)
            choixMode, direction = detection_evenement(ev, ty, choixMode,
                                                       direction,
                                                       opt_deplacement,
                                                       joueur="j1")
            direction2 = ia(direction2, serpent, serpent2, pommes, obstacles)

            # Création des objets (serpent, pommes, obstacles)
            pommes = creation_pommes(pommes, serpent, opt_pommes, obstacles, 2,
                                     serpent2)

            serpent = deplacement_serpent(serpent, direction)[0]
            serpent2 = deplacement_serpent(serpent2, direction2)[0]

            obstacles = creation_obstacles(obstacles, serpent, pommes,
                                           opt_obstacles, serpent2)

            # Détection de la défaite du joueur
            choixMode, modeTemp, gain = fin_jeu(serpent, choixMode, obstacles,
                                                serpentEnnemi, opt_torique,
                                                serpent2, 1)

            if choixMode != "finJeu":
                choixMode, modeTemp, gain = fin_jeu(serpent2, choixMode,
                                                    obstacles, serpentEnnemi,
                                                    opt_torique, serpent, 2)

            # Détection de la collision entre la tête du serpent et les pommes
            pommes_attente, nb_pommes, score, im_obscu = collision_pommes(
                pommes, serpent, nb_pommes, pommes_attente, score, im_obscu)

            pommes_att2, nb_pommes, score, im_obscu = collision_pommes(
                pommes, serpent2, nb_pommes, pommes_att2, score, im_obscu)

            # Gestion de la taille du serpent
            serpent, pommes_attente, im_obscu = grandir_serpent(serpent,
                                                                pommes_attente,
                                                                im_obscu)

            serpent2, pommes_att2, im_obscu = grandir_serpent(serpent2,
                                                              pommes_att2,
                                                              im_obscu)

            temps_nuit, image_nuit, cycle_nuit, prog_nuit = cycle_jn(
                temps_nuit, image_nuit, cycle_nuit, prog_nuit, opt_nuit)

            # Chronométrage de la partie en secondes
            chrono, progres_chrono, score, temps_nuit, prog_nuit = temps(
                chrono, progres_chrono, framerate, score, temps_nuit,
                prog_nuit, opt_nuit)

            gestion_framerate()

        # - - - - - - - Mode de Jeu : Contre l'Ordinateur - - - - - - - #

        while choixMode == "contreOrdinateur":
            temps_debut = time()

            affichage()

            ev = fltk.donne_ev()
            ty = fltk.type_ev(ev)

            choixMode, direction = detection_evenement(ev, ty, choixMode,
                                                       direction,
                                                       opt_deplacement)

            pommes = creation_pommes(pommes, serpent, opt_pommes, obstacles, 1)
            serpent, obscurite = deplacement_serpent(serpent, direction,
                                                     opt_obscurite, obscurite)
            obstacles = creation_obstacles(obstacles, serpent, pommes,
                                           opt_obstacles)

            # Création des serpents ennemis
            serpentEnnemi = creation_ennemi(serpentEnnemi)

            # Gèrent les événement des serpents ennemis
            # (déplacement, collisions avec les murs et le joueur)
            serpentEnnemi, score, nb_kills = evenements_ennemis(serpent,
                                                                serpentEnnemi,
                                                                score,
                                                                pommes_attente,
                                                                nb_kills)

            choixMode, modeTemp, gain = fin_jeu(serpent, choixMode, obstacles,
                                                serpentEnnemi, opt_torique)

            pommes_attente, nb_pommes, score, im_obscu = collision_pommes(
                pommes, serpent, nb_pommes, pommes_attente, score, im_obscu)

            serpent, pommes_attente, im_obscu = grandir_serpent(serpent,
                                                                pommes_attente,
                                                                im_obscu)

            temps_nuit, image_nuit, cycle_nuit, prog_nuit = cycle_jn(
                temps_nuit, image_nuit, cycle_nuit, prog_nuit, opt_nuit)

            chrono, progres_chrono, score, temps_nuit, prog_nuit = temps(
                chrono, progres_chrono, framerate, score, temps_nuit,
                prog_nuit, opt_nuit)

            gestion_framerate()

        # - - - - - - - Menu des Options - - - - - - - #

        choixMode = menu_options(choixMode)

        # - - - - - - -Tableau des Scores - - - - - - - #

        choixMode, modeTemp = tableau_score(choixMode, modeTemp, gain)

    fltk.ferme_fenetre()
