import pygame
from pygame.locals import *

# ================================================== FONCTIONS GLOBALES ===============================================

def update():
	''' Affiche les sprites sur l'écran, selon l'ordre indiqué '''
	for objet in Mur.liste:
		objet.update()

	for objet in Sol.liste:
		objet.update()
		
	for objet in Character.liste:
		objet.update()

def move():
	''' Actualise la position des objets '''		
	for objet in Character.liste:
		objet.move()

def hitbox():
	''' On check si les hitbox des sprites interragissent avec certains objets 
		Hitbox d'attaque, projectile, pic au sol, etc. '''

	for objet in Sol.liste:
		if objet.hitbox: # si l'objet a une hitbox active ...
			liste_collide = collide(objet.hitbox, sprite_type="character") # bug étrange avec "all"
			if liste_collide:
				if objet in liste_collide:
					liste_collide.remove(objet) # on enlève l'objet lui même de la liste des sprite touchés ...
				if liste_collide:
					objet.action(liste_collide) # on appel la fonction d'action de l'objet, avec les cibles en arguments

def collide(rect, sprite_type="all"):
	''' Renvoit la liste des objets touchés par le rect '''
	objet = pygame.sprite.Sprite()
	objet.rect = rect

	# on limite le nombre de sprite à tester selon le type donné
	if sprite_type == "all":
		group = Objet.liste	
	elif sprite_type == "mur":
		group = Mur.liste
	elif sprite_type == "sol":
		group = Sol.liste
	elif sprite_type == "character":
		group = Character.liste
	else:
		return None

	''' il semble y avoir un bug étrange avec les groupes, conflit p-e ...'''

	reponse = pygame.sprite.spritecollideany(objet, group)
	if not type(reponse) == type([]) and reponse: # si un seul sprite est renvoyé, l'inclure dans une liste.
		return [reponse]
	else:
		return reponse
		
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

	def move(self):
		''' Actualise la position de l'objet, selon ses vecteurs de vitesse '''
		vx = self.vx * self.speed
		vy = self.vy * self.speed

		fantome = self.rect.copy()
		fantome.x += vx
		fantome.y += vy

		liste_collide = collide(fantome, sprite_type="mur") # Check des collisions
		if liste_collide:
			if self in liste_collide:
				liste_collide.remove(self) # on enlève l'objet lui même de la liste des sprite touché ...

		if not liste_collide:
			self.px += vx # on enregistre la position en float ...
			self.py += vy
			self.rect.center = (self.px, self.py) # ... convertit en int par le rect

	def action(self, cible):
		''' Enclenche une action contre une cible '''
		for objet in cible:
			print(objet+" touché !")


class Personnage(Character):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Personnage.liste.add(self)

		self.speed = 1

	def gauche(self):
		self.vx = -1

	def droite(self):
		self.vx = 1

	def bas(self):
		self.vy = 1

	def haut(self):
		self.vy = -1


# ======================================================= OBJET IMMOBILE ================================================

class Mur(Objet):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Mur.liste.add(self)

		self.image.fill((0, 0, 0))


class Sol(Objet):
	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Sol.liste.add(self)

class Escalier(Sol):

	liste = pygame.sprite.Group()
	def __init__(self, position, dimension):
		super().__init__(position, dimension)
		Escalier.liste.add(self)

		self.image.fill((0, 0, 255))
		self.hitbox = self.rect.copy()

	def action(self, cible):
		''' Met fin au niveau'''
		print("FIN DU NIVEAU")

		
		
		
		
		