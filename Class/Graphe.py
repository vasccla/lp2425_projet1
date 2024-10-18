#Class/Pile.py
from collections import defaultdict

class Graphe:
    "La classe représente un graphe à l'aide d'une liste d'adjacence."

    def __init__(self):
        self.liste_adjacence = defaultdict(dict)
    
    def ajouter_arete(self, sommet_depart, sommet_arrivee, capacite):
        """
        Ajout d'une arête avec une capacité donnée.
        :param sommet_depart: Le sommet de départ de l'arête
        :param sommet_arrivee: Le sommet d'arriver de l'arête
        :param capacite: La capacité de l'arête
        """

        self.liste_adjacence[sommet_depart][sommet_arrivee] = capacite
        self.liste_adjacence[sommet_arrivee][sommet_depart] = 0

    def obtenir_voisins(self, sommet):
        return self.liste_adjacence[sommet].keys()