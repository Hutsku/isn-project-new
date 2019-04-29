import pygame
from pygame.locals import *

import math
import json

import editeur.widget as widget
import objet
import dongeon
import config

# ========================================= INITIALISATION =======================================

taille_parametre = 300
taille_level = config.getConfig()["taille_niveau"]
taille_ecran = (taille_level+taille_parametre, taille_level)
pygame.init() #initialisation des modules py.game
fenetre = pygame.display.set_mode(taille_ecran) # creation de la fenetre (avec taille en parametre)

fond = pygame.Surface(taille_ecran) # Création du fond, de taille equivalente à la fenêtre
fond.fill((100, 100, 100)) # on colorie en gris

# ================================================================================================

class Editeur():
	def __init__(self, taille_parametre, taille_level):
		self.taille_parametre = taille_parametre
		self.taille_level = taille_level
		self.taille_case = config.getConfig()["taille_case"]
		self.nb_case = config.getConfig()["nb_case"]

		self.niveau = niveau = dongeon.Niveau("../niveau/niveau1.txt")
		self.type_case = "mur"

		self._entry = None

		self._init_editeur()

	# ========================= PARAMETRES EDITEUR =============================

	def _init_editeur(self):
		for x in range(self.nb_case):
			pygame.draw.line(fond, (0, 0, 0), (x*self.taille_case+self.taille_case, 0), (x*self.taille_case+self.taille_case, self.taille_level))
			pygame.draw.line(fond, (0, 0, 0), (0, x*self.taille_case+self.taille_case), (self.taille_level, x*self.taille_case+self.taille_case))

		frame1 = widget.Frame((510, 10), (280, 90), color=(100, 100,100), border=1)
		frame2 = widget.Frame((510, 110), (280, 280), color=(100, 100,100), border=1)
		frame3 = widget.Frame((510, 400), (280, 90), color=(100, 100,100), border=1)

		self._entry = widget.Entry((10, 10), adapt=True, border=0, border_color=(255, 0, 0), text="niveau1", frame=frame1)
		widget.Button((150, 50), text="Ouvrir", frame=frame1, action=self.load_level, hoover_color=(200, 200, 255), centered=True)
		widget.Button((10, 50), text="Enregistrer", frame=frame1, action=self.save_level, hoover_color=(200, 200, 255), centered=True)

		widget.ImageButton((10, 10), size=(30, 30), action=self.type_mur, path="../image/mur.png", frame=frame3)
		widget.ImageButton((10, 50), size=(30, 30), action=self.type_sol, path="../image/sol.png", frame=frame3)
		widget.ImageButton((50, 10), size=(30, 30), action=self.type_fin, path="../image/fin.png", frame=frame3)
		widget.ImageButton((50, 50), size=(30, 30), action=self.type_spawn, path="../image/spawn.png", frame=frame3)

		self.build_level()

	def build_level(self):
		'''construit les murs et objets d'après les coordonnées du niveau'''
		x=0
		for a in self.niveau.coord["terrain"]:
			y=0
			for case in self.niveau.coord["terrain"][x]:
				position = (x*self.taille_case, y*self.taille_case)
				type_case = case["type"]
				if type_case == "mur":
					objet.Mur(position, (self.taille_case, self.taille_case))
				if type_case == "sol":
					objet.Sol(position, (self.taille_case, self.taille_case))
				if type_case == "fin":
					objet.Escalier(position, (self.taille_case, self.taille_case))
					self.niveau.fin = (x, y)
				y += 1
			x += 1

	def delete_level(self):
		'''on détruit le niveau actuel'''
		for case in objet.Objet.liste:
			case.kill()

	def add_case(self, x, y):
		pos_x = math.floor(x/self.taille_case)
		pos_y = math.floor(y/self.taille_case)
		position = (pos_x*self.taille_case, pos_y*self.taille_case)

		self.supp_case(x, y)
		if self.type_case == "mur":
			objet.Mur(position, (self.taille_case, self.taille_case))
		if self.type_case == "sol":
			objet.Sol(position, (self.taille_case, self.taille_case))
		if self.type_case == "spawn":
			self.niveau.spawn = (x, y)
		if self.type_case == "fin":
			objet.Escalier(position, (self.taille_case, self.taille_case))
			self.niveau.fin = (x, y)
		self.niveau.coord["terrain"][pos_x][pos_y]["type"] = self.type_case

	def supp_case(self, x, y):
		pos_x = math.floor(x/self.taille_case)
		pos_y = math.floor(y/self.taille_case)
		self.niveau.coord["terrain"][pos_x][pos_y]["type"] = None

		_objet = pygame.sprite.Sprite() # on crée un point correspondant au clique de la souris
		_objet.rect = pygame.Rect((x, y), (1, 1))
		response = pygame.sprite.spritecollideany(_objet, objet.Objet.liste)
		if response:
			response.kill()

	def type_mur(self):
		self.type_case = "mur"
	def type_sol(self):
		self.type_case = "sol"
	def type_fin(self):
		self.type_case = "fin"
	def type_spawn(self):
		self.type_case = "spawn"

	# ============================= SAVE/LOAD NIVEAU ===========================

	def save_level(self):
		print("save")
		lien = "../niveau/"+self._entry.text+".txt"
		dic = {"spawn": self.niveau.spawn, "terrain":self.niveau.coord["terrain"], "objets":self.niveau.coord["objets"]}
		with open(lien, "w") as fichier:
			json_dic = json.dumps(dic)
			fichier.write(json_dic)

	def load_level(self):
		print("load")
		lien = "../niveau/"+self._entry.text+".txt"
		with open(lien, "r") as fichier:
			json_dic = fichier.read()
			dic = json.loads(json_dic)

			self.niveau.spawn = dic["spawn"]
			self.niveau.coord["terrain"] = dic["terrain"]
			self.niveau.coord["objets"] = dic["objets"]
			self.delete_level()
			self.build_level()

# ========================================== FONCTIONS ===========================================

def objetEvent():
	objet.move() # On actualise la position des objets sur l'écran (collision etc)
	objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
	objet.update() # on affiche les sprites à l'écran

# ===================================== BOUCLE PRINCIPALE ========================================

editeur = Editeur(taille_parametre, taille_level)

boucle = True
while boucle:
	fenetre.blit(fond, (0, 0)) # on colle le fond

	# on gère les evenements claviers et souris 
	for event in pygame.event.get():
		widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)

		if event.type == QUIT: #si clic sur croix rouge
			boucle = False #fin de boucle

		if event.type == KEYDOWN:
			pass

		if event.type == MOUSEBUTTONDOWN:
			(mouse_x, mouse_y) = pygame.mouse.get_pos()
			if 0 <= mouse_x <= taille_level and 0 <= mouse_y <= taille_level: # si le clique intervient dans le niveau...
				if event.dict["button"] == 3: # clique droit
					editeur.supp_case(mouse_x, mouse_y)
				if event.dict["button"] == 1: # clique gauche
					editeur.add_case(mouse_x, mouse_y)

	widget.update()
	objetEvent() # Evenements relatifs aux objets
	pygame.display.flip() # raffraichissement de la fenêtre

# ================================================================================================