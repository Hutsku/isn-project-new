import pygame
from pygame.locals import *

import objet
import dongeon
import config

# ========================================= INITIALISATION =======================================

taille_ecran = config.getConfig()["taille_ecran"]
taille_personnage = config.getConfig()["taille_personnage"]

pygame.init() #initialisation des modules py.game
pygame.key.set_repeat(1) # Autorise la repetition d'event KEYDOWN si la touche est maintenue
fenetre = pygame.display.set_mode((taille_ecran, taille_ecran)) # creation de la fenetre (avec taille en parametre)

fond = pygame.Surface((taille_ecran, taille_ecran)) # Création du fond, de taille equivalente à la fenêtre
fond.fill((100, 100, 100)) # on colorie en gris

environnement = dongeon.Dongeon() # on initialise le dongeon (1 seul possible)
environnement.build() # on génère le 1er niveau 
spawn = environnement.get_spawn()

perso = objet.Personnage(spawn, (taille_personnage, taille_personnage)) # on crée le personnage au spawn du niveau
perso.image.fill((255, 0, 0)) #attribution de la couleur personnage

# ========================================== FONCTIONS ===========================================

def objetEvent():
	objet.move() # On actualise la position des objets sur l'écran (collision etc)
	objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
	objet.update() # on affiche les sprites à l'écran

def guiEvent():
	pass

def dongeonEvent():
	pass

# ===================================== BOUCLE PRINCIPALE ========================================

boucle = True
while boucle:
	perso.vx = 0 #initialisation de la vitesse axe X personnage a 0
	perso.vy = 0 #initialisation de la vitesse axe Y personnage a 0
	fenetre.blit(fond, (0, 0)) # on colle le fond

	# on gère les evenements claviers et souris 
	for event in pygame.event.get():
		if event.type == QUIT: #si clic sur croix rouge
			boucle = False #fin de boucle

		if event.type == KEYDOWN:
			if event.unicode == "d":
				perso.droite()	
			if event.unicode == "q":
				perso.gauche()
			if event.unicode == "z":
				perso.haut()
			if event.unicode == "s":
				perso.bas()

	objetEvent() # Evenements relatifs aux objets
	guiEvent() # Evenements relatifs à l'interface
	dongeonEvent() # Evenements relatifs au niveau en général

	pygame.display.flip() # raffraichissement de la fenêtre

# ================================================================================================
# '''
