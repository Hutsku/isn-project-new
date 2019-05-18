# coding: utf-8

import pygame
from pygame.locals import *

import math
import json

import editeur.widget as widget
import objet
import dongeon
import config

# ========================================= INITIALISATION =======================================

taille_level = config.getConfig()["taille_level"]
taille_editeur = config.getConfig()["taille_editeur"]
taille_ecran = (taille_editeur, taille_level)
pygame.init() #initialisation des modules py.game
fenetre = pygame.display.set_mode(taille_ecran) # creation de la fenetre (avec taille en parametre)
config.init()

fond = pygame.Surface(taille_ecran) # Création du fond, de taille equivalente à la fenêtre
fond.fill((100, 100, 100)) # on colorie en gris

# ================================================================================================

class Editeur():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.taille_case = config.getConfig()["taille_case"]
		self.nb_case = config.getConfig()["nb_case"]

		self.niveau = niveau = dongeon.Niveau("../niveau/exemple/blank_level.txt")
		self.type_case = "mur"
		self.type_mode = "selection"
		self.case_selection = None
		self.case_selection_cible = []

		''' on crée un carré qui servira à montrer la selection d'une case. '''
		self._selection_rect = pygame.Surface((self.taille_case, self.taille_case)).convert_alpha()
		self._selection_rect.fill((0, 0, 0, 0))
		self._selection_cible_rect = self._selection_rect.copy()
		pygame.draw.rect(self._selection_rect, (255, 0, 0), Rect((0, 0), (self.taille_case, self.taille_case)), 1)
		pygame.draw.rect(self._selection_cible_rect, (0, 0, 255), Rect((0, 0), (self.taille_case, self.taille_case)), 1)

		''' variables contenant les widget à mettre à jour '''
		self.widg_entry = None 
		self.widg_select_mode = None
		self.widg_label_param = None 
		self.widg_button_cible = None
		self.widg_button_mode = None
		self.widg_button_test = None # Bouton permettant de tester le niveau en cours
		self.frame1 = None
		self.frame2 = None
		self.frame3 = None

		''' Variable pour le personnage, seulement en mode test '''
		self.perso = None 

		self._init_editeur()

	# ================================== EDITION NIVEAU =============================

	def _init_editeur(self):
		for x in range(self.nb_case):
			pygame.draw.line(fond, (0, 0, 0), (x*self.taille_case+self.taille_case, 0), (x*self.taille_case+self.taille_case, self.height))
			pygame.draw.line(fond, (0, 0, 0), (0, x*self.taille_case+self.taille_case), (self.height, x*self.taille_case+self.taille_case))

		''' Définition des Frames (cadres) de l'editeur '''
		frame1 = widget.Frame((self.height+10, 10), (280, 90), color=(100, 100,100), border=1)
		frame2 = widget.Frame((self.height+10, 110), (280, 280), color=(100, 100,100), border=1)
		frame3 = widget.Frame((self.height+10, 400), (280, 130), color=(100, 100,100), border=1)
		self.frame2 = frame2 # On stocke le frame 2

		''' FRAME 1 - Sauvegarde / Ouverture d'un niveau '''
		self.widg_entry = widget.Entry((10, 10), border=0, border_color=(255, 0, 0), text="nom ?", frame=frame1)
		widget.Button((150, 50), text="Ouvrir", frame=frame1, action=self.load_level, hoover_color=(200, 200, 255), centered=True)
		widget.Button((10, 50), text="Enregistrer", frame=frame1, action=self.save_level, hoover_color=(200, 200, 255), centered=True)
		widget.Button((150, 10), text="Reset", frame=frame1, action=self.reset_level, hoover_color=(200, 200, 255), centered=True)

		''' FRAME 2 - Paramètres de selection d'une case '''
		self.widg_image_case = widget.Image((10, 10), size=(30, 30), border=1, path="", frame=frame2)
		self.widg_label_case = widget.Label((40, 10), size=(150, 30), text="None", color=(100, 100, 100), frame=frame2)
		self.widg_label_param = widget.Label((10, 40), size=(260, 30), text="Aucun(s) paramètre(s)", color=(100, 100, 100), frame=frame2)

		self.widg_button_test = widget.Button((10, 200), text="Tester niveau", frame=frame2, action=(self.change_mode, "test niveau"), hoover_color=(200, 200, 255), centered=True)
		self.widg_button_mode = widget.Button((10, 240), text="Changer mode", frame=frame2, action=(self.change_mode, "edition"), hoover_color=(200, 200, 255), centered=True)
		self.widg_select_mode = widget.Label((120, 240), size=(150, 30), text="Mode: selection", text_color=(0, 0, 255), color=(100, 100, 100), frame=frame2)

		''' FRAME 3 - Type de case à ajouter '''
		widget.ImageButton((10, 10), size=(30, 30), action=(self.change_type, "sol"), path="../image/sol.png", frame=frame3)
		widget.ImageButton((10, 50), size=(30, 30), action=(self.change_type, "fin"), path="../image/fin.png", frame=frame3)
		widget.ImageButton((10, 90), size=(30, 30), action=(self.change_type, "spawn"), path="../image/spawn.png", frame=frame3)
		widget.ImageButton((50, 10), size=(30, 30), action=(self.change_type, "mur"), path="../image/mur.png", frame=frame3)
		widget.ImageButton((50, 50), size=(30, 30), action=(self.change_type, "eau"), path="../image/eau.png", frame=frame3)
		widget.ImageButton((50, 90), size=(30, 30), action=(self.change_type, "vide"), path="../image/vide.png", frame=frame3)
		widget.ImageButton((90, 10), size=(30, 30), action=(self.change_type, "lave"), path="../image/lave.png", frame=frame3)
		widget.ImageButton((130, 10), size=(30, 30), action=(self.change_type, "pic"), path="../image/pic_on.png", frame=frame3)
		widget.ImageButton((130, 50), size=(30, 30), action=(self.change_type, "pic intervalle"), path="../image/pic_on.png", frame=frame3)
		widget.ImageButton((130, 90), size=(30, 30), action=(self.change_type, "pic interrupteur"), path="../image/pic_on.png", frame=frame3)
		widget.ImageButton((170, 10), size=(30, 30), action=(self.change_type, "porte"), path="../image/porte.png", frame=frame3)
		widget.ImageButton((170, 50), size=(30, 30), action=(self.change_type, "interrupteur"), path="../image/interrupteur_off.png", frame=frame3)
		widget.ImageButton((170, 90), size=(30, 30), action=(self.change_type, "interrupteur timer"), path="../image/interrupteur_off.png", frame=frame3)
		widget.ImageButton((210, 10), size=(30, 30), action=(self.change_type, "bonus"), path="../image/bonus.png", frame=frame3)

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
				elif type_case == "eau":
					objet.Eau(position, (self.taille_case, self.taille_case))
				elif type_case == "vide":
					objet.Vide(position, (self.taille_case, self.taille_case))
				elif type_case == "sol":
					objet.Sol(position, (self.taille_case, self.taille_case))
				elif type_case == "fin":
					objet.Escalier(position, (self.taille_case, self.taille_case))
				elif type_case == "spawn":
					objet.SolSpawn(position, (self.taille_case, self.taille_case))
				elif type_case == "porte":
					objet.PorteInterrupteur(position, (self.taille_case, self.taille_case), interrupteur=case["cible"])
				elif type_case == "interrupteur":
					objet.Interrupteur(position, (self.taille_case, self.taille_case), cible=case["cible"])
				elif type_case == "interrupteur timer":
					objet.InterrupteurTimer(position, (self.taille_case, self.taille_case), cible=case["cible"])
				elif type_case == "lave":
					objet.Lave(position, (self.taille_case, self.taille_case))
				elif type_case == "pic":
					objet.Pic(position, (self.taille_case, self.taille_case))
				elif type_case == "pic intervalle":
					objet.PicIntervalle(position, (self.taille_case, self.taille_case))
				elif type_case == "pic interrupteur":
					objet.PicInterrupteur(position, (self.taille_case, self.taille_case), interrupteur=case["cible"])
				elif type_case == "bonus":
					objet.Bonus(position, (self.taille_case, self.taille_case))
				y += 1
			x += 1

	def delete_level(self):
		'''on détruit le niveau actuel'''
		for case in objet.Objet.liste:
			case.kill()

	def add_case(self, x, y, type_case=None):
		''' Ajoute et/ou remplace une case du niveau '''
		pos_x = math.floor(x/self.taille_case)
		pos_y = math.floor(y/self.taille_case)
		position = (pos_x*self.taille_case, pos_y*self.taille_case)

		self.supp_case(x, y, replace=True)
		self.niveau.coord["terrain"][pos_x][pos_y]["type"] = self.type_case

		if self.type_case == "mur":
			objet.Mur(position, (self.taille_case, self.taille_case))
		elif self.type_case == "eau":
			objet.Eau(position, (self.taille_case, self.taille_case))
		elif self.type_case == "vide":
			objet.Vide(position, (self.taille_case, self.taille_case))
		elif self.type_case == "sol":
			objet.Sol(position, (self.taille_case, self.taille_case))
		elif self.type_case == "spawn":
			self.niveau.spawn = (pos_x, pos_y)
			objet.SolSpawn(position, (self.taille_case, self.taille_case)) # une simple case Sol rouge
		elif self.type_case == "fin":
			objet.Escalier(position, (self.taille_case, self.taille_case))
		elif self.type_case == "porte":
			objet.PorteInterrupteur(position, (self.taille_case, self.taille_case))
			self.niveau.coord["terrain"][pos_x][pos_y]["cible"] = []
		elif self.type_case == "interrupteur":
			objet.Interrupteur(position, (self.taille_case, self.taille_case))
			self.niveau.coord["terrain"][pos_x][pos_y]["cible"] = []
		elif self.type_case == "interrupteur timer":
			objet.InterrupteurTimer(position, (self.taille_case, self.taille_case))
			self.niveau.coord["terrain"][pos_x][pos_y]["cible"] = []
		elif self.type_case == "lave":
			objet.Lave(position, (self.taille_case, self.taille_case))
		elif self.type_case == "pic":
			objet.Pic(position, (self.taille_case, self.taille_case))
		elif self.type_case == "pic intervalle":
			objet.PicIntervalle(position, (self.taille_case, self.taille_case))
		elif self.type_case == "pic interrupteur":
			objet.PicInterrupteur(position, (self.taille_case, self.taille_case))
			self.niveau.coord["terrain"][pos_x][pos_y]["cible"] = []
		elif self.type_case == "bonus":
			objet.Bonus(position, (self.taille_case, self.taille_case))
		else:
			print("type invalide: "+self.type_case)

	def supp_case(self, x, y, replace=False):
		''' Remplace la case du niveau par du sol '''
		pos_x = math.floor(x/self.taille_case)
		pos_y = math.floor(y/self.taille_case)
		position = (pos_x*self.taille_case, pos_y*self.taille_case)

		_objet = pygame.sprite.Sprite() # on crée un point correspondant au clique de la souris
		_objet.rect = pygame.Rect((x, y), (1, 1))
		response = pygame.sprite.spritecollideany(_objet, objet.Objet.liste)
		if response:
			response.kill()

		''' Si on ne remplace pas la case (clique droit), on remplace par du sol '''
		if not replace:
			self.niveau.coord["terrain"][pos_x][pos_y]["type"] = "sol"
			objet.Sol(position, (self.taille_case, self.taille_case))

	def select_case(self, x, y):
		''' Selectionne une case du niveau puis affiche les infos '''
		pos_x = math.floor(x/self.taille_case)
		pos_y = math.floor(y/self.taille_case)
		type_case = self.niveau.coord["terrain"][pos_x][pos_y]["type"]

		self.case_selection = [pos_x, pos_y]

		cible=None
		if type_case in ["porte", "interrupteur", "interrupteur timer", "pic interrupteur"]:
			cible = self.niveau.coord["terrain"][pos_x][pos_y]["cible"]

		self.select_case_info(type_case, cible=cible)

	def select_case_info(self, type_case, cible=None):
		''' Modifie les infos de la case séléctionnée'''
		if not cible:
			cible = []

		self.widg_label_case.change_text(text=type_case)
		self.widg_image_case.change_image(image=config.getImage(type_case))

		''' On détruit tout les anciens widget de paramètre, dans le doute '''
		if self.widg_button_cible:
			self.widg_button_cible.kill()

		''' On va créer les widget de pramètre correspondant à la case '''
		if type_case == "porte":
			self.widg_label_param.change_text(text="- Porte reliée à ({}) mécanisme(s).".format(len(cible)))
			self.widg_button_cible = widget.Button((10, 70), size=(200, 30), text="Selectionner cibles", action=(self.change_mode, "selection cible"), hoover_color=(200, 200, 255), centered=True, frame=self.frame2)
			self.case_selection_cible = cible
		elif type_case in ["interrupteur", "interrupteur timer"]:
			self.widg_label_param.change_text(text="- Interrupteur reliée à ({}) mécanisme(s).".format(len(cible)))
			self.widg_button_cible = widget.Button((10, 70), size=(200, 30), text="Selectionner cibles", action=(self.change_mode, "selection cible"), hoover_color=(200, 200, 255), centered=True, frame=self.frame2)
			self.case_selection_cible = cible
		elif type_case == "pic interrupteur":
			self.widg_label_param.change_text(text="- Pic reliée à ({}) mécanisme(s).".format(len(cible)))
			self.widg_button_cible = widget.Button((10, 70), size=(200, 30), text="Selectionner cibles", action=(self.change_mode, "selection cible"), hoover_color=(200, 200, 255), centered=True, frame=self.frame2)
			self.case_selection_cible = cible

		else:
			self.widg_label_param.change_text(text="Aucun(s) paramètre(s)")
			self.case_selection_cible = []

	def add_case_cible(self, x, y):
		''' Ajoute une cible à la case sélectionnée '''
		pos_x = math.floor(x/self.taille_case)
		pos_y = math.floor(y/self.taille_case)
		case_cible = self.niveau.coord["terrain"][pos_x][pos_y]

		''' si la case ciblé est bien une cible potentielle ... '''
		if case_cible["type"] in ["porte", "interrupteur", "interrupteur timer", "pic interrupteur"]:
			if not [pos_x, pos_y] in self.case_selection_cible: # si la case selectionné ne l'est pas
				self.case_selection_cible.append([pos_x, pos_y])

	def supp_case_cible(self, x, y):
		pos_x = math.floor(x/self.taille_case)
		pos_y = math.floor(y/self.taille_case)
		case_cible = self.niveau.coord["terrain"][pos_x][pos_y]

		if [pos_x, pos_y] in self.case_selection_cible:
			self.case_selection_cible.remove([pos_x, pos_y])

			''' on supprime ensuite le lien dans l'autre sens de la cible vers mecanisme '''
			if case_cible["type"] == "interrupteur" or case_cible["type"] == "porte":
				if self.case_selection in case_cible["cible"]:
					case_cible["cible"].remove(self.case_selection)

	def valider_cible(self):
		(x, y) = self.case_selection
		case = self.niveau.coord["terrain"][x][y]

		case["cible"] = self.case_selection_cible
		for (cible_x, cible_y) in self.case_selection_cible:
			if not [x, y] in self.niveau.coord["terrain"][cible_x][cible_y]["cible"]:
				self.niveau.coord["terrain"][cible_x][cible_y]["cible"].append([x, y])

		''' On met à jour les widget '''
		nb_cible = len(case["cible"])
		self.widg_label_param.change_text(text="- Interrupteur reliée à ({}) mécanisme(s)")
		self.widg_button_cible.change_text(text="Selectionner cibles")
		self.widg_button_cible.action = (self.change_mode, "selection cible")

		self.case_selection_cible = []
		self.type_mode = "selection"

	# ============================= PARAMETRES EDITEURS ===========================

	def change_type(self, type_case):
		''' change le type de case selectionné '''
		self.type_case = type_case
		self.select_case_info(type_case)

	def change_mode(self, mode):
		''' change le mode de selection ou d'edition du niveau '''
		self.type_mode = mode

		if mode == "test niveau":
			self.widg_select_mode.change_text(text="Mode: Test du niveau")
			self.widg_button_test.change_text(text="Arrêter test")
			self.widg_button_test.action = (self.change_mode, "selection")
			self.case_selection = None
			self.case_selection_cible = []
			taille_case = config.getConfig()["taille_case"]

			''' On va rechercher et ajouter les cible à leur mecanisme (l'objet lui-même, pas les coordonnées) '''
			for porte in objet.PorteInterrupteur.liste:
				list_cible = []
				for (cible_x, cible_y) in porte.interrupteur:
					position_cible = (cible_x*taille_case, cible_y*taille_case)
					for interrupteur in objet.Interrupteur.liste:
						if interrupteur.rect.topleft == position_cible:
							list_cible.append(interrupteur)
				porte.interrupteur = list_cible

			for pic in objet.PicInterrupteur.liste:
				list_cible = []
				for (cible_x, cible_y) in pic.interrupteur:
					position_cible = (cible_x*taille_case, cible_y*taille_case)
					for interrupteur in objet.Interrupteur.liste:
						if interrupteur.rect.topleft == position_cible:
							list_cible.append(interrupteur)
				pic.interrupteur = list_cible

			for interrupteur in objet.Interrupteur.liste:
				list_cible = []
				for (cible_x, cible_y) in interrupteur.cible:
					position_cible = (cible_x*taille_case, cible_y*taille_case)
					for porte in objet.PorteInterrupteur.liste:
						if porte.rect.topleft == position_cible:
							list_cible.append(porte)
					for pic in objet.PicInterrupteur.liste:
						if pic.rect.topleft == position_cible:
							list_cible.append(pic)
				interrupteur.cible = list_cible

			taille_perso = config.getConfig()["taille_personnage"]
			spawn = (self.niveau.spawn[0]*self.taille_case, self.niveau.spawn[1]*self.taille_case)
			self.perso = objet.Personnage(spawn, (taille_perso, taille_perso))

		else:
			self.widg_button_test.change_text(text="Tester niveau")
			self.widg_button_test.action = (self.change_mode, "test niveau")
			if self.perso:
				self.perso.kill()
				self.perso = None

				taille_case = config.getConfig()["taille_case"]
				for porte in objet.PorteInterrupteur.liste:
					list_cible = []
					for interr in porte.interrupteur:
						(x, y) = interr.rect.topleft
						list_cible.append((x/taille_case, y/taille_case))
					porte.interrupteur = list_cible
				for pic in objet.PicInterrupteur.liste:
					list_cible = []
					for interr in pic.interrupteur:
						(x, y) = interr.rect.topleft
						list_cible.append((x/taille_case, y/taille_case))
					porte.interrupteur = list_cible
				for interrupteur in objet.Interrupteur.liste:
					list_cible = []
					for cible in interrupteur.cible:
						(x, y) = porte.rect.topleft
						list_cible.append((x/taille_case, y/taille_case))
					interrupteur.cible = list_cible

		if mode == "selection cible":
			self.widg_select_mode.change_text(text="Mode: selection (cible)")
			self.widg_button_cible.change_text(text="Valider")
			self.widg_button_cible.action = self.valider_cible

			(x, y) = self.case_selection
			self.case_selection_cible = self.niveau.coord["terrain"][x][y]["cible"]

		elif mode == "edition":
			self.widg_select_mode.change_text(text="Mode: edition")
			self.widg_button_mode.action = (self.change_mode, "selection")
			self.case_selection = None
			self.case_selection_cible = []

		elif mode == "selection":
			self.widg_select_mode.change_text(text="Mode: selection")
			self.widg_button_mode.action = (self.change_mode, "edition")
			self.case_selection_cible = []

	def save_level(self):
		''' Enregistre la map actuelle'''
		print("save")
		lien = "../niveau/"+self.widg_entry.text+".txt"
		dic = {"spawn": self.niveau.spawn, "terrain":self.niveau.coord["terrain"]}
		with open(lien, "w") as fichier:
			json_dic = json.dumps(dic)
			fichier.write(json_dic)

	def load_level(self):
		'''Charge une map '''
		print("load")
		lien = "../niveau/"+self.widg_entry.text+".txt"
		with open(lien, "r") as fichier:
			json_dic = fichier.read()
			dic = json.loads(json_dic)

			self.niveau.spawn = dic["spawn"]
			self.niveau.coord["terrain"] = dic["terrain"]
			self.delete_level()
			self.build_level()

	def reset_level(self):
		''' Charge la map de base '''
		print("load")
		lien = "../niveau/exemple/blank_level.txt"
		with open(lien, "r") as fichier:
			json_dic = fichier.read()
			dic = json.loads(json_dic)

			self.niveau.spawn = dic["spawn"]
			self.niveau.coord["terrain"] = dic["terrain"]
			self.delete_level()
			self.build_level()

# ========================================== FONCTIONS ===========================================

def objetEvent():
	objet.move() # On actualise la position des objets sur l'écran (collision etc)
	objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
	objet.update() # on affiche les sprites à l'écran

# ===================================== BOUCLE PRINCIPALE ========================================

editeur = Editeur(taille_editeur, taille_level)
key_trad = {"a": 113, "z":119, "d":100, "q":97, "s":115} # traduction unicode et n° key

clock = pygame.time.Clock()
boucle = True
while boucle:
	clock.tick()
	pygame.display.set_caption( str(clock.get_fps()))
	fenetre.blit(fond, (0, 0)) # on colle le fond

	# ========================== CHECK DU MODE TEST OU NON =====================================

	if not editeur.type_mode == "test niveau":
		# on gère les evenements claviers et souris 
		for event in pygame.event.get():
			widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)

			if event.type == QUIT: #si clic sur croix rouge
				boucle = False #fin de boucle

			if event.type == MOUSEBUTTONDOWN:
				(mouse_x, mouse_y) = pygame.mouse.get_pos()
				if 0 <= mouse_x <= taille_level and 0 <= mouse_y <= taille_level: # si le clique intervient dans le niveau...
					if event.dict["button"] == 3: # clique droit
						if editeur.type_mode == "edition":
							editeur.supp_case(mouse_x, mouse_y)
						elif editeur.type_mode == "selection cible":
							editeur.supp_case_cible(mouse_x, mouse_y) # sinon, si en selection ...

					if event.dict["button"] == 1: # clique gauche
						if editeur.type_mode == "edition":
							editeur.add_case(mouse_x, mouse_y) # si l'editeur est en mode edition ...
						elif editeur.type_mode == "selection":
							editeur.select_case(mouse_x, mouse_y) # sinon, si en selection ...
						elif editeur.type_mode == "selection cible":
							editeur.add_case_cible(mouse_x, mouse_y) # sinon, si en selection ...

		widget.update()
		objet.update()

		''' On affiche les rectangle de selection '''
		if editeur.case_selection:
			(pos_x, pos_y) = editeur.case_selection
			position = (pos_x*editeur.taille_case, pos_y*editeur.taille_case)
			fenetre.blit(editeur._selection_rect, position)
		if editeur.case_selection_cible:
			taille_case = editeur.taille_case
			for case in editeur.case_selection_cible:
				(pos_x, pos_y) = case
				position = (pos_x*editeur.taille_case, pos_y*editeur.taille_case)
				fenetre.blit(editeur._selection_cible_rect, position)

				case_selection = editeur.case_selection
				position_debut = ((pos_x*taille_case)+taille_case/2, (pos_y*taille_case)+taille_case/2)
				position_fin = ((case_selection[0]*taille_case)+taille_case/2, (case_selection[1]*taille_case)+taille_case/2)
				pygame.draw.line(fenetre, (0, 0, 255), position_debut, position_fin)

	else:
		perso = editeur.perso
		for event in pygame.event.get():
			widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
			if event.type == QUIT: #si clic sur croix rouge
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
				if event.unicode == "a":
					perso.action()

			if event.type == KEYUP:
				''' L'event KEYUP ne donne pas de traduction unicode. J'utilise donc un dic fait maison '''
				if key_trad["d"] == event.key or key_trad["q"] == event.key:
					perso.vx = 0
				if key_trad["z"] == event.key or key_trad["s"] == event.key:
					perso.vy = 0

		widget.update()
		objetEvent() # Evenements relatifs aux objets

	pygame.display.flip() # raffraichissement de la fenêtre

# ================================================================================================