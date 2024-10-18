from collections import defaultdict # Importation pour utiliser des dictionnaires avec des valeurs par défaut

class Graphe:
    """
    Représente un graphe à l'aide d'une liste d'adjacence.
    Les arêtes sont orientées avec une capacité associée.
    """

    def __init__(self):
        """
        Initialise un graphe vide avec une liste d'adjacence.
        """
        self.liste_adjacence = defaultdict(dict)
    
    def ajouter_arete(self, sommet_depart, sommet_arrivee, capacite):
        """
        Ajoute une arête entre deux sommets avec une capacité.
        
        :param sommet_depart: Sommet de départ
        :param sommet_arrivee: Sommet d'arrivée
        :param capacite: Capacité de l'arête
        """
        self.liste_adjacence[sommet_depart][sommet_arrivee] = capacite
        self.liste_adjacence[sommet_arrivee][sommet_depart] = 0

    def obtenir_voisins(self, sommet):
        """
        Retourne les voisins d'un sommet.
        
        :param sommet: Le sommet dont on veut les voisins
        :return: Liste des voisins du sommet
        """
        return self.liste_adjacence[sommet].keys()
