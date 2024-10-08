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

    