# coding: utf-8

#========================================== IMPORT FICHIERS NECESSAIRES ================================================
import pygame
from pygame.locals import *
import os

import config
import editeur.widget as widget
import objet
import dongeon
import hud
import json

#========================================== IMPORT CONFIG =============================================================

dic_config = config.getConfig() 

#========================================== CREATION DE LA FENETRE ====================================================

taille_ecran = dic_config["taille_ecran"] #Dimension de la fenêtre / Largeurconfig["taille_ecran"] #Dimension de la fenêtre / Longueur

#========================================== CREATION DES DIFFERENTES INTERFACES =======================================

class Menu :
    """ Création et gestion des boutons du menu """
    def __init__(self, application) :

        ''' Destruction préventive des widget precedant (comme les notif) '''
        for  widg in widget.Widget.group:
            widg.kill()
			
        record_score = self.meilleur_score_menu()
        width = 200
        height = 50
        x = taille_ecran[0]/2 - (width/2)
        y = taille_ecran[1]/3 - (height/2)
        self.widg_jouer = widget.Button((x, y), size=(width, height), text="JOUER", action=application.jeu, 
                font="Razer Regular", centered=True, police=24, bold=True, hoover_color=(0, 255, 0)) # Bouton "JOUER"
        self.widg_quitter = widget.Button((x, 2*y), size=(width, height), text="QUITTER", action=application.quitter,
                font="Razer Regular", centered=True, police=24, bold=True, hoover_color=(255, 0, 0)) # Bouton "QUITTER"
        self.widg_record = widget.Label((x,1.5*y), size=(width, height), text="Meilleur score: " + record_score,
                text_color=(255,255,255), font="Razer Regular", centered=True, police=26, bold=True, color = (255,255,255,0)) # affichage du score

        fond = config.getImage("fond menu") # recuperation de l'image du fond menu
        fond = pygame.transform.scale(fond, taille_ecran) #redimension de l'image
        pygame.display.get_surface().blit(fond, (0, 0)) # on colle le fond
		
    def meilleur_score_menu(self):
        ''' Renvoit et remplace le nouveau record si besoin'''

        ''' Si le fichier existe ... sinon on le crée'''
        try:
            with open("../save.txt", "r") as fichier:
                ''' On lit le contenu de la save '''
                json_dic = fichier.read()
                dic = json.loads(json_dic)       
            return str(dic["record"]) # on renvoit le meilleur score

        except FileNotFoundError:
            return "0"

    def detruire(self) :
        ''' Efface le menu en détruisant les boutons '''
        self.widg_jouer.kill()
        self.widg_quitter.kill()
        self.widg_record.kill()
 
class Game_over :
    """ Création et gestion des boutons du game over """
    def __init__(self, application, score) :

        ''' Destruction préventive des widget precedant (comme les notif) '''
        for  widg in widget.Widget.group: 
            widg.kill()
			
        record_score = self.meilleur_score(score)
        score = str(score)

        width = 200
        height = 50
        x = taille_ecran[0]/2 - (width/2)
        y = taille_ecran[1]/3 - (height/2)
        self.widg_rejouer = widget.Button((x, y), size=(width, height), text="REJOUER", action=application.jeu,
                font="Razer Regular", centered=True, police=26, bold=True, hoover_color=(0, 255, 0)) # Bouton "REJOUER"
        self.widg_menu = widget.Button((x, 2*y), size=(width, height), text="MENU", action=application.menu, 
                font="Razer Regular", centered=True, police=26, bold=True, hoover_color=(255, 0, 0)) # Bouton "MENU"
        self.widg_score = widget.Label((0.75*x,1.4*y), size=(2*width, height), text="Score de la partie: " + score, 
                text_color = (200,200,200), font="Razer Regular", centered=True, police=26, bold=False, color = (0,0,0,0)) # affichage du score
        self.widg_record = widget.Label((0.75*x,1.6*y), size=(2*width, height), text="Meilleur score: " + record_score, 
                text_color = (200,200,200), font="Razer Regular", centered=True, police=26, bold=False, color = (0,0,0,0)) # affichage du score

        fond = config.getImage("fond game over") # recuperation de l'image du fond menu
        fond = pygame.transform.scale(fond, taille_ecran) # redimension de l'image
        pygame.display.get_surface().blit(fond, (0, 0)) # on colle le fond

    def meilleur_score(self, score):
        ''' Renvoit et remplace le nouveau record si besoin'''

        ''' Si le fichier existe ... sinon on le crée'''
        try:
            with open("../save.txt", "r+") as fichier:
                ''' On lit le contenu de la save '''
                json_dic = fichier.read()
                dic = json.loads(json_dic)       

                ''' Si on a un nouveau record, on le sauvegarde '''
                if dic["record"] < score:
                    dic["record"] = score
                    json_dic = json.dumps(dic)
                    fichier.write(json_dic)

            return str(dic["record"]) # on renvoit le meilleur score

        except FileNotFoundError:
            with open("../save.txt", "w") as fichier:
                json_dic = json.dumps({"record": score})
                fichier.write(json_dic) # on stocke le meilleur score

            return str(score)


    def detruire(self) :
        ''' Efface le game over en supprimant tout les widget '''
        self.widg_rejouer.kill()
        self.widg_menu.kill()
        self.widg_score.kill()
        self.widg_record.kill()
				
class Jeu:
    ''' S'occupe de gérer le jeu principale (la fenêtre du moins) '''
    def __init__(self, application):
        taille_ecran = dic_config["taille_ecran"]
        taille_HUD = dic_config["taille_HUD"]
        taille_personnage = dic_config["taille_personnage"]

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
 
    def start(self):
        ''' Lance le menu au démarrage '''
        self.menu()

    def quitter(self):
        ''' Arrêt total du jeu '''
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
