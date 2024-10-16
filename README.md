# Implémentation des algorithmes de sélection de rencontres sportives pour un tournoi à élimination directe.

*Licence Pro 2024-2025*

Ce projet consiste en une génération d'un calendrier de rencontres sportives entre joueurs selon leurs catégories et leurs appartenances à un club.

Préréquis : 
Pour bien utiliser le document, assurez vous de bien avoir installer pandas.'
`Assurez vous que pip est bien insstallé : pip --version`
`pip install pandas`

Pour la lecture de fichier .ods, veuillez installer odfpy.
`pip install odfpy`


## UTILISATION : 

Pour générer les matchs, il vous faut insérer la liste des joueurs qui participent au tournoi. Exécutez le script exemple_tri.py en rentrant en paramètre le nom de votre fichier .ods ainsi que la feuille de calcul contenant la liste des joueurs.
`python3 .\exemple_tri.py {fichier_ods} {feuille_de_calcul}`