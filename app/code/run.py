
# coding: utf-8
#========================================== IMPORT FICHIERS NECESSAIRES ================================================
import pygame
from pygame.locals import *
from pygame import *

import config
import hud
import application
import dongeon
import objet
import editeur.widget as widget

#========================================== IMPORT CONFIIG ================================================
pygame.init() # Initialise pygame

config_dic = config.getConfig() # Recupère les paramètres de base
taille = config_dic["taille_ecran"] # Definie la taille de l'ecran

fenetre = pygame.display.set_mode(taille) # Création de la fenêtre
pygame.display.set_caption("Under the infinite dungeon") # Change le nom de la fenêtre

config.init() # initialisation du module de configuration (pour les images)

debug = config_dic["debug"] # permet d'activer le debug mode

#========================================== FONCTION D'EVENT ================================================
def objetEvent():
    '''Event lié aux objet'''
    objet.move() # On actualise la position des objets sur l'écran (collision etc)
    objet.hitbox() # On test les hitbox des sprites entre eux (dégat et trigger)
    objet.update() # On affiche les sprites à l'écran

def hudEvent(app):
    '''Event lié a l'hud'''
    app.ecran.hud.update(app.ecran.environnement.get_temps(), app.ecran.environnement.get_nombre_de_lvl()) # Update de l'hud avec le temps, et le score


def dongeonEvent(app):
    '''Event lié au dongeon'''
    environnement = application.get_dongeon(app)
    dongeon.check_fin_niveau(environnement) # On regarde si un escalier a été activé (pour changer de niveau)

def timerEvent(app):
    '''Event lié au timer'''
    timer = app.ecran.environnement.change_timer(-1) # temps - 1
    for chara in objet.Character.liste:
        timer = app.ecran.environnement.change_timer(chara.check_temps_additionel()) # Ajoute le temps bonus/malus des personnages

    if timer <= 0: # Si le timer est fini ...
        app.game_over(app.ecran.environnement.get_nombre_de_lvl()) # ... Game Over !

# ========================================= BOUCLE PRINCIPALE ===========================================

key_trad = {"a": 113, "z":119, "d":100, "q":97, "s":115} # Traduction unicode et n° key

app = application.Application() # On crée l'objet Application (qui gère les changements entre menu, jeu etc.)
app.start() # Demarre l'application (le jeu)

clock = pygame.time.Clock() # Initialise un horloge
pygame.time.set_timer(USEREVENT, 1000) # Creation d'un event de temps toute les secondes (utile pour le compte a rebour)

boucle = True # Variable de la boucle
while boucle:	 
    clock.tick(config_dic["fps"]) # FPS bloqués à ...
    if debug :
        pygame.display.set_caption(str(clock.get_fps())) # permet d'afficher le nombre de fps a la place du nom de la fenetre (debug)
	
    ''' Quitter l'application '''
    if application.check_statut_quitter(app): # A-t-on quitté le jeu ?
        boucle = False 

    ''' Boucle du menu '''
    if application.check_statut_menu(app): # Sommes-nous sur le menu ?
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: # Si clic sur croix rouge ...
                boucle = False 

        widget.update() #update des widgets
        pygame.display.flip() # raffraichissement de la fenêtre

    ''' Boucle game over '''
    if application.check_statut_game_over(app): # A-t-on un game over ?
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: # Si clic sur croix rouge ...
                boucle = False 

        widget.update() # update des widgets
        pygame.display.flip() # raffraichissement de la fenêtre	

    ''' Boucle du jeu '''
    if application.check_statut_jeu(app): # Sommes-nous en jeu ?
        perso = application.get_perso(app) # On stocke le personnage dans une variable
        retour_menu = False # permet de desactiver le retour menu

        # on gère les evenements claviers, souris et temps
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: # si clic sur croix rouge ...
                boucle = False
                    
            if event.type == KEYDOWN: # Si une touche est enfoncée ...
                if event.unicode == "d": # regarde si c'est la touche d
                    perso.droite() # voir fichier objet ligne 145
                if event.unicode == "q": # regarde si c'est la touche q
                    perso.gauche() # voir fichier objet ligne 142
                if event.unicode == "z": # regarde si c'est la touche z
                    perso.haut() # voir fichier objet ligne 151
                if event.unicode == "s": # regarde si c'est la touche s
                    perso.bas() # voir fichier objet ligne 148
                if event.unicode == " ": # regarde si c'est la touche espace
                    perso.action() # voir fichier objet ligne 80
                if event.key == K_ESCAPE:  # Echap -> retour menu
                    retour_menu = True # permet un retour menu
                    
            if event.type == pygame.USEREVENT: # si il y a un USEREVENT (c'est a dire toute les seconde, voir ligne 74)
                timerEvent(app) # voir ligne 44

            if event.type == KEYUP: # Si une touche est relachée ...
                ''' L'event KEYUP ne donne pas de traduction unicode. J'utilise donc un dic fait maison (ligne 56)'''
                if key_trad["d"] == event.key or key_trad["q"] == event.key:
                    perso.vx = 0 # reinitialise la vitesse x personnage a 0
                if key_trad["z"] == event.key or key_trad["s"] == event.key:
                    perso.vy = 0 # reinitialise la vitesse y personnage a 0

        if not application.check_statut_game_over(app):	# Si le jeu n'est pas game over, on actualise
            ''' On actualise tout l'écran '''
            objetEvent() 
            dongeonEvent(app) 
            widget.update() 
            hudEvent(app) 

        pygame.display.update() # raffraichissement de la fenêtre
        
        if retour_menu:
                app.menu() #retourne au menu
# ================================================================================================
