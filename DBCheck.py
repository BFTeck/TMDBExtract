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

path = "Y:\Dessins animés - Enfants\Paw_Patrol"
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

# Create table

c.execute(
    '''CREATE TABLE IF NOT EXISTS `episode_manquant`(saisons varchar(250)  NOT NULL default '',episodes varchar(250)  NOT NULL default '',title varchar(250)  NOT NULL default '',originaux varchar(250)  NOT NULL default '',images varchar(250)  NOT NULL default '' );''')

sqlcommand = "DELETE FROM `episode_manquant`;"
c.execute(sqlcommand)
conn.commit()
sqlcommand = "INSERT INTO `episode_manquant` SELECT * FROM episode_list;"
c.execute(sqlcommand)
conn.commit()

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
            sqlcommand = "SELECT * FROM `episode_manquant` WHERE title = '" + title + "';"
            #print(sqlcommand)
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

                        sqlcommand = "DELETE FROM `episode_manquant` WHERE title = '"+title+"';"
                        c.execute(sqlcommand)
                        conn.commit()

sqlcommand = "SELECT * FROM `episode_manquant`;"
# print(sqlcommand)
for row in c.execute(sqlcommand):
            print("S"+row[0]+" Ep"+row[1]+" - "+row[2])

conn.commit()
conn.close()