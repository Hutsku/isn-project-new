# coding: utf-8

#========================================== IMPORT FICHIERS NECESSAIRES ================================================
import pygame
from pygame.locals import *

import config
import editeur.widget as widget
import objet
import dongeon
import hud

#========================================== IMPORT CONFIG =============================================================
config = config.getConfig() 

#========================================== CREATION DE LA FENETRE ====================================================
taille_ecran = config["taille_ecran"] #Dimension de la fenêtre / Largeurconfig["taille_ecran"] #Dimension de la fenêtre / Longueur


#========================================== CREATION DES DIFFERENTES INTERFACES =======================================
class Menu :
    """ Création et gestion des boutons du menu """
    def __init__(self, application) : 
        # noms des menus et commandes associées

        width = 200
        height = 50
        x = taille_ecran[0]/2 - (width/2)
        y = taille_ecran[1]/3 - (height/2)
        self.widg_jouer = widget.Button((x, y), size=(width, height), text="JOUER", action=application.jeu,  #bouton jouer
                font="Razer Regular", centered=True, police=24, bold=True, hoover_color=(0, 255, 0))
        self.widg_quitter = widget.Button((x, 2*y), size=(width, height), text="QUITTER", action=application.quitter, #bouton quitter
                font="Razer Regular", centered=True, police=24, bold=True, hoover_color=(255, 0, 0))

    def detruire(self) : #permet de supprimer les boutons
        self.widg_jouer.kill()
        self.widg_quitter.kill() 
 

class Game_over :
    """ Création et gestion des boutons du game over """
    def __init__(self, application, score) :

        for  widg in widget.Widget.group: #empeche les notifs de rester affichées
            widg.kill()
			
        score = str(score)
        width = 200
        height = 50
        x = taille_ecran[0]/2 - (width/2)
        y = taille_ecran[1]/3 - (height/2)
        self.widg_rejouer = widget.Button((x, y), size=(width, height), text="REJOUER", action=application.jeu, #bouton rejouer
                font="Razer Regular", centered=True, police=26, bold=True, hoover_color=(0, 255, 0))
        self.widg_menu = widget.Button((x, 2*y), size=(width, height), text="MENU", action=application.menu, #bouton menu
                font="Razer Regular", centered=True, police=26, bold=True, hoover_color=(255, 0, 0))
        self.widg_score = widget.Label((0.75*x,1.5*y), size=(2*width, height), text="Score de la partie: " + score, text_color = (200,200,200), font="Razer Regular", centered=True, police=26, bold=True, color = (0,0,0,0)) #affichage score


    def detruire(self) : #permet de supprimer boutons et texte
        self.widg_rejouer.kill()
        self.widg_menu.kill()
        self.widg_score.kill()
		
		
class Jeu:
    def __init__(self, application):
        taille_ecran = config["taille_ecran"]
        taille_HUD = config["taille_HUD"]
        taille_personnage = config["taille_personnage"]

        self.environnement = dongeon.Dongeon() # on initialise le dongeon (1 seul possible)
        self.spawn = self.environnement.get_spawn() #recuperation du spawn
        self.perso = objet.Personnage(self.spawn, (taille_personnage, taille_personnage)) #creation du personnage
        self.hud = hud.Hud() #creation de l'hud
		
		
    def detruire(self):
        ''' Efface tout les sprite de la fenêtre '''
        for sprite in objet.Objet.liste:
            sprite.kill()
            self.hud.kill()
			
class Application :
    """ Classe maîtresse gérant les différentes interfaces et menu du jeu """
	
    def __init__(self) :
        self._menu = False
        self._jeu = False
        self._quitter = False
        self._game_over = False
        self.ecran = None
 
    def start(self): #permet de lancer le menu
        self.menu()

    def quitter(self): #permet l'erret total et la fermeture du programme
        self._quitter = True

    def menu(self) :
        ''' Permet l'affichage du menu '''
        if self.ecran:
            self.ecran.detruire()
        self.ecran = Menu(self)
        self._menu = True
        self._jeu = False
        self._game_over= False

    def jeu(self):
        ''' Permet l'affichage du jeu '''
        if self.ecran:
            self.ecran.detruire()
        self.ecran = Jeu(self)
        self._jeu = True
        self._menu = False
        self._game_over = False
	
    def game_over(self, score):
        ''' Permet l'affichage du game over '''
        if self.ecran:
            self.ecran.detruire()
            self.ecran = Game_over(self, score)
        self._jeu = False
        self._menu = False
        self._game_over = True

#==================================================================================================
""" permettent de verifier le statut actuel des interfaces (la quelle est lancée) """
	
def check_statut_quitter(application): 
    return application._quitter
    
def check_statut_menu(application):
    return application._menu

def check_statut_jeu(application):
    return application._jeu

def check_statut_game_over(application):
    return application._game_over

#==================================================================================================
""" permettent d'obtenir des infos sur des elements """

def get_perso(application):
    return application.ecran.perso

def get_dongeon(application):
	return application.ecran.environnement
