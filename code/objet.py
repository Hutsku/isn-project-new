import pygame
from pygame.locals import *


		
# ======================================================== CLASSE MERE ==================================================

class Objet(pygame.sprite.Sprite):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__()
		Objet.liste.add(self)

		self.image = pygame.Surface(dimension)
		self.rect = self.image.get_rect()
		self.rect.topleft = position

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


class Personnage(Character):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Personnage.liste.add(self)

		self.speed = 1
		self.image.fill((255, 0, 0))

	def gauche(self):
		self.vx = -1

	def droite(self):
		self.vx = 1

	def bas(self):
		self.vy = 1

	def haut(self):
		self.vy = -1

# =============================================== OBJET IMMOBILE ========================================================

class Mur(Objet):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Mur.liste.add(self)

		self.image = pygame.image.load("../image/mur.png")
		self.image = pygame.transform.scale(self.image, dimension)


class Sol(Objet):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Sol.liste.add(self)

		self.image = pygame.image.load("../image/sol.png")
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

		self.image.fill((0, 200, 200))
		self.cible = cible
		self.statut = False

		self.hitbox = self.rect.copy()	

	def action(self, cible=None):
		self.statut =  not self.statut

		if type(self.cible) == type([]):
			for cible in self.cible:
				cible.action()
		elif self.cible:
			self.cible.action()


class PorteInterrupteur(Porte):
	''' Porte qui s'ouvre à l'aide d'un interrupteur '''
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension, interrupteur=None):
		super().__init__(position, dimension)
		PorteInterrupteur.liste.add(self)

		self.image.fill((0, 200, 0))
		self.interrupteur = interrupteur

	def action(self, cible=None):
		''' Ouvre ou ferme la porte'''
		if type(self.interrupteur) == type([]): # Si on a plusieurs interrupteurs ....
			all_activated = True
			for interrupteur in self.interrupteur:
				if not interrupteur.statut:
					all_activated = False

			if all_activated: # on regarde si ils sont tous activés et on ouvre la porte
				self.statut = True
			else:
				self.statut = False
				
		elif self.interrupteur:
			if self.interrupteur: # si l'interrupteur est activé, on ouvre la porte
				self.statut = True
			else:
				self.statut = False
		

# ===================================================== AUTRES ========================================================

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

		self.image = pygame.image.load("../image/fin.png")
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

def hitbox(groupe=None):
	''' On check si les hitbox des sprites interragissent avec certains objets 
		Hitbox d'attaque, projectile, pic au sol, etc. '''
	if not groupe:
		groupe = Sol.liste # par défaut on vérifie les hitbox au sol type pic etc.

	for objet in groupe:
		if objet.hitbox: # si l'objet a une hitbox active ...
			liste_collide = collide(objet.hitbox, groupe=Character.liste) # bug étrange avec "all"
			if liste_collide:
				if objet in liste_collide:
					liste_collide.remove(objet) # on enlève l'objet lui même de la liste des sprite touchés ...
				if liste_collide:
					objet.action(liste_collide) # on appel la fonction d'action de l'objet, avec les cibles en arguments

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