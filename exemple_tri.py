import random
import sys
from collections import defaultdict

import pandas as pd # Utilisation de pandas pour une manipulation plus simple et plus flexible des données

from Class.Graphe import Graphe #Importation de la classe Graphe qui est implémenter dans Class/Graphe.py

def recherche_largeur(graphe:Graphe(), source, puits, parent):
    visite = {source}
    file = [source]

    while file:
        sommet = file.pop(0)

        for voisin in graphe.obtenir_voisins(sommet):
            if voisin not in visite and graphe.liste_adjacence[sommet][voisin] > 0:
                visite.add(voisin)
                parent[voisin] = sommet
                if voisin == puits:
                    return True
                file.append(voisin)
    return False

def edmonds_karp(graphe:Graphe(), source, puits):
    # Dictionnaire pour stocker le chemin parent pour la reconstruction des chemins
    parent = {}
    # Initialisation du flot maximum à 0
    flot_maximum = 0

    # Tant qu'il existe un chemin augmentant du source au puits
    while recherche_largeur(graphe, source, puits, parent):
        # Initialise le flot minimum du chemin courant à l'infini
        flot_chemin = float('Inf')
        v = puits # On commence à partir du puits

        # Remonter le chemin depuis le puits jusqu'à la source
        while v != source:
            # Si le sommet n'a âs de parent, on sort
            if v not in parent:
                return flot_maximum # Retourne le flot maximum atteint
            
            s = parent[v]  # Récupère le sommet parent de v
            # Mis à jour de la capactié minimale du chemin actuel
            flot_chemin = min(flot_chemin, graphe.liste_adjacence[s][v]) 
            v = s # Remonter au sommet parent

        # Mettre à jour les capacités du graphe
        v = puits # Réinitialisation de v au puits
        while v != source:
            u = parent[v] # Récuperation du sommet parent v
            # Réduction de l'arête u -> v
            graphe.liste_adjacence[u][v] -= flot_chemin
            # Augmentation de la capacaité de l'arête v -> u
            graphe.liste_adjacence[v][u] += flot_chemin
            v = parent[v] # Remonter au sommet parent

        # Ajouter le flot du chemin courant au flot maximum
        flot_maximum += flot_chemin

    return flot_maximum # Retourner le flot maximum calculé


"""
Le fichier csv des joueurs sera générer par la fonction ci-dessous.
Si le fichier n'existe pas, il sera créer.
Si des joueurs sont rajouter dans le fichier ods dans l'avenir, les données du fichier csv seront écrasés et le fichier sera remis à jour.
"""

def lire_joueur_ods(fichier_ods: str, nom_feuille: str):
    # Lire la feuille spécifiée en tant que DataFrame
    df = pd.read_excel(fichier_ods, sheet_name=nom_feuille)

    # Sélectionner les colonnes souhaitées
    colonnes_souhaitees = ['NOM', 'PRÉNOM', 'POIDS', 'AGE', 'CLUB'] # Remplacez par les noms réels de vos colonnes
    df_selection = df[colonnes_souhaitees].copy()

    # Modifier les noms des colonnes
    noms_nouveaux = {'NOM': 'nom', 'PRÉNOM': 'prenom', 'POIDS': 'poids', 'AGE': 'age', 'CLUB': 'club'} # Remplacez par vos nouveaux noms
    df_selection.rename(columns=noms_nouveaux, inplace=True)

    # Enregistrer le DataFrame filtré avec les nouveaux noms en CSV
    csv_file_path = f"joueur.csv"
    df_selection.to_csv(csv_file_path, index=False)
    return csv_file_path

def lecture_joueurs_et_categories(fichier_joueurs:str, fichier_categories:str):

    try:
            # Lecture du fichier csv avec les joueurs
        joueurs = pd.read_csv(fichier_joueurs) # On met le résultat dans la variable 'joueurs' de type DataFrame
    
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_joueurs} n'a pas été trouvé.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Erreur : Le fichier {fichier_joueurs} est vide ou corrompu.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier joueurs : {e}")
        return None
    
    try:
            # Lecture du fichier csv avec les catégories
        categories = pd.read_csv(fichier_categories) # On met le résultat dans la variable 'categories' de type DataFrame
    
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_categories} n'a pas été trouvé.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Erreur : Le fichier {fichier_categories} est vide ou corrompu.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier joueurs : {e}")
        return None
    

    """ On commence par extraire l'âge et le poids du joueur.
     Pour chaque catégorie d'âge définie dans le dictionnaire categories_age_poids, on vérifie si l'âge
     du joueur se situe dans les limites de la catégorie.
     Si c'est le cas, on parcourt les plages de poids associées à cette catégories pour déterminer si 
     le poids du joueur est compris dans l'une d'elles.
     Si les 2 conditions sont réunis, on retourne la catégorie d'âge et la plage de poids sous la forme
     "20-25kg". Si il n'y a aucune correspondance, on retourne None, None """

    def assigner_categorie(joueur):
        """
            ATTRIBUTION CATEGORIE D'AGE ET DE POIDS POUR CHAQUES JOUEURS

            On commence par extraire l'âge et le poids du joueur.
            Pour chaque catégorie d'âge définie dans le dictionnaire categories_age_poids,
            on vérifie si l'âge du joueur se situe dans les limites de la catégorie.
            Si c'est le cas, on parcourt les plages de poids associées à cette
            catégories pour déterminer si 
            le poids du joueur est compris dans l'une d'elles.
            Si les 2 conditions sont réunis, on retourne la catégorie d'âge et
            la plage de poids sous la forme '20-25kg'
            Si il n'y a aucune correspondance, on retourne None, None
        """
        age:int = joueur['age']
        poids:float = joueur['poids']
        categorie_assignee = None
        plage_poids = None

        for _, row in categories.iterrows():
            if row['age_min'] <= age <= row['age_max']:
                if poids <= row['poids_max']:
                    categorie_assignee = row['categorie']
                    plage_poids = f"{row['poids_min']}-{row['poids_max']}kg"
                    break  # Sortir de la boucle dès qu'on trouve la catégorie valide
                else:
                    # On garde la catégorie si le poids dépasse
                    categorie_assignee = row['categorie']
                    plage_poids = f"{row['poids_max']}kg+"

    # Si une catégorie a été assignée, retourner la catégorie et la plage de poids
        if categorie_assignee:
            return (categorie_assignee, plage_poids)

        return None, None


    """ On applique la fonction assigner_categorie à chaque ligne du DataFrame "joueurs", issue de la lecture du fichier csv
     On le réalise ligne par ligne "axis=1" et non par colonne "axis=0"
     Si la fonction renvoie une liste ou un tuple pour chaque ligne,  'expand' va étendre la sortie sur plusieurs colonnes """

    try:
        joueurs[['categorie_age', 'categorie_poids']] = joueurs.apply(assigner_categorie, axis=1, result_type='expand')

        # Calcul du nombre de joueurs par club dans chaque catégorie
        joueurs['nb_joueurs_club'] = joueurs.groupby(['categorie_age', 'categorie_poids', 'club'])['nom'].transform('count')
    except Exception as e:
        print(f"Erreur lors du traitement des joueurs : {e}")
        return None

    # Affichage des joueurs par catégories d'âge et de poids
    """
    for (cat_age, cat_poids), group in joueurs.groupby(['categorie_age', 'categorie_poids']):
        group = group.sort_values(by='nb_joueurs_club', ascending=False)
        
        print(f"Joueur(s) dans la catégorie {cat_age} {cat_poids}:")
        print(group[['nom', 'prenom', 'poids', 'age', 'club', 'nb_joueurs_club']],'\n')
        """
    return joueurs


def organiser_matchs_par_categories(joueurs):
    # Groupement des joueurs par catégories d'âge et de poids
    groupes = joueurs.groupby(['categorie_age', 'categorie_poids'])
    matchs_par_categorie = {}

    for (cat_age, cat_poids), joueurs in groupes:
        graphe = Graphe()
        source = 'source'
        puits = 'puits'

        # Si le nombre de joueurs est impair, attribuer un "bye"
        joueur_bye = None
        if len(joueurs) % 2 != 0:
            joueur_bye_index = random.choice(joueurs.index)
            joueur_bye = joueurs.loc[joueur_bye_index]
            joueurs = joueurs.drop(joueur_bye_index)

        for _, joueur in joueurs.iterrows():
            joueur_id = f"{joueur['prenom']} {joueur['nom']} ({joueur['club']})"
            graphe.ajouter_arete(source, joueur_id, 1)

        # Ajouter les arêtes entre les joueurs (éviter les rencontres intra-clubs)
        for i in range(len(joueurs)):
            for j in range(i + 1, len(joueurs)):
                if joueurs['club'].iloc[i] != joueurs['club'].iloc[j]:
                    joueur1 = f"{joueurs['prenom'].iloc[i]} {joueurs['nom'].iloc[i]} ({joueurs['club'].iloc[i]})"
                    joueur2 = f"{joueurs['prenom'].iloc[j]} {joueurs['nom'].iloc[j]} ({joueurs['club'].iloc[j]})"
                    graphe.ajouter_arete(joueur1, joueur2, 1)

        # Ajouter les arêtes entre les joueurs et le puits
        for _, joueur in joueurs.iterrows():
            joueur_id = f"{joueur['prenom']} {joueur['nom']} ({joueur['club']})"
            graphe.ajouter_arete(joueur_id, puits, 1)

        # Calculer le flot maximum
        edmonds_karp(graphe, source, puits)

        tab_match = []
        bye_list = []

        # Enregistrer le joueur qui a reçu un bye
        if joueur_bye is not None:
            bye_list.append(f"{joueur_bye['nom']} {joueur_bye['prenom']} ({joueur_bye['club']})")

        # Trouver les matchs
        joueurs_utilises = set()
        for index, joueur in joueurs.iterrows():
            joueur_id = f"{joueur['prenom']} {joueur['nom']} ({joueur['club']})"
            if joueur_id in joueurs_utilises:
                continue  # Ignorer les joueurs déjà appariés
            for v in graphe.obtenir_voisins(joueur_id):
                if graphe.liste_adjacence[joueur_id][v] == 0 and v != puits and v not in joueurs_utilises:
                    tab_match.append([joueur_id, v])
                    joueurs_utilises.add(joueur_id)
                    joueurs_utilises.add(v)
                    break  # Un match par joueur


        matchs_par_categorie[(cat_age, cat_poids)] = {
            "matches": tab_match,
            "byes": bye_list
        }
    return matchs_par_categorie
            
def afficher_matchs(matchs_par_categorie):
    for (cat_age, cat_poids), data in matchs_par_categorie.items():
        print(f"\n{'=' * 40}")
        print(f"Matchs pour la catégorie {cat_age} {cat_poids} : ")
        print(f"{'=' * 40}")

        for match in data['matches']:
            j1 = match[0]
            j2 = match[1]
            print(f"{j1:<30} VS {j2:<30}")

        if data['byes']:
            print("Byes : "+", ".join(data['byes']))
        print(f"{'=' * 40}")



def main():
    try:
        if len(sys.argv) < 3:
            print("Erreur: Veuillez fournir deux fichiers CSV comme arguments.")
            print("Usage: Python exemple_tri.py <fichier_ods> <fichier_categories>")
            sys.exit(1)

        fichier_ods = sys.argv[1]
        nom_feuille = sys.argv[2]
        fichier_joueur = lire_joueur_ods(fichier_ods, nom_feuille) 
        
        joueurs = lecture_joueurs_et_categories(fichier_joueur, 'categorie.csv')

        if joueurs is not None:
            match = organiser_matchs_par_categories(joueurs)
            afficher_matchs(match)
    except Exception as e:
        print(f"Erreur dans l'execution du programme : {e}")

if __name__ == "__main__":
    main()