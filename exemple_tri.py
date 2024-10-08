import pandas as pd

def tri_joueurs_par_categories(fichier_csv):

    # Lectue du fichier csv avec les joueurs
    joueurs = pd.read_csv(fichier_csv)

    if joueurs.empty:
        print("Le fichier CSV est vide ou non valide.")
        return None
    

