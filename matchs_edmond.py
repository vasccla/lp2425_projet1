import random
import json
from Class.Graphe import Graphe #Importation de la classe Graphe, implémenter dans Class/Graphe.py

def recherche_largeur(graphe:Graphe, source, puits, parent) -> bool:
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

def edmonds_karp(graphe:Graphe, source, puits):
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

def organiser_matchs_par_edmond(joueurs):
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

        joueurs = joueurs.sample(frac=1).reset_index(drop=True)

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
        for _, joueur in joueurs.iterrows():
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


def json2(matchs_par_categorie, nom_fichier:str) -> None:
    """
    Enregistre les matchs dans un fichier JSON.
    
    :param matchs_par_categorie: Dictionnaire contenant les matchs par catégorie
    :param nom_fichier: Nom du fichier dans lequel enregistrer les données
    """
    # Transformer les clés de tuple en chaînes de caractères
    matchs_modifies = {
        str(cat): data for cat, data in matchs_par_categorie.items()
    }

    try:
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            json.dump(matchs_modifies, f, ensure_ascii=False, indent=4)
        print(f"Les matchs ont été enregistrés dans le fichier {nom_fichier}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans le fichier JSON : {e}")


def matchs_edmonds(matchs_par_categorie):
    print("\n")
    print("#######################################################")
    print("################# MATCHS PAR EDMOND ###############")
    print("#######################################################")
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
