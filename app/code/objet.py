# coding: utf-8

import pygame
from pygame.locals import *

import config
import editeur.widget as widget
		
# /!\  ========================================= AVIS SUR LES COMMENTAIRES ======================================== /!\ 

''' Les classes se ressemblant beaucoup les une des autres et étant hierarchisées, les commentaires décrivant l'action 
des attrributs et fonctions ne se feront que dans la classe mère si possible '''

# ======================================================== CLASSE MERE ================================================

class Objet(pygame.sprite.Sprite):
	''' Classe basique pour chaque élément du jeu '''
	liste = pygame.sprite.Group() # Liste de toute les objets de cette classe
	def __init__(self, position, dimension):
		super().__init__()
		Objet.liste.add(self) # S'ajoute à la liste

		self.image = pygame.Surface(dimension) # image de l'objet
		self.rect = self.image.get_rect() # dimension de l'image
		self.rect.topleft = position # position de l'objet
		self.size = dimension # dimension de l'objet

		self.hitbox = None # Definie si l'objet doit avoir une hitbox

	def update(self):
		''' Affiche le sprite sur l'écran '''
		pygame.display.get_surface().blit(self.image, self.rect)

# ======================================================= OBJET MOBILE ================================================

class Character(Objet):
	'''Permet la creation d'un personnage qui bouge (jouable ou non)'''
	liste = pygame.sprite.Group()
	def __init__ (self, position, dimension):
		super().__init__(position, dimension)
		Character.liste.add(self)

		self.speed = 1 # Coef de vitesse

		# vecteur de position (float)
		self.px = position[0]
		self.py = position[1]
		# Vecteur de vitesse (déplacement)
		self.vx = 0
		self.vy = 0

		self.hitbox = self.rect # Sa hitbox correspond à sa taille
		self.frame_invincibilite = config.getConfig()["incinvibility"] # nb de frame avant qu'une autre attaque puisse le toucher
		self._frame_time = 0 # False si le timer est reset, sinon ce sera le nb de frame qu'il reste 
		
		self.temps_additionel = 0 # valeur temporaire de bonus ou malus de temps

	def move(self, coord=None):
		''' Actualise la position de l'objet, selon ses vecteurs de vitesse et sa position '''

		''' Si des positions sont données, alors on bouge simplement le personnage à la destination '''
		if coord:
			self.rect.topleft = coord
			(self.px, self.py) = coord
			return

		''' Sa vitesse effective correspond à la vitesse qui lui ai donnée et à ses vecteurs de vitesse '''
		vx = self.vx * self.speed
		vy = self.vy * self.speed

		''' On crée un "fantôme" à la destination cible '''
		fantome = self.rect.copy()
		fantome.x += vx
		fantome.y += vy

		liste_collision_mur = collide(fantome, Mur.liste) # Check des collisions avec les murs.
		liste_collision_porte = collide(fantome, Porte.liste) # Check des collisions avec les portes.

		liste_collision_porte_ferme = [] #creation de la liste des porte fermée
		for porte in liste_collision_porte:
			if not porte.statut: # si la porte est fermée
				liste_collision_porte_ferme.append(porte) # Si une porte est fermée, on comptabilise la collision

		''' Si le "fantôme" n'as pas de collision, on le remplace par le personnage '''
		if (not liste_collision_mur) and (not liste_collision_porte_ferme):
			self.px += vx # on enregistre la position en float ...
			self.py += vy
			self.rect.topleft = (self.px, self.py) # ... convertit en int par le rect

	def action(self, cible=None):
		''' Interagit avec une cible '''
		hitbox(groupe=Interrupteur.liste) # Interaction avec les interrupteurs

	def update(self):
		''' A chaque frame, on decroit le compteur si besoin '''
		if self._frame_time:
			self._frame_time -= 1

		super().update() # on appelle la fonction update de sa classe mère (ici Objet)

	def degat(self, valeur):
		''' Inflige un malus de temps '''
		if not self._frame_time:
			print("DEGAT !") #debug
			self.temps_additionel -= valeur
			self._frame_time = self.frame_invincibilite # on initialise le compteur d'invencibilité

	def bonus(self, valeur):
		''' Ajoute un bonus de temps '''
		print("BONUS !") #debug
		self.temps_additionel += valeur
	
	def check_temps_additionel(self):
		'''retourne les malus/bonus de temps total'''
		temps = self.temps_additionel
		self.temps_additionel = 0	# reset les bonus/malus à 0	
		return temps

class Personnage(Character):
	''' Permet la création d'un personnage controllable '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Personnage.liste.add(self)

		dim = dimension[1] #recupere la dimension du personnage 
		dim = int(dim) #transforme la dimension en nombre entier
		self.dimension = (dim, dim) # recree la dimension du personnage sous forme (x,y)
		self.speed = 3 #vitesse du personnage
		
		self.image_b = config.getImage("personnage b") #image du personnage
		self.image_b = pygame.transform.scale(self.image_b, self.dimension) #redimensionne l'image du personnage
		
		self.image_h = config.getImage("personnage h") #image du personnage
		self.image_h = pygame.transform.scale(self.image_h, self.dimension) #redimensionne l'image du personnage
		
		self.image_d = config.getImage("personnage d") #image du personnage
		self.image_d = pygame.transform.scale(self.image_d, self.dimension) #redimensionne l'image du personnage
		
		self.image_g = config.getImage("personnage g") #image du personnage
		self.image_g = pygame.transform.scale(self.image_g, self.dimension) #redimensionne l'image du personnage

		self.image = self.image_b
		
		self._notif = None # creation des futures notification pour le personnage

	def update(self):
		'''Permet l'affichege des notifs'''
		if self._notif:
			self._notif.rect.center = (self.rect.centerx, self.rect.y-20)

		super().update()

	def notif(self, text): 
		'''Crée le texte de notification'''
		self._notif = widget.Label(self.rect.topleft, size=(200, 20), text=text, color=[0, 0, 0, 0], centered=True, bold=True)
		self._notif.rect.center = (self.rect.centerx, self.rect.y-20)

	def supp_notif(self):
		'''Supprime le texte de notification'''
		self._notif.kill()
		self._notif = None

	def gauche(self):
		''' Permet de bouget vers la gauche'''
		self.vx = -1
		self.image = self.image_g

	def droite(self):
		''' Permet de bouget vers la droite'''
		self.vx = 1
		self.image = self.image_d

	def bas(self):
		''' Permet de bouget vers le bas'''
		self.vy = 1
		self.image = self.image_b

	def haut(self):
		''' Permet de bouget vers le haut'''
		self.vy = -1
		self.image = self.image_h

# =============================================== OBJET IMMOBILE ======================================================

class Sol(Objet):
	'''Creation des sols'''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Sol.liste.add(self)

		self.image = config.getImage("sol") #recuperation de l'image du sol
		self.image = pygame.transform.scale(self.image, dimension) #redimension de l'image

class Mur(Objet):
	'''Creation des murs'''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension): 
		super().__init__(position, dimension)
		Mur.liste.add(self)

		self.image = config.getImage("mur") #recuperation de l'image du mur
		self.image = pygame.transform.scale(self.image, dimension)#redimension de l'image

class Eau(Mur):
	''' Permet la création d'une case d'eau (infranchissable) '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Eau.liste.add(self)

		self.image = config.getImage("eau")
		self.image = pygame.transform.scale(self.image, dimension)

class Vide(Mur):
	''' Permet la création d'une case de vide (infranchissable) '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Vide.liste.add(self)

		self.image = config.getImage("vide")
		self.image = pygame.transform.scale(self.image, dimension)

# ================================================ PORTE / INTERRUPTEUR ===============================================

class Porte(Objet):
	''' Porte pouvant tour à tour être ouverte ou fermée '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Porte.liste.add(self)

		self.image.fill((0, 200, 0))
		self.statut = False # False => porte fermée

class Interrupteur(Objet):
	''' Interrupteur permettant d'activer un mecanisme / porte '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, cible=None):
		super().__init__(position, dimension)
		Interrupteur.liste.add(self)

		self.dimension = dimension

		self.image = config.getImage("interrupteur")
		self.image = pygame.transform.scale(self.image, dimension)

		self.cible = cible #permet de donner l'objet qu'il active
		self.statut = False #False => interrupteur non activé

		self.hitbox = self.rect.copy()

	def action(self, cible=None):
		'''Fait les action lié a son activation'''
		self.statut =  not self.statut

		''' Si on a une liste de cible ...'''
		if type(self.cible) == type([]): 
			for cible in self.cible:
				cible.action() #fait l'action de l'objet lié
				if self.statut:  # Image -> position on
					self.image = config.getImage("interrupteur on")
					self.image = pygame.transform.scale(self.image, self.dimension)
				if self.statut == False: # Image -> position off
					self.image = config.getImage("interrupteur")
					self.image = pygame.transform.scale(self.image, self.dimension)

		elif self.cible:
			self.cible.action()
			self.image = config.getImage("interrupteur") # Image -> position off
			self.image = pygame.transform.scale(self.image, self.dimension)

class InterrupteurTimer(Interrupteur):
	''' Interrupteur a temps permettant d'activer un mecanisme / porte '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, cible=[]):
		super().__init__(position, dimension, cible=cible)
		InterrupteurTimer.liste.add(self)

		self.frame_activation = 500 # nb de frame de l'activation
		self._frame_time = 0 # timer

	def update(self):
		''' A chaque frame, on decroit le compteur si besoin '''
		if self._frame_time:
			self._frame_time -= 1 #decroit le temps
		elif self.statut:
			self.action() #permet de faire l'action

		super().update()

	def action(self, cible=None):
		self.statut = not self.statut

		''' Si on a plusieurs cibles ...'''
		if type(self.cible) == type([]):
			for cible in self.cible:
				cible.action()
				if self.statut: # Image -> position on
					self.image = config.getImage("interrupteur on")
					self.image = pygame.transform.scale(self.image, self.dimension)
					self._frame_time = self.frame_activation # On active le timer
				if not self.statut: # Image -> position off
					self.image = config.getImage("interrupteur")
					self.image = pygame.transform.scale(self.image, self.dimension)
					self._frame_time = 0 # remise a 0 du timer

		elif self.cible:
			if self.statut: # Image -> position on
				self.image = config.getImage("interrupteur on")
				self.image = pygame.transform.scale(self.image, self.dimension)
				self._frame_time = self.frame_activation # On active le timer
			if not self.statut: # Image -> position off
				self.image = config.getImage("interrupteur")
				self.image = pygame.transform.scale(self.image, self.dimension)
				self._frame_time = 0#remise a 0 du timer

class PorteInterrupteur(Porte):
	''' Porte qui s'ouvre à l'aide d'un interrupteur '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, interrupteur=[]):
		super().__init__(position, dimension)
		PorteInterrupteur.liste.add(self)

		self.image = config.getImage("porte")
		self.image = pygame.transform.scale(self.image, dimension) 
		self.interrupteur = interrupteur #donnes les infos des interrupteurs liés

	def action(self, cible=None):
		''' Ouvre ou ferme la porte'''
		if type(self.interrupteur) == type([]): # Si on a plusieurs interrupteurs ....
			all_activated = True 
			for interrupteur in self.interrupteur: #si tout ne sont pas activé alors all_activated est faux
				if not interrupteur.statut:
					all_activated = False

			if all_activated: # on regarde s'ils sont tous activés et on ouvre la porte
				if not self.statut:# Image -> position ouverte
					self.image = config.getImage("sol") 
					self.image = pygame.transform.scale(self.image, self.size) 
				self.statut = True
			else: #sinon on la ferme
				if self.statut:  # Image -> position fermée
					self.image = config.getImage("porte") 
					self.image = pygame.transform.scale(self.image, self.size)
				self.statut = False

# ==================================================== PIEGES =========================================================

class Pic(Sol):
	'''pic traversable mais qui inflige des degats'''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Pic.liste.add(self)

		self.image = config.getImage("pic")
		self.image = pygame.transform.scale(self.image, dimension)
		self.hitbox = self.rect.copy()

		self.degat = config.getConfig()["degat_pics"] #definition des degats des pics

	def action(self, cible):
		''' Inflige des dégats aux cibles'''
		if cible:
			for objet in cible:
				objet.degat(self.degat)

class PicInterrupteur(Pic):
	''' Pics activable par un interrupteur '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, interrupteur=[]):
		super().__init__(position, dimension)
		PicInterrupteur.liste.add(self)

		self.interrupteur = interrupteur 

	def action(self, cible=None):
		''' Ouvre ou ferme les pics'''
		if not cible:
			if type(self.interrupteur) == type([]): # Si on a plusieurs interrupteurs ....
				all_activated = True
				for interrupteur in self.interrupteur: #si tout ne sont pas activé alors all_activated est faux
					if not interrupteur.statut:
						all_activated = False

				if all_activated: # on regarde s'ils sont tous activés et on desactive les pics
					self.image = config.getImage("pic off")
					self.image = pygame.transform.scale(self.image, self.size)
					self.hitbox = None #desactive la hitbox (pour plus avoir de degats)
				else:
					self.image = config.getImage("pic")
					self.image = pygame.transform.scale(self.image, self.size)
					self.hitbox = self.rect.copy() #reactive la hitbox
					
		super().action(cible)

class PicIntervalle(Pic):
	''' Pics s'enclanchant à intervalle regulier '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		PicIntervalle.liste.add(self)

		self.frame_activation = config.getConfig()["intervalle_pics"] # temps de frame entre chaque état du pic
		self._frame_time = self.frame_activation # timer d'activation

	def update(self):
		''' A chaque frame, on decroit le compteur si besoin '''
		if self._frame_time:
			self._frame_time -= 1

		''' Quand timer à 0: On met à jour l'image et l'etat du pic '''
		if not self._frame_time:
			if self.hitbox:
				self.image = config.getImage("pic off")
				self.image = pygame.transform.scale(self.image, self.size)
				self.hitbox = None #desactive la hitbox (pour plus avoir de degats)
			else:
				self.image = config.getImage("pic")
				self.image = pygame.transform.scale(self.image, self.size)
				self.hitbox = self.rect.copy() #reactive la hitbox

			self._frame_time = self.frame_activation #reset du timer


		super().update()

class Lave(Pic):
	'''creation de la lave traversable mais a degat (=pic)'''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Lave.liste.add(self)

		self.image = config.getImage("lave")
		self.image = pygame.transform.scale(self.image, dimension)
		self.hitbox = self.rect.copy()

		self.degat = config.getConfig()["degat_lave"]

# ===================================================== AUTRES ========================================================

class SolSpawn(Sol):
	'''case de spawn (editeur uniquement)'''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		SolSpawn.liste.add(self)

		self.image = config.getImage("spawn")
		self.image = pygame.transform.scale(self.image, dimension)

class Escalier(Sol):
	'''Case de fin de niveau'''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Escalier.liste.add(self)

		self.image = config.getImage("fin")
		self.image = pygame.transform.scale(self.image, dimension)
		self.hitbox = self.rect.copy()

		self.statut = False #True => fin du niveau

	def action(self, cible):
		''' Met fin au niveau'''
		self.statut = True

class Bonus(Sol):
	'''case de bonus de temps'''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Bonus.liste.add(self)

		self.image = config.getImage("bonus")
		self.image = pygame.transform.scale(self.image, dimension)
		self.hitbox = self.rect.copy()

		self.bonus = config.getConfig()["bonus"]

	def action(self, cible):
		''' Ajoute un bonus '''
		if cible:
			for objet in cible:
				objet.bonus(self.bonus)

			''' On fait ensuite "disparaître" le bonus '''
			self.hitbox = None
			self.image = pygame.transform.scale(config.getImage("sol"), self.size) #remplace par une case de sol

# ================================================== FONCTIONS GLOBALES ===============================================

def update():
	''' Affiche les sprites sur l'écran, selon l'ordre indiqué '''
	for objet in Sol.liste: #sols 
		objet.update()

	for objet in Interrupteur.liste: #tous les interupteurs
		objet.update()

	for objet in Mur.liste: #murs
		objet.update()

	for objet in Porte.liste: #toutes les portes
		objet.update()
		
	for objet in Bonus.liste: #bonus
		objet.update()	

	for objet in Character.liste: #tous les personnages (1 seul)
		objet.update()

def move():
	''' Actualise la position des objets '''		
	for objet in Character.liste:
		objet.move() # Lance la fonction move() de chaque objet

def hitbox(groupe=Sol.liste):
	''' On check si les hitbox des sprites interragissent avec certains objets 
		Hitbox d'attaque, projectile, pic au sol, etc. '''

	for objet in groupe:
		if objet.hitbox: # si l'objet a une hitbox active ...
			liste_collide = collide(objet.hitbox, groupe=Character.liste) # bug étrange avec "all"
			if liste_collide:
				if objet in liste_collide:
					liste_collide.remove(objet) # on enlève l'objet lui même de la liste des sprite touchés ...
				if liste_collide:
					objet.action(liste_collide) # on appel la fonction d'action de l'objet, avec les cibles en arguments

	for perso in Personnage.liste:
		''' Si il est bien sur un interrupteur et qu'il n'y a pas de notif ...'''
		if collide(perso.hitbox, groupe=Interrupteur.liste):
			if not perso._notif: 
				perso.notif("(spc) Interragir")
		elif perso._notif: # Si il y a deja une notif mais que le perso n'est plus dessus, on supprime
			perso.supp_notif()

def collide(rect, groupe=Objet.liste):
	''' Renvoit la liste des objets touchés par le rect '''
	objet = pygame.sprite.Sprite()
	objet.rect = rect

	''' il semble y avoir un bug étrange avec les groupes, conflit p-e ...'''

	reponse = pygame.sprite.spritecollideany(objet, groupe)
	if (not type(reponse) == type([])) and reponse: # si un seul sprite est renvoyé, l'inclure dans une liste.
		return [reponse]
	elif not reponse: # Si rien n'est donné, renvoyé une liste vide (qu'on puisse iterer sans erreurs)
		return []
	else:
		return reponse