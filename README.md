# BulletinsMensuelsDesPostes
Utilisation des API Gallica et remise en forme des données
Il est fort probable que ce nous allons faire ici puisse fonctionner sur la plupart des périoques de Gallica

Gallica met à disposition tout un tas de métadonnées qui peuvent permettre le traitement en masse des documents scannés.
Grâce à leurs API http://api.bnf.fr/api-document-de-gallica nous avons accès à ces métadonnées

# Table des matières (TOC)
Ces TOC sont la base même de la récupération de données des Bulletins Mensuels des Postes (BM).
Le but est de fabriquer un tableau qui permettra ensuite (après injection dans une base de données par exemple) de faire des recherches plus simplement que depuis l'interface de la BNF
Ex : https://gallica.bnf.fr/services/Toc?ark=bpt6k5518984r

## Types de TOC
Il y a 2 grands types de données retournées par la fonction TOC :
* les tables des matières (TdM) qui concernent le contenu du document en question.
* les Index qui concernent le contenu d'autres documents (ce qui est extrêmement bien géré par Gallica qui fait effectivement les renvois vers les documents en question)
**Il peut y avoir plusieurs occurrences de chaque type dans un document.**

On trouve des TdM dans toutes les TOC des BM et des Index notamment dans les BM de décembre qui sont des récapitulatifs de l'année.
Le TOC https://gallica.bnf.fr/services/Toc?ark=bpt6k5511454q aura servi à l'élaboration de ce qui va suivre.

## Traitement des TdM
Voici un exmple de TdM extait de https://gallica.bnf.fr/services/Toc?ark=bpt6k5518984r que l'on peut voir dans le document sous sa forme originelle sur https://gallica.bnf.fr/ark:/12148/bpt6k5518984r
```xml
<div1 type="TdM">
    <head>SOMMAIRE. JUIN 1858. N° 34.</head>
    <div2>
    <head>1° INSTRUCTIONS DE L'ADMINISTRATION.</head>
    <div3>
    <head>
        CIRCULAIRE N° 85. - 1
        <hi rend="sup">re</hi>
        DIVISION. - 2
        <hi rend="sup">e</hi>
        BUREAU.
    </head>
    <table>
      <row>
        <cell>
          <seg n="int.000001">EXECUTION de la Convention de poste conclue entre la France et la Bavière, le 19 mars 1858. - Notification d'un décret pour l'exécution de cette Convention. - Instructions à ce sujet</seg>
        </cell>
        <cell>
          <xref from="FOREIGN (5518984/000002.TIF)" n="lie.000001" to="FOREIGN (5518984/000009.TIF)" type="image">246 à 253</xref>
        </cell>
      </row>
```
On voit bien, ici, la hiérarchisation de l'information :
div1 : Titre du sommaire : SOMMAIRE. JUIN 1858. N° 34
  div 2 :  Suet1 => 1° INSTRUCTIONS DE L'ADMINISTRATION
  div 3 : complément Sujet : CIRCULAIRE N° 85. - 1
  table : liste des liens/articles
Sommaire/Sujet1/Articles/lien :
* SOMMAIRE. JUIN 1858. N° 34./1° INSTRUCTIONS DE L'ADMINISTRATION./CIRCULAIRE N° 85. - 1/EXECUTION de la Convention de poste conclue entre la Fra.../**lien**
* SOMMAIRE. JUIN 1858. N° 34./1° INSTRUCTIONS DE L'ADMINISTRATION./CIRCULAIRE N° 85. - 1/DECRET impérial du 1er Juin...

## format des liens
```xml           <xref from="FOREIGN (5518984/000002.TIF)" n="lie.000001" to="FOREIGN (5518984/000009.TIF)" type="image">246 � 253</xref>```
Les liens sont de la forme : from/to (de la page from à la page to)=> ce qui nous importe peu dans notre cas, le but étant, pour nous, de remonter le lien de début d'article.

```xml FOREIGN (5518984/000002.TIF)``` est la partie qui nous intéresse.
### ark du document
*5518984* : début du NOID du document référencé. Il manque ici la clé de validation qu'il va falloir calculer en utilisant l'algorithme indiqué sur : https://metacpan.org/pod/distribution/Noid/noid#NOID-CHECK-DIGIT-ALGORITHM
il faut rajouter bptk6k au NOID
* bpt6k5511454 => bpt6k5511454q
* bpt6k5511363 => bpt6k5511363b
On utilisera la fonction du module bm.py => get_full_ark()
**Toutefois, il est à noter que le lien peut pointer sur un autre document**
### page
000002.TIF => il faudra donc afficher la page 2 en utilisant l'url :
https://gallica.bnf.fr/ark:/12148/*arkCalculé*/f*numPage*

## Python
### extraction des données en Python
* Utilisation de BeautifulSoup
* le xml du TOC contenant "head" qui est supprimé par BeautifulSoup, on remplace le tag "head" par "texte"
```Python
page_html=session.get(url)
# on remplace la balise head par texte sinon bs ne fonctionne pas bien, il enlève les head
page2=page_html.html.html.replace('head','texte')
soup=bs.BeautifulSoup(page2,'lxml')
```
Pour chaque div1
  on note le titre du sommaire
  pour chaque div2
    on note le Sujet1
    pour chaque div3
      on complète le sujet
      pour chaque tableau
        on prend le titre de l'article
        on prend le lien
    pour chaque tableau
      on prend le titre de l'article
      on prend le lien
  pour chaque tableau
    on prend le titre de l'article
    on prend le lien




### Traitement de l'arborescence
