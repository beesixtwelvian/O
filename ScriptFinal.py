#!/usr/bin/python3
#-*- coding : utf-8 -*-
__authors__ = ("Robin", "LIOUTAUD")
__contact__ = ("robin.lioutaud@etu.umontpellier.fr")
__version__ = "0.0.1"
__date__ = "06/12/2022"

# SPECIFICATIONS
# https://samtools.github.io/hts-specs/SAMv1.pdf
# FLAG
# https://www.samformat.info/sam-format-flag

fileselected = "not"
while 1 == 1:
    print("SELECT AN OPTION :")
    print("-> 1 : Select the file to study (" + fileselected + " selected)")
    print("-> 2 : Compute descriptive data about reads")
    print("-> 0 : Exit the program")
    prgm = int(input("=> "))
    if prgm == 0:
        exit()
    if prgm == 1:
        #
        # Recherche le fichier
        print("FILE PATH")
        print("Enter the file path, WITHOUT its name")
        print("( tip : right clic on file > properties > copy its path )")
        print("( paste path here, by doing Ctrl Maj V, with / at the end )")
        path = input("File path => ") or "/home/e20210021830/Documents/ADBI/"
        #the 'or' is a default value to gain time and could be deleted at the end
        print("     entered : " + path)
        print("FILE NAME")
        print("Enter file name including its .sam extension")
        file = input("File name => ") or "mapping.sam"
        print("     entered : " + file)
        path_file = path + file
        print("     path and file : " + path_file)
        fileselected = str(file)
        #
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
        #
        # Chrono 1 start
        import time
        chrono1s = time.time()
        #
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
        #
        # Extrait l'entête du tableau, les métadonnées commençant par @
        head = []
        tab = []
        for row in tabhead:
            if row[0][0][0] == '@': # the last [0] doesn't refer to a list index but rather to the 1st char
                head.append(row)
            if row[0][0][0] != '@':
                tab.append(row)
        del tabhead # after separating tabhead in half, head (heading) and tab (data), we delete tabhead
        chrono1f = time.time()
        chrono1 = chrono1f - chrono1s
        print("Ready ! (in " + str(chrono1) + " secondes)")

    if prgm == 2:
        if tab:
            NbOfReads = "Compute the number of read occurencies"
            NbOfMappedReads = "Compute the number of mapped read occurencies"
            NbOfQualityReads = "Compute the number of quality/well-mapped read occurencies"
            NbOfMismappedAndMismappedAndPairedReads = "Compute the number of mismapped reads quantity and mismapped & paired read occurencies"
            NbOfProperPairedReads = "Compute the number of properly paired read occurencies"
            NbOfTotallyPairedReads = "Compute the number of totally-paired read occurencies"
            while 1 == 1:
                print("SELECT AN OPTION :")
                print("-> 1 : " + NbOfReads)
                print("-> 2 : " + NbOfMappedReads)
                print("-> 3 : " + NbOfQualityReads)
                print("-> 4 : " + NbOfMismappedAndMismappedAndPairedReads)
                print("-> 5 : " + NbOfProperPairedReads)
                print("-> 6 : " + NbOfTotallyPairedReads)
                print("-> 7 : Compute ALL these properties")
                print("-> 8 : Export the data above in a .dat file in the current directory")
                print("-> 0 : Exit the calculator")
                menu = int(input("=> "))
                # Option de retour au menu précédent
                if menu == 0:
                    break
                # Chrono 2 start (if menu = 7)
                if menu == 7:
                    chrono2s = time.time()
                if menu == 1 or menu == 7:
                    # a) Nombre de données de départ ?
                    NbOfReads = str(file + " contains " + str(len(tab)) + " reads (individuals, regardless of pairing).")
                    # len() gives the length of the tab list,
                    # the list being our lines, thereby len() gives the number of lines
                if menu == 2 or menu == 7:
                    # b) Combien de reads mappés ?
                    mappe = []
                    for row in tab:
                        if int(row[1][0]) & int(4) != int(4): # if flag HASN'T BEEN summated by +4
                            mappe.append(row)
                    NbOfMappedReads = str(file + " contains " + str(len(mappe)) + " reads mapped.")
                if menu == 3 or menu == 7:
                # c) Combien de reads bien mappés, de qualité, >20 ?
                    quali = []
                    qual = -1
                    while int(qual) < 0 or int(qual) > 100:
                        qual = input("Quality level desired (default value >20, press Enter to skip) -> ") or 20
                        if int(qual) < 0 or int(qual) > 100:
                            print("ERROR : quality level is a value between 0 and 100. Redo")
                    for row in tab:
                        if int(row[1][3]) >= int(qual): # if the quality indicator is >20
                            quali.append(row)
                    NbOfQualityReads = str(file + " contains " + str(len(quali)) + " quality reads (considering MAPQ >" + str(qual) + ").")
                    # here we could make an input of the quality threshold wanted by the user
                    # with a quality = input("Enter the value here : ")
                if menu == 4 or menu == 7:
                    # Combien de reads mal mappés ?
                    unmapped = []
                    for row in tab:
                        if int(row[1][0]) & int(4) == int(4): # if flag HAS BEEN summated by +4 ("segment unmapped")
                            unmapped.append(row)
                    NbOfUnmappedReads = str(file + " contains " + str(len(unmapped)) + " reads unmapped.")
                    #
                    # d1) Parmi ces mal mappés, combien de paired ?
                    unmappedpaired = []
                    for row in unmapped:
                        if int(row[1][0]) & int(1) == int(1): # if flag HAS BEEN summated by +1
                            unmappedpaired.append(row)
                    NbOfUnmappedPairedReads = str(file + " contains " + str(len(unmappedpaired)) + " reads paired unmapped (at least one in two).")
                    NbOfMismappedAndMismappedAndPairedReads = NbOfUnmappedReads + '\n' + "       " + NbOfUnmappedPairedReads
                if menu == 5 or menu == 7:
                    # d2) Parmi ces mal mappés paired, combien de ''proper paired'' ?
                        properpaired = []
                        for row in tab:
                            if int(row[1][0]) & int(2) == int(2): # if flag HAS BEEN summated by +2
                                properpaired.append(row)
                        NbOfProperPairedReads = str(file + " contains " + str(len(properpaired)) + " reads proper(ly) paired.")
                if menu == 6 or menu == 7:
                    # e) Combien de reads totalement mappés/alignés ?
                    cigar100m = []
                    for row in tab:
                        if str(row[1][4]).split("M")[0] == "100": # if cigar = 100M
                            cigar100m.append(row)
                    NbOfTotallyPairedReads = str(file + " contains " + str(len(cigar100m)) + " reads fully mapped/aligned/matched (with CIGAR = 100M).")
                if menu == 8:
                    # Création fichier dat avec données
                    nomfichierdat = file.split(".")
                    fichierdat = nomfichierdat[0] + ".dat"

                    fichierdatpath = os.path.join(path, fichierdat)

                    fptr = open(fichierdat, "w")
                    fptr.write(NbOfReads + '\n')
                    fptr.write(NbOfMappedReads + '\n')
                    fptr.write(NbOfQualityReads + '\n')
                    fptr.write(NbOfMismappedAndMismappedAndPairedReads + '\n')
                    fptr.write(NbOfProperPairedReads + '\n')
                    fptr.write(NbOfTotallyPairedReads + '\n')
                    fptr.close()
                print("Done !")
                #
                # Chrono 2 end (if menu = 7)
                if menu == 7:
                    chrono2f = time.time()
                    chrono2 = chrono2f - chrono2s
                    print("(in " + str(chrono2) + " seconds including quality level selection duration)")                
