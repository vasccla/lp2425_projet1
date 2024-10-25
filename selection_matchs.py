"""
Module pour organiser et afficher des matchs en fonction des données des joueurs.
Ce module inclut des fonctions pour lire les données des joueurs à partir de fichiers CSV,
assigner des catégories et générer des appariements en utilisant différents algorithmes.
"""

import sys
import pandas as pd
from matchs_tri_simple import organiser_matchs_par_tri_simple, matchs_tri_simple, json1
from matchs_edmond import organiser_matchs_par_edmond,matchs_edmonds,json2
from affichage_edmond import affichage_graphique_matchs_edmond
from affichage_simple import affichage_graphique_matchs_simple

def lire_joueur_ods(fichier_ods: str, nom_feuille: str) -> str:
    """
    Lit les données des joueurs à partir d'un fichier ODS et les enregistre dans un fichier CSV.

    :param fichier_ods: Chemin du fichier ODS contenant les données des joueurs
    :param nom_feuille: Nom de la feuille dans le fichier ODS à lire
    :return: Chemin du fichier CSV généré contenant les informations des joueurs
    """
    # Lire la feuille spécifiée en tant que DataFrame
    joueur_df = pd.read_excel(fichier_ods, sheet_name=nom_feuille)

    # Sélectionner les colonnes souhaitées
    colonnes_souhaitees = ['NOM', 'PRÉNOM', 'POIDS', 'AGE', 'CLUB']
    df_selection = joueur_df[colonnes_souhaitees].copy()

    # Modifier les noms des colonnes
    noms_nouveaux = {'NOM':'nom', 'PRÉNOM':'prenom', 'POIDS':'poids', 'AGE':'age', 'CLUB':'club'}
    df_selection.rename(columns=noms_nouveaux, inplace=True)

    # Enregistrer le DataFrame filtré avec les nouveaux noms en CSV
    csv_file_path = "joueur.csv"
    df_selection.to_csv(csv_file_path, index=False)
    return csv_file_path

def lecture_joueurs_et_categories(fichier_joueurs:str, fichier_categories:str):
    """ Assignation des joueurs par catégories """
    try:
        # On met le résultat dans la variable 'joueurs' de type DataFrame
        joueurs = pd.read_csv(fichier_joueurs)

    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_joueurs} n'a pas été trouvé.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Erreur : Le fichier {fichier_joueurs} est vide ou corrompu.")
        return None
    except ValueError as error:
        print(f"Erreur lors de la lecture du fichier joueurs : {error}")
        return None

    try:
        # On met le résultat dans la variable 'categories' de type DataFrame
        categories = pd.read_csv(fichier_categories)

    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_categories} n'a pas été trouvé.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Erreur : Le fichier {fichier_categories} est vide ou corrompu.")
        return None
    except Exception as error:
        print(f"Erreur lors de la lecture du fichier joueurs : {error}")
        return None


    def assigner_categorie(joueur):
        """
        Assigne une catégorie d'âge et de poids à un joueur en fonction de ses caractéristiques.

        :param joueur: Ligne du DataFrame contenant les informations du joueur
        :return: Tuple contenant la catégorie d'âge et la plage de poids, ou (None, None)
        si aucune correspondance
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

                # On garde la catégorie si le poids dépasse
                categorie_assignee = row['categorie']
                plage_poids = f"{row['poids_max']}kg+"

    # Si une catégorie a été assignée, retourner la catégorie et la plage de poids
        if categorie_assignee:
            return (categorie_assignee, plage_poids)

        return None, None

    try:
        joueurs[['categorie_age', 'categorie_poids']] = joueurs.apply(assigner_categorie, axis=1, result_type='expand')
    except Exception as e:
        print(f"Erreur lors du traitement des joueurs : {e}")
        return None

    return joueurs


def main():
    """
    Fonction principale du programme, gère l'entrée des fichiers, 
    le menu interactif pour organiser les matchs et les cas d'erreurs.

    :return: None
    """
    try:
        if len(sys.argv) < 3:
            print("ERREUR: Fichiers requis manquants.")
            print("Veuillez fournir un fichier .ods et le nom de la feuille de calcul.")
            print("USAGE: python exemple_tri.py <fichier_ods> <feuille de calcul>")
            sys.exit(1)

        fichier_ods = sys.argv[1]
        nom_feuille = sys.argv[2]
        fichier_joueur = lire_joueur_ods(fichier_ods, nom_feuille)

        joueurs = lecture_joueurs_et_categories(fichier_joueur, 'categorie.csv')

        if joueurs is not None:
            while True:
                print("\nMenu : ")
                print("1. Géneration de matchs par tri simple")
                print("2. Géneration de matchs par l'algorithme d'Edmond")
                #print("2. Enregistrer la sélection de match au format .json")
                print("3. Quitter")

                choix:str = input("Veuillez entrer votre choix (1-3) : ")

                if choix == '1':
                    match, byes = organiser_matchs_par_tri_simple(joueurs)
                    matchs_tri_simple(match, byes)

                    choix_affichage:str = input("\nVoulez-vous afficher graphiquement les matchs (O/N) : ").lower()
                    
                    if choix_affichage == 'o':
                        affichage_graphique_matchs_simple(match, byes)

                    choix_json:str = input("\nVoulez-vous le format json (O/N) : ").lower()

                    if choix_json == 'o':
                        json1(match, byes, "matchs.json")


                elif choix == '2':
                    match = organiser_matchs_par_edmond(joueurs)
                    matchs_edmonds(match)

                    choix_affichage:str = input("\nVoulez-vous afficher graphiquement les matchs (O/N) : ").lower()
                    
                    if choix_affichage == 'o':
                        affichage_graphique_matchs_edmond(match)

                    choix_json:str = input("\nVoulez-vous le format json (O/N) : ").lower()

                    if choix_json == 'o':
                        json2(match, 'matchs.json')

                elif choix == '3':
                    print("Au revoir !")
                    break

                else:
                    print("Choix invalide, veuillez réessayer.")

    except FileNotFoundError:
        print("Erreur : Le fichier n'a pas été trouvé.")
    except ValueError as error:
        print(f"Erreur de valeur : {error}")
    except TypeError as error:
        print(f"Erreur de type : {error}")

if __name__ == "__main__":
    main()
