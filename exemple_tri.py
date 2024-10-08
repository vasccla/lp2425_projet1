import pandas as pd

def tri_joueurs_par_categories(fichier_csv):

    # Lectue du fichier csv avec les joueurs
    joueurs = pd.read_csv(fichier_csv)

    if joueurs.empty:
        print("Le fichier CSV est vide ou non valide.")
        return None
    
    # Définition des catégories d'âge et de poids
    # Chaque catégorie a une plage d'âges et des intervalles de poids correspondants
    categories_age_poids = {
        'Poussin': {'age_min': 6, 'age_max': 7, 'poids': [(0,20), (20,25), (25,30), (30,35), (35,40), (40,45)]},
        'Pupille': {'age_min': 8, 'age_max': 9, 'poids': [(0,25), (25,30), (30,35), (35,40), (40,45), (45,50)]},
        'Benjamin': {'age_min': 10, 'age_max': 11, 'poids': [(0,30), (30,35), (35,40), (40,45), (45,50), (50,55)]},
        'Minime': {'age_min': 12, 'age_max': 13, 'poids': [(0,35), (35,40), (40,45), (45,50), (50,55), (55,60), (60, 65)]},
        'Cadet': {'age_min': 14, 'age_max': 15, 'poids': [(0,42), (42,47), (47,54), (54,60), (60,70)]},
        'Junior': {'age_min': 16, 'age_max': 17, 'poids': [(0,48), (48,53), (53,59)]},
        'Espoir': {'age_min': 18, 'age_max': 20, 'poids': [(0,50), (50,55), (55,61), (61,68), (68,75), (75,84)]},
        'Senior': {'age_min': 18, 'age_max': 34, 'poids': [(0,50), (50,55), (55,61), (61,68), (68,75), (75,84)]},
        'V1': {'age_min': 35, 'age_max': 45, 'poids': [(0,55), (55,61), (61,68), (68,75), (75,84)]},
        'V2': {'age_min': 46, 'age_max': 55, 'poids': [(0,55), (55,61), (61,68), (68,75), (75,84)]},
        'V3': {'age_min': 56, 'age_max': 65, 'poids': [(0,55), (55,61), (61,68), (68,75), (75,84)]},
    }

    # Fonction pour attribuer une catégorie d'âge et de poids à chaque joueurs
    def assigner_categorie(joueur):
        age, poids = joueur['age'], joueur['poids']

        for cat, details in categories_age_poids.items():
            # Vérifier si l'âge du joueur est dans les limites de la catégorie
            if details['age_min'] <= age <= details['age_max']:
                # Vérifier si le poids du joueur est dans les limites de la catégorie
                for poids_min, poids_max in details['poids']:
                    if poids_min <= poids <= poids_max:
                        # Retourne la catégorie correspondante
                        return cat, f'{poids_min}-{poids_max}kg'
        return None, None

    # Assignation des catégories à chaque joueur
    # On applique la fonction assigner_categorie à chaque ligne de "joueurs"
    # On le réalise ligne par ligne "axis=1" et non par colonne "axis=0"
    # Si la fonction renvoie une liste ou un tuple pour chaque ligne,  'expand' va étendre la sortie sur plusieurs colonnes 
    joueurs[['categorie_age', 'categorie_poids']] = joueurs.apply(assigner_categorie, axis=1, result_type='expand')

    # Affichage des joueurs par catégories d'âge et de poids
    for (cat_age, cat_poids), group in joueurs.groupby(['categorie_age', 'categorie_poids']):
        print(f"Joueurs dans la catégorie {cat_age} {cat_poids}:")
        print(group[['nom', 'prenom', 'poids', 'age', 'club']])
        
    return joueurs

joueur = tri_joueurs_par_categories('joueur.csv')