#Class/Pile.py
class Pile():
    def __init__(self): # Initialisation de la pile
        self.valeurs = []

    def empiler(self,valeur): # Fonction qui permet d'empiler la valeur dans la pile
        self.valeurs.append(valeur) # Ajout de la valeur à la pile

    def depiler(self): # Fonction qui permet de dépiler la dernière valeur de la pile
        if len(self.valeurs) == 0: # Vérification de la longueur de la pile
            return None # Ne retourne rien si la pile est vide
        return self.valeurs.pop() # Suppression de la dernière valeur de la pile
    
    def afficher(self): # Affichage de la pile
        temp:list = []
        for i in range(len(self.valeurs)):
            temp.append(self.valeurs[i])
        return temp