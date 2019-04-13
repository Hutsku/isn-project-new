import pygame
from pygame.locals import *

def update():
	for objet in Mur.liste_objet:
		objet.update()

		
	for objet in Escalier.liste_objet:
		objet.update()
		
	for objet in Personnage.liste_objet:
		objet.update()

def evenement():
	pass
		
class Personnage (pygame.sprite.Sprite):
		liste_objet = pygame.sprite.Group()
		def __init__(self, position, dimension):
			pygame.sprite.Sprite.__init__(self)
			Personnage.liste_objet.add(self)
			
			self.image = pygame.Surface(dimension) # on affiche un carre (50x50px)
			self.image.fill((255, 0, 0)) # on colorie en rouge le carre
			
			self.rect = self.image.get_rect()
			self.rect.topleft = position
			
		def deplacement(self, x, y):

			perso_fantome = pygame.sprite.Sprite() # On crée un "double" du personnage (qui ne s'affiche pas)
			perso_fantome.rect = self.rect.copy()
			
			perso_fantome.rect.x += x # on déplace le fantome
			perso_fantome.rect.y += y
			
			# Test avec un mur
			reponse = pygame.sprite.spritecollideany(perso_fantome, Mur.liste_objet) # On verfie si il y a collision entre le perso et un mur
			
			if reponse == None: # si il n'y a pas collision
				self.rect.x += x # on déplace le fantome
				self.rect.y += y
				
			# Test avec Escalier
			reponse = pygame.sprite.spritecollideany(perso_fantome, Escalier.liste_objet) # On verfie si il y a collision entre le perso et un mur
			
			if reponse: # si on est sur l'escalier
				print("FIN DU NIVEAU")
			
		def gauche(self):
			self.deplacement(-1, 0)
		def droite(self):
			self.deplacement(1, 0)
		def bas(self):
			self.deplacement(0, 1)
		def haut(self):
			self.deplacement(0, -1)
			
		def update(self):
			pygame.display.get_surface().blit(self.image, self.rect)
			

class Mur (pygame.sprite.Sprite):
		liste_objet = pygame.sprite.Group()
		def __init__(self, position, dimension):
			pygame.sprite.Sprite.__init__(self)
			Mur.liste_objet.add(self)
			
			self.image = pygame.Surface(dimension) # on affiche un carre (50x50px)
			self.image.fill((0, 0, 0)) # on colorie en noir le mur
			
			self.rect = self.image.get_rect()
			self.rect.topleft = position
			
		def update(self):
			pygame.display.get_surface().blit(self.image, self.rect)
			
class Escalier (pygame.sprite.Sprite):
		liste_objet = pygame.sprite.Group()
		def __init__(self, position, dimension):
			pygame.sprite.Sprite.__init__(self)
			Escalier.liste_objet.add(self)
			
			self.image = pygame.Surface(dimension) # on affiche un carre (50x50px)
			self.image.fill((0, 0, 255)) # on colorie en bleu
			
			self.rect = self.image.get_rect()
			self.rect.topleft = position
			
		def update(self):
			pygame.display.get_surface().blit(self.image, self.rect)