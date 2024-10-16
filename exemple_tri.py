import random
import sys

import pandas as pd # Utilisation de pandas pour une manipulation plus simple et plus flexible des données

from Class.File import File
from Class.Pile import Pile

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

        for _, row in categories.iterrows():
            if row['age_min'] <= age <= row['age_max']:
                if row['poids_min'] <= poids <= row['poids_max']:
                    return row['categorie'], f"{row['poids_min']}-{row['poids_max']}kg"
                
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
        temp_pile:Pile = Pile()
        temp_file:File = File()
        tab_match:list = []
        bye_list = [] # Liste pour stocker les byes

        # Si le nombre de joueurs est impair, attribuer un "bye"
        if len(joueurs) % 2 != 0:
            joueur_bye_index = random.choice(joueurs.index)
            joueur_bye = joueurs.loc[joueur_bye_index]
            bye_list.append(f"{joueur_bye['nom']} {joueur_bye['prenom']} ({joueur_bye['club']})")
            joueurs = joueurs.drop(joueur_bye_index)

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
            # Sauvegarde des matchs pour cette catégorie
        matchs_par_categorie[(cat_age, cat_poids)] = {
            "matches": tab_match,
            "byes": bye_list
        }
    return matchs_par_categorie
            
def afficher_matchs(matchs_par_categorie):
    for(cat_age, cat_poids), data in matchs_par_categorie.items():
        print(f"\n{'=' * 40}")
        print(f"Matchs pour la catégorie {cat_age} {cat_poids} : ")
        print(f"{'=' * 40}")

        for match in data['matches']:
            j1 = f"{match[0][0]} {match[0][1]} ({match[0][2]})"
            j2 = f"{match[1][0]} {match[1][1]} ({match[1][2]})"
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