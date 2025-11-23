class Graph():
    def __init__(self):
        self.vertex = {}

    def __init__(self, fileName):
        self.vertex = {}
        with open(fileName, 'r', encoding='utf-8') as file:
            return

    def add_vertex(self, vertex):
        self.vertex[vertex.index] = vertex

    def add_edge(self, from_index, to_index, cost, doneOnce): # Considère que les sommets existent déjà
        from_vertex = self.vertex[from_index]
        to_vertex = self.vertex[to_index]
        edge = Edge(cost, to_vertex)
        from_vertex.add_edge(edge)
        if not doneOnce:
            self.add_edge(to_index, from_index, cost, True) # Graphe non orienté, pourrait créer une boucle infinie

    def is_connexe(self):
        if self.vertes.len() == 0:
            return True

        left_to_visit = set(self.vertex.keys()) # Ensemble des sommets à visiter
        first_vertex = self.vertex.values()[0] #on choisie arbitrairement le premier sommet du dictionnaire
        return len(first_vertex.bfs(left_to_visit)) == 0 # Vérifie qu'il ne reste plus de sommets à visiter
    


class Vertex():
    def __init__(self):
        self.index = -1
        self.name = ""
        self.edges = []
        self.numLigne = "" # Le numéro de ligne est un string car il y a des bis, le fait qu'il y ait des ; à la fin me conforte dans cette idée
        self.terminus = False
        self.direction = -1
    def __init__(self, index, name, numLigne, terminus, direction):
        self.index = index
        self.name = name
        self.edges = []
        self.numLigne = numLigne # Le numéro de ligne est un string car il y a des bis, le fait qu'il y ait des ; à la fin me conforte dans cette idée
        self.terminus = terminus
        self.direction = direction

    def add_edge(self, edge):
        self.edges.append(edge)
    
    def bfs(self, left_to_visit):
        left_to_visit.remove(self.index)
        for edge in self.edges:
            if edge.destination.index in left_to_visit:
                edge.destination.bfs(left_to_visit)
        return left_to_visit


class Edge():
    def __init__(self, cost, destination):
        self.cost = cost
        self.destination = destination
    