import pygame
from pygame.locals import *

import config
import hud
import application
import dongeon
import objet
import editeur.widget as widget

#========================================== IMPORT CONFIIG ================================================
config = config.getConfig()
taille = config["taille_ecran"]

pygame.init()
fenetre = pygame.display.set_mode(taille) # création de la fenêtre
fond = pygame.Surface(taille)
fond.fill((0, 0, 0))

def objetEvent():
    objet.move() # On actualise la position des objets sur l'écran (collision etc)
    objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
    objet.update() # on affiche les sprites à l'écran

def hudEvent():
    hud.hudfix()

def dongeonEvent(app):
    environnement = application.get_dongeon(app)
    dongeon.check_fin_niveau(environnement) # On regarde si un escalier a été activé (pour changer de niveau)

# ========================================= BOUCLE PRINCIPALE ===========================================

key_trad = {"a": 113, "z":119, "d":100, "q":97, "s":115} # traduction unicode et n° key

app = application.Application()
app.start()
clock = pygame.time.Clock()
boucle = True
while boucle:	 
    clock.tick()
    pygame.display.set_caption( str(clock.get_fps()))
    if application.check_statut_quitter(app):
        boucle = False

    elif application.check_statut_menu(app):
        fond.fill((0, 0, 0))
        fenetre.blit(fond, (0, 0)) # on colle le fond
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: #si clic sur croix rouge
                boucle = False

        widget.update()
        pygame.display.flip() # raffraichissement de la fenêtre

    elif application.check_statut_transition(app):
        pass

    elif application.check_statut_jeu(app):
        fond.fill((100, 100, 100))
        perso = application.get_perso(app)
        #perso.vx = 0 #initialisation de la vitesse axe X personnage a 0
        #perso.vy = 0 #initialisation de la vitesse axe Y personnage a 0
        fenetre.blit(fond, (0, 0)) # on colle le fond

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

            if event.type == KEYUP:
                ''' L'event KEYUP ne donne pas de traduction unicode. J'utilise donc un dic fait maison '''
                if key_trad["d"] == event.key or key_trad["q"] == event.key:
                   perso.vx = 0
                if key_trad["z"] == event.key or key_trad["s"] == event.key:
                    perso.vy = 0

        widget.update()
        objetEvent() # Evenements relatifs aux objets
        dongeonEvent(app) # Evenements relatifs au niveau en général
        #hudEvent() # Evenements relatifs à l'interface

        pygame.display.flip() # raffraichissement de la fenêtre

# ================================================================================================
# '''
