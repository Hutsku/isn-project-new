import pygame
from pygame.locals import *

import objet
import dongeon
import config
import hud
import menu
#========================================== IMPORT CONFIIG ================================================
config = config.getConfig()
# ========================================= VARIABLE ON/OFF =======================================

fonctionnement_boucle =True
menu_boucle = True
jeu_boucle = False
editeur_boucle = False
option_boucle = False

# ========================================= BOUCLE PRINCIPALE ===========================================

while fonctionnement_boucle:
# ========================================= LANCEMENT MENU =======================================
	
    if menu_boucle:
# ========================================= MENU =======================================
        menu.start()
        if menu.check_statut_quitter():
            menu_boucle = False
            fonctionnement_boucle = False
        if menu.check_statut_jeu():
            menu_boucle = False
            jeu_boucle = True


# ========================================= LANCEMENT JEU =======================================
	
    if jeu_boucle:
# ========================================= INITIALISATION JEU =======================================

                taille_ecran = config["taille_ecran"]
                taille_HUD = config["taille_HUD"]
                taille_personnage = config["taille_personnage"]

                pygame.init() #initialisation des modules py.game
                pygame.key.set_repeat(1) # Autorise la repetition d'event KEYDOWN si la touche est maintenue
                fenetre = pygame.display.set_mode((taille_ecran+taille_HUD, taille_ecran)) # creation de la fenetre (avec taille en parametre)

                fond = pygame.Surface((taille_ecran, taille_ecran)) # Création du fond, de taille equivalente à la fenêtre
                fond.fill((100, 100, 100)) # on colorie en gris

                environnement = dongeon.Dongeon() # on initialise le dongeon (1 seul possible)
                spawn = environnement.get_spawn()

                hud.hudfix() #creation de l'hud (qui n'a pas besoin d'update)

                perso = objet.Personnage(spawn, (taille_personnage, taille_personnage)) # on crée le personnage au spawn du niveau
                perso.image.fill((255, 0, 0)) #attribution de la couleur personnage

# ========================================== FONCTIONS JEU ===========================================

                def objetEvent():
                	objet.move() # On actualise la position des objets sur l'écran (collision etc)
                	objet.hitbox() # on test les hitbox des sprites entre eux (dégat et trigger)
                	objet.update() # on affiche les sprites à l'écran

                def guiEvent():
                	pass
                
                def dongeonEvent():
                	dongeon.check_fin_niveau(environnement) # On regarde si un escalier a été activé (pour changer de niveau)

# ===================================== BOUCLE PRINCIPALE JEU ========================================
                while jeu_boucle:
                        perso.vx = 0 #initialisation de la vitesse axe X personnage a 0
                        perso.vy = 0 #initialisation de la vitesse axe Y personnage a 0
                        fenetre.blit(fond, (0, 0)) # on colle le fond
                        # on gère les evenements claviers et souris 
                        for event in pygame.event.get():
                                if event.type == QUIT: #si clic sur croix rouge
                                    print("stop")
                                    jeu_boucle =  False
                                    menu_boucle = True
                                        
                                if event.type == KEYDOWN:
                                    if event.unicode == "d":
                                            perso.droite()
                                    if event.unicode == "q":
                                            perso.gauche()
                                    if event.unicode == "z":
                                            perso.haut()
                                    if event.unicode == "s":
                                            perso.bas()

                        objetEvent() # Evenements relatifs aux objets
                        dongeonEvent() # Evenements relatifs au niveau en général
                        guiEvent() # Evenements relatifs à l'interface
                        pygame.display.flip() # raffraichissement de la fenêtre

# ================================================================================================
# '''
