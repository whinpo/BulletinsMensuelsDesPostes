# -*- coding: utf-8 -*-
import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '.')
# from gallica import *






# # test
# noid='5511454'
# ark=get_full_ark(noid)
# bm1=bm(ark)
# print(bm1.title)
# print(bm1.description)


import bs4 as bs
import urllib.request, urllib.error, urllib.parse
import re
import os
import requests
import wget
from pathlib import Path
from datetime import datetime
from requests_html import HTMLSession
import certifi
import csv
import json
from pprint import pprint

def get_full_ark(noid):
    tab=['0','1','2','3','4','5','6','7','8','9','b','c','d','f','g','h','j','k','m','n','p','q','r','s','t','v','w','x','z']
    value=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    total=0
    i=1
    ark='bpt6k{}'.format(noid)
    for chars in ark:
        # on multiplie la valeur du char par sa position (i)
        try:
            total+=value[tab.index(chars)] * i
        except:
            print('rien')
        i=i+1
    modulo = total%29
    cle=tab[value.index(modulo)]
    ret='{}{}'.format(ark,cle)
    # print('ark {} -- total {} -- modulo {} -- cle {} -- obtient : {}{}'.format(ark,total,modulo,cle,ark,cle))
    return ret

def get_lien(xref):
    # FOREIGN (5511454/000060.TIF)
    # foreign=5511454/000060
    foreign=xref.split('(')[1].split(')')[0].split('.')[0]
    # noid=5511454
    noid=foreign.split("/")[0]
    # ark =
    ark=get_full_ark(noid)
    #page=60
    page=foreign.split("/")[1].lstrip('0')
    ret='https://gallica.bnf.fr/ark:/12148/{}/f{}.image'.format(ark,page)
    # print(ret)
    return(ret)

# permet de rechercher les div arborescences de div.
# i : permet de rechercher les divi : div0, div1  etc..
# def get_div(soup,i):
#     divI='div{}'.format(i)
#     # print(divI)
#     # print("boucle {}".format(divI))
#     # try:
#     for div in soup.find_all(divI):
#         print()
#         if (div.get('type') != 'Index') :
            # print(soup.div['type'])
        # if soup.div1['type'] != 'Index' :
            # print('ononon')
    #         tab="\t"*i
    #         # print('{}on descend'.format(tab))
    #         print('{}{}'.format(tab,div.contenu.text))
    #         try:
    #             j=i+1
    #             # # on incrémente I pour descendre dans l'arborescence
    #             get_div(div,j)

    #             # on lit les tables de div
    #             try:
    #                 # print()
    #                 # print('{}table'.format(tab))
    #                 # print('{}{}'.format(tab,div.table.prettify()))
    #                 for tables in div.find_all('table',recursive=False):
    #                     # print('{}{}'.format(tab,tables.prettify()))
    #                     for rows in tables:
    #                         for cells in rows.find_all('cell'):
    #                             try:
    #                                 print("\t{}Article - {}".format(tab,cells.seg.text))
    #                             except:
    #                                 xref=cells.xref.attrs.get("from")
    #                                 print("\t\t{}-{}".format(tab,get_lien(xref)))
    #             except:
    #                 # print('pas de tableau ici')
    #                 pass
    #             # on lit les listes
    #             try:
    #                 for listes in div.find_all('list',recursive=False):
    #                     for items in listes:
    #                             # print(items)
    #                             try:
    #                                 print("\t{}Liste-Article - {}".format(tab,items.seg.text))
    #                             except:
    #                                 pass
    #                             try:
    #                                 xref=items.xref.attrs.get("from")
    #                                 print("\t\t{}Liste-Lien - {}".format(tab,get_lien(xref)))
    #                             except:
    #                                 pass
    #             except:
    #                 # print('pas de liste ici')
    #                 pass
    #         except:
    #             # print('on remonte')
    #             pass
    # # except  Exception as e:
    # #     print('po')
    # #     print(e)
    # #     pass


url='https://gallica.bnf.fr/services/Toc?ark=bpt6k5511454q'
# url='https://gallica.bnf.fr/services/Toc?ark=bpt6k55112845'
session = HTMLSession()
page_html=session.get(url)
# on remplace la balise head par texte sinon bs ne fonctionne pas bien, il enlève les head
page2=page_html.html.html.replace('head','contenu')
soup=bs.BeautifulSoup(page2,'lxml')
Table=soup.find("contenu", text=re.compile('TABLE CHRONO'))
tdm=Table.previous_element

# get_div(soup,0)

#if soup.div1.has_attr('type') and soup.div1['type'] == 'Index'






#
# tree=etree.fromstring(page_html.html.html.encode('utf8'))
# tree.xpath('/TEI.2/text/body/div0/div1/head')
# >>> for child_of_root in root:
# ...     for children in child_of_root:
# ...             for children2 in children:
# ...                     print('{} -{}'.format(children2.tag, children2.attrib))
