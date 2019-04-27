#On Importe les bibliothèques nécessaires
import pygame
from pygame.locals import *

import config
import widget
import hud
import objet

#Création de la fenêtre
config = config.getConfig() 
surfaceW = config["taille_menux"] #Dimension de la fenêtre / Largeur
surfaceH = config["taille_menuy"] #Dimension de la fenêtre / Longueur

class Menu :
    """ Création et gestion des boutons d'un menu """
    def __init__(self, application) : 
        # noms des menus et commandes associées
        self.widg_jouer = widget.Button((500, 350), size=(200, 50), text="JOUER", action=application.jeu, font="Razer Regular")
        self.widg_quitter = widget.Button((500, 470), size=(200, 50), text="QUITTER", action=application.quitter, font="Razer Regular")
 
    def detruire(self) :
        self.widg_jouer.kill()
        self.widg_quitter.kill() 
 
class JeuOLD :
    """ Simulation de l'interface du jeu """
    def __init__(self, jeu, *groupes) :
        self._fenetre = jeu.fenetre
        jeu.fond = (0,)*3 
 
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
        self.texte = self._font.render(
            'JEU EN COURS',
			True, 
			next(self._couleurTexte))
 
    def update(self, events) :
        self._fenetre.blit(self.texte, self.rectTexte)
        for event in events :
            if event.type == self._CLIGNOTER :
                self.creerTexte()
                break
 
    def detruire(self) :
        pygame.time.set_timer(self._CLIGNOTER, 0) # désactivation du timer

class Jeu:
    def __init__(self, application):
        taille_ecran = config["taille_ecran"]
        taille_HUD = config["taille_HUD"]
        taille_personnage = config["taille_personnage"]

        self.environnement = dongeon.Dongeon() # on initialise le dongeon (1 seul possible)
        self.spawn = self.environnement.get_spawn()

        hud.hudfix() #creation de l'hud (qui n'a pas besoin d'update)

        self.perso = objet.Personnage(self.spawn, (taille_personnage, taille_personnage)) # on crée le personnage au spawn du niveau
        self.perso.image.fill((255, 0, 0)) # attribution de la couleur personnage

    def detruire(self):
        ''' Efface tout les sprite de la fenêtre '''
        for sprite in objet.Objet.liste:
            sprite.kill()
 
class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self) :
        self.menu = False
        self.jeu = False
        self.quitter = False
        self.ecran = None
 
    def start():
        self.menu()

    def menu(self) :
        ''' Affichage du menu '''
        pygame.display.set_caption("MENU DU JEU")
        if self.ecran:
            self.ecran.detruire()
        self.ecran = Menu(self)
        self.menu = True
        self.jeu = False

    def jeu():
        pygame.display.set_caption("JEU EN COURS")
        if self.ecran:
            self.ecran.detruire()
        self.ecran = Jeu(self)
        self.jeu = True
        self.menu = False

    def update(self) :
        events = pygame.event.get()
 
        for event in events :
            if event.type == pygame.QUIT :
                self.quitter()
                return
 
        self.fenetre.fill(self.fond)
        self.ecran.update(events)
        self.groupeGlobal.update()
        self.groupeGlobal.draw(self.fenetre)
        pygame.display.update()


def check_statut_quitter(application):
    return application.quitter
    
def check_statut_menu(application):
    return application.menu

def check_statut_jeu(application):
    return application.jeu

def get_perso(application):
    return application.ecran.perso

