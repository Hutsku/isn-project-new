import pygame
from pygame.locals import *

import config
import hud
import application
import dongeon
import objet

#========================================== IMPORT CONFIIG ================================================
pygame.init()
fenetre = pygame.display.set_mode((surfaceW,surfaceH)) # création de la fenêtre
fond = pygame.Surface((surfaceW,surfaceH))
fond.fill((100, 100, 100))
pygame.key.set_repeat(1) # Autorise la repetition d'event KEYDOWN si la touche est maintenue
config = config.getConfig()

def objetEvent():
    objet.move() # On actualise la position des objets sur l'écran (collision etc)
    objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
    objet.update() # on affiche les sprites à l'écran

def guiEvent():
    pass

def dongeonEvent():
    dongeon.check_fin_niveau(environnement) # On regarde si un escalier a été activé (pour changer de niveau)

# ========================================= BOUCLE PRINCIPALE ===========================================

application.start()
boucle = True
while boucle:	
    if application.check_statut_quitter():
        boucle = False

    if application.check_statut_menu():
        for event in pygame.event.get():
            widget.event(event) # Gestion des evenements sur les widget (pour les boutons par ex)
            if event.type == QUIT: #si clic sur croix rouge
                boucle = False

        widget.update()

    if application.check_statut_jeu():
        perso = application.get_perso()
        perso.vx = 0 #initialisation de la vitesse axe X personnage a 0
        perso.vy = 0 #initialisation de la vitesse axe Y personnage a 0
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

        widget.update()
        objetEvent() # Evenements relatifs aux objets
        dongeonEvent() # Evenements relatifs au niveau en général
        guiEvent() # Evenements relatifs à l'interface

        pygame.display.flip() # raffraichissement de la fenêtre

# ================================================================================================
# '''
