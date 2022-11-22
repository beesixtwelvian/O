#!/usr/bin/python3
#-*- coding : utf-8 -*-
__authors__ = ("Robin", "LIOUTAUD")
__contact__ = ("robin.lioutaud@etu.umontpellier.fr")
__version__ = "0.0.1"
__date__ = "22/11/2022"

# SPECIFICATIONS
# https://samtools.github.io/hts-specs/SAMv1.pdf
# FLAG
# https://www.samformat.info/sam-format-flag

# Recherche le fichier
print("FILE PATH")
print("Enter the file path, WITHOUT its name")
print("( tip : right clic on file > properties > copy its path )")
print("( paste path here, by doing Ctrl Maj V, with / at the end )")
path = input("File path -> ") or "/home/e20210021830/Documents/ADBI/"
#the 'or' is a default value to gain time and could be deleted at the end
print("     entered : " + path)
print("FILE NAME")
print("Enter file name including its .sam extension")
file = input("File name -> ") or "mapping.sam"
print("     entered : " + file)
path_file = path + file
print("     path and file : " + path_file)

# Teste si c'est un bon fichier
import os
import pathlib
# the 'imports' could be ahead
if not os.path.isfile(file):
    print("ERROR : that is not a file !")
    exit()
if not pathlib.Path(file).suffix == ".sam":
    print("ERROR : file extension isn't .sam !")
    exit()
if os.path.getsize(file) == 0:
    print("ERROR : file is empty !")
    exit()

# Récupère les données du fichier
f = open(path_file)
print("Wait ...")
# inform the user to wait because results do not appear instantly
sam = f.readlines()
subtab = []
for samline in sam:
    subtab.append(samline.split('\t'))
    # We can split tabulations because sam format specifications indicate that
    # the file is << TAB-delimited >> (at least the first columns that interest us)
tabhead = []
for tabrow in subtab:
    tabhead.append([tabrow[0], tabrow[1:]])
    # Place the read at list's 1st item, and next, its infos in a nested list

# Extrait l'entête du tableau, les métadonnées commençant par @
head = []
tab = []
for row in tabhead:
    if row[0][0][0] == '@': # the last [0] doesn't refer to a list index but rather to the 1st char
        head.append(row)
    if row[0][0][0] != '@':
        tab.append(row)
del tabhead # after separating tabhead in half, head (heading) and tab (data), we delete tabhead
print("Ready !")

# a) Nombre de données de départ ?
print(file + " contains " + str(len(tab)) + " reads (individuals, regardless of pairing).")
# len() gives the length of the tab list,
# the list being our lines, thereby len() gives the number of lines

# b) Combien de reads mappés ?
mappe = []
for row in tab:
    if int(row[1][0]) & int(4) != int(4): # if flag HASN'T BEEN summated by +4
        mappe.append(row)
print(file + " contains " + str(len(mappe)) + " reads mapped.")

# c) Combien de reads bien mappés, de qualité, >20 ?
quali = []
for row in tab:
    if int(row[1][3]) >= int(20): # if the quality indicator is >20
        quali.append(row)
print(file + " contains " + str(len(quali)) + " quality reads (considering MAPQ >20).")
# here we could make an input of the quality threshold wanted by the user
# with a quality = input("Enter the value here : ")

# Combien de reads mal mappés ?
unmapped = []
for row in tab:
    if int(row[1][0]) & int(4) == int(4): # if flag HAS BEEN summated by +4 ("segment unmapped")
        unmapped.append(row)
print(file + " contains " + str(len(unmapped)) + " reads unmapped.")

# d1) Parmi ces mal mappés, combien de paired ?
unmappedpaired = []
for row in unmapped:
    if int(row[1][0]) & int(1) == int(1): # if flag HAS BEEN summated by +1
        unmappedpaired.append(row)
print(file + " contains " + str(len(unmappedpaired)) + " reads paired unmapped (at least one in two).")

# d2) Parmi ces mal mappés paired, combien de ''proper paired'' ?
properpaired = []
for row in tab:
    if int(row[1][0]) & int(2) == int(2): # if flag HAS BEEN summated by +2
        properpaired.append(row)
print(file + " contains " + str(len(properpaired)) + " reads proper(ly) paired.")

# e) Combien de reads totalement mappés/alignés ?
cigar100m = []
for row in tab:
    if row[1][4] == "100M": # if cigar = 100M
        cigar100m.append(row)
print(file + " contains " + str(len(cigar100m)) + " reads fully mapped/aligned (with CIGAR = 100M).")

print("Terminé")
