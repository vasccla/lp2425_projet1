import random

import pandas as pd # Utilisation de pandas pour une manipulation plus simple et plus flexible des données

from Class.File import File
from Class.Pile import Pile

def lecture_joueurs_et_categories(fichier_joueurs:str, fichier_categories:str):

    # Lecture du fichier csv avec les joueurs
    joueurs = pd.read_csv(fichier_joueurs) # On met le résultat de la requête dans une variable 'joueurs' de type DataFrame

    if joueurs.empty:
        print("Le fichier CSV est vide ou non valide.")
        return None
    
    # Lecture du fichier csv avec les catégories
    categories = pd.read_csv(fichier_categories) # On met le résultat de la requête dans une variable 'categories' de type DataFrame

    if categories.empty:
        print("Le fichier CSV est vide ou non valide.")
        return None

    

    def assigner_categorie(joueur):
        """
            ATTRIBUTION CATEGORIE D'AGE ET DE POIDS POUR CHAQUES JOUEURS

            On commence par extraire l'âge et le poids du joueur.
            Pour chaque catégorie d'âge définie dans le dictionnaire categories_age_poids, on vérifie si l'âge
            du joueur se situe dans les limites de la catégorie.
            Si c'est le cas, on parcourt les plages de poids associées à cette catégories pour déterminer si 
            le poids du joueur est compris dans l'une d'elles.
            Si les 2 conditions sont réunis, on retourne la catégorie d'âge et la plage de poids sous la forme
            '20-25kg'
            Si il n'y a aucune correspondance, on retourne None, None
        """
        age, poids = joueur['age'], joueur['poids']

        for _, row in categories.iterrows():
            if row['age_min'] <= age <= row['age_max']:
                if row['poids_min'] <= poids <= row['poids_max']:
                    return row['categorie'], f"{row['poids_min']}-{row['poids_max']}kg"
                
        return None, None

    # On applique la fonction assigner_categorie à chaque ligne du DataFrame "joueurs", issue de la lecture du fichier csv
    # On le réalise ligne par ligne "axis=1" et non par colonne "axis=0"
    # Si la fonction renvoie une liste ou un tuple pour chaque ligne,  'expand' va étendre la sortie sur plusieurs colonnes 
    joueurs[['categorie_age', 'categorie_poids']] = joueurs.apply(assigner_categorie, axis=1, result_type='expand')

    # Calcul du nombre de joueurs par club dans chaque catégorie
    joueurs['nb_joueurs_club'] = joueurs.groupby(['categorie_age', 'categorie_poids', 'club'])['nom'].transform('count')


    # Affichage des joueurs par catégories d'âge et de poids
    
    for (cat_age, cat_poids), group in joueurs.groupby(['categorie_age', 'categorie_poids']):
        group = group.sort_values(by='nb_joueurs_club', ascending=False)
        """
        print(f"Joueur(s) dans la catégorie {cat_age} {cat_poids}:")
        print(group[['nom', 'prenom', 'poids', 'age', 'club', 'nb_joueurs_club']],'\n')
        """
        
    
    return joueurs


def organiser_et_afficher_matchs_par_categories(joueurs):
    # Groupement des joueurs par catégories d'âge et de poids
    groupes = joueurs.groupby(['categorie_age', 'categorie_poids'])

    for (cat_age, cat_poids), joueurs in groupes:
        print(f"\nMatch pour la catégorie {cat_age} {cat_poids} : ")
        temp_pile:Pile = Pile()
        temp_file:File = File()
        tab_match:list = []

        # Si le nombre de joueurs est impair, attribuer un "bye"
        if len(joueurs) % 2 != 0:
            joueur_bye = random.choice(joueurs.index)
            print(f"Bye pour : {joueurs['nom'][joueur_bye]} {joueurs['prenom'][joueur_bye]}")
            joueurs = joueurs.drop(joueur_bye)

        # Remplissage de la file avec les données joueurs à partir du début de la DF
        for i in range(0, len(joueurs)//2):
            temp_file.emfiler([joueurs["nom"].iloc[i],joueurs["prenom"].iloc[i],joueurs["club"].iloc[i]])

        # Remplissage de la pile avec les données joueurs à partir de la moitié de la DF
        for i in range(len(joueurs)//2,len(joueurs)):
            temp_pile.empiler([joueurs["nom"].iloc[i],joueurs["prenom"].iloc[i],joueurs["club"].iloc[i]])
        # print("Affichage file (length : %s) : %s \n Affichage pile (length : %s) : %s" % (len(temp_file.afficher()),temp_file.afficher(),len(temp_pile.afficher()),temp_pile.afficher()))    

        # Association du premier joueur avec le dernier joueur et ainsi de suite
        while len(temp_file.afficher()) != 0 and len(temp_pile.afficher()) != 0:
            tab_match.append([temp_file.defiler(),temp_pile.depiler()])
            
        # Affichage des matchs
        for j in range(0,len(tab_match),1):
            print("%s %s vs %s %s" % (tab_match[j][0][0],tab_match[j][0][1],tab_match[j][1][0],tab_match[j][1][1]))

joueur = lecture_joueurs_et_categories('joueur.csv', 'categorie.csv')
organiser_et_afficher_matchs_par_categories(joueur)