import pygame
from pygame.locals import *

import config
import editeur.widget as widget
		
# ======================================================== CLASSE MERE ==================================================

class Objet(pygame.sprite.Sprite):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__()
		Objet.liste.add(self)

		self.image = pygame.Surface(dimension)
		self.rect = self.image.get_rect()
		self.rect.topleft = position
		self.size = dimension

		self.hitbox = None

	def update(self):
		''' Affiche le sprite sur l'écran '''
		pygame.display.get_surface().blit(self.image, self.rect)

# ======================================================= OBJET MOBILE ==================================================

class Character(Objet):
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

		self.hitbox = self.rect
		self.frame_invincibilite = 75 # nb de frame avant qu'une autre attaque puisse le toucher
		self._frame_time = 0 # False si le timer est reset, sinon ce sera le nb de frame qu'il reste 
		
		self.temp_degat = 0 #valeur temporaire de degat a l'instant t

	def move(self, coord=None):
		''' Actualise la position de l'objet, selon ses vecteurs de vitesse '''
		if coord:
			self.rect.topleft = coord
			(self.px, self.py) = coord
			
			return

		vx = self.vx * self.speed
		vy = self.vy * self.speed

		fantome = self.rect.copy()
		fantome.x += vx
		fantome.y += vy

		liste_collision_mur = collide(fantome, Mur.liste) # Check des collisions avec les murs.
		liste_collision_porte = collide(fantome, Porte.liste) # Check des collisions avec les portes.

		liste_collision_porte_ferme = []
		for porte in liste_collision_porte:
			if not porte.statut: # si la porte est fermée
				liste_collision_porte_ferme.append(porte) # Si une porte est fermée, on comptabilise la collision

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

		super().update()

	def degat(self, valeur):
		if not self._frame_time:
			print("DEGAT !")
			self.temp_degat = valeur
			self._frame_time = self.frame_invincibilite # on initialise le compteur
	
	def check_degat(self):
		degat = -self.temp_degat 
		self.temp_degat = 0	#reset les degat a 0
		return degat

class Personnage(Character):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Personnage.liste.add(self)

		self.speed = 3
		self.image.fill((255, 0, 0))

		self._notif = None

	def update(self):
		if self._notif:
			self._notif.rect.center = (self.rect.centerx, self.rect.y-20)

		super().update() # on appelle update() de Widget

	def notif(self, text):
		self._notif = widget.Label(self.rect.topleft, size=(200, 20), text=text, color=[0, 0, 0, 0], centered=True, bold=True)
		self._notif.rect.center = (self.rect.centerx, self.rect.y-20)

	def supp_notif(self):
		self._notif.kill()
		self._notif = None

	def gauche(self):
		self.vx = -1

	def droite(self):
		self.vx = 1

	def bas(self):
		self.vy = 1

	def haut(self):
		self.vy = -1

# =============================================== OBJET IMMOBILE ========================================================

class Sol(Objet):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Sol.liste.add(self)

		self.image = config.getImage("sol")
		self.image = pygame.transform.scale(self.image, dimension)

class Mur(Objet):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Mur.liste.add(self)

		self.image = config.getImage("mur")
		self.image = pygame.transform.scale(self.image, dimension)

class Eau(Mur):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Eau.liste.add(self)

		self.image = config.getImage("eau")
		self.image = pygame.transform.scale(self.image, dimension)

class Vide(Mur):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Vide.liste.add(self)

		self.image = config.getImage("vide")
		self.image = pygame.transform.scale(self.image, dimension)

# ================================================ PORTE / INTERRUPTEUR ==================================================

class Porte(Objet):
	''' Porte pouvant tour à tour être ouverte ou fermée '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Porte.liste.add(self)

		self.image.fill((0, 200, 0))
		self.statut = False # False => ferme

class Interrupteur(Objet):
	''' Interrupteur permettant d'activer un mecanisme / porte '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, cible=None):
		super().__init__(position, dimension)
		Interrupteur.liste.add(self)
		self.dimension = dimension
		self.statut = False

		self.image = config.getImage("interrupteur")
		self.image = pygame.transform.scale(self.image, dimension)

		self.cible = cible
		self.statut = False

		self.hitbox = self.rect.copy()	

	def action(self, cible=None):
		self.statut =  not self.statut

		if type(self.cible) == type([]):
			for cible in self.cible:
				cible.action()
				if self.statut:
					self.image = config.getImage("interrupteur on")
					self.image = pygame.transform.scale(self.image, self.dimension)
					self.statut = True
				if self.statut == False:
					self.image = config.getImage("interrupteur")
					self.image = pygame.transform.scale(self.image, self.dimension)
					self.statut = False
		elif self.cible:
			self.cible.action()
			self.image = config.getImage("interrupteur")
			self.image = pygame.transform.scale(self.image, self.dimension)

class InterrupteurTimer(Interrupteur):
	''' Interrupteur permettant d'activer un mecanisme / porte '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, cible=[]):
		super().__init__(position, dimension, cible=cible)
		InterrupteurTimer.liste.add(self)

		self.frame_activation = 500 # nb de frame de l'activation
		self._frame_time = 0 # timer

	def update(self):
		''' A chaque frame, on decroit le compteur si besoin '''
		if self._frame_time:
			self._frame_time -= 1
		elif self.statut:
			self.action()

		super().update()

	def action(self, cible=None):
		self.statut = not self.statut

		if type(self.cible) == type([]):
			for cible in self.cible:
				cible.action()
				if self.statut:
					self.image = config.getImage("interrupteur on")
					self.image = pygame.transform.scale(self.image, self.dimension)
					self.statut = True
					self._frame_time = self.frame_activation # On active le timer
				if not self.statut:
					self.image = config.getImage("interrupteur")
					self.image = pygame.transform.scale(self.image, self.dimension)
					self.statut = False
					self._frame_time = 0
		elif self.cible:
			if self.statut:
				self.image = config.getImage("interrupteur on")
				self.image = pygame.transform.scale(self.image, self.dimension)
				self.statut = True
				self._frame_time = self.frame_activation # On active le timer
			if not self.statut:
				self.image = config.getImage("interrupteur")
				self.image = pygame.transform.scale(self.image, self.dimension)
				self.statut = False
				self._frame_time = 0

class PorteInterrupteur(Porte):
	''' Porte qui s'ouvre à l'aide d'un interrupteur '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, interrupteur=[]):
		super().__init__(position, dimension)
		PorteInterrupteur.liste.add(self)

		self.image = config.getImage("porte")
		self.image = pygame.transform.scale(self.image, dimension)
		self.interrupteur = interrupteur

	def action(self, cible=None):
		''' Ouvre ou ferme la porte'''
		if type(self.interrupteur) == type([]): # Si on a plusieurs interrupteurs ....
			all_activated = True
			for interrupteur in self.interrupteur:
				if not interrupteur.statut:
					all_activated = False

			if all_activated: # on regarde si ils sont tous activés et on ouvre la porte
				if not self.statut:
					self.image = config.getImage("sol")
					self.image = pygame.transform.scale(self.image, self.size)
				self.statut = True
			else:
				if self.statut:
					self.image = config.getImage("porte")
					self.image = pygame.transform.scale(self.image, self.size)
				self.statut = False
				
		elif self.interrupteur:
			if self.interrupteur.statut: # si l'interrupteur est activé, on ouvre la porte
				self.statut = True
			else:
				self.statut = False
		
# ==================================================== PIEGES ===========================================================

class Pic(Sol):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Pic.liste.add(self)

		self.image = config.getImage("pic")
		self.image = pygame.transform.scale(self.image, dimension)
		self.hitbox = self.rect.copy()

		self.degat = 5 #met 5 de degat

	def action(self, cible):
		''' Inflige des dégats aux cibles'''
		if cible:
			for objet in cible:
				objet.degat(self.degat)

class PicInterrupteur(Pic):
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
				for interrupteur in self.interrupteur:
					if not interrupteur.statut:
						all_activated = False

				if all_activated: # on regarde si ils sont tous activés et on ouvre la porte
					self.image = config.getImage("pic off")
					self.image = pygame.transform.scale(self.image, self.size)
					self.hitbox = None
				else:
					self.image = config.getImage("pic")
					self.image = pygame.transform.scale(self.image, self.size)
					self.hitbox = self.rect.copy()
					
			elif self.interrupteur:
				if self.interrupteur.statut: # si l'interrupteur est activé, on ouvre la porte
					self.image = config.getImage("pic off")
					self.image = pygame.transform.scale(self.image, self.size)
					self.hitbox = None
				else:
					self.image = config.getImage("pic")
					self.image = pygame.transform.scale(self.image, self.size)
					self.hitbox = self.rect.copy()

		super().action(cible)

class PicIntervalle(Pic):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		PicIntervalle.liste.add(self)

		self.frame_activation = 200 # temps  de frame entre chaque état du pic
		self._frame_time = self.frame_activation # timer

	def update(self):
		''' A chaque frame, on decroit le compteur si besoin '''
		if self._frame_time:
			self._frame_time -= 1

		''' Quand timer à 0: On met à jour l'image et l'etat du pic '''
		if not self._frame_time:
			if self.hitbox:
				self.image = config.getImage("pic off")
				self.image = pygame.transform.scale(self.image, self.size)
				self.hitbox = None
			else:
				self.image = config.getImage("pic")
				self.image = pygame.transform.scale(self.image, self.size)
				self.hitbox = self.rect.copy()

			self._frame_time = self.frame_activation


		super().update()

class Lave(Pic):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Lave.liste.add(self)

		self.image = config.getImage("lave")
		self.image = pygame.transform.scale(self.image, dimension)
		self.hitbox = self.rect.copy()

		self.degat = 10 # Inflige 10 dégats

# ===================================================== AUTRES ==========================================================

class SolSpawn(Sol):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		SolSpawn.liste.add(self)

		self.image.fill((255, 0, 0))

class Escalier(Sol):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Escalier.liste.add(self)

		self.image = config.getImage("fin")
		self.image = pygame.transform.scale(self.image, dimension)
		self.hitbox = self.rect.copy()

		self.statut = False

	def action(self, cible):
		''' Met fin au niveau'''
		self.statut = True

# ================================================== FONCTIONS GLOBALES ===============================================

def update():
	''' Affiche les sprites sur l'écran, selon l'ordre indiqué '''
	for objet in Sol.liste:
		objet.update()

	for objet in Interrupteur.liste:
		objet.update()

	for objet in Mur.liste:
		objet.update()

	for objet in Porte.liste:
		objet.update()
		
	for objet in Character.liste:
		objet.update()

def move():
	''' Actualise la position des objets '''		
	for objet in Character.liste:
		objet.move()

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
				perso.notif("(A) Interragir")
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