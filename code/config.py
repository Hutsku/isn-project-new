def getConfig():
	taille_ecran = 800 #taille de l'espace de jeu
	nb_case = 20 #nombre de case de jeu
	taille_case = round(taille_ecran/nb_case) #definie la taille d'une case (auto)
	taille_personnage = taille_case #definie taille personnage
	taille_HUD = round((20*taille_ecran)/100) #definie la taille de l'hud (auto)
	taille_menux = 1000 #Dimension de la fenêtre du menu / Largeur
	taille_menuy = 800 #Dimension de la fenêtre du menu / Longueur
	dic = {"taille_ecran":taille_ecran, "nb_case":nb_case, "taille_case":taille_case, "taille_personnage":taille_personnage, "taille_HUD":taille_HUD, "taille_menux":taille_menux, "taille_menuy":taille_menuy} #dictionnaire pour utilisation de la configue
	return dic

	