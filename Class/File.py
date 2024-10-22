#Class/File.py
class File():
    def __init__(self): # Initialisation de la file
        self.valeurs = []

    def enfiler(self,valeur): # Fonction qui permet d'emfiler la valeur dans la file
        self.valeurs.append(valeur) # Ajout de la valeur à la file

    def defiler(self): # Fonction qui permet de défiler la dernière valeur de la file
        if len(self.valeurs) == 0: # Vérification de la longueur de la file
            return None # Ne retourne rien si la file est vide
        return self.valeurs.pop(0) # Suppression de la première valeur de la file
    
    def afficher(self): # Affichage de la file
        temp:list = []
        for i in range(len(self.valeurs)):
            temp.append(self.valeurs[i])
        return temp


