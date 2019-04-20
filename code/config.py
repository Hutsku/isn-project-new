def getConfig():
	taille_personnage = 15
	taille_ecran = 548
	nb_case = 15
	taille_case = round(taille_ecran/nb_case)

	dic = {"taille_ecran":taille_ecran, "nb_case":nb_case, "taille_case":taille_case, "taille_personnage":taille_personnage}
	return dic