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
import cfscrape as cloudscraper
from bs4 import BeautifulSoup
import sqlite3
import os
import platform
from urllib.parse import urlparse


#--------------------------------------------#
#                Variables                   #
#--------------------------------------------#
a = "Hello World"
url = "https://www.themoviedb.org/tv/57532-paw-patrol"

#--------------------------------------------#
#             Code Fonction                  #
#--------------------------------------------#





#--------------------------------------------#
#               Code Principal               #
#--------------------------------------------#

url_decopose = urlparse(url)
domain = url_decopose.netloc.split('.')
website = url_decopose.scheme + "://" + url_decopose.netloc
path = url_decopose.path.split('/')
seriename = path[2]


os.remove(seriename+'.db')

conn = sqlite3.connect(seriename+'.db')
c = conn.cursor()

# Create table
c.execute(
    '''CREATE TABLE IF NOT EXISTS `episode_list`(saisons varchar(250)  NOT NULL default '',episodes varchar(250)  NOT NULL default '',title varchar(250)  NOT NULL default '',originaux varchar(250)  NOT NULL default '',images varchar(250)  NOT NULL default '' );''')
#scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# One TLS v1.3 cipher and one TLS v1.2 cipher
cloudscraper.DEFAULT_CIPHERS = 'TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES256-SHA384'
scraper = cloudscraper.create_scraper()

# Recherche de <li><a href="/tv/57532-paw-patrol/seasons">Saisons</a></li>
# "https://www.themoviedb.org/tv/57532-paw-patrol/seasons?language=fr-FR"
# https://www.themoviedb.org/tv/57532-paw-patrol/season/2?language=fr-FR
index = 0
endoflist = False
precedent=""
original=""
image=""
while endoflist == False:
    newurl = url + '/season/' + str(index)+'?language=fr-FR'
    print(newurl)
    html_doc = scraper.get(newurl).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    liste_ep = soup.find_all("div", class_="card")

    for x in liste_ep:

        idx_episode = str(x).find('<a class="no_click open" episode="')+34
        #idx_title = str(x).find('title="')+7
        #idx_title = str(x).find('-',idx_title) + 2
        idx_title = str(x).find('<img alt="')+10
        idx_img = str(x).find('srcset="') + 8
        idx_fepisode = str(x).find('"', idx_episode)
        #idx_ftitle = str(x).find('"', idx_title)
        idx_ftitle = str(x).find('"', idx_title)
        idx_fimg = str(x).find('"', idx_img)

        #print("EP Debut: " + str(idx_episode)+" - Fin: " + str(idx_fepisode))
        #print("TIT Debut: " + str(idx_title) + " - Fin: " + str(idx_ftitle))
        #print("IMG Debut: " + str(idx_img) + " - Fin: " + str(idx_fimg))
        #print(x)

        if (idx_img >8):
            setdimages = str(x)[idx_img:idx_fimg]
            #print(setdimages)
            aimages = setdimages.split(",")
            #print(aimages)
            idx_lostimage = len(aimages) - 1
            #print(aimages[idx_lostimage])
            #print(aimages[idx_lostimage].split(" "))
            aimages = aimages[idx_lostimage].strip().split(" ")
            image = website + aimages[0]
            #print("Image: " + image)
        else:
            image=""
            idx_title = str(x).find('title="')+7
            idx_title = str(x).find('-',idx_title) + 2
            idx_ftitle = str(x).find('"', idx_title)

        episode=str(x)[idx_episode:idx_fepisode]
        #print("Episode: "+ episode)

        title=str(x)[idx_title:idx_ftitle]
        #print("Titre: "+ title)

        title = title.replace("à", "a")
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
        title = title.replace('"','')
        title = title.replace("' ", "_")
        title = title.replace("'","_")
        title = title.replace(" ","_")

        newepurl = url + "/season/"+str(index)+"/episode/"+episode+"?language=en-EN"
        #print(newepurl)
        html_doc = scraper.get(newepurl).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        idx_titleen= str(soup).find('<h3><a class="no_click open" episode="'+episode+'"')+35
        idx_titleen = str(soup).find('>',idx_titleen)+1
        idx_ftitleen = str(soup).find('<', idx_titleen)
        original=str(soup)[idx_titleen:idx_ftitleen]
        original = original.replace("à", "a")
        original = original.replace("â", "a")
        original = original.replace("ù", "u")
        original = original.replace("û", "u")
        original = original.replace("ô", "o")
        original = original.replace("é", "e")
        original = original.replace("è", "e")
        original = original.replace("ê", "e")
        original = original.replace("ç", "c")

        original = original.replace(" !", "")
        original = original.replace(" ?", "")
        original = original.replace(" : ", "-")
        original = original.replace(": ", "-")
        original = original.replace(":", "-")
        original = original.replace('"', '')
        original = original.replace("' ", "_")
        original = original.replace("'", "_")
        original = original.replace(" ", "_")

        trouve="S" + str(index)+".E"+episode+"."+title


        if trouve != precedent:
            #print("S" + str(index)+".E"+episode+"."+title)
            sqlcommand = "INSERT INTO episode_list (saisons,episodes , title, originaux, images) VALUES ('"+str(index)+"','"+episode+"','"+title+"','"+original+"','"+image+"');"
            print(sqlcommand)
            c.execute(sqlcommand)
        precedent=trouve


    index = index + 1
    texte = soup.get_text()
    oups = texte.find("Oops! We can't find the page you're looking for")

    if index > 1 and oups!=-1:
        endoflist = True


conn.commit()

conn.close()