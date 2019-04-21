def getConfig():
	taille_ecran = 500
	nb_case = 17
	taille_case = round(taille_ecran/nb_case)
	taille_personnage = taille_case

	dic = {"taille_ecran":taille_ecran, "nb_case":nb_case, "taille_case":taille_case, "taille_personnage":taille_personnage}
	return dic