import sys, os
from cx_Freeze import setup, Executable

path = sys.path
includes = []
excludes = []
packages = ["app/code"]
includefiles = ["app/image", "app/level"]

optimize = 0
silent = True

options = {"path": path,
       "includes": includes,
       "excludes": excludes,
       "packages": packages,
       "include_files": includefiles,
       "optimize": optimize,
       "silent": silent
       }

base = Win32GUI

cible_1 = Executable(
    script="app/code/run.py",
    )

cible_2 = Executable(
    script="app/code/run - editeur.py",
    )

setup(
    name="project",
    version="1.0",
    description="blabla",
    options={"build_exe": options},
    executables=[cible_1, cible_2]
    )