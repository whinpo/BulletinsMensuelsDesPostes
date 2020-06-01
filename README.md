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
* les tables des matières (TdM) qui concerne le contenu du document en question 
* les Index qui concernent le contenu d'autres documents (ce qui est extrêmement bien géré par Gallica qui fait effectivement les renvois vers les documents en question)

On trouve des TdM dans toues les TOC des BM et des Index notamment dans les BM de décembre qui sont des récapitulatifs de l'année
Le TOC https://gallica.bnf.fr/services/Toc?ark=bpt6k5511454q aura servi à l'élaboration de ce qui va suivre

