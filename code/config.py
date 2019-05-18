#========================================== IMPORT FICHIERS NECESSAIRES ================================================
import pygame


#========================================== IMPORT DES IMAGES ==========================================================
dic_image = {}

def init():
	global dic_image

	surface = pygame.image.load("../image/sol.png").convert()
	pygame.draw.circle(surface, (0, 0, 255), (120, 120), 75)

	dic_image = {
		"mur": pygame.image.load("../image/mur.png").convert(), #dictionnaire pour les images
		"eau": pygame.image.load("../image/eau.png").convert(),
		"vide": pygame.image.load("../image/vide.png").convert(),
		"sol": pygame.image.load("../image/sol.png").convert(),
		"fin": pygame.image.load("../image/fin.png").convert(),
		"porte": pygame.image.load("../image/porte.png").convert(),
		"spawn": pygame.image.load("../image/spawn.png").convert(),
		"personnage": pygame.image.load("../image/personnage.png").convert_alpha(),
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

#==========================================  CONFIGS ==================================================================
def getConfig():
	'''config niveau'''
	debug = False #permet d'activer le debug											(defaut False)
	taille_level = 800 #taille de l'espace de jeu 										(defaut 800)
	nb_case = 20 #nombre de case de jeu 												(defaut 20)
	taille_HUD = round((20*taille_level)/100) #definie la taille de l'hud largeur		(auto)
	taille_editeur = taille_level + 300 #definie taille editeur 						(auto)
	taille_case = round(taille_level/nb_case) #definie la taille d'une case 			(auto)
	taille_ecran = (taille_level+taille_HUD, taille_level) #definie taille de l'ecrant 	(auto)
	taille_personnage = 0.8*taille_case #definie taille personnage 						(default 0.8*taille_case)
	temps_de_base = 30 #temps d'une partie (en secondes)								(defaut 30)
	degat_des_pics = 5 #temps malus (en seconde) pour les degats des pics				(defaut 5)
	degat_lave = 10 #temps malus (en seconde) pour les degats de la lave				(defaut 10)
	bonus_de_temps = 10 #temps bonus (en seconde)										(defaut 10)
	intervalle_pics = 200 #temps d'intervalle entre pic ouvert/fermée (en frame)		(defaut 200)
	incinvibility = 75 #temps d'invencibilité entre chaque degat (en frame)				(defaut 75)
	fps = 120 #nombre de fps max en jeu (en frame)										(defaut 120)

	
#======================================================================================================================	
	dic = {"taille_ecran":taille_ecran, #dictionnaire pour utilisation de la config
			"nb_case":nb_case,
			"taille_case":taille_case,
			"taille_personnage":taille_personnage, 
			"taille_HUD":taille_HUD,
			"taille_level":taille_level,
			"taille_editeur": taille_editeur,
			"temps": temps_de_base,
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

	
