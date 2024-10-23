# Implémentation des algorithmes de sélection de rencontres sportives pour un tournoi à élimination directe.

*Licence Pro 2024-2025*

Ce projet consiste en une génération d'un calendrier de rencontres sportives entre joueurs selon leurs catégories et leurs appartenances à un club.

## PRÉRÉQUIS : 

Pour bien utiliser le document, assurez vous de bien avoir installer pandas.
Assurez vous que pip soit bien installé : `pip --version`

Installer pandas via la commande : `pip install pandas`

Pour la lecture de fichier .ods, veuillez installer odfpy : `pip install odfpy`


## UTILISATION : 

Pour générer les matchs, il vous faut insérer la liste des joueurs qui participent au tournoi. Exécutez le script exemple_tri.py en rentrant en paramètre le nom de votre fichier .ods ainsi que la feuille de calcul contenant la liste des joueurs.
`python3 .\selection_matchs.py 2425_lpro_data_projet1 data`

*Si vous voulez ajouter ou supprimer des joueurs, veuillez modifier la liste des joueurs du fichier 2425_lpro_data_projet1.ods*