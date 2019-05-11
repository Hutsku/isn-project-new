import pygame
from pygame.locals import *
import os
import random
import json

import objet
import config


def check_fin_niveau(dongeon_actuel):
	for escalier in objet.Escalier.liste:
		if escalier.statut:
			dongeon_actuel.change_level()
		

class Dongeon ():
	def __init__(self):
		self.lien_dossier = "../niveau/"
		self.nombre_lvl = -1 #nombre de niveau traversé	
		self.niveau = None # aucun niveau par défaut
		self.change_level() # Choisi un niveau aléatoirement
			
		self.timer = 30 #temps d'un partie (en seconde)

	def change_timer(self, temps):
		self.timer += temps
		return self.timer
		
	def build(self):
		'''construit les murs et objets d'après les coordonnées du niveau'''
		taille_case = config.getConfig()["taille_case"]
		taille_personnage = config.getConfig()["taille_personnage"]
		spawn = (self.niveau.spawn[0]*taille_case, self.niveau.spawn[1]*taille_case)

		x=0
		for a in self.niveau.coord["terrain"]:
			y=0
			for case in self.niveau.coord["terrain"][x]:
				position = (x*taille_case, y*taille_case)
				type_case = case["type"]
				if type_case == "mur":
					objet.Mur(position, (taille_case, taille_case))
				if type_case == "eau":
					objet.Eau(position, (taille_case, taille_case))
				if type_case == "vide":
					objet.Vide(position, (taille_case, taille_case))
				if type_case == "sol":
					objet.Sol(position, (taille_case, taille_case))
				if type_case == "fin":
					objet.Escalier(position, (taille_case, taille_case))
				if type_case == "spawn":
					objet.Sol(position, (taille_case, taille_case))
				if type_case == "porte":
					objet.PorteInterrupteur(position, (taille_case, taille_case), interrupteur=case["cible"])
				if type_case == "interrupteur":
					objet.Interrupteur(position, (taille_case, taille_case), cible=case["cible"])
				if type_case == "interrupteur timer":
					objet.InterrupteurTimer(position, (taille_case, taille_case), cible=case["cible"])
				if type_case == "pic":
					objet.Pic(position, (taille_case, taille_case))
				if type_case == "pic intervalle":
					objet.PicIntervalle(position, (taille_case, taille_case))
				if type_case == "pic interrupteur":
					objet.PicInterrupteur(position, (taille_case, taille_case), interrupteur=case["cible"])
				if type_case == "lave":
					objet.Lave(position, (taille_case, taille_case))
				y += 1
			x += 1

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

		''' On spawn le perso au bon endroit '''
		for perso in objet.Personnage.liste:
			perso.move(coord=spawn)
	
	def effacer(self):
		''' Détruit tout les objets présent sur le niveau (sauf le perso) '''
		for sprite in objet.Objet.liste:
			if not objet.Personnage.liste.has(sprite): # si le sprite n'est pas le perso, on le détruit
				sprite.kill()

	# ============================== FONCTION GET =====================================

	def get_spawn(self):
		''' Renvoit la position du spawn du personnage '''
		taille_case = config.getConfig()["taille_case"]
		return (self.niveau.spawn[0]*taille_case, self.niveau.spawn[1]*taille_case)

	def get_level(self):
		''' Renvoit le niveau actuel '''
		return self.niveau

	def get_nombre_de_lvl(self):
		return self.nombre_lvl
		print(self.nombre_lvl)
		
	# ================================== PARAMETRE NIVEAU ============================

	def change_level(self, lien_niveau=""):
		''' Change le niveau du dongeon '''
		if lien_niveau: # Si un niveau est passé en paramètre, on met celui-ci ...
			self.niveau = Niveau(lien_niveau)

		else: # ... sinon c'est automatique
			(path, dirs, filenames) = next(os.walk(self.lien_dossier)) # liste tout les niveaux présent ...
			
			if self.niveau: # si il y a déjà un niveau avant ...
				niveau_actuel = self.niveau.lien_lvl.split("/")[-1] # on recupère le nom du level et on l'arrange
				filenames.remove(niveau_actuel) # on enlève de la liste le niveau actuel

			fichier = random.choice(filenames)
			self.niveau = Niveau(self.lien_dossier+fichier)	# ... puis on en choisit un et on créer le niveau.		
				
		self.effacer() # Puis on efface le précedant ...
		self.build() # ... et on construit le nouveau.
		self.nombre_lvl += 1 #ajout d'un niveau
		
class Niveau ():
	def __init__(self, lien):
		self.lien_lvl = lien
		self.spawn = None
		self.coord = {"terrain": [], "objets": []}
		
		self.build()
		
	def build (self):
		with open(self.lien_lvl, "r") as fichier: # on ouvre le fichier du lien
			json_dic = fichier.read()
			dic = json.loads(json_dic)

			self.spawn = dic["spawn"]
			self.coord["terrain"] = dic["terrain"]
			self.coord["objets"] = dic["objets"]
	

	