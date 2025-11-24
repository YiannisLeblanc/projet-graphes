#!/usr/bin/python3
class Graph():
    def __init__(self):
        self.vertex = {}

    def loadFile(self, fileName):
        self.vertex = {}
        with open(fileName, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line == "" or line == "\n":
                    continue
                if line[0:2] == "V ":
                    newVertex = Vertex()
                    newVertex.initFromString(line[2:])
                    if(newVertex.index != -1):
                        self.add_vertex(newVertex)
                elif line[0:2] == "E ":
                    self.add_edge_from_string(line[2:])

    def add_vertex(self, vertex):
        self.vertex[vertex.index] = vertex

    def add_edge(self, from_index: int, to_index: int, cost: int, doneOnce = False): # Considère que les sommets existent déjà
        from_vertex = self.vertex[from_index]
        to_vertex = self.vertex[to_index]
        edge = Edge(cost, to_vertex)
        from_vertex.add_edge(edge)
        if not doneOnce:
            self.add_edge(to_index, from_index, cost, True) # Graphe non orienté, pourrait créer une boucle infinie
        
    def add_edge_from_string(self, string_line): # Je me méfie de celui-là, les lectures de ligne de fichier peuvent toujours créer des problèmes si mal formatées
        i = 0
        from_string = ""
        to_string = ""
        cost_string = ""
        while i < len(string_line) and string_line[i] != ' ':
            from_string += string_line[i]
            i += 1
        i += 1
        while i < len(string_line) and string_line[i] != ' ':
            to_string += string_line[i]
            i += 1
        i += 1
        while i < len(string_line) and string_line[i] != '\n':
            cost_string += string_line[i]
            i += 1
        # vérifier que from_string, to_string et cost_string contiennent bien des entiers
        from_string = from_string.strip()
        to_string = to_string.strip()
        cost_string = cost_string.strip()
        if not (from_string.isdigit() and to_string.isdigit() and cost_string.isdigit()):
            return
        from_index = int(from_string.strip())
        to_index = int(to_string.strip())
        cost = int(cost_string.strip())
        self.add_edge(from_index, to_index, cost)

    def is_connexe(self):
        if self.vertex.keys() == []:
            return True

        left_to_visit = set(self.vertex.keys()) # Ensemble des sommets à visiter
        first_vertex = list(self.vertex.values())[0] # Petit trick bizarre mais c'est accéder à un élément quelconde du dictionnaire. Utiliser la key 0 pourrait être dangereux si pour quelque raison l'on décidait de commencer à 1 par exemple
        return len(first_vertex.bfs(left_to_visit)) == 0 # Vérifie qu'il ne reste plus de sommets à visiter
    
    def print(self):
        for v in self.vertex.values():
            print("Sommet", v.index, ":", v.name)
            for e in v.edges:
                print("  ->", e.destination.index, "coût :", e.cost)
    def acp(self):
        newVertex = Vertex()
        newVertex.setCopy(list(self.vertex.values())[0])
        tree = Graph()
        left_vertex = set(self.vertex.keys())
        left_vertex.remove(newVertex.index)
        tree.add_vertex(newVertex)
        while len(left_vertex) > 0:
            min_edge = None
            from_vertex = None
            for v in tree.vertex.values():
                for e in self.vertex[v.index].edges:
                    if e.destination.index in left_vertex:
                        if min_edge is None or (e.cost < min_edge.cost and e.destination.index in left_vertex):
                            min_edge = e
                            from_vertex = v
            if min_edge is not None:
                newVertex = Vertex()
                newVertex.setCopy(min_edge.destination)
                tree.add_vertex(newVertex)
                tree.add_edge(from_vertex.index, newVertex.index, min_edge.cost)
                left_vertex.remove(newVertex.index)
        return tree

    def one_to_all(self, from_index): # Sous la forme d'un dico {index_sommet: (coût, index_sommet_précédent)}
        result = {}
        to_do = set()
        result[from_index] = (0, -1)
        to_do.add(from_index)
        while len(to_do) > 0:
            current_index = to_do.pop()
            current_vertex = self.vertex[current_index]
            for edge in current_vertex.edges:
                if edge.destination.index not in result:
                    result[edge.destination.index] = (edge.cost, current_index)
                    to_do.add(edge.destination.index)
                else:
                    current_cost = result[edge.destination.index][0]
                    new_cost = result[current_index][0] + edge.cost
                    if new_cost < current_cost:
                        result[edge.destination.index] = (new_cost, current_index)
                        to_do.add(edge.destination.index)
                if current_index == 147 or edge.destination.index == 191:
                    print("Debug :", current_index, "->", edge.destination.index, "coût actuel :", result[edge.destination.index][0], "nouveau coût :", new_cost)
                    pass
        return result
    
    def pcc(self, from_index, to_index): # Sous la forme (coût, [liste des indices du chemin])
        one_to_all_result = self.one_to_all(from_index)
        cost = one_to_all_result[to_index][0]
        path = []
        current_index = to_index
        while current_index != -1:
            path.append(current_index)
            current_index = one_to_all_result[current_index][1]
        path.reverse()
        return (cost, path)
    
    def pcc_verbose(self, from_index, to_index):
        pcc = self.pcc(from_index, to_index)
        result = (pcc[0], [])
        for index in pcc[1]:
            result[1].append(self.vertex[index].name)
        return result


class Vertex():
    def __init__(self, index = -1, name = "", numLigne = "", terminus = False, direction = 0):
        self.index = index
        self.name = name
        self.edges = []
        self.numLigne = numLigne # Le numéro de ligne est un string car il y a des bis, le fait qu'il y ait des ; à la fin me conforte dans cette idée
        self.terminus = terminus
        self.direction = direction
    
    def setCopy(self, other):
        self.index = other.index
        self.name = other.name
        self.numLigne = other.numLigne
        self.terminus = other.terminus
        self.direction = other.direction

    def initFromString(self, string_line: str):
        i = 0
        index_string = ""
        name = ""
        numLigne = ""
        terminus_string = ""
        direction_string = ""
        while i < len(string_line) and string_line[i] != ' ':
            index_string += string_line[i]
            i += 1
        i += 1
        while i < len(string_line) and string_line[i] != ';':
            name += string_line[i]
            i += 1
        name = name.strip() # Enlever l'espace final
        i += 1
        while i < len(string_line) and string_line[i] != ';':
            numLigne += string_line[i]
            i += 1
        numLigne = numLigne.strip()
        i += 1
        while i < len(string_line) and string_line[i] != ' ':
            terminus_string += string_line[i]
            i += 1
        i += 1
        while i < len(string_line) and string_line[i] != '\n':
            direction_string += string_line[i]
            i += 1
        index_string = index_string.strip()
        direction_string = direction_string.strip()
        if not index_string.isdigit() or not direction_string.isdigit():
            self.index = -1
            return
        self.index = int(index_string)
        self.name = name
        self.edges = []
        self.numLigne = numLigne
        self.terminus = (terminus_string == "True")
        self.direction = int(direction_string)

    def add_edge(self, edge):
        self.edges.append(edge)
    
    def bfs(self, left_to_visit: set):
        left_to_visit.remove(self.index)
        for edge in self.edges:
            if edge.destination.index in left_to_visit:
                edge.destination.bfs(left_to_visit)
        return left_to_visit


class Edge():
    def __init__(self, cost, destination: Vertex):
        self.cost = cost
        self.destination = destination


# Test code
if __name__ == "__main__":
    graph = Graph()
    graph.loadFile("Data/metro.txt")
    print("Le graphe est connexe :", graph.is_connexe())
    print("Nombre de sommets dans le graphe :", len(graph.vertex))
    print("Nombre d'arêtes dans le graphe :", sum(len(v.edges) for v in graph.vertex.values()) // 2) # Divisé par 2 car graphe non orienté
    print("Arbre couvrant de coût minimal :")
    acp_graph = graph.acp()
    acp_graph.print()
    print("Connexité de l'arbre couvrant :", acp_graph.is_connexe())
    print("Nombre de sommets de l'ACP égal au graphe d'origine :", len(acp_graph.vertex) == len(graph.vertex))
    print("Plus cours chemin de 0268 à 0276:")
    print(graph.pcc_verbose(268, 276))