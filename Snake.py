###############################################################################
#                              Pré-Projet : Snake                             #
#                         Jeu Snake aux Noms Multiples                        #
#                                    v1.0                                     #
#                     Valentin Bernier - Alain Coserariu                      #
###############################################################################


import fltk
from time import sleep, time
from random import randint

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
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affichage():
    """
    Affiche tous les éléments du jeu à l'écran

    :return: void
    """
    global pommes, serpent, serpentEnnemi, opt_obstacles, obstacles, score,\
        choixMode, obscurite, opt_obscurite, im_obscu, opt_nuit, image_nuit,\
        largeurEcran, hauteurEcran, chrono, nb_pommes, nb_kills,\
        meilleur_score, fps, nb_titre, serpent2

    fltk.efface_tout()

    afficheFond(fond)

    affiche_pommes(pommes)
    affiche_serpent(serpent, "joueur")

    if choixMode == "deuxJoueur":
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
    return randint(1, min(6, niveau))


###############################################################################
#                                Serpent                                      #
###############################################################################


# - - - - - - - Affichage - - - - - - - #


def affiche_serpent(serpent, couleur):
    """
    Appelle les fonction qui affichent le serpent

    :param couleur:
    :param serpent: Liste des coordonnées de chaque parties du serpent
    :return: void
    """
    afficher_tete_serpent(serpent, couleur)
    afficher_corps_serpent(serpent, couleur)
    afficher_queu_serpent(serpent, couleur)


def afficher_tete_serpent(serpent, color):
    """
    Affiche la tête du serpent

    :param couleur:
    :param serpent: Liste des coordonnées de chaque parties du serpent
    :return: void
    """
    x, y = case_vers_pixel(serpent[0])
    # Coordonnées du second élément du serpent :
    xApres, yApres = case_vers_pixel(serpent[1])

    if xApres + taille_case == x or xApres - largeurEcran + taille_case == x:
        fltk.image(x, y, f'image/serpent/serpentTete_{color}.png')
    elif xApres - taille_case == x or xApres + largeurEcran - taille_case == x:
        fltk.image(x, y, f'image/serpent/serpentTeteGauche_{color}.png')
    elif yApres + taille_case == y or yApres - hauteurEcran + taille_case == y:
        fltk.image(x, y, f'image/serpent/serpentTeteBas_{color}.png')
    elif yApres - taille_case == y or yApres + hauteurEcran - taille_case == y:
        fltk.image(x, y, f'image/serpent/serpentTeteHaut_{color}.png')


def afficher_corps_serpent(serpent, color):
    """
    Affiche le corps du serpent

    :param couleur:
    :param serpent: Liste des coordonnées de chaque parties du serpent
    :return: void
    """
    for i in range(1, len(serpent) - 1):
        # Compare la position de chaque élément du corps du serpent avec la
        # position du précédent et du suivant afin de trouver l'orientation de
        # l'image a afficher
        x, y = case_vers_pixel(serpent[i])
        xAvant, yAvant = case_vers_pixel(serpent[i - 1])
        xApres, yApres = case_vers_pixel(serpent[i + 1])

        if yAvant == y == yApres:
            fltk.image(x, y, f'image/serpent/serpentCorp_{color}.png',)
        elif xAvant == x == xApres:
            fltk.image(x, y, f'image/serpent/serpentCorpVertical_{color}.png')

        elif (xApres - taille_case == x or
              xApres + largeurEcran - taille_case == x) and\
                (yAvant - taille_case == y or
                 yAvant + hauteurEcran - taille_case == y) or\
                (yApres - taille_case == y or
                 yApres + hauteurEcran - taille_case == y) and\
                (xAvant - taille_case == x or
                 xAvant + largeurEcran - taille_case == x):
            fltk.image(x, y, f'image/serpent/serpentCorp4_{color}.png')

        elif (xApres + taille_case == x or
              xApres - largeurEcran + taille_case == x) and\
                (yAvant - taille_case == y or
                 yAvant + hauteurEcran - taille_case == y) or\
                (yApres - taille_case == y or
                 yApres + hauteurEcran - taille_case == y) and\
                (xAvant + taille_case == x or
                 xAvant - largeurEcran + taille_case == x):
            fltk.image(x, y, f'image/serpent/serpentCorp3_{color}.png')

        elif (xApres - taille_case == x or
              xApres + largeurEcran - taille_case == x) and\
                (yAvant + taille_case == y or
                 yAvant - hauteurEcran + taille_case == y) or\
                (xAvant - taille_case == x or
                 xAvant + largeurEcran - taille_case == x) and\
                (yApres + taille_case == y or
                 yApres - hauteurEcran + taille_case == y):
            fltk.image(x, y, f'image/serpent/serpentCorp1_{color}.png')

        elif (xApres + taille_case == x or
              xApres - largeurEcran + taille_case == x) and\
                (yAvant + taille_case == y or
                 yAvant - hauteurEcran + taille_case == y) or\
                (xAvant + taille_case == x or
                 xAvant - largeurEcran + taille_case == x) and\
                (yApres + taille_case == y or
                 yApres - hauteurEcran + taille_case == y):
            fltk.image(x, y, f'image/serpent/serpentCorp2_{color}.png')


def afficher_queu_serpent(serpent, color):
    """
    Affiche la queue du serpent

    :param couleur:
    :param serpent: Liste des coordonnées de chaque parties du serpent
    :return: void
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
    :return: Couple de la direction
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
    :return: Couple de la direction
    """
    if (direction == (0, -1) and touche == gauche) or\
            (direction == (0, 1) and touche == droite):
        return -1, 0
    elif (direction == (-1, 0) and touche == gauche) or\
            (direction == (1, 0) and touche == droite):
        return 0, 1
    elif (direction == (0, 1) and touche == gauche) or\
            (direction == (0, -1) and touche == droite):
        return 1, 0
    elif (direction == (1, 0) and touche == gauche) or\
            (direction == (-1, 0) and touche == droite):
        return 0, -1
    else:
        return direction


def deplacement_direction(direction, touche, haut, bas, gauche, droite):
    """
    Changement de direction en fonction de la touche pressée (4 touches)

    :param direction: Couple de la direction du serpent
    :param touche: Touche pressée
    :return: Couple de la direction
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

    :param opt_obscurite:
    :param obscurite:
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param direction: Couple de la direction du serpent
    :return: Nouvelles coordonnées du serpent
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


def collision_serpent(serpent, larg, haut, obstacles, ennemiSerpent,
                      opt_torique, serpent2):
    """
    Verifie les collision du serpent avec des éléments qui provoquent sa mort

    :param opt_torique:
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param larg: Largeur de la zone de jeu
    :param haut: Hauteur de la zone de jeu
    :param obstacles: Liste des couples de coordonées des obstacles
    :param ennemiSerpent: Liste qui contient des serpents (voir plus haut)
    :return: Booleen, True si il y a collision
    """
    # Bords de la zone
    if bord_zone(serpent, larg, haut, opt_torique):
        return True

    # Obstacles (arbres)
    if serpent[0] in obstacles:
        return True

    # Lui même
    if serpent[0] in serpent[1:]:  # De l'élément 1 à la fin de la liste
        return True

    if serpent[0] in serpent2:
        return True

    # Autres serpents
    for j in ennemiSerpent:
        if serpent[0] in j:
            return True

    return False


def bord_zone(serpent, larg, haut, opt_torique):
    if (serpent[0][0] < 0 or serpent[0][0] > larg - 1 or serpent[0][1] < 0 or
        serpent[0][1] > haut - 1)\
            and not opt_torique:
        return True
    else:
        if serpent[0][0] < 0:
            serpent[0] = (larg - 1, serpent[0][1])
        elif serpent[0][0] > larg - 1:
            serpent[0] = (0, serpent[0][1])
        elif serpent[0][1] < 0:
            serpent[0] = (serpent[0][0], haut - 1)
        elif serpent[0][1] > haut - 1:
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
    :return: Mode de jeu, Direction du serpent
    """
    if ty == 'Quitte':
        choixMode = 'menu'
    elif ty == 'Touche':
        direction = change_direction(direction, fltk.touche(ev),
                                     opt_deplacement, joueur)
    return choixMode, direction


###############################################################################
#                            Gestion des pommes                               #
###############################################################################


# - - - - - - - Affichage - - - - - - - #


def affiche_pommes(pommes):
    """
    Affiche les pommes

    :param pommes: Liste des couples de coordonées des pommes
    :return: void
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        fltk.image(x, y, 'image/divers/pomme.png')


# - - - - - - - Création - - - - - - - #


def creation_pommes(pommes, serpent, opt_pommes, obstacles, serpent2=[]):
    """
    Appelle les fonctions de génération de pommes en fonction de l'option
    de génération choisie

    :param pommes: Liste des couples de coordonées des pommes
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param opt_pommes: Booléen de l'option de génération de pommes
    :param obstacles: Liste des couples de coordonées des obstacles
    :return: Liste des couples de coordonées des pommes
    """
    if opt_pommes:
        pommes = pommes_multi(pommes, serpent, obstacles, serpent2)
    else:
        pommes = pommes_unique(pommes, serpent, obstacles, serpent2)
    return pommes


def pommes_multi(pommes, serpent, obstacles, serpent2):
    """
    Génère des pommes à des moments et des endroits aléatoires

    :param pommes: Liste des couples de coordonées des pommes
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param obstacles: Liste des couples de coordonées des obstacles
    :return: Liste des couples de coordonées des pommes
    """
    # Les valeurs pour l'aléatoire sont définies afin que plus il y a de pommes
    # présentes, plus il est rare qu'une nouvelle se génère
    if randint(0, 20 + 5 * len(pommes)) == 0:
        pommeX = randint(1, largeur_plateau - 1)
        pommeY = randint(1, hauteur_plateau - 1)
        # Pour empêcher la génération d'un objet dans un autre :
        if (pommeX, pommeY) not in serpent and (pommeX, pommeY) not in pommes\
                and (pommeX, pommeY) not in obstacles and (pommeX, pommeY)\
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
    :return: Liste des couples de coordonées des pommes
    """
    if len(pommes) == 0:
        pommeX = randint(1, largeur_plateau - 1)
        pommeY = randint(1, hauteur_plateau - 1)
        while (pommeX, pommeY) in serpent or (pommeX, pommeY) in obstacles or\
                (pommeX, pommeY) in serpent2:
            pommeX = randint(1, largeur_plateau - 1)
            pommeY = randint(1, hauteur_plateau - 1)
        pommes.append((pommeX, pommeY))
    return pommes


# - - - - - - - Collisions - - - - - - - #


def collision_pommes(pommes, serpent, nb_pommes, pommes_attente,  score=None,
                     im_obscu=None):
    """
    Detecte la collision entre la tête du serpent et une pomme

    :param im_obscu:
    :param pommes_attente:
    :param pommes: Liste des couples de coordonées des pommes
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param nb_pommes: Nombre de pommes mangées
    :pommes_attente: Liste des coordonnées des pommes mangées
    :param score: Score du joueur (défaut : None)
    :return: Couple contenant les coordonnées de la pomme mangée et la longeur
        du serpent ; Nombre de pommes ; Score du joueur
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

    :param image_obscurite:
    :param pommes_attente:
    :param serpent: Liste des couples de coordonées du corps du serpent
    :pommes_attente: Liste des coordonnées des pommes mangées
    :return: serpent ; pommes_attente
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
    :return: void
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


def creation_obstacles(obstacles, serpent, pommes, opt_obstacles, serpent2=[]):
    """
    Appelle les fonctions de génération d'obstacles si l'option obstacle
    a été choisie

    :param opt_obstacles:
    :param obstacles: Liste des couples de coordonées des obstacles
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param pommes: Liste des couples de coordonées des pommes
    :return: Liste des couples de coordonées des obstacles
    """
    if opt_obstacles:
        x = randint(0, 30 + 2 * len(obstacles))
        if x == 0:
            obstacleX = randint(1, largeur_plateau - 1)
            obstacleY = randint(1, hauteur_plateau - 1)
            if (obstacleX, obstacleY) not in serpent and\
                    (obstacleX, obstacleY) not in obstacles and\
                    (obstacleX, obstacleY) not in pommes and\
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

    :param pommes_attente:
    :param serpent: Liste des couples de coordonnées du serpent
    :param serpentEnnemi: Liste des serpents ennemis
        (serpents = listes de couples de coordonnées)
    :param score: Score du joueur
    :pommes_attente: Liste des coordonnées des pommes mangées
    :return: Liste des serpents ennemis ; Score du joueur
    """
    for serpents in serpentEnnemi:

        # Déplacement des serpents
        if serpents[0][0] > serpents[1][0]:
            serpents, p = deplacement_serpent(serpents, (1, 0), taille_case)
        elif serpents[0][0] < serpents[1][0]:
            serpents, p = deplacement_serpent(serpents, (-1, 0), taille_case)
        elif serpents[0][1] > serpents[1][1]:
            serpents, p = deplacement_serpent(serpents, (0, 1), taille_case)
        elif serpents[0][1] < serpents[1][1]:
            serpents, p = deplacement_serpent(serpents, (0, -1), taille_case)

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

    :return: void
    """
    global framerate, score, opt_acceleration, temps_debut, temps_fin,\
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

    :param score: Score du joueur
    :return: Framerate
    """
    return 10 + chrono // 250


def temps(chrono, progression, ips, score, temps_nuit, prog_nuit,
          opt_nuit):
    """
    Compte les secondes depuis le début de la partie
    (mise à jour du chrono et du score)

    :param prog_nuit:
    :param temps_nuit:
    :param opt_nuit:
    :param chrono: Temps de la partie (en secondes)
    :param progression: Nombre de frames depuis la dernière seconde passée
    :param framerate: Framerate du jeu
    :param score: Score du joueur
    :return: chrono ; progression ; score
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
    """
    if score > meilleur_score:
        return score
    return meilleur_score


###############################################################################
#                             Gestion du menu                                 #
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
    """
    if typeEvenement == "ClicGauche" \
            and rectangleAX < fltk.abscisse(evenement) < rectangleBX \
            and rectangleAY < fltk.ordonnee(evenement) < rectangleBY:
        return True
    return False


def bouton(niveau):
    global boutonPommes, boutonObstacles, boutonAcceleration, bouton2Joueurs,\
        boutonDeplacement, boutonTorique, boutonNuit, boutonContreOrdi,\
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


def fin_jeu(serpent, larg, haut, choixMode, obstacles, ennemiSerpent,
            opt_torique, serpent2=[], id_serpent=1):
    """
    Déclenche la fin de la partie quand le joueur perd

    :param opt_torique:
    :param serpent: Liste des couples de coordonées du corps du serpent
    :param larg: Largeur de la zone de jeu
    :param haut: Hauteur de la zone de jeu
    :param choixMode: Mode de jeu selectionné
    :param obstacles: Liste des couples de coordonées des obstacles
    :param ennemiSerpent: Liste qui contient des serpents (voir plus haut)
    :return: Mode de jeu, Tableau des score en cas de défaite sinon mode actuel
    """
    if collision_serpent(serpent, larg, haut, obstacles, ennemiSerpent,
                         opt_torique, serpent2):
        if id_serpent == 1:
            print("vert mort")
        elif id_serpent == 2:
            print("rouge mort")
        return "finJeu", choixMode
    return choixMode, choixMode  # Le jeu continue


# - - - - - - - Menu Principal - - - - - - - #


def menu(niveau, xp, fps):
    """
    Gère le menu principal du jeu

    :param niveau: Niveau du joueur
    :param xp: Expérience du joueur
    :return: Mode de jeu choisi ; Niveau ; Expérience
    """

    # Affichages des éléments qui n'ont pas besoin d'être actualisés

    fltk.image(0, 0, "image/menu/fond.png", ancrage="nw")

    # Titre
    nb_titre = titre_aleatoire()
    fltk.image((largeurEcran + 426) // 2, hauteurEcran // 4,
               f"image/menu/nom{nb_titre}.png")

    fltk.image(largeurEcran + 421, 5, "image/menu/meilleurScore.png",
               ancrage="ne")
    fltk.texte(largeurEcran + 392, 10, "{:0>6d}".format(meilleur_score),
               taille=45, ancrage="ne")

    fltk.image((largeurEcran + 426) // 2, 475,
               "image/menu/boutonJouer.png")

    fltk.image((largeurEcran + 426) // 2 - 275, 775,
               "image/menu/boutonOptions.png")

    fltk.image((largeurEcran + 426) // 2 + 275, 775,
               "image/menu/boutonQuitter.png")

    while True:

        fltk.efface("reset")

        # Barre d'expérience
        fltk.image(5, 5, "image/menu/barreXP.png", ancrage="nw", tag="reset")
        fltk.image(5, 49, "image/menu/niveau.png", ancrage="nw", tag="reset")
        fltk.rectangle(12, 12, 12 + xp * 400 // (niveau ** 2 * 1000), 42,
                       couleur="red", remplissage="red", tag="reset")

        fltk.texte(145, 45, str(niveau), taille=31, tag="reset")
        fltk.texte(207, 27, f"{xp}/{niveau ** 2 * 1000}", taille=20,
                   ancrage="center", tag="reset")

        if fps:
            fltk.texte(1696, 80, f"{ips} FPS", ancrage="ne", taille=15,
                       tag="reset")

        bouton(niveau)

        fltk.image((largeurEcran + 426) // 2 - 275, 625,
                   f"image/menu/bouton2Joueurs{bouton2Joueurs}.png",
                   tag="reset")

        fltk.image((largeurEcran + 426) // 2 + 275, 625,
                   f"image/menu/boutonContreOrdi{boutonContreOrdi}.png",
                   tag="reset")

        fltk.mise_a_jour()

        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)

        if dansRectangle(evenement, type_evenement, 353, 425, 1353, 525):
            return 'jouer', niveau, xp, fps, titre_aleatoire()

        elif niveau >= 5 and dansRectangle(evenement, type_evenement, 353, 575,
                                           803, 675):
            return "deuxJoueur", niveau, xp, fps, titre_aleatoire()

        elif niveau >= 10 and dansRectangle(evenement, type_evenement, 903,
                                            575, 1353, 675):
            return 'contreOrdinateur', niveau, xp, fps, titre_aleatoire()

        elif dansRectangle(evenement, type_evenement, 353, 725, 803, 825):
            return 'option', niveau, xp, fps, titre_aleatoire()

        elif dansRectangle(evenement, type_evenement, 903, 725, 1353, 825):
            return "quitte", niveau, xp, fps, titre_aleatoire()

        # Mode développeur pour modifier le niveau du joueur
        elif type_evenement == "Touche":
            niveau, xp = mode_developpeur(evenement, niveau, xp)
            if fltk.touche(evenement) == "i":
                fps = not fps


def mode_developpeur(evenement, niveau, xp):
    if fltk.touche(evenement) == "equal":
        xp = 0
        niveau += 1
    elif fltk.touche(evenement) == "parenright" and niveau != 1:
        xp = 0
        niveau -= 1
    return niveau, xp


# - - - - - - - Menu Options - - - - - - - #


def menu_options():

    global opt_pommes, opt_obstacles, opt_acceleration, opt_deplacement,\
        opt_torique, opt_obscurite,  opt_nuit, opt_paint

    while True:

        # Affichage
        fltk.efface_tout()

        bouton(niveau)

        fltk.image(0, 0, "image/menu/fond.png", ancrage="nw")

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


def detection_boutons_options():
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

    if dansRectangle(evenement, type_evenement, 353, 725, 1353, 825):
        return "menu"

    return choixMode


def tableau_score(modeTemp):
    fltk.efface_tout()
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

    while True:

        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)

        if dansRectangle(evenement, type_evenement, 453, 750, 803, 850):
            return "menu", modeTemp

        if dansRectangle(evenement, type_evenement, 903, 750, 1253, 850):
            return "menu", "menu"



###############################################################################
#                                Gestion des fonds                            #
###############################################################################


def afficheFond(fond):
    """
    Affiche le fond du jeu

    :param fond: String contenant le type de fond à utiliser
    :return:
    """
    fltk.image(largeurEcran / 2, hauteurEcran / 2, f"image/fond/{fond}.png")


def choixFond(niveau):
    x = randint(1, min(niveau // 3 + 1, 3))
    if x == 1:
        return "fondHerbe"
    elif x == 2:
        return "fondDesert"
    elif x == 3:
        return "fondGlace"


###############################################################################
#                                Sauvegarde                                   #
###############################################################################


def sauvegarde(meilleur_score, niveau, xp):
    """
    Sauvegarde dans un fichier txt le meilleur score, le niveau et l'expérience

    :param meilleur_score: Meilleur score du joueur
    :param niveau: Niveau du joueur
    :param xp: Expérience du joueur
    :return: void
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


def reset_variables():
    """
    Initialise ou réinitialise les variables globales en fin de partie

    :return: void
    """
    global framerate, chrono, progres_chrono, nb_pommes, score, direction,\
        pommes, pommes_attente, serpentEnnemi, obstacles, serpent, obscurite,\
        im_obscu, image_nuit, temps_nuit, cycle_nuit, prog_nuit, ips,\
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
    opt_pommes = False
    opt_acceleration = False
    opt_obstacles = False
    opt_deplacement = False
    opt_obscurite = False
    opt_nuit = False
    opt_torique = False
    opt_paint = False

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
            pommes = creation_pommes(pommes, serpent, opt_pommes, obstacles)
            serpent, obscurite = deplacement_serpent(serpent, direction,
                                                     opt_obscurite, obscurite)

            obstacles = creation_obstacles(obstacles, serpent, pommes,
                                           opt_obstacles)

            # Détection de la défaite du joueur
            choixMode, modeTemp = fin_jeu(serpent, largeur_plateau,
                                          hauteur_plateau, choixMode,
                                          obstacles, serpentEnnemi,
                                          opt_torique)

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
            pommes = creation_pommes(pommes, serpent, opt_pommes, obstacles,
                                     serpent2)

            serpent, p = deplacement_serpent(serpent, direction,)
            serpent2, p = deplacement_serpent(serpent2, direction2)

            obstacles = creation_obstacles(obstacles, serpent, pommes,
                                           opt_obstacles, serpent2)

            # Détection de la défaite du joueur
            choixMode, modeTemp = fin_jeu(serpent, largeur_plateau,
                                          hauteur_plateau, choixMode,
                                          obstacles, serpentEnnemi,
                                          opt_torique, serpent2, 1)

            choixMode, modeTemp = fin_jeu(serpent2, largeur_plateau,
                                          hauteur_plateau, choixMode,
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

            pommes = creation_pommes(pommes, serpent, opt_pommes, obstacles)
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

            choixMode, modeTemp = fin_jeu(serpent, largeur_plateau,
                                          hauteur_plateau, choixMode,
                                          obstacles, serpentEnnemi,
                                          opt_torique)

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

        while choixMode == "option":
            choixMode = menu_options()

        if choixMode == "finJeu":
            choixMode, modeTemp = tableau_score(modeTemp)

    fltk.ferme_fenetre()
