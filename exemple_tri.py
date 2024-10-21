import sys
import pandas as pd
import json
from matchs_tri_simple import organiser_matchs_par_tri_simple, afficher_matchs_tri_simple
from matchs_edmond import organiser_matchs_par_edmond, afficher_matchs_edmonds

"""
Le fichier csv des joueurs sera générer par la fonction ci-dessous.
Si le fichier n'existe pas, il sera créer.
Si des joueurs sont rajouter dans le fichier ods dans l'avenir, les données du fichier csv seront écrasés et le fichier sera remis à jour.
"""

def lire_joueur_ods(fichier_ods: str, nom_feuille: str):
    # Lire la feuille spécifiée en tant que DataFrameg
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

    return joueurs


def enregistrer_matchs_json(matchs_par_categorie, nom_fichier):
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
            while True:
                print("\nMenu : ")
                print("1. Géneration de matchs par tri simple")
                print("2. Géneration de matchs par l'algorithme d'Edmond")
                print("3. Quitter")

                choix = input("Veuillez entrer votre choix (1-3) : ")

                if choix == '1':
                    match, byes = organiser_matchs_par_tri_simple(joueurs)
                    afficher_matchs_tri_simple(match, byes)

                elif choix == '2':
                    match = organiser_matchs_par_edmond(joueurs)
                    afficher_matchs_edmonds(match)
                    enregistrer_matchs_json(match, 'matchs.json')

                elif choix == '3':
                    print("Au revoir !")
                    break
                
                else:
                    print("Choix invalide, veuillez réessayer.")

    except Exception as e:
        print(f"Erreur dans l'execution du programme : {e}")

if __name__ == "__main__":
    main()