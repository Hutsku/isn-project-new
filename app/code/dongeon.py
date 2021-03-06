# coding: utf-8

#========================================== IMPORT FICHIERS NECESSAIRES ================================================
import pygame
from pygame.locals import *
import os
import random
import json

import objet
import config

#========================================== FONCTION CHECK ==============================================================

def check_fin_niveau(dongeon_actuel): #verifie si c'est la fin du niveau
	for escalier in objet.Escalier.liste: #verifie si le perso est sur l'un des escalier de la liste
		if escalier.statut:
			dongeon_actuel.change_level()
		
#========================================== DONJON JOUER ================================================================
class Dongeon ():
	def __init__(self):
		self.lien_dossier = "../niveau/" #lien vers le fichier de sauvegarde
		self.nombre_lvl = -1 #nombre de niveau traversé (-1 important!)
		self.niveau = None # aucun niveau par défaut
		self.liste_lvl = [] # Liste des niveaux
		self.liste_niveau() # créé une liste
		self.change_level() # Choisi un niveau aléatoirement

		self.timer = config.getConfig()["temps"] #recupere le temps d'une partie


	def liste_niveau(self) : #permet de lister tous les niveau
		(path, dirs, filenames) = next(os.walk(self.lien_dossier)) #liste tout les niveaux present
		self.liste_lvl = filenames #enregistre la liste
		
	def change_timer(self, temps):
		'''fonction pour modifier le temps'''
		self.timer += temps #modifie le temps
		return self.timer #renvois le temps
		
	def build(self):
		'''Construit les murs et objets d'après les coordonnées du niveau'''
		taille_case = config.getConfig()["taille_case"] #recupere le nombre de case
		taille_personnage = config.getConfig()["taille_personnage"] #recupere la taille du perso jouable
		spawn = (self.niveau.spawn[0]*taille_case, self.niveau.spawn[1]*taille_case) #definie le lieu de spawn

		''' Construit les éléments du niveaux'''
		x=0
		for a in self.niveau.coord["terrain"]:
			y=0
			for case in self.niveau.coord["terrain"][x]:
				position = (x*taille_case, y*taille_case)
				type_case = case["type"]
				if type_case == "mur":
					objet.Mur(position, (taille_case, taille_case))
				elif type_case == "eau":
					objet.Eau(position, (taille_case, taille_case))
				elif type_case == "vide":
					objet.Vide(position, (taille_case, taille_case))
				elif type_case == "sol":
					objet.Sol(position, (taille_case, taille_case))
				elif type_case == "fin":
					objet.Escalier(position, (taille_case, taille_case))
				elif type_case == "spawn":
					objet.Sol(position, (taille_case, taille_case))
				elif type_case == "porte":
					objet.PorteInterrupteur(position, (taille_case, taille_case), interrupteur=case["cible"])
				elif type_case == "interrupteur":
					objet.Interrupteur(position, (taille_case, taille_case), cible=case["cible"])
				elif type_case == "interrupteur timer":
					objet.InterrupteurTimer(position, (taille_case, taille_case), cible=case["cible"])
				elif type_case == "pic":
					objet.Pic(position, (taille_case, taille_case))
				elif type_case == "pic intervalle":
					objet.PicIntervalle(position, (taille_case, taille_case))
				elif type_case == "pic interrupteur":
					objet.PicInterrupteur(position, (taille_case, taille_case), interrupteur=case["cible"])
				elif type_case == "lave":
					objet.Lave(position, (taille_case, taille_case))
				elif type_case == "bonus":
					objet.Bonus(position, (taille_case, taille_case))

				y += 1 #passe a la ligne suivante
			x += 1 #passe a la colonne suivante

		''' On va rechercher et ajouter les cible à leur mecanisme (l'objet lui-même, pas les coordonnées) '''
		for porte in objet.PorteInterrupteur.liste: #pour les porte a interrupteur
			list_cible = []
			for (cible_x, cible_y) in porte.interrupteur:
				position_cible = (cible_x*taille_case, cible_y*taille_case)
				for interrupteur in objet.Interrupteur.liste:
					if interrupteur.rect.topleft == position_cible:
						list_cible.append(interrupteur)
			porte.interrupteur = list_cible

		for pic in objet.PicInterrupteur.liste: #pour les pics a interrupteur
			list_cible = []
			for (cible_x, cible_y) in pic.interrupteur:
				position_cible = (cible_x*taille_case, cible_y*taille_case)
				for interrupteur in objet.Interrupteur.liste:
					if interrupteur.rect.topleft == position_cible:
						list_cible.append(interrupteur)
			pic.interrupteur = list_cible

		for interrupteur in objet.Interrupteur.liste: #pour les interrupteur
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
		'''renvoit le nombre de niveau parcouru'''
		return self.nombre_lvl
	
	def get_temps(self):
		'''renvoit le temps actuelle'''
		return self.timer
		
	# ================================== PARAMETRE NIVEAU ============================

	def change_level(self, lien_niveau=""):
		''' Change le niveau du dongeon '''
		if lien_niveau: # Si un niveau est passé en paramètre, on met celui-ci ... (debug)
			self.niveau = Niveau(lien_niveau)

		
		else: # ... sinon c'est automatique			
			
			if self.niveau: # si il y a déjà un niveau avant ...
				niveau_actuel = self.niveau.lien_lvl.split("/")[-1] # on recupère le nom du level et on l'arrange
				self.liste_lvl.remove(niveau_actuel) # on enlève de la liste le niveau actuel (pour eviter de le jouer 2 fois de suite)
				
			if not self.liste_lvl: #si la liste de niveau est vide
				self.liste_niveau() #creation d'une liste
			

			fichier = random.choice(self.liste_lvl) #on choisit au hasard
			self.niveau = Niveau(self.lien_dossier+fichier)	#on créer le niveau.		
				
		self.effacer() # Puis on efface le précedant ...
		self.build() # ... et on construit le nouveau.
		self.nombre_lvl += 1 #ajout d'un niveau au score
		print(str(fichier))
		
class Niveau ():
	'''permet la sauvegarde de differents parametre niveau'''
	def __init__(self, lien):
		self.lien_lvl = lien #lien du niveau
		self.spawn = None #coordonnées du spawn du niveau
		self.coord = {"terrain": []} #coordonnées de tous les elements
		
		self.build() #lance la création
		
	def build (self):
		with open(self.lien_lvl, "r") as fichier: # on ouvre le fichier du lien
			json_dic = fichier.read()
			dic = json.loads(json_dic)

			self.spawn = dic["spawn"]
			self.coord["terrain"] = dic["terrain"]
	

	
