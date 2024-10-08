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
        'Minime': {'age_min': 10, 'age_max': 12, 'poids': [(0,20), (20,25), (25,30)]},
        'Junior': {'age_min': 13, 'age_max': 16, 'poids': [(0,40), (40,50), (50,60)]},
        'Cadet': {'age_min': 17, 'age_max': 19, 'poids': [(0,60), (60,70), (70,80)]},
        'Senior': {'age_min': 20, 'age_max': 100, 'poids': [(0,80), (80,90), (90,100)]},
    }
