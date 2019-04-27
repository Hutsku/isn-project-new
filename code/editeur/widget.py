
import pygame
from pygame.locals import *
import time

def update():
	Widget.group.update()

def event(event):
	for widget in Widget.group:
		widget.event(event)

def return_key_name_unicode(event):
        return pygame.key.name(event.key), event.unicode

class Widget(pygame.sprite.Sprite):
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
		self.image = pygame.Surface(self.size).convert_alpha()
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()

	def update(self):
		# Met à jour l'affichage du Widget
		self._build()

		if self.frame:
			self.frame.image.blit(self.image, self.rect)
		else:
			pygame.display.get_surface().blit(self.image, self.rect)

	def event(self, event):
		# S'occupe de la gestion des evenements pygame, comme la souris par exemple.
		# Inutile par défaut sur les widget (sauf cas speciaux type boutons).
		pass

	def set_pos(self, pos_x, pos_y):
		self.rect.center = (pos_x, pos_y)

	def resize(self, size):
		self.image = pygame.transform.scale(self.image, size)
		self.size = size
		self.rect = self.image.get_rect(center=self.rect.center)


class Label(Widget):
	def __init__(self, position, size=(100, 30), color = [255, 255, 255], border = 0, border_color = [0, 0, 0], text = "", text_color = [0, 0, 0],
	             centered = False, font = "arial", police = 14, adapt=False, frame=None, bold=False, hoover_color=None):

		super().__init__(position, size, frame)
		self.text = text
		self.font = font
		self.police = police
		self.adapt = adapt
		self.bold = bold

		self.border = border
		self.border_color = border_color
		self.color = color
		self.text_color = text_color
		self.centered = centered
		self._indent = 10
		self.hoover_color = hoover_color
		self._hoover = False

		self._build()

	def _build(self):
		# On remplit la couleur de fond
		if self._hoover:
			self.image.fill(self.hoover_color) 
		else:
			self.image.fill(self.color)

		# On initialise le texte
		font = pygame.font.SysFont(self.font, self.police, bold=self.bold, italic=False)

		if self.adapt:
			self.rect.width = font.size(self.text)[0] + 2*self._indent
			self.resize((self.rect.width, self.rect.height))

		# On créer un rect de reference (sans les positions)
		rect = self.rect.copy() 
		rect.x, rect.y = 0, 0

		if self.border:
			border = pygame.draw.rect(self.image, self.border_color, rect, self.border)

		if self.text:
			obj_text = font.render(self.text, False, self.text_color)
			if self.centered:
				textpos = obj_text.get_rect(centerx = self.rect.width/2, centery = self.rect.height/2)
			else:
				textpos = obj_text.get_rect(x = self._indent, centery = self.rect.height/2)

			# Une fois les paramètres appliqués, on colle le texte.
			self.image.blit(obj_text, textpos)

	def event(self, event):
		if self.hoover_color:
			rect = self.rect.copy()
			if self.frame:
				rect.x += self.frame.rect.x
				rect.y += self.frame.rect.y
			if rect.collidepoint(pygame.mouse.get_pos()):
				self._hoover = True
			else:
				self._hoover = False


class Image(Widget):
	def __init__(self, position, size=(100, 100), foreground = [0, 0, 0, 0], border = 0, border_color = [0, 0, 0], path = "", 
				frame=None, image=None):

		super().__init__(position, size, frame) # On met une dimension par défaut qui changera après de toute façon

		self.border = border
		self.border_color = border_color
		self.foreground = foreground
		self.size = size
		self.path = path
		self.image = image

		self._build()

	def _build(self):
		# On affiche l'image
		if self.path: 
			self.image = pygame.image.load(self.path).convert_alpha()

		self.image = pygame.transform.scale(self.image, self.size)
		self.rect = self.image.get_rect(center=self.rect.center)

		# On créer un rect de reference (sans les positions)
		rect = self.rect.copy() 
		rect.x, rect.y = 0, 0

		if self.border:
			border = pygame.draw.rect(self.image, self.border_color, rect, self.border)


class Button(Label):
	def __init__(self, position, size=(100, 30), border = 0, border_color = [0, 0, 0], color = [255, 255, 255], text = "", text_color = [0, 0, 0],
	 			centered = False, font = "arial", police = 14, adapt=False, action = None, frame=None, bold=False, hoover_color=None):

		super().__init__(position, size, color=color, border=border, border_color=border_color, text=text, text_color=text_color,
					centered=centered, font=font, police=police, adapt=adapt, frame=frame, bold=bold, hoover_color=hoover_color)

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
				if self.action:
					self.action()


class ImageButton(Image):
	def __init__(self, position, size=(100, 100), path = "", border = 0, border_color = [0, 0, 0], foreground = [255, 255, 255], 
				action = None, frame=None, image=None):

		super().__init__(position, size=size, foreground=foreground, border=border, border_color=border_color, path=path, 
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
				if self.action:
					self.action()


class Entry(Label):
	def __init__(self, position, size=(100, 30), text = "", border = 0, border_color = [0, 0, 0], foreground = [255, 255, 255], text_color = [0, 0, 0], 
    			font = "arial", police = 14, adapt=False, limit_character=None, frame=None):

		super().__init__(position, size, foreground=foreground, border=border, border_color=border_color, text=text, text_color=text_color,
				centered=None, font=font, police=police, adapt=adapt, frame=frame)

		self.unicode = True
		self._time = time.time()
		self._state_cursor = False
		self.delay = 0.5
		self.cursor = "|"
		self._focus = False # Définit si le widget à le "focus" ou non

		if not limit_character:
			self.limit_character = round(self.rect.width/9)
		else:
			self.limit_character = limit_character

		self._build()

	def _build(self):
		# On remplit la couleur de fond
		self.image.fill(self.foreground) 

		# On initialise le texte
		font = pygame.font.SysFont(self.font, self.police, bold=False, italic=False)

		if self.adapt:
			self.rect.width = font.size(self.text)[0] + 2*self._indent
			self.resize((self.rect.width, self.rect.height))

		# On créer un rect de reference (sans les positions)
		rect = self.rect.copy() 
		rect.x, rect.y = 0, 0

		if self.border:
			border = pygame.draw.rect(self.image, self.border_color, rect, self.border)

		if self.text:
			obj_text = font.render(self.text, False, self.text_color)
			if self.centered:
				textpos = obj_text.get_rect(centerx = self.rect.width/2, centery = self.rect.height/2)
			else:
				textpos = obj_text.get_rect(x = self._indent, centery = self.rect.height/2)

			# Une fois les paramètres appliqués, on colle le texte.
			self.image.blit(obj_text, textpos)

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
				print("entry")
				self._focus = True
			else:
				self._focus = False

	def update(self):
		text = self.text

		self._build()
		self.verify_delay_cursor() # On update le curseur

		# On initialise le texte à afficher (avec le curseur)
		font = pygame.font.SysFont(self.font, self.police, bold=False, italic=False)
		if not self._state_cursor:
			obj_text = font.render(self.text, False, self.text_color)
		else:
			obj_text = font.render(self.text+self.cursor, False, self.text_color)

		textpos = obj_text.get_rect(x = self._indent, centery = self.rect.height/2)
		self.image.blit(obj_text, textpos) # On applique le texte à l'image ...

		if self.frame:
			self.frame.image.blit(self.image, self.rect)
		else:
			pygame.display.get_surface().blit(self.image, self.rect)

	def print_key(self, key):
		if key == "\x08": # Pour la touche Delete
			self.text = self.text[:-1]
		elif key == "\r": # Pour la touche Enter
			pass
		else:
			self.text += key

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


class Frame(Widget):
	group = pygame.sprite.Group()

	def __init__(self, position, size, frame=None, border=0, border_color=(0, 0, 0), color=(255, 255, 255)):
		# Call the parent class (Widget) constructor
		super().__init__(position, size, frame)
		Frame.group.add(self)

		self.border = border
		self.border_color = border_color
		self.color = color

		self.image.fill(self.color)

	def _build(self): 
		if self.border:
			rect = self.rect.copy() 
			rect.x, rect.y = 0, 0
			border = pygame.draw.rect(self.image, self.border_color, rect, self.border)