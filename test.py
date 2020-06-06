import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '.')
from gallica import *






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
from tei_reader import TeiReader
url='https://gallica.bnf.fr/services/Toc?ark=bpt6k5511454q'
session = HTMLSession()
page_html=session.get(url)
# on remplace la balise head par texte sinon bs ne fonctionne pas bien, il enlève les head
page2=page_html.html.html.replace('head','contenu')
soup=bs.BeautifulSoup(page2,'lxml')
# for div in soup.find_all('div0'):
for div in soup.find_all('div0'):
    print("Div : {}".format(div.contenu.text))
    try:
        for div1 in div.find_all('div1'):
        # for div1 in div.find('div1'):
            print("\tDiv1 {}".format(div1.contenu.text))
            try:
                for div2 in div1.find_all('div2'):
                    print("\t\tDiv2 {}".format(div2.contenu.text))
                    try:
                        for div3 in div1.find_all('div3'):
                            print("\t\t\tDiv3 {}".format(div3.contenu.text))
                    except:
                        pass
            except:
                pass
        print("\n")
    except:
        pass



#
# tree=etree.fromstring(page_html.html.html.encode('utf8'))
# tree.xpath('/TEI.2/text/body/div0/div1/head')
# >>> for child_of_root in root:
# ...     for children in child_of_root:
# ...             for children2 in children:
# ...                     print('{} -{}'.format(children2.tag, children2.attrib))
