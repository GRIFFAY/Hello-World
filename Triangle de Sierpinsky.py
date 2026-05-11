# Programme Triangle de Sierpinsky

import tkinter as tk
import random
import math

# =========================================================
# DEMANDE DU NOMBRE DE SOMMETS
# =========================================================

while True:
    try:
        nb_sommets = int(input("Nombre de sommets du polygone régulier : "))

        if nb_sommets >= 3:
            break
        else:
            print("Le polygone doit avoir au moins 3 sommets.")

    except ValueError:
        print("Veuillez entrer un entier valide.")

# =========================================================
# PARAMÈTRES
# =========================================================

LARGEUR = 1000
HAUTEUR = 1000

FOND = "black"
VERT_CLAIR = "#90EE90"

HAUTEUR_POLYGONE = 800

ZOOM_FACTEUR = 1.1

# Couleurs du dégradé
# Centre = jaune vif
# Bord = bleu ciel

COULEUR_CENTRE = (255, 255, 0)
COULEUR_BORD = (150, 150, 255)

# =========================================================
# FENÊTRE
# =========================================================

fenetre = tk.Tk()
fenetre.title("Polygone régulier fractal")

canvas = tk.Canvas(
    fenetre,
    width=LARGEUR,
    height=HAUTEUR,
    bg=FOND,
    highlightthickness=0
)

canvas.pack(fill="both", expand=True)

# =========================================================
# CALCUL DES SOMMETS
# =========================================================

centre_x = LARGEUR / 2
centre_y = HAUTEUR / 2

rayon = HAUTEUR_POLYGONE / 2

sommets = []

# Rotation initiale
angle_depart = -math.pi / 2

# Ajustement pour avoir une base horizontale
if nb_sommets % 2 == 0:
    angle_depart += math.pi / nb_sommets

for i in range(nb_sommets):

    angle = angle_depart + (2 * math.pi * i / nb_sommets)

    x = centre_x + rayon * math.cos(angle)
    y = centre_y + rayon * math.sin(angle)

    sommets.append((x, y))

# =========================================================
# DESSIN DU POLYGONE
# =========================================================

def dessiner_polygone():

    coords = []

    for x, y in sommets:
        coords.extend([x, y])

    canvas.create_polygon(
        coords,
        outline=VERT_CLAIR,
        fill="",
        width=1,
        tags="polygone"
    )

dessiner_polygone()

# =========================================================
# TEST SI POINT DANS POLYGONE
# =========================================================

def point_dans_polygone(x, y, poly):

    dedans = False

    j = len(poly) - 1

    for i in range(len(poly)):

        xi, yi = poly[i]
        xj, yj = poly[j]

        intersecte = (
            ((yi > y) != (yj > y))
            and
            (
                x <
                (xj - xi) * (y - yi) / (yj - yi + 1e-12)
                + xi
            )
        )

        if intersecte:
            dedans = not dedans

        j = i

    return dedans

# =========================================================
# CALCUL DU DÉGRADÉ
# =========================================================

def couleur_degrade(x, y):

    dx = x - centre_x
    dy = y - centre_y

    distance = math.sqrt(dx * dx + dy * dy)

    # Normalisation entre 0 et 1
    t = min(distance / rayon, 1.0)

    r = int(
        COULEUR_CENTRE[0] * (1 - t)
        + COULEUR_BORD[0] * t
    )

    g = int(
        COULEUR_CENTRE[1] * (1 - t)
        + COULEUR_BORD[1] * t
    )

    b = int(
        COULEUR_CENTRE[2] * (1 - t)
        + COULEUR_BORD[2] * t
    )

    return f"#{r:02x}{g:02x}{b:02x}"

# =========================================================
# DESSIN D'UN PIXEL
# =========================================================

def dessiner_pixel(x, y, couleur):

    canvas.create_line(
        x,
        y,
        x + 1,
        y,
        fill=couleur,
        tags="point"
    )

# =========================================================
# GESTION DU CLIC SOURIS
# =========================================================

def clic_souris(event):

    x = event.x
    y = event.y

    # Vérifie si le clic est dans le polygone
    if point_dans_polygone(x, y, sommets):

        courant = (x, y)

        # Point initial
        dessiner_pixel(x, y, VERT_CLAIR)

        # Répétition 5000 fois
        for _ in range(5000):

            sommet = random.choice(sommets)

            # Milieu entre le point courant et un sommet
           # nx = (courant[0] + sommet[0]) / 2
           # ny = (courant[1] + sommet[1]) / 2
            nx = courant[0] + (sommet[0]-courant[0])/2
            ny = courant[1] + (sommet[1]-courant[1])/2
            

            # Couleur du dégradé
            couleur = couleur_degrade(nx, ny)

            # Affichage
            dessiner_pixel(nx, ny, couleur)

            # Mise à jour du point courant
            courant = (nx, ny)

        canvas.update()

# =========================================================
# ZOOM À LA MOLETTE
# =========================================================

def appliquer_zoom(facteur, zx, zy):

    global sommets
    global centre_x, centre_y
    global rayon

    # Zoom graphique
    canvas.scale(
        "all",
        zx,
        zy,
        facteur,
        facteur
    )

    # Mise à jour des coordonnées
    nouveaux_sommets = []

    for x, y in sommets:

        nx = zx + (x - zx) * facteur
        ny = zy + (y - zy) * facteur

        nouveaux_sommets.append((nx, ny))

    sommets = nouveaux_sommets

    # Mise à jour du centre
    centre_x = zx + (centre_x - zx) * facteur
    centre_y = zy + (centre_y - zy) * facteur

    # Mise à jour du rayon
    rayon *= facteur

# ---------------------------------------------------------
# WINDOWS / MAC
# ---------------------------------------------------------

def molette(event):

    if event.delta > 0:
        appliquer_zoom(
            ZOOM_FACTEUR,
            event.x,
            event.y
        )

    else:
        appliquer_zoom(
            1 / ZOOM_FACTEUR,
            event.x,
            event.y
        )

# ---------------------------------------------------------
# LINUX
# ---------------------------------------------------------

def molette_haut(event):
    appliquer_zoom(
        ZOOM_FACTEUR,
        event.x,
        event.y
    )

def molette_bas(event):
    appliquer_zoom(
        1 / ZOOM_FACTEUR,
        event.x,
        event.y
    )

# =========================================================
# ASSOCIATION DES ÉVÉNEMENTS
# =========================================================

canvas.bind("<Button-1>", clic_souris)

canvas.bind("<MouseWheel>", molette)

canvas.bind("<Button-4>", molette_haut)
canvas.bind("<Button-5>", molette_bas)

# =========================================================
# BOUCLE PRINCIPALE
# =========================================================

fenetre.mainloop()