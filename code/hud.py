import pygame
from pygame.locals import *

import config

config = config.getConfig()
taille_ecran = config["taille_ecran"] #recuperation de la zone d'espace de jeu

def hudfix():
	''' Affiche les sprite sur l'ecran'''
	hud_1()
	hud_2()
	hud_texte()
	
# ====================================================== DIFFERENT HUD ===================================================
def hud_1():
	taillex_hud = config["taille_HUD"] #recuperation taille x de l'hud
	tailley_hud = config["taille_ecran"] #recuperation taille y de l'hud
	image = pygame.Surface((taillex_hud, tailley_hud)) #creation de la zone d'hud
	image.fill((255, 0, 0)) #ajout couleur
	rect = image.get_rect() #creation d'une image rectangle
	rect.topleft = (taille_ecran, 0) #definition des coordonnées a partir du point haut gauche
	pygame.display.get_surface().blit(image, rect) #disposition image à l'ecran

def hud_2():
	taillex_hud = round(config["taille_HUD"]-((config["taille_HUD"]*10)/100)) #recuperation taille x (plus ajustement) de l'hud
	tailley_hud = round(config["taille_ecran"]-((config["taille_ecran"]*2.5)/100)) #recuperation taille y (plus ajustement) de l'hud
	positionx = (taille_ecran+((config["taille_HUD"]*5)/100)) #creation de la zone de positionnement en x
	positiony = (config["taille_ecran"]*1.25)/100 #creation de la zone de positionnement en y
	image = pygame.Surface((taillex_hud, tailley_hud)) #creation de la zone d'hud
	image.fill((0, 255, 0)) #ajout couleur
	rect = image.get_rect() #creation d'une image rectangle
	rect.topleft = (positionx, positiony) #definition des coordonnées a partir du point haut gauche
	pygame.display.get_surface().blit(image, rect) #disposition image à l'ecran

def hud_texte():
	taille_texte = round((50*config["taille_case"])/100)
	police = pygame.font.SysFont("Arial", taille_texte, True) #initialisation de la police (police, taille_police
	couleur_police = (0, 0, 255)
	texte = police.render("Temps restant :", True, couleur_police)
	position_texte = texte.get_rect()
	positionx = (taille_ecran+((config["taille_HUD"]*15)/100)) #creation de la zone de positionnement en x
	positiony = (config["taille_ecran"]*2)/100 #creation de la zone de positionnement en y
	position_texte.topleft = (positionx, positiony)
	pygame.display.get_surface().blit(texte, position_texte) #disposition texte à l'ecran