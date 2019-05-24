# coding: utf-8

#========================================== IMPORT FICHIERS NECESSAIRES ================================================

import pygame

#========================================== CONFIGS ====================================================================

'''config niveau'''
debug = False #permet d'activer le debug											(defaut False)
taille_level = 800 #taille de l'espace de jeu 										(defaut 800)
nb_case = 20 #nombre de case de jeu 												(defaut 20)
taille_HUD = round((20*taille_level)/100) #definie la taille de l'hud largeur		(auto)
taille_editeur = taille_level + 300 #definie taille editeur 						(auto)
taille_case = round(taille_level/nb_case) #definie la taille d'une case 			(auto)
taille_ecran = (taille_level+taille_HUD, taille_level) #definie taille de l'ecrant 	(auto)
taille_personnage = 0.75*taille_case #definie taille personnage 					(defaut 0.75*taille_case)
vitesse_personnage = 3 #vitesse du personnage en jeu								(defaut 3)
temps_de_base = 30 #temps d'une partie (en secondes)								(defaut 30)
degat_des_pics = 5 #temps malus (en seconde) pour les degats des pics				(defaut 5)
degat_lave = 10 #temps malus (en seconde) pour les degats de la lave				(defaut 10)
bonus_de_temps = 10 #temps bonus (en seconde)										(defaut 10)
intervalle_pics = 200 #temps d'intervalle entre pic ouvert/fermée (en frame)		(defaut 200)
incinvibility = 75 #temps d'invencibilité entre chaque degat (en frame)				(defaut 75)
fps = 120 #nombre de fps max en jeu (en frame)										(defaut 120)
	


dic_image = {}


#========================================== IMPORT DES IMAGES ==========================================================

def init():
	global dic_image
	'''permet de convertire les images'''
	surface = pygame.image.load("../image/sol.png").convert()
	pygame.draw.circle(surface, (0, 0, 255), (120, 120), 75)
	''''''
#========================================== DEBUG SPRITE ===============================================================
	if debug: #permet d'afficher le sprite du personnage sans le fond transparent
		personnage_h = pygame.image.load("../image/personnage_h.png").convert()
		personnage_b = pygame.image.load("../image/personnage_b.png").convert()
		personnage_d = pygame.image.load("../image/personnage_d.png").convert()
		personnage_g = pygame.image.load("../image/personnage_g.png").convert()
		
	else: #permet d'afficher le sprite du personnage avec le fond transparent
		personnage_h = pygame.image.load("../image/personnage_h.png").convert_alpha()
		personnage_b = pygame.image.load("../image/personnage_b.png").convert_alpha()
		personnage_d = pygame.image.load("../image/personnage_d.png").convert_alpha()
		personnage_g = pygame.image.load("../image/personnage_g.png").convert_alpha()	

	dic_image = { #dictionnaire pour les images
		"mur": pygame.image.load("../image/mur.png").convert(),
		"eau": pygame.image.load("../image/eau.png").convert(),
		"vide": pygame.image.load("../image/vide.png").convert(),
		"sol": pygame.image.load("../image/sol.png").convert(),
		"fin": pygame.image.load("../image/fin.png").convert(),
		"porte": pygame.image.load("../image/porte.png").convert(),
		"spawn": pygame.image.load("../image/spawn.png").convert(),
		"personnage h": personnage_h,
		"personnage b": personnage_b,
		"personnage d": personnage_d,
		"personnage g": personnage_g,		
		"interrupteur": pygame.image.load("../image/interrupteur_off.png").convert(),
		"interrupteur timer": pygame.image.load("../image/interrupteur_off.png").convert(),
		"interrupteur on": pygame.image.load("../image/interrupteur_on.png").convert(),
		"pic": pygame.image.load("../image/pic_on.png").convert(),
		"pic intervalle": pygame.image.load("../image/pic_on.png").convert(),
		"pic interrupteur": pygame.image.load("../image/pic_on.png").convert(),
		"pic off": pygame.image.load("../image/pic_off.png").convert(),
		"lave": pygame.image.load("../image/lave.png").convert(),

		"bonus": pygame.image.load("../image/bonus.png").convert(),
		"hud": pygame.image.load("../image/hud.png").convert(),
		
		"fond menu": pygame.image.load("../image/menu_fond.png").convert(),
		"fond game over" : pygame.image.load("../image/game_over.png").convert(),
	}

#========================================== RECUPERATION CONFIGS ==================================================================
def getConfig():
	dic = {"taille_ecran":taille_ecran, #dictionnaire pour utilisation de la config
			"nb_case":nb_case,
			"taille_case":taille_case,
			"taille_personnage":taille_personnage, 
			"taille_HUD":taille_HUD,
			"taille_level":taille_level,
			"taille_editeur": taille_editeur,
			"temps": temps_de_base,
			"vitesse": vitesse_personnage,
			"degat_pics": degat_des_pics,
			"degat_lave": degat_lave,
			"bonus": bonus_de_temps,
			"intervalle_pics": intervalle_pics,
			"incinvibility": incinvibility,
			"fps": fps,
			"debug": debug}
	return dic

#========================================== RECUPERATION SPRITE ======================================================
def getImage(sprite=None):
	''' Renvoit l'image associé au sprite '''
	if sprite:
		return dic_image[sprite]
	else:
		return dic_image

	
