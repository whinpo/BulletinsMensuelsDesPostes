# from bs4 import BeautifulSoup
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

global urlBNF
urlBNF="https://gallica.bnf.fr/"

# retourne un ark complet avec la clé calculée à partir d'un fragment de noid retourné par une TOC
#https://metacpan.org/pod/distribution/Noid/noid#NOID-CHECK-DIGIT-ALGORITHM
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

# OAI="{}/services/OAIRecord?ark={}".format(urlBNF,ark)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class bm:
    def __init__(self, ark):
        self.ark = ark
        self.oai=self.get_oai()
        self.url="{}ark:/12148/{}".format(urlBNF,self.ark)
        self.date=self.oai['date']
        self.annee=self.date.split('-',1)[0]
        self.title=self.oai['title']
        self.description=self.oai['description']
        # print('\tGénération {} - {} - {}'.format(self.ark,self.description, self.url))
        # self.toc=self.get_toc()
        self.urlPDF="{}{}".format(self.url,".pdf")
        self.urlTexteBrut="{}{}".format(self.url,".texteBrut")
        self.nqamoyen=self.oai['nqamoyen']
        # self.properties={
        #     "ark" :ark ,
        #     "url" : self.url,
        #     "toc" : self.toc,
        #     "oai" : self.oai,
        #     "date" : self.date,
        #     "title" : self.title,
        #     "description" : self.description,
        #     "urlPDF" : self.urlPDF,
        #     "urlTexteBrut" : self.urlTexteBrut,
        #     "nqamoyen" : self.nqamoyen
        # }
        # self.json=json.dumps(self.properties)
    # récupération infos document date et titre
    def get_oai(self):
        oai={}
        urlOAI="{}services/OAIRecord?ark={}".format(urlBNF,self.ark)
        # print(urlOAI)
        session = HTMLSession()
        page_html=session.get(urlOAI)
        soup=bs.BeautifulSoup(page_html.html.html,'lxml')
        # Récupération du titre
        oai['title']=soup.metadata.find('dc:title').get_text()
        # récupération de la description
        # on prend la 2ème
        # <dc:description>
        #  juillet 1922
        # </dc:description>
        # <dc:description>
        #  1922/07 (N8)-1922/12.
        # </dc:description>
        # <dc:description>
        # </dc:description>
        # => 1922/07 (N8)-1922/12.
        oai['description']=soup.metadata.find_all('dc:description')[1].get_text()
        # on récupère la date au format 1895-05 ou 1930-12-05
        # on essaie de convertir la date à l'un des 2 formats puis on remet en texte
        # pour que le json fonctionne
        dateTmp=soup.date.get_text()
        try:
            dateTmp1=datetime.strptime(dateTmp,"%Y-%m-%d")
        except:
            try:
                dateTmp1=datetime.strptime(dateTmp,"%Y-%m")
            except:
                dateTmp1=datetime.strptime(dateTmp,"%Y")
        oai['date']=datetime.strftime(dateTmp1,"%Y-%m-%d")
        # nqamoyen doit être supérieur à 60 pour recherche full texte
        oai['nqamoyen']=soup.nqamoyen.get_text()
        return oai

    # récupération table des matières sous forme d'une liste
    # à faire pour https://gallica.bnf.fr/services/Toc?ark=bpt6k5511454q => on obtient pour le moment n'importe quoi
    # voir la liste des div1 et div2 et head head2
    # on a 2 types de tableaux :
    # <div1 type="TdM"> => table des matières
    # <div1 type="Index"> => index qui renvoie sur d'autres documents

    # les index sont
   # <div1 type="Index">
   #    <head>SOMMAIRE. DECEMBRE 1856. N� 16, 2<hi rend="sup">e</hi>
   #      suppl�ment.</head>
   #    <div2>
   #      <head>INSTRUCTIONS DE L'ADMINISTRATION.</head>
   #      <div3>
   #        <head>CIRCULAIRE N� 38. - 1<hi rend="sup">re</hi>
   #          DIVISION. - 2<hi rend="sup">e</hi>
   #          BUREAU.</head>
   #        <list>
   #          <item>
   #            <seg n="int.000022">EXECUTION de la Convention de poste conclue entre la France et le Grand-Duch� de Bade le 14 octobre 1856. - Notification d'un d�cret pour l'ex�cution de cette Convention. - Instructions � ce sujet</seg>
   #            <xref from="FOREIGN (5511454/000075.TIF)" n="lie.000022" to="FOREIGN (5511454/000086.TIF)" type="image">710 � 721</xref>
   #          </item>
   #          <item>


# <div1 type="TdM">
#     <head>SOMMAIRE. JUIN 1858. N° 34.</head>
#     <div2>
#     <head>1° INSTRUCTIONS DE L'ADMINISTRATION.</head>
#     <div3>
#     <head>
#         CIRCULAIRE N° 85. - 1
#         <hi rend="sup">re</hi>
#         DIVISION. - 2
#         <hi rend="sup">e</hi>
#         BUREAU.
#     </head>
#     <table>
#         <row>
#             <cell>
#                 <seg n="int.000001">
#                     EXECUTION de la Convention de poste conclue entre la France et la Bavière, le 19 mars 1858. - Notification d'un décret pour l'exécution de cette Convention. - Instructions à ce sujet
#                 </seg>
#             </cell>
#
    def get_toc(self):
        # liste TOC
        arraytoc=[]
        # connexion
        urlTOC="{}services/Toc?ark={}".format(urlBNF,self.ark)
        print(urlTOC)
        # print(urlTOC)
        session = HTMLSession()
        page_html=session.get(urlTOC)
        # on peut avoir des TOC vides ex : https://gallica.bnf.fr/ark:/12148/bpt6k5514117b
        try:
            soup=bs.BeautifulSoup(page_html.html.html,'lxml')
            # récupération du contenu on prend tous les 'row'
            # <row>
            #    <cell>
            #     <seg n="int.000001">
            #      <hi rend="bold">
            #       Table chronologique des Bulletins
            #      </hi>
            #     </seg>
            #    </cell>
            #    <cell>
            #     <xref from="FOREIGN (5504258/000286.TIF)" n="lie.000001" type="image">
            #      277
            #     </xref>
            #    </cell>
            #   </row>
            # <row>
            rows=soup.find_all('row')
            rows
            for row in rows:
                try:
                    # contenu du champ seg en enlevant le HTML
                    texte= row.seg.get_text()
                    # print(texte)
                except:
                    texte=row.get_text()
                    # print(row)
                # récupération du numéro de page
                # <xref from="FOREIGN (5504258/000286.TIF)" n="lie.000001" type="image">
                # => devient 286
                # url= urldudoc/f286

                #on met la page à 1 au cas où il n'y aurait pas de page dans le sommaire
                page=1
                try:
                    page=row.xref.get('from').split('/')[1].split('.')[0].lstrip('0')

                except:
                    # on peut avoir des lignes vides retournées par Gallica : on les ignore
                    # voir les autres pb possibles
                    # si on a un sommaire de la forme : page 18 à 25 il est possible qu'une des 2 pages soit en type:unresolved et n'ait pas de from
                    # => on boucle
                    print("\t\t{}Pb page TOC {}{}".format(bcolors.WARNING,self.ark,bcolors.ENDC))
                    print(texte)
                # print(urlPage)
                # print("\n")
                # arraytoc.append({"texte" : texte, "page": page,"urlPage" : urlPage})
                arraytoc.append({"texte" : texte, "page": page})
        except Exception as e:
            toto="p"
            print(e)
            print("\t\t{}Pas de TOC pour {}{}".format(bcolors.WARNING,self.ark,bcolors.ENDC))
        # print('fin')
        # print(arraytoc)
        return arraytoc
    def print_properties_a_plat(self):
        for toc in self.toc:
            prop={
                        "ark" : self.ark ,
                        "url" : self.url,
                        "toc" : toc,
                        "oai" : self.oai,
                        "date" : self.date,
                        "annee" : self.annee,
                        "title" : self.title,
                        "description" : self.description,
                        "urlPDF" : self.urlPDF,
                        "urlTexteBrut" : self.urlTexteBrut,
                        "nqamoyen" : self.nqamoyen
            }
            # with open(fileName, "a") as outfile:
            # # Append 'hello' at the end of file
            #     json.dump(prop,outfile, indent=4)
            #     outfile.write(',')
            print(prop)

        # print("{}\n".format(ret))
def get_TOC_debut_fin(anneedebut,anneefin):
    global filePath
    filePath="/mnt/700G/Bulletins mensuels des postes/TOC"
    # si le répertoire n'existe pas on le crée
    dirAcreer = Path(filePath)
    if not dirAcreer.exists():
        dirAcreer.mkdir(parents=True, exist_ok=True)
        global fileName
    fileName="{}/{}-{}.json".format(filePath,anneedebut,anneefin)
    print(fileName)
    # on supprime le fichier si il existe
    if os.path.exists(fileName):
            os.remove(fileName)
    for annee in range(anneedebut, anneefin):
        listebm=[]
        print("On traite l'année: {}".format(annee))
        #

        # if not dirAcreer.exists():
        # 	dirAcreer.mkdir(parents=True, exist_ok=True)
        # dirAcreer = Path("{0}/TXT".format(download_dir))
        # if not dirAcreer.exists():
        # 	dirAcreer.mkdir(parents=True, exist_ok=True)
        # dirAcreer = Path("{0}/PDF".format(download_dir))
        # if not dirAcreer.exists():
        # 	dirAcreer.mkdir(parents=True, exist_ok=True)


        session = HTMLSession()

        # 1878-1935
        urlannee="https://gallica.bnf.fr/ark:/12148/cb32730626t/date{0}".format(annee)
        # 1855 -1878
        urlannee="https://gallica.bnf.fr/ark:/12148/cb32729505j/date{0}".format(annee)
        page_html=session.get(urlannee)
        # on exécute le javascript
        print('Analyse page année {0}...'.format(urlannee))
        page_html.html.render(sleep=2)

        #page_html.html.html contient le html avec javascript exécuté
        soup=bs.BeautifulSoup(page_html.html.html,'lxml')
        # on récupère tous les liens de l'année
        resultat=soup.find_all('span',{"class": "day-number"})
        for spans in resultat:
            if spans.a.get('href'):
                finalurl=spans.a.get('href')
                # finalurl="https://gallica.bnf.fr/ark:/12148/cb32730626t/date{0}0101".format(annee)
                # print(finalurl)

                #urllib.request.urlopen(finalurl)
                #urllib.request.urlopen(finalurl)
                session = HTMLSession()
                page_html=session.get(finalurl)

                # on exécute le javascript
                print('Analyse contenu page {0}...'.format(finalurl))
                page_html.html.render(sleep=2)

                #page_html.html.html contient le html avec javascript exécuté
                soup=bs.BeautifulSoup(page_html.html.html,'lxml')

                # on regarde si la page a affiché une liste de documents ou si elle affiche directement un item
                # exemple : https://gallica.bnf.fr/ark:/12148/cb32730626t/date19330111 =>
                # donne en fait une url https://gallica.bnf.fr/ark:/12148/bpt6k5827116v.item
                urldest=page_html.url
                # print("urldest {0}".format(urldest))
                if ".item" in urldest:
                    # print("lien direct {0}".format(urldest))
                    print("\t{}Lien direct {}{}".format(bcolors.WARNING,urldest,bcolors.ENDC))
                    # https://gallica.bnf.fr/ark:/12148/bpt6k5827116v.item
                    # => https://gallica.bnf.fr/ark:/12148/bpt6k5827116v
                    lien=urldest.split('.item')[0]
                    ark=lien.split('ark:/12148/')[1]
                    bmobject=bm(ark)
                    bmobject.print_properties_a_plat()

                else:
                    # on extrait les résultats de la recherche
                    for numeros in soup.find_all('div',class_='resultat_img'):
                        # on éclate l'url et on récupère le ark
                        #https://gallica.bnf.fr/ark:/12148/bpt6k5504258b?rk=214593;2
                        # => ark:/12148/bpt6k5504258b
                        lien=numeros.a.get('href').split('?')[0]
                        ark=lien.split('ark:/12148/')[1]
                        bmobject=bm(ark)
                        bmobject.print_properties_a_plat()
                        # on écrit dans le fichier
        # with open(fileName, "a") as outfile:
        #     # Append 'hello' at the end of file
        #     json.dump(listebm,outfile, indent=4)
        # listebm
