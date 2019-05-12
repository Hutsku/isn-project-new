
import pygame
from pygame.locals import *
import time

def update(): #permet la mise a jour des widget
	Widget.group.update()

def event(event): #permet de faire les events de widget
	for widget in Widget.group:
		widget.event(event)

def return_key_name_unicode(event): #permet d'obtenir l'unicode d'une touche
        return pygame.key.name(event.key), event.unicode

class Widget(pygame.sprite.Sprite): #classe princiaple de widget
	group = pygame.sprite.Group()

	def __init__(self, position, size, frame=None):
		# Call the parent class (Sprite) constructor
		super().__init__()
		Widget.group.add(self)

		# Create the image object
		self.size = size
		self.image = pygame.Surface(size).convert_alpha()
		self.image.fill((255, 255, 255))

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values of rect.x and rect.y
		self.rect = self.image.get_rect()
		self.rect.topleft = position

		self.frame = frame

	def _build(self):
		self.rect = self.image.get_rect()

	def kill(self):
		if self.frame:
			self.frame._build()
		super().kill()

	def update(self):
		''' Met à jour l'affichage du Widget '''
		if self.frame:
			self.frame.image.blit(self.image, self.rect)
		else:
			pygame.display.get_surface().blit(self.image, self.rect)

	def event(self, event):
		# S'occupe de la gestion des evenements pygame, comme la souris par exemple.
		# Inutile par défaut sur les widget (sauf cas speciaux type boutons).
		pass

	def set_pos(self, pos_x, pos_y):
		self.rect.topleft = (pos_x, pos_y)

	def resize(self, size):
		self.image = pygame.transform.scale(self.image, size)
		self.size = size
		self.rect = self.image.get_rect(topleft=self.rect.topleft)


class Label(Widget): #pour du texte
	def __init__(self, position, size=(100, 30), color = [255, 255, 255], border = 0, border_color = [0, 0, 0], text = "", text_color = [0, 0, 0],
	             centered = False, font = "arial", police = 14, frame=None, bold=False, hoover_color=None):

		super().__init__(position, size, frame)
		self.text = text
		self.font = font
		self.police = police
		self.bold = bold
		self.text_color = text_color
		self._sys_font = pygame.font.SysFont(self.font, self.police, bold=self.bold, italic=False)
		self._obj_text = self._sys_font.render(self.text, True, self.text_color)

		self.border = border
		self.border_color = border_color
		self.color = color
		self.centered = centered
		self._indent = 10

		self.hoover_color = hoover_color
		if not self.hoover_color:
			self.hoover_color = self.color
		self._hoover = False
		self._current_color = self.color

		self._build()

	def _build(self):
		''' On change le fond '''
		if self._hoover:
			self._current_color = self.hoover_color
		else:
			self._current_color = self.color

		self.image.fill(self._current_color)

		''' On dessine les bords du cadre '''
		rect = self.rect.copy() 
		rect.x, rect.y = 0, 0

		pygame.draw.rect(self.image, self._current_color, rect, self.border)

		''' On affiche le texte '''
		if self.centered:
				textpos = self._obj_text.get_rect(centerx = self.rect.width/2, centery = self.rect.height/2)
		else:
			textpos = self._obj_text.get_rect(x = self._indent, centery = self.rect.height/2)

		self.image.blit(self._obj_text, textpos)

	def change_text(self, text=None, color=None, police=None, font=None, bold=None):
		''' Fonction permettant de changer le text du widget '''
		if not text:
			text=self.text
		if not color:
			color=self.text_color
		if not police:
			police=self.police
		if not font:
			font=self.font
		if not bold:
			bold=self.bold

		''' On recrée l'objet Font si besoin '''
		if font != self.font or bold != self.bold or police != self.police: # Si la police est changée ...
			self.font = font
			self.bold = bold
			self.police = police
			self._sys_font = pygame.font.SysFont(font, police, bold=bold, italic=False)

		''' On recrée l'objet Text si besoin '''
		if text != self.text or color != self.color:
			self.text = text
			self.text_color = color
			self._obj_text = self._sys_font.render(self.text, True, self.text_color)

		self._build()

	def change_border(self, color=None, border=None):
		''' Fonction permettant de modifier les bordures '''
		if not color:
			color=self.border_color
		if not border:
			border=self.border

		self.border = border
		self.border_color = color

		self._build()
		
	def change_color(self, color=None, hoover_color=None):
		if not color:
			color=self.color
		if not hoover_color:
			hoover_color=self.hoover_color

		self.color=color
		self.hoover_color=hoover_color
		if self._hoover:
			self._current_color = self.hoover_color
		else:
			self._current_color = self.color

		self._build()

	def event(self, event):
		if self.hoover_color:
			rect = self.rect.copy()
			if self.frame:
				rect.x += self.frame.rect.x
				rect.y += self.frame.rect.y
			if rect.collidepoint(pygame.mouse.get_pos()):
				self._hoover = True
				if not self._current_color == self.hoover_color:
					self.change_color()
			else:
				self._hoover = False
				if not self._current_color == self.color:
					self.change_color()


class Image(Widget): #pour une image
	def __init__(self, position, size=(100, 100), color = [0, 0, 0, 0], border = 0, border_color = [0, 0, 0], path = "", 
				frame=None, image=None):

		super().__init__(position, size, frame) # On met une dimension par défaut qui changera après de toute façon

		self.border = border
		self.border_color = border_color
		self.color = color
		self.size = size
		self.path = path
		self.image = image

		self._build()

	def _build(self):
		''' On affiche l'image '''
		if self.path: 
			self.image = pygame.image.load(self.path).convert_alpha()
			self.image = pygame.transform.scale(self.image, self.size)
		elif not self.image:
			self.image = pygame.Surface(self.size).convert_alpha()
			self.image.fill((0, 0, 0, 0))

		''' On dessine les bords du cadre '''
		if self.border:
			rect = self.rect.copy() 
			rect.x, rect.y = 0, 0
			pygame.draw.rect(self.image, self.border_color, rect, self.border)

	def change_border(self, color=None, border=None):
		''' Fonction permettant de modifier les bordures '''
		if not color:
			color=self.border_color
		if not border:
			border=self.border

		self.border = border
		self.border_color = color
		
		self._build()

	def change_image(self, path=None, image=None):
		if not path:
			path=self.path
		if not image:
			image=self.image

		self.path = path
		self.image = pygame.transform.scale(image, self.size)

		self._build()


class Button(Label): #pour un bouton
	def __init__(self, position, size=(100, 30), border = 0, border_color = [0, 0, 0], color = [255, 255, 255], text = "", text_color = [0, 0, 0],
	 			centered = False, font = "arial", police = 14, action = None, frame=None, bold=False, hoover_color=None):

		super().__init__(position, size, color=color, border=border, border_color=border_color, text=text, text_color=text_color,
					centered=centered, font=font, police=police, frame=frame, bold=bold, hoover_color=hoover_color)

		self.action = action

		self._build()

	def event(self, event):
		super().event(event) # on appelle la fonction event de Label
		if event.type == MOUSEBUTTONUP:
			rect = self.rect.copy()
			if self.frame:
				rect.x += self.frame.rect.x
				rect.y += self.frame.rect.y
			if rect.collidepoint(pygame.mouse.get_pos()):
				if type(self.action) ==  type((0, 0)): # si c'est un tuple en argument
					fonction = self.action[0] # Le premier element est la fonction
					arg = self.action[1] # Et le deuxième l'argument
					fonction(arg)
				elif self.action: # Si c'est une simple fonction ...
					self.action()


class ImageButton(Image): #pour un boutton image
	def __init__(self, position, size=(100, 100), path = "", border = 0, border_color = [0, 0, 0], color = [255, 255, 255], 
				action = None, frame=None, image=None):

		super().__init__(position, size=size, color=color, border=border, border_color=border_color, path=path, 
					frame=frame, image=image)

		self.action = action

		self._build()

	def event(self, event):
		if event.type == MOUSEBUTTONUP:
			rect = self.rect.copy()
			if self.frame:
				rect.x += self.frame.rect.x
				rect.y += self.frame.rect.y

			if rect.collidepoint(pygame.mouse.get_pos()):
				if type(self.action) ==  type((0, 0)): # si c'est un tuple en argument
					fonction = self.action[0] # Le premier element est la fonction
					arg = self.action[1] # Et le deuxième l'argument
					fonction(arg)
				elif self.action: # Si c'est une simple fonction ...
					self.action()


class Entry(Label): #pour un bouton a texte (a entrer)
	def __init__(self, position, size=(100, 30), text = "", border = 0, border_color = [0, 0, 0], color = [255, 255, 255], text_color = [0, 0, 0], 
    			font = "arial", police = 14, frame=None):

		super().__init__(position, size, color=color, border=border, border_color=border_color, text=text, text_color=text_color,
				centered=None, font=font, police=police, frame=frame)

		self.unicode = True
		self._time = time.time()
		self._state_cursor = False
		self.delay = 0.5
		self.cursor = "|"
		self._focus = False # Définit si le widget à le "focus" ou non

		self._build()

	def event(self, event):
		if event.type == KEYDOWN:
			key_name, key_unicode = return_key_name_unicode(event)
			if self._focus:
				if self.unicode:
					self.print_key(key_unicode)
				else:
					self.print_key(key_name)

		if event.type == MOUSEBUTTONUP:
			rect = self.rect.copy()
			if self.frame:
				rect.x += self.frame.rect.x
				rect.y += self.frame.rect.y

			if rect.collidepoint(pygame.mouse.get_pos()):
				self._focus = True
			else:
				if self._focus:
					self._build()
				self._focus = False

	def update(self):
		self.verify_delay_cursor() # On update le curseur

		# On initialise le texte à afficher (avec le curseur ou non)
		if self._focus:
			rect = self.rect.copy() 
			rect.x, rect.y = 0, 0
			pygame.draw.rect(self.image, (255, 0, 0), rect, 1)

		super().update()

	def print_key(self, key):
		if key == "\x08": # Pour la touche Delete
			self.change_text(text=self.text[:-1])
		elif key == "\r": # Pour la touche Enter
			pass
		else:
			self.change_text(text=self.text+key)

	def verify_delay_cursor(self):
		if self._focus:
			local_time = time.time()
			if local_time - self._time >= self.delay:
				if self._state_cursor:
					self._state_cursor = False
				else:
					self._state_cursor = True
				self._time = time.time()
		else:
			self._state_cursor = False


class Frame(Widget): #pour faire une uniforme
	group = pygame.sprite.Group()

	def __init__(self, position, size, frame=None, border=0, border_color=(0, 0, 0), color=(255, 255, 255)):
		# Call the parent class (Widget) constructor
		super().__init__(position, size, frame)
		Frame.group.add(self)

		self.border = border
		self.border_color = border_color
		self.color = color

		self._build()

	def _build(self): 
		self.image.fill(self.color)
		if self.border:
			rect = self.rect.copy() 
			rect.x, rect.y = 0, 0
			border = pygame.draw.rect(self.image, self.border_color, rect, self.border)