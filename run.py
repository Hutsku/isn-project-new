import pygame
from pygame.locals import *

import objet
import dongeon

# ========================================= INITIALISATION =======================================

pygame.init()
pygame.key.set_repeat(1) # Autorise la repetition d'event KEYDOWN si la touche est maintenue
fenetre = pygame.display.set_mode((500, 500)) # creation de la fenetre (avec taille en parametre)

fond = pygame.Surface((500, 500)) # Création du fond, de taille equivalente à la fenêtre
fond.fill((100, 100, 100)) # on colorie en gris

environnement = dongeon.Dongeon() # on initialise le dongeon (1 seul possible)
environnement.build() # on génère le 1er niveau 
niveau = environnement.get_level()

perso = objet.Personnage(niveau.spawn, (50, 50)) # on crée le personnage au spawn du niveau
perso.image.fill((255, 0, 0))

# ===================================== BOUCLE PRINCIPALE ========================================

boucle = True
while boucle:
	perso.vx = 0
	perso.vy = 0
	fenetre.blit(fond, (0, 0)) # on colle le fond

	# on gère les evenements claviers et souris
	for event in pygame.event.get():
		if event.type == QUIT:
			boucle = False

		if event.type == KEYDOWN:
			if event.unicode == "d":
				perso.droite()	
			if event.unicode == "q":
				perso.gauche()
			if event.unicode == "z":
				perso.haut()
			if event.unicode == "s":
				perso.bas()

	objet.move() # On actualise la position des objets sur l'écran
	objet.update() # on affiche les sprites à l'écran
	objet.hitbox() # on test les hitbox des sprites entre eux

	pygame.display.flip() # raffraichissement de la fenêtre

# ================================================================================================
