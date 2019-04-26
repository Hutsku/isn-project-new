def getConfig():
	taille_niveau = 500
	nb_case = 20
	taille_case = round(taille_niveau/nb_case)
	taille_personnage = taille_case

	dic = {"taille_niveau":taille_niveau, "nb_case":nb_case, "taille_case":taille_case, "taille_personnage":taille_personnage}
	return dic

	