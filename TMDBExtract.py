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




conn = sqlite3.connect(seriename+'.db')
c = conn.cursor()

# Create table
c.execute(
    '''CREATE TABLE IF NOT EXISTS `episode_list`(saisons varchar(250)  NOT NULL default '',episodes varchar(250)  NOT NULL default '',title varchar(250)  NOT NULL default '' );''')
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
while endoflist == False:
    newurl = url + '/season/' + str(index)+'?language=fr-FR'
    print(newurl)
    html_doc = scraper.get(newurl).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    liste_ep = soup.find_all("a", class_="no_click open")

    for x in liste_ep:
        #print(x)
        idx_episode = str(x).find('episode="')+9
        idx_title = str(x).find('title="')+7
        idx_title = str(x).find('-',idx_title) + 2
        idx_fepisode = str(x).find('"', idx_episode)
        idx_ftitle = str(x).find('"', idx_title)
        #print("EP Debut: " + str(idx_episode)+" - Fin: " + str(idx_fepisode))
        #print("TIT Debut: " + str(idx_title) + " - Fin: " + str(idx_ftitle))
        episode=str(x)[idx_episode:idx_fepisode]
        title=str(x)[idx_title:idx_ftitle]
        title=title.replace('"','').replace("'","_").replace(" ","_")
        trouve="S" + str(index)+".E"+episode+"."+title


        if trouve != precedent:
            print("S" + str(index)+".E"+episode+"."+title)
            sqlcommand = "INSERT INTO episode_list (saisons,episodes , title) VALUES ('"+str(index)+"','"+episode+"','"+title+"');"
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