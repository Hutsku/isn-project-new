import pygame
from pygame.locals import *

import classe
import niveau

pygame.init()
pygame.key.set_repeat(1) # Autorise la repetition d'event KEYDOWN si la touche est maintenue
fenetre = pygame.display.set_mode((500, 500)) # creation de la fenetre (avec taille en parametre)

spawn = (50, 50)

fond = pygame.Surface((500, 500)) # Création du fond, de taille equivalente à la fenêtre
fond.fill((100, 100, 100)) # on colorie en gris

environnement = niveau.Niveau((50, 50), (400, 400))
perso = classe.Personnage(environnement.spawn, (50, 50))

boucle = True
while boucle:
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

	fenetre.blit(fond, (0, 0)) # on colle le fond
	classe.update()
	pygame.display.flip() # met à jour la fenetre
