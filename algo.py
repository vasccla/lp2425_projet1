import random
import sys
from collections import defaultdict
import pandas as pd

class Graphe:
    def __init__(self):
        """
        Initialise une instance de la classe Graphe.
        Utilise un dictionnaire pour représenter la liste d'adjacence.
        """
        self.liste_adjacence = defaultdict(dict)

    def ajouter_arete(self, sommet_depart, sommet_arrivee, capacite):
        """
        Ajoute une arête au graphe avec une capacité donnée.

        :param sommet_depart: Le sommet de départ de l'arête
        :param sommet_arrivee: Le sommet d'arrivée de l'arête
        :param capacite: La capacité de l'arête
        """
        self.liste_adjacence[sommet_depart][sommet_arrivee] = capacite
        self.liste_adjacence[sommet_arrivee][sommet_depart] = 0  # Arête inverse avec capacité 0

    def obtenir_voisins(self, sommet):
        """
        Retourne les voisins d'un sommet donné.

        :param sommet: Le sommet dont on veut les voisins
        :return: Les voisins du sommet
        """
        return self.liste_adjacence[sommet].keys()

def recherche_largeur(graphe, source, puits, parent):
    """
    Effectue une recherche en largeur pour trouver un chemin augmentant.

    :param graphe: Le graphe dans lequel effectuer la recherche
    :param source: Le sommet source
    :param puits: Le sommet puits
    :param parent: Dictionnaire pour stocker le chemin
    :return: True si un chemin augmentant est trouvé, sinon False
    """
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

def edmonds_karp(graphe, source, puits):
    """
    Implémente l'algorithme d'Edmonds-Karp pour trouver le flot maximum.

    :param graphe: Le graphe sur lequel appliquer l'algorithme
    :param source: Le sommet source
    :param puits: Le sommet puits
    :return: La valeur du flot maximum
    """
    parent = {}
    flot_maximum = 0

    while recherche_largeur(graphe, source, puits, parent):
        flot_chemin = float('Inf')
        s = puits

        # Trouver le flot minimum dans le chemin augmentant
        while s != source:
            flot_chemin = min(flot_chemin, graphe.liste_adjacence[parent[s]][s])
            s = parent[s]

        v = puits
        # Mettre à jour les capacités des arêtes dans le chemin
        while v != source:
            u = parent[v]
            graphe.liste_adjacence[u][v] -= flot_chemin
            graphe.liste_adjacence[v][u] += flot_chemin
            v = parent[v]

        flot_maximum += flot_chemin

    return flot_maximum

def lire_joueur_ods(fichier_ods: str, nom_feuille: str):
    """
    Lit les données des joueurs à partir d'un fichier ODS et les enregistre en CSV.

    :param fichier_ods: Chemin du fichier ODS
    :param nom_feuille: Nom de la feuille à lire
    :return: Chemin du fichier CSV généré
    """
    df = pd.read_excel(fichier_ods, sheet_name=nom_feuille)
    colonnes_souhaitees = ['NOM', 'PRÉNOM', 'POIDS', 'AGE', 'CLUB']
    df_selection = df[colonnes_souhaitees].copy()
    noms_nouveaux = {'NOM':'nom', 'PRÉNOM':'prenom', 'POIDS':'poids', 'AGE':'age', 'CLUB':'club'}
    df_selection.rename(columns=noms_nouveaux, inplace=True)
    chemin_csv = "joueur.csv"
    df_selection.to_csv(chemin_csv, index=False)
    return chemin_csv

def lecture_joueurs_et_categories(fichier_joueurs: str, fichier_categories: str):
    """
    Lit les fichiers CSV des joueurs et des catégories, et assigne les catégories aux joueurs.

    :param fichier_joueurs: Chemin du fichier CSV des joueurs
    :param fichier_categories: Chemin du fichier CSV des catégories
    :return: DataFrame des joueurs avec les catégories assignées
    """
    try:
        joueurs = pd.read_csv(fichier_joueurs)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier joueurs : {e}")
        return None
    
    try:
        categories = pd.read_csv(fichier_categories)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier catégories : {e}")
        return None

    def assigner_categorie(joueur):
        """
        Assigne une catégorie d'âge et de poids à un joueur.

        :param joueur: La ligne du joueur sous forme de Series
        :return: La catégorie d'âge et de poids
        """
        age = joueur['age']
        poids = joueur['poids']
        for _, row in categories.iterrows():
            if row['age_min']<=age<=row['age_max'] and row['poids_min']<=poids<=row['poids_max']:
                return row['categorie'], f"{row['poids_min']}-{row['poids_max']}kg"
        return None, None

    try:
        joueurs[['categorie_age', 'categorie_poids']] = joueurs.apply(assigner_categorie, axis=1, result_type='expand')
        joueurs['nb_joueurs_club']=joueurs.groupby(['categorie_age', 'categorie_poids', 'club'])['nom'].transform('count')
    except Exception as e:
        print(f"Erreur lors du traitement des joueurs : {e}")
        return None

    return joueurs

def organiser_matchs_par_categories(joueurs):
    """
    Organise les matchs par catégories d'âge et de poids à l'aide de l'algorithme d'Edmonds-Karp.

    :param joueurs: DataFrame des joueurs avec leurs informations
    :return: Dictionnaire contenant les matchs organisés par catégorie
    """
    groupes = joueurs.groupby(['categorie_age', 'categorie_poids'])
    matchs_par_categorie = {}

    for (cat_age, cat_poids), joueurs in groupes:
        graphe = Graphe()
        source = 'source'
        puits = 'puits'

        # Ajouter les arêtes entre la source et les joueurs
        for _, joueur in joueurs.iterrows():
            joueur_id = f"{joueur['prenom']} {joueur['nom']} ({joueur['club']})"
            graphe.ajouter_arete(source, joueur_id, 1)

        # Ajouter les arêtes entre les joueurs (éviter les rencontres intra-clubs)
        for i in range(len(joueurs)):
            for j in range(i + 1, len(joueurs)):
                if joueurs['club'].iloc[i] != joueurs['club'].iloc[j]:  # Vérifier si les joueurs sont d'un même club
                    joueur1 = f"{joueurs['prenom'].iloc[i]} {joueurs['nom'].iloc[i]} ({joueurs['club'].iloc[i]})"
                    joueur2 = f"{joueurs['prenom'].iloc[j]} {joueurs['nom'].iloc[j]} ({joueurs['club'].iloc[j]})"
                    graphe.ajouter_arete(joueur1, joueur2, 1)

        # Ajouter les arêtes entre les joueurs et le puits
        for index, joueur in joueurs.iterrows():
            joueur_id = f"{joueur['prenom']} {joueur['nom']} ({joueur['club']})"
            graphe.ajouter_arete(joueur_id, puits, 1)

        # Calculer le flot maximum
        edmonds_karp(graphe, source, puits)

        tab_match = []
        bye_list = []

        # Gérer un bye si le nombre de joueurs est impair
        if len(joueurs) % 2 != 0:
            bye_index = random.choice(joueurs.index)
            joueur_bye = joueurs.loc[bye_index]
            bye_list.append(f"{joueur_bye['nom']} {joueur_bye['prenom']} ({joueur_bye['club']})")
            joueurs = joueurs.drop(bye_index)

        # Trouver les matchs
        joueurs_utilises = set()  # Ensemble pour suivre les joueurs déjà appariés
        for index, joueur in joueurs.iterrows():
            joueur_id = f"{joueur['prenom']} {joueur['nom']} ({joueur['club']})"
            for v in graphe.obtenir_voisins(joueur_id):
                if graphe.liste_adjacence[joueur_id][v] == 0 and v != puits and v not in joueurs_utilises:
                    tab_match.append([joueur_id, v])
                    joueurs_utilises.add(joueur_id)  # Marquer ce joueur comme utilisé
                    joueurs_utilises.add(v)  # Marquer l'adversaire comme utilisé
                    break  # Un match par joueur

        matchs_par_categorie[(cat_age, cat_poids)] = {
            "matches": tab_match,
            "byes": bye_list
        }

    return matchs_par_categorie

def afficher_matchs(matchs_par_categorie):
    """
    Affiche les matchs organisés par catégorie.

    :param matchs_par_categorie: Dictionnaire des matchs organisés
    """
    for (cat_age, cat_poids), data in matchs_par_categorie.items():
        print(f"\n{'=' * 40}")
        print(f"Matchs pour la catégorie {cat_age} {cat_poids} : ")
        print(f"{'=' * 40}")

        for match in data['matches']:
            j1 = match[0]
            j2 = match[1]
            print(f"{j1:<30} VS {j2:<30}")

        if data['byes']:
            print("Byes : " + ", ".join(data['byes']))
        print(f"{'=' * 40}")

def main():
    """
    Fonction principale du programme.
    Lit les fichiers fournis en arguments et organise les matchs.
    """
    try:
        if len(sys.argv) < 3:
            print("Erreur: Veuillez fournir deux fichiers CSV comme arguments.")
            print("Usage: Python exemple_tri.py <fichier_ods> <fichier_categories>")
            sys.exit(1)

        fichier_ods = sys.argv[1]
        nom_feuille = sys.argv[2]
        chemin_joueur = lire_joueur_ods(fichier_ods, nom_feuille) 
        
        joueurs = lecture_joueurs_et_categories(chemin_joueur, 'categorie.csv')

        if joueurs is not None:
            matchs = organiser_matchs_par_categories(joueurs)
            afficher_matchs(matchs)
    except Exception as e:
        print(f"Erreur dans l'exécution du programme : {e}")

if __name__ == "__main__":
    main()
