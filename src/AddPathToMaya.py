import sys

prjPath = "D:/profile redirect/aljimen6/Desktop/MayaPlugins/src"
moduleDir = "D:/profile redirect/aljimen6/Desktop"

if prjPath not in sys.path:
    sys.path.append(prjPath)

if moduleDir not in sys.path:
    sys.path.append(moduleDir)