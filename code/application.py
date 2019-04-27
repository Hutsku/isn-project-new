#On Importe les bibliothèques nécessaires
import pygame
from pygame.locals import *

import config
import editeur.widget as widget
import hud
import objet
import dongeon

#Création de la fenêtre
config = config.getConfig() 
taille_ecran = config["taille_ecran"] #Dimension de la fenêtre / Largeurconfig["taille_ecran"] #Dimension de la fenêtre / Longueur

class Menu :
    """ Création et gestion des boutons d'un menu """
    def __init__(self, application) : 
        # noms des menus et commandes associées

        width = 200
        height = 50
        x = taille_ecran[0]/2 - (width/2)
        y = taille_ecran[1]/3 - (height/2)
        self.widg_jouer = widget.Button((x, y), size=(width, height), text="JOUER", action=application.jeu, 
                font="Razer Regular", centered=True, police=26, bold=True, hoover_color=(0, 255, 0))
        self.widg_quitter = widget.Button((x, 2*y), size=(width, height), text="QUITTER", action=application.quitter, 
                font="Razer Regular", centered=True, police=26, bold=True, hoover_color=(255, 0, 0))

    def detruire(self) :
        self.widg_jouer.kill()
        self.widg_quitter.kill() 
 

'''class Transition :
    """ Simulation de l'interface du jeu """
    def __init__(self, application) :
        from itertools import cycle
        couleurs = [(0, i, 0) for i in range(0, 255, 15)]
        couleurs.extend(sorted(couleurs[1:-1], reverse=True))
        self._couleurTexte = cycle(couleurs)
 
        self._font = pygame.font.SysFont('arial', 40, bold=True, italic=False)
        self.creerTexte()
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (surfaceW/2, surfaceH/2)

        # Création d'un event
        self._CLIGNOTER = pygame.USEREVENT + 1
        pygame.time.set_timer(self._CLIGNOTER, 60)
 
    def creerTexte(self) :
        self.texte = self._font.render('JEU EN COURS', True, next(self._couleurTexte))
 
    def update(self, events) :
        self._fenetre.blit(self.texte, self.rectTexte)
        for event in events :
            if event.type == self._CLIGNOTER :
                self.creerTexte()
 
    def detruire(self) :
        pygame.time.set_timer(self._CLIGNOTER, 0) # désactivation du timer

'''
class Jeu:
    def __init__(self, application):
        taille_ecran = config["taille_ecran"]
        taille_HUD = config["taille_HUD"]
        taille_personnage = config["taille_personnage"]

        self.environnement = dongeon.Dongeon() # on initialise le dongeon (1 seul possible)
        self.spawn = self.environnement.get_spawn()

        self.perso = objet.Personnage(self.spawn, (taille_personnage, taille_personnage)) # on crée le personnage au spawn du niveau
        self.perso.image.fill((255, 0, 0)) # attribution de la couleur personnage

    def detruire(self):
        ''' Efface tout les sprite de la fenêtre '''
        for sprite in objet.Objet.liste:
            sprite.kill()
 

class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self) :
        self._menu = False
        self._jeu = False
        self._quitter = False
        self._transition = False
        self.ecran = None
 
    def start(self):
        self.menu()

    def quitter(self):
        self._quitter = True

    def menu(self) :
        ''' Affichage du menu '''
        pygame.display.set_caption("MENU DU JEU")
        if self.ecran:
            self.ecran.detruire()
        self.ecran = Menu(self)
        self._menu = True
        self._jeu = False

    def jeu(self):
        pygame.display.set_caption("JEU EN COURS")
        if self.ecran:
            self.ecran.detruire()
        self.ecran = Jeu(self)
        self._jeu = True
        self._menu = False


def check_statut_quitter(application):
    return application._quitter
    
def check_statut_menu(application):
    return application._menu

def check_statut_jeu(application):
    return application._jeu

def check_statut_transition(application):
    return application._transition

def get_perso(application):
    return application.ecran.perso

def get_dongeon(application):
    return application.ecran.environnement

