import numpy as np
class Graphe :
    def __init__(self,dico={}) :
        self.dico = dico
        self.n = len(self.dico)

    def getVertices(self) :
        return [sommet for sommet in self.dico]

    def getEdges(self) :
        liste = []
        for sommet in self.dico :
            for sommet2 in self.dico[sommet] :
                if {sommet,sommet2} not in liste :
                    liste.append({sommet,sommet2})
        return liste

    def adjacency_matrix(self) :
        matrix = [[ 0 for _ in range(self.n)] for _ in range(self.n)]
        for sommet in self.dico :
            for sommet2 in self.dico[sommet] :
                matrix[int(sommet[1])-1][int(sommet2[1])-1] = 1
        return np.array(matrix)


    def matrix_transpose(self) :
        mat = self.adjacency_matrix()
        new_mat = np.transpose(mat)
        return new_mat



g = { "v1" : [("v2"),("v3")],
      "v2" : [("v1"),("v3")],
      "v3" : [("v1"), ("v2"),("v5"),("v6")],
      "v4" : [],
      "v5" : [("v3"),("v6")],
      "v6" : [("v3"),("v5")],
      "v7" : []
    }

graphe = Graphe(g)

print("Vertices of graph:")
print(graphe.getVertices())
print("Edges of graph:")
print(graphe.getEdges())
print("Adjacency Matrix")
print(graphe.adjacency_matrix())
print("Adjacency Matrix Transpose")
print(graphe.matrix_transpose())
