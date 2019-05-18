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
pygame.init() #initialise pygame

config_dic = config.getConfig() #recupere les configs
taille = config_dic["taille_ecran"] #definie la taille de l'ecran


fenetre = pygame.display.set_mode(taille) # création de la fenêtre
fond = pygame.Surface(taille) #creation d'un fond

config.init() #initialisation de la config (pour les images)

debug = config_dic["debug"]

#========================================== FONCTION D'EVENT ================================================
def objetEvent():
        '''event lié aux objet'''
        objet.move() # On actualise la position des objets sur l'écran (collision etc)
        objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
        objet.update() # on affiche les sprites à l'écran

def hudEvent(app):
        '''event lié a l'hud'''
        app.ecran.hud.update(app.ecran.environnement.get_temps(), app.ecran.environnement.get_nombre_de_lvl()) #update de l'hud avec le temps, et le score
	

def dongeonEvent(app):
        '''event lié au dongeon'''
        environnement = application.get_dongeon(app)
        dongeon.check_fin_niveau(environnement) # On regarde si un escalier a été activé (pour changer de niveau)

def timerEvent(app):
        '''event lié au timer'''
        timer = app.ecran.environnement.change_timer(-1) #perd 1 seconde
        for chara in objet.Character.liste:
                timer = app.ecran.environnement.change_timer(chara.check_temps_additionel()) #ajoute le temps bonus des personnages

        if timer <= 0: #si le timer est arrivé a 0
                print("TIME'S UP") #debug
                app.game_over(app.ecran.environnement.get_nombre_de_lvl()) #affiche le game over (avec le score)

#########################################
#           fichier sonor	        #
#########################################
'''
mixer.init()
music = mixer.Sound("../music/Thunderstorm.wav")
son = mixer.Sound("../music/bruitage1.wav")'''



# ========================================= BOUCLE PRINCIPALE ===========================================

key_trad = {"a": 113, "z":119, "d":100, "q":97, "s":115} # traduction unicode et n° key

pic = objet.Pic((200, 200), (100, 100)) #initialise les pics (wtf)

app = application.Application() #initialise l'application qui gere les differents menus
app.start() #demarre l'application

clock = pygame.time.Clock() #initialise un horloge
pygame.time.set_timer(USEREVENT, 1000) #creation d'un event de temps toute les secondes (utile pour le compte a rebour)

pygame.display.set_caption("Under the infinite dungeon") #Cahnge le nom de la fenetre

boucle = True #petmet le fonctionnement de la boucle principale

while boucle:	 
    clock.tick(config_dic["fps"]) #definie le nombre de frame max par seconde (fps)
    if debug :
        pygame.display.set_caption(str(clock.get_fps())) #permet d'afficher le nombre de fps a la place du nom de la fenetre (debug)
	
    ''' Quitter l'application '''
    if application.check_statut_quitter(app): #voir fichier application
        boucle = False #fin programme

    ''' Boucle du menu '''
    if application.check_statut_menu(app): #voir fichier application
        fond = config.getImage("fond menu")	#recuperation de l'image du fond menu
        fond = pygame.transform.scale(fond, taille) #redimension de l'image
        fenetre.blit(fond, (0, 0)) # on colle le fond
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: #si clic sur croix rouge
                boucle = False #fin programme

        widget.update() #update des widgets
        pygame.display.flip() # raffraichissement de la fenêtre
       # music.stop()          #lorsque le joueur est dans le menu pas de musique

    ''' boucle game over '''
    if application.check_statut_game_over(app):
        fond = config.getImage("fond game over")	#recuperation de l'image du fond menu
        fond = pygame.transform.scale(fond, taille) #redimension de l'image
        fenetre.blit(fond, (0, 0)) # on colle le fond
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: #si clic sur croix rouge
                boucle = False #fin programme

        widget.update() #update des widgets
        pygame.display.flip() # raffraichissement de la fenêtre	

    ''' Boucle du jeu '''
    if application.check_statut_jeu(app): #voir fichier application
        perso = application.get_perso(app) #voir fichier application
        retour_menu = False #permet de desactiver le retour menu

        # on gère les evenements claviers, souris et temps
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: #si clic sur croix rouge
                boucle = False #fin programme
                    
            if event.type == KEYDOWN: #permet de detecter une touche enfoncée
                if event.unicode == "d": #regarde si c'est la touche d
                    perso.droite() #voir fichier objet ligne 145
                if event.unicode == "q": #regarde si c'est la touche q
                    perso.gauche() #voir fichier objet ligne 142
                if event.unicode == "z": #regarde si c'est la touche z
                    perso.haut() #voir fichier objet ligne 151
                if event.unicode == "s": #regarde si c'est la touche s
                    perso.bas() #voir fichier objet ligne 148
                if event.unicode == " ": #regarde si c'est la touche espace
                    perso.action() #voir fichier objet ligne 80
                if event.key == K_ESCAPE:   #on appuie sur échape pour revenir au menu
                    retour_menu = True #permet un retour menu
                    
            if event.type == pygame.USEREVENT: #si il y a un USEREVENT (c'est a dire toute les seconde, voir ligne 74)
                timerEvent(app) #voir ligne 44

            if event.type == KEYUP: #permet de detecter une touche relachée
                ''' L'event KEYUP ne donne pas de traduction unicode. J'utilise donc un dic fait maison '''
                if key_trad["d"] == event.key or key_trad["q"] == event.key:
                   perso.vx = 0 #reinitialise la vitesse personnage a 0
                if key_trad["z"] == event.key or key_trad["s"] == event.key:
                    perso.vy = 0 #reinitialise la vitesse personnage a 0
        if not application.check_statut_game_over(app):	#voir fichier application	
            objetEvent() # voir ligne 28
            dongeonEvent(app) # voir ligne 39
            widget.update() #voir fichier widget
            hudEvent(app) #voir ligne 34

        pygame.display.update() # raffraichissement de la fenêtre
        
        if retour_menu:
                app.menu() #retourne au menu
# ================================================================================================
# '''
# '''
