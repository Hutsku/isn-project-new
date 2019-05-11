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
pygame.init()

config_dic = config.getConfig()
taille = config_dic["taille_ecran"]

fenetre = pygame.display.set_mode(taille) # création de la fenêtre
fond = pygame.Surface(taille)
fond.fill((0, 0, 0))

config.init()

def objetEvent():
    objet.move() # On actualise la position des objets sur l'écran (collision etc)
    objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
    objet.update() # on affiche les sprites à l'écran

def hudEvent():
    hud.hudfix()

def dongeonEvent(app):
    environnement = application.get_dongeon(app)
    dongeon.check_fin_niveau(environnement) # On regarde si un escalier a été activé (pour changer de niveau)

def timerEvent(app):
	timer = app.ecran.environnement.change_timer(-1)
	for chara in objet.Character.liste:
		timer = app.ecran.environnement.change_timer(chara.check_degat())
	print(timer)
	if timer <= 0:
		print("TIME'S UP")
		app.game_over()

######################################
# fichier sonor
######################################

mixer.init()
music = mixer.Sound("Thunderstorm.wav")

# ========================================= BOUCLE PRINCIPALE ===========================================

key_trad = {"a": 113, "z":119, "d":100, "q":97, "s":115} # traduction unicode et n° key
pic = objet.Pic((200, 200), (100, 100))

app = application.Application()
app.start()
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 1000)

boucle = True
while boucle:	 
    clock.tick(120)
    pygame.display.set_caption(str(clock.get_fps()))
	
    ''' Quitter l'application '''
    if application.check_statut_quitter(app):
        boucle = False

    ''' Boucle du menu '''
    if application.check_statut_menu(app):
        fond.fill((0, 0, 0))
        fenetre.blit(fond, (0, 0)) # on colle le fond
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: #si clic sur croix rouge
                boucle = False

        widget.update()
        pygame.display.flip() # raffraichissement de la fenêtre
        music.stop()          #lorsque le joueur est dans le menu pas de musique

    ''' Boucle in game '''
    if application.check_statut_jeu(app):
        fond.fill((100, 100, 100))
        perso = application.get_perso(app)
        fenetre.blit(fond, (0, 0)) # on colle le fond
        retour_menu = False
        music.play()               #si le joueur et dans le jeu alors musique

        # on gère les evenements claviers et souris 
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: #si clic sur croix rouge
                boucle = False
                    
            if event.type == KEYDOWN:
                if event.unicode == "d":
                    perso.droite()
                if event.unicode == "q":
                    perso.gauche()
                if event.unicode == "z":
                    perso.haut()
                if event.unicode == "s":
                    perso.bas()
                if event.unicode == "a":
                    perso.action()
                if event.key == K_ESCAPE:   #on appuie sur échape pour revenir au menu
                    retour_menu = True
                    
            if event.type == pygame.USEREVENT:
                timerEvent(app)

            if event.type == KEYUP:
                ''' L'event KEYUP ne donne pas de traduction unicode. J'utilise donc un dic fait maison '''
                if key_trad["d"] == event.key or key_trad["q"] == event.key:
                   perso.vx = 0
                if key_trad["z"] == event.key or key_trad["s"] == event.key:
                    perso.vy = 0

        objetEvent() # Evenements relatifs aux objets
        dongeonEvent(app) # Evenements relatifs au niveau en général
        #hudEvent() # Evenements relatifs à l'interface
        widget.update()

        pygame.display.update() # raffraichissement de la fenêtre
        if retour_menu: app.menu()


# ================================================================================================
# '''
