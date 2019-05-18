# coding: utf-8

#========================================== IMPORT FICHIERS NECESSAIRES ================================================
import pygame
from pygame.locals import *

import editeur.widget as widget
import config
# ========================================= INITIALISATION =======================================
config_info = config.getConfig() #recupere les configs
# ================================================================================================
		
class Hud(): #classe de l'hud
	def __init__(self):		
		self.dimension = (config_info["taille_HUD"], config_info["taille_level"]) #creer les dimension de l'hud
		self.largeur = config_info["taille_HUD"] #donne la largeur de l'hud
		self.position = (config_info["taille_level"], 0) #donne la position haute gauche de l'hud (en bord de niveau à droite)
		self.taille_level = config_info["taille_level"] #recupere la taille de l'evel




		self.image = config.getImage("hud") #recupere l'image de l'hud
		self.image = pygame.transform.scale(self.image, self.dimension) #redimensionne l'image (uniquement en cas de changement de taille de la fenetre)
		
		self.rect_hud = self.image.get_rect() 
		self.rect_hud.topleft = (config_info["taille_level"], 0) #permet l'affichage de l'hud

		self.widg_temps = widget.Label(((self.taille_level+(self.largeur/160)*22), (self.taille_level/800)*227), size=(112,36), color = (0, 0, 0, 0), text = "temps", text_color = (255, 255, 255), centered = True, police = 20, bold = True) #texte du temps
		self.widg_score = widget.Label(((self.taille_level+(self.largeur/160)*22), (self.taille_level/800)*382), size=(112,36), color = (0, 0, 0, 0), text = "score", text_color = (255, 255, 255), centered = True, police = 20, bold = True) #texte du score
		
	def update(self, temps, score): #permet la mise a jour de l'hud
		pygame.display.get_surface().blit(self.image, self.rect_hud)  #imprime a l'ecran l'hud
		self.widg_temps.change_text(str(temps)) #met a jour le text du temps
		self.widg_score.change_text(str(score)) #met a jour le text du score
		self.widg_score.update() #met a jour l'affichage du score
		self.widg_temps.update() #met a jour l'affichage du temps
		
	def kill(self): #permet de suprimer les textes de temps et de score 
		self.widg_score.kill()
		self.widg_temps.kill()