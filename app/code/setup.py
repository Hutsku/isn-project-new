import sys, os
from cx_Freeze import setup, Executable

# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path

includes = [] # nommer les modules non trouves par cx_freeze
excludes = []
packages = [] # nommer les packages utilises

# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = ["../image", "../niveau"]

# niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True

# construction du dictionnaire des options
options = {"path": path,
       "includes": includes,
       "excludes": excludes,
       "packages": packages,
       "include_files": includefiles,
       "optimize": optimize,
       "silent": silent
       }

base ="Win32GUI"

cible_1 = Executable(
    script="run.py",
    )

cible_2 = Executable(
    script="run - editeur.py",
    )

# creation du setup
setup(
    name="project",
    version="1.0",
    description="blabla",
    options={"build_exe": options},
    executables=[cible_1, cible_2]
    )