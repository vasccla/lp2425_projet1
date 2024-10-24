import random
import json

from Class.Pile import Pile
from Class.File import File

def organiser_matchs_par_tri_simple(joueurs):
    # Groupement des joueurs par catégories d'âge et de poids
    groupes = joueurs.groupby(['categorie_age', 'categorie_poids'])
    tous_les_matchs = []  # Liste pour stocker tous les matchs
    byes_par_categorie = {}

    for (cat_age, cat_poids), joueurs in groupes:
        temp_pile:Pile = Pile()
        temp_file:File = File()
        tabMatch = []

        if len(joueurs) % 2 != 0:
            joueur_bye_index = random.choice(joueurs.index)
            joueur_bye = joueurs.loc[joueur_bye_index]
            byes_par_categorie.setdefault((cat_age, cat_poids), []).append(f"{joueur_bye['nom']} {joueur_bye['prenom']} ({joueur_bye['club']})")
            joueurs = joueurs.drop(joueur_bye_index)

        joueurs = joueurs.sample(frac=1).reset_index(drop=True)

        # Remplissage de la file avec les données joueurs à partir du début de la DF
        for i in range(0, len(joueurs) // 2):
            temp_file.enfiler([joueurs["nom"].iloc[i], joueurs["prenom"].iloc[i], joueurs["club"].iloc[i]])
        # Remplissage de la pile avec les données joueurs à partir de la moitié de la DF
        for i in range(len(joueurs) // 2, len(joueurs)):
            temp_pile.empiler([joueurs["nom"].iloc[i], joueurs["prenom"].iloc[i], joueurs["club"].iloc[i]])

        while len(temp_file.afficher()) != 0 and len(temp_pile.afficher()) != 0:
            tabMatch.append([temp_file.defiler(), temp_pile.depiler()])

        # Ajouter les matchs de cette catégorie à la liste globale
        tous_les_matchs.append((cat_age, cat_poids, tabMatch))

    return tous_les_matchs, byes_par_categorie



def enregistrer_matchs_json1(matchs, byes_par_categorie, chemin_fichier):
    """
    Enregistre les matchs et les byes au format JSON.

    :param matchs: Liste des matchs à enregistrer
    :param byes_par_categorie: Dictionnaire des byes par catégorie
    :param chemin_fichier: Chemin où enregistrer le fichier JSON
    """
    # Structurer les données pour JSON
    data = {}

    for cat_age, cat_poids, tabMatch in matchs:
        categorie_key = f"('{cat_age}', '{cat_poids}')"  # Convertir le tuple en chaîne
        match_data = {
            "matches": []
        }
        for j in tabMatch:
            match_data["matches"].append([
                f"{j[0][0]} {j[0][1]} ({j[0][2]})",
                f"{j[1][0]} {j[1][1]} ({j[1][2]})"
            ])
        
        # Ajouter les byes pour cette catégorie si disponibles
        if (cat_age, cat_poids) in byes_par_categorie:
            match_data["byes"] = byes_par_categorie[(cat_age, cat_poids)]
        else:
            match_data["byes"] = []

        data[categorie_key] = match_data

    # Enregistrer les données dans un fichier JSON
    with open(chemin_fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Matchs et byes enregistrés dans le fichier : {chemin_fichier}")



def afficher_matchs_tri_simple(matchs, byes_par_categorie):
    print("\n")
    print("#######################################################")
    print("################# MATCHS PAR TRI SIMPLE ###############")
    print("#######################################################")
    for cat_age, cat_poids, tabMatch in matchs:
        print(f"\n{'=' * 40}")
        print(f"Match pour la catégorie {cat_age} {cat_poids} : ")
        print(f"{'=' * 40}")
        for j in tabMatch:
            j1 = f"{j[0][0]} {j[0][1]} ({j[0][2]})"
            j2 = f"{j[1][0]} {j[1][1]} ({j[1][2]})"

            print(f"{j1:<30} vs {j2:<30}")

        if (cat_age, cat_poids) in byes_par_categorie:
            print("Byes : " + ", ".join(byes_par_categorie[(cat_age, cat_poids)]))
        print(f"{'=' * 40}")
