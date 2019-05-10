import pygame

dic_image = {}

def init():
	global dic_image
	dic_image = {
		"mur": pygame.image.load("../image/mur.png").convert(),
		"eau": pygame.image.load("../image/eau.png").convert(),
		"vide": pygame.image.load("../image/vide.png").convert(),
		"sol": pygame.image.load("../image/sol.png").convert(),
		"fin": pygame.image.load("../image/fin.png").convert(),
		"porte": pygame.image.load("../image/porte.png").convert(),
		"spawn": pygame.image.load("../image/spawn.png").convert(),
		"interrupteur": pygame.image.load("../image/interrupteur_off.png").convert(),
		"interrupteur timer": pygame.image.load("../image/interrupteur_off.png").convert(),
		"interrupteur on": pygame.image.load("../image/interrupteur_on.png").convert(),
		"pic": pygame.image.load("../image/pic_on.png").convert(),
		"pic intervalle": pygame.image.load("../image/pic_on.png").convert(),
		"pic interrupteur": pygame.image.load("../image/pic_on.png").convert(),
		"pic off": pygame.image.load("../image/pic_off.png").convert(),
		"lave": pygame.image.load("../image/lave.png").convert(),
	}

def getConfig():
	taille_level = 800 #taille de l'espace de jeu
	nb_case = 20 #nombre de case de jeu
	taille_HUD = round((20*taille_level)/100) #definie la taille de l'hud (auto)
	taille_editeur = taille_level + 300
	taille_case = round(taille_level/nb_case) #definie la taille d'une case (auto)
	taille_ecran = (taille_level+taille_HUD, taille_level)
	taille_personnage = 0.8*taille_case #definie taille personnage
	dic = {"taille_ecran":taille_ecran, "nb_case":nb_case, "taille_case":taille_case, "taille_personnage":taille_personnage, 
			"taille_HUD":taille_HUD, "taille_level":taille_level, "taille_editeur": taille_editeur} #dictionnaire pour utilisation de la configue
	return dic

def getImage(sprite=None):
	''' Renvoit l'image associé au sprite '''
	if sprite:
		return dic_image[sprite]
	else:
		return dic_image

	