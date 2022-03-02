#!/usr/bin/PYTHON
# -*-coding:utf-8 -*

#===================================================================#
#-------------------------------------------------------------------#
#                                MDownloader                        #
#-------------------------------------------------------------------#
#*******************************************************************#
#                  BFTeck - 19-02-2022                              #
#-------------------------------------------------------------------#
#                         Notes                                     #
#                                                                   #
#-------------------------------------------------------------------#
#                            HISTORY                                #
#   V0.1.0    BFTeck - 19-02-2022                                   #
#             Initial                                               #
#===================================================================#


#--------------------------------------------#
#                  Packages                  #
#--------------------------------------------#
import sqlite3
import os
import re
import requests



#--------------------------------------------#
#                Variables                   #
#--------------------------------------------#

path = "Y:\ATRIER\PatPatrouille"
#path = "Y:\Dessins animés - Enfants\Paw_Patrol"
dbname="57532-paw-patrol.db"
nomdelaseries="La Pat'Patrouille"
#--------------------------------------------#
#             Code Fonction                  #
#--------------------------------------------#





#--------------------------------------------#
#               Code Principal               #
#--------------------------------------------#

conn = sqlite3.connect(dbname)
c = conn.cursor()

listoffiles = os.listdir(path)


for filepath in listoffiles:
    completepath=path + os.sep + filepath
    #print(completepath)
    basename_without_ext = os.path.splitext(os.path.basename(completepath))[0]
    extension = os.path.splitext(os.path.basename(completepath))[1]
    #print(basename_without_ext)
    #print(extension)
    # filename

    title = basename_without_ext.replace("à", "a")
    title = title.replace("â", "a")
    title = title.replace("ù", "u")
    title = title.replace("û", "u")
    title = title.replace("ô", "o")
    title = title.replace("é", "e")
    title = title.replace("è", "e")
    title = title.replace("ê", "e")
    title = title.replace("ç", "c")

    title = title.replace(" !", "")
    title = title.replace(" ?", "")
    title = title.replace(" : ", "-")
    title = title.replace(": ", "-")
    title = title.replace(":", "-")
    title = title.replace('"', '')
    title = title.replace("' ", "_")
    title = title.replace("'", "_")
    title = title.replace(" ", "_")

    #print(title)
    sqlcommand = "SELECT * FROM episode_list WHERE title LIKE '%"+title+"%';"
    #print(sqlcommand)
    renamed=False
    for row in c.execute(sqlcommand):
        print(row)
        titre_de_lepisode = row[2]
        duree = titre_de_lepisode.find("___(21_min)")
        if duree > -1:
            titre_de_lepisode = titre_de_lepisode[:duree]
        if int(row[0]) < 10:
            if int(row[1]) < 10:
                newcompletepath = path + os.sep + nomdelaseries + ".S0" + row[0] + ".E0" + row[
                    1] + "." + titre_de_lepisode + extension
            else:
                newcompletepath = path + os.sep + nomdelaseries + ".S0" + row[0] + ".E" + row[
                    1] + "." + titre_de_lepisode + extension
        else:
            if int(row[1]) < 10:
                newcompletepath = path + os.sep + nomdelaseries + ".S" + row[0] + ".E0" + row[
                    1] + "." + titre_de_lepisode + extension
            else:
                newcompletepath = path + os.sep + nomdelaseries + ".S" + row[0] + ".E" + row[
                    1] + "." + titre_de_lepisode + extension
        print(completepath+" ==> "+newcompletepath)
        os.rename(completepath, newcompletepath)
        renamed = True
    if renamed == False:
        sqlcommand = "SELECT * FROM episode_list WHERE originaux LIKE '%" + title + "%';"
        # print(sqlcommand)

        for row in c.execute(sqlcommand):
            print(row)
            # La Pat'Patrouille.S06.E24.La Super Patrouille - L'incroyable Hellinger.ts
            titre_de_lepisode = row[2]
            duree = titre_de_lepisode.find("___(21_min)")
            if duree > -1:
                titre_de_lepisode = titre_de_lepisode[:duree]
            if int(row[0]) < 10:
                if int(row[1]) < 10:
                    newcompletepath = path + os.sep + nomdelaseries + ".S0" + row[0] + ".E0" + row[
                        1] + "." + titre_de_lepisode + extension
                else:
                    newcompletepath = path + os.sep + nomdelaseries + ".S0" + row[0] + ".E" + row[
                        1] + "." + titre_de_lepisode + extension
            else:
                if int(row[1]) < 10:
                    newcompletepath = path + os.sep + nomdelaseries + ".S" + row[0] + ".E0" + row[
                        1] + "." + titre_de_lepisode + extension
                else:
                    newcompletepath = path + os.sep + nomdelaseries + ".S" + row[0] + ".E" + row[
                        1] + "." + titre_de_lepisode + extension
            print(completepath + " ==> " + newcompletepath)
            os.rename(completepath, newcompletepath)
            renamed = True

listoffiles = os.listdir(path)

for filepath in listoffiles:
        completepath = path + os.sep + filepath
        #print(completepath)
        basename_without_ext = os.path.splitext(os.path.basename(completepath))[0]
        extension = os.path.splitext(os.path.basename(completepath))[1]
        # print(basename_without_ext)
        # print(extension)
        # filename

        txt = basename_without_ext
        x = re.search(nomdelaseries + ".S([0-9]{2}).E([0-9]{2}).(.*)", txt)
        if x:
            #print(x)
            #print(basename_without_ext[26:])
            fichierimages = basename_without_ext + ".jpg"
            title = basename_without_ext[26:].replace("à", "a")
            title = title.replace("â", "a")
            title = title.replace("ù", "u")
            title = title.replace("û", "u")
            title = title.replace("ô", "o")
            title = title.replace("é", "e")
            title = title.replace("è", "e")
            title = title.replace("ê", "e")
            title = title.replace("ç", "c")

            title = title.replace(" !", "")
            title = title.replace(" ?", "")
            title = title.replace(" : ", "-")
            title = title.replace(": ", "-")
            title = title.replace(":", "-")
            title = title.replace('"', '')
            title = title.replace("' ", "_")
            title = title.replace("'", "_")
            title = title.replace(" ", "_")
            sqlcommand = "SELECT * FROM episode_list WHERE title = '" + title + "';"
            # print(sqlcommand)
            correct = False
            for row in c.execute(sqlcommand):

                if int(row[0]) < 10:
                    checksaison = "0" + row[0]
                else:
                    checksaison = row[0]

                if int(row[1]) < 10:
                    checkepisode = "0" + row[1]
                else:
                    checkepisode = row[1]


                if checksaison == x[1]:
                    if checkepisode == x[2]:
                        correct = True

            if correct == False:
                #print("Pblm avec "+ completepath)
                #print("Saison: " +checksaison+ " vs " + x[1])
                #print("Episode: " + checkepisode + " vs " + x[2])

                sqlcommand = "SELECT * FROM episode_list WHERE title LIKE '%" + title + "%';"
                for row in c.execute(sqlcommand):
                    titre_de_lepisode = row[2]
                    duree = titre_de_lepisode.find("___(21_min)")
                    if duree > -1:
                        titre_de_lepisode=titre_de_lepisode[:duree]
                    if int(row[0]) < 10:
                        if int(row[1]) < 10:
                            newcompletepath = path + os.sep + nomdelaseries + ".S0" + row[0] + ".E0" + row[1] + "." + titre_de_lepisode + extension
                        else:
                            newcompletepath = path + os.sep + nomdelaseries + ".S0" + row[0] + ".E" + row[1] + "." + titre_de_lepisode + extension
                    else:
                        if int(row[1]) < 10:
                            newcompletepath = path + os.sep + nomdelaseries + ".S" + row[0] + ".E0" + row[1] + "." + titre_de_lepisode + extension
                        else:
                            newcompletepath = path + os.sep + nomdelaseries + ".S" + row[0] + ".E" + row[1] + "." + titre_de_lepisode + extension

                    print(completepath + " ==> " + newcompletepath)
                    os.rename(completepath, newcompletepath)

for filepath in listoffiles:
        completepath = path + os.sep + filepath
        #print(completepath)
        basename_without_ext = os.path.splitext(os.path.basename(completepath))[0]
        extension = os.path.splitext(os.path.basename(completepath))[1]
        # print(basename_without_ext)
        # print(extension)
        # filename

        txt = basename_without_ext
        x = re.search(nomdelaseries + ".S([0-9]{2}).E([0-9]{2}).(.*)", txt)
        if x:
            #print(x)
            #print(basename_without_ext[26:])
            fichierimages = basename_without_ext + ".jpg"
            completepath = path + os.sep + fichierimages
            imagedone = False
            if os.path.isfile(completepath):
                #print("Image find for: "+ basename_without_ext)
                imagedone = True
            else:
                title = basename_without_ext[26:].replace("à", "a")
                title = title.replace("â", "a")
                title = title.replace("ù", "u")
                title = title.replace("û", "u")
                title = title.replace("ô", "o")
                title = title.replace("é", "e")
                title = title.replace("è", "e")
                title = title.replace("ê", "e")
                title = title.replace("ç", "c")

                title = title.replace(" !", "")
                title = title.replace(" ?", "")
                title = title.replace(" : ", "-")
                title = title.replace(": ", "-")
                title = title.replace(":", "-")
                title = title.replace('"', '')
                title = title.replace("' ", "_")
                title = title.replace("'", "_")
                title = title.replace(" ", "_")
                sqlcommand = "SELECT * FROM episode_list WHERE title = '" + title + "';"
                # print(sqlcommand)
                for row in c.execute(sqlcommand):
                    print("Fichier a telecharger: " + row[4])
                    img_data = requests.get(row[4]).content
                    with open(completepath, 'wb') as handler:
                        handler.write(img_data)
                    imagedone = True



# verif table


conn.close()