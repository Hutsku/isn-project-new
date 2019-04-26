#On Importe les bibliothèques nécessaires
import pygame
from pygame.locals import *

import config
#Initialisation de la bibliothèque Pygame
pygame.init()

#Création de la fenêtre
config = config.getConfig() 
surfaceW = config["taille_menux"] #Dimension de la fenêtre / Largeur
surfaceH = config["taille_menuy"] #Dimension de la fenêtre / Longueur

#variable de statut
global statut_jeu, statut_quit, statut
statut_jeu = False
statut_quit = False
statut = True

class Menu :
    """ Création et gestion des boutons d'un menu """
    def __init__(self, application, *groupes) :
        self.couleurs = dict(
            normal=(255, 255, 255), # couleur de base des "boutons"
            survol=(0, 255, 0),) #lorsque la souris esr sur les "boutons"
        font = pygame.font.SysFont('Razer Regular', 26, bold=True, italic=False) # police + sa taille + en gras mais pas en italique 
        # noms des menus et commandes associées
        items = (
            ('JOUER', application.jeu),
            ('QUITTER', application.quitter))
        x = 500 # position x des items
        y = 350 # position y des items
        self._boutons = []
        for texte, cmd in items :
            mb = MenuBouton(
                texte,
                self.couleurs['normal'],
                font,
                x,
                y,
                200,
                50,
                cmd)
            self._boutons.append(mb)
            y += 120
            for groupe in groupes :
                groupe.add(mb)
 
    def update(self, events) :
        clicGauche, *_ = pygame.mouse.get_pressed()
        posPointeur = pygame.mouse.get_pos()
        for bouton in self._boutons :
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur) :
                # Changement du curseur par un quelconque
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche :
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else :
                # Le pointeur n'est pas sur le bouton
                bouton.dessiner(self.couleurs['normal'])
        else :
            # Le pointeur n'est pas sur l'un des boutons
            # initialisation au pointeur par défaut
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
 
    def detruire(self) :
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # initialisation du pointeur
 
 
 
class MenuBouton(pygame.sprite.Sprite) :
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande) :
        super().__init__()
        self._commande = commande
 
        self.image = pygame.Surface((largeur, hauteur))
 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur/2, hauteur/2)
 
        self.dessiner(couleur)
 
    def dessiner(self, couleur) :
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)
 
    def executerCommande(self) :
        # Appel de la commande du bouton
        self._commande()
 
 
class Jeu :
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
 
 
class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self) :
        pygame.init()
        pygame.display.set_caption("MENU DU JEU")
 
        self.fond = (0,)*3 # couleur (ou image) du fond du menu 
 
        self.fenetre = pygame.display.set_mode((surfaceW,surfaceH))
        # Groupe de sprites utilisé pour l'affichage
        self.groupeGlobal = pygame.sprite.Group()
        
    def _initialiser(self) :
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass
 
    def menu(self) :
        # Affichage du menu
        self._initialiser()
        self.ecran = Menu(self, self.groupeGlobal)
 
    def jeu(self) :
        # Affichage du jeu
        global statut, statut_jeu
        statut = False
        statut_jeu = True
 
    def quitter(self) :
        global statut, statut_quit
        statut = False
        statut_quit = True
	
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

def start():
    statut_jeu = False
    statut_quit = False
    print(statut_jeu)
    app = Application()
    app.menu()
    clock = pygame.time.Clock()
    while statut :
        app.update()
        clock.tick(30)
    pygame.quit()

def check_statut_quitter():
    print(statut_quit)
    return(statut_quit)
    
def check_statut_jeu():
    print("effectué2")
    return(statut_jeu)

