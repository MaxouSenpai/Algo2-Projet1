import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
class Graph :
    def __init__(self,V={},E={},incidenceMatrix=[]) :
        self.sommets = 7
        self.V = V
        self.n = len(self.V)
        self.E = E
        self.Vertices = self.getVertices()
        self.Edges = self.getEdges()
        self.PrimalGraph = self.PrimalGraphMatrix()
        self.incidenceMatrix = incidenceMatrix if incidenceMatrix != [] else self.incidence_Matrix()

    def getVertices(self) :
        return [sommet for sommet in self.V]

    def getEdges(self) :
        liste = []
        for sommet in self.V :
            for sommet2 in self.V[sommet] :
                if {sommet,sommet2} not in liste :
                    liste.append({sommet,sommet2})
        return liste

    def PrimalGraphMatrix(self) :
        matrix = [[ 0 for _ in range(self.sommets)] for _ in range(self.sommets)]
        for sommet in self.V :
            for sommet2 in self.V[sommet] :
                matrix[int(sommet[-1])-1][int(sommet2[-1])-1] = 1
        return np.array(matrix)

    def incidence_Matrix(self) :
        matrix = [[0 for _ in range(len(self.E))] for _ in range(self.n) ]
        for hyperarete in self.E :
            for sommet in self.E[hyperarete] :
                matrix[int(sommet[-1])-1][int(hyperarete[-1])-1] = 1

        return np.array(matrix)


    def incidenceMatrixTranspose(self) :
        return np.transpose(self.incidenceMatrix)

    @staticmethod
    def generateDualGraph(incidenceMatrix) :
        V = {}
        E = {}
        for i in range(len(incidenceMatrix)) :
            name = "E" + str(i+1)
            V[name] = []
            E[name] = []
            for j in range(len(incidenceMatrix[0])) :
                if incidenceMatrix[i][j] == 1 :
                    name2 = "Ev" + str(j+1)
                    E[name].append(name2)

        return Graph(E,V,incidenceMatrix)

    def __str__(self) :
        for elem in self.V :
            print(elem + " :" , self.V[elem])
        return ""




V = { "v1" : [("v2"),("v3")],
      "v2" : [("v1"),("v3")],
      "v3" : [("v1"), ("v2"),("v5"),("v6")],
      "v4" : [],
      "v5" : [("v3"),("v6")],
      "v6" : [("v3"),("v5")],
      "v7" : []
    }

E = { "E1" : ["v1","v2","v3"] ,
      "E2" : ["v2","v3"],
      "E3" : ["v3","v5","v6"] ,
      "E4" : ["v4"]
    }

graphe = Graph(V,E)
print("Vertices of graph:")
print(graphe.Vertices)
print("Edges of graph:")
print(graphe.Edges)
print("Adjacency Matrix")
print(graphe.PrimalGraphMatrix())
print("Incidence Matrix ")
print(graphe.incidenceMatrix)
print("Incidence Matrix Transpose")
print(graphe.incidenceMatrixTranspose())
print("\n\n\n\n")
grapheDual = Graph.generateDualGraph(graphe.incidenceMatrixTranspose())
print("Vertices of dual graph:")
print(grapheDual.Vertices)
print("Edges of dual graph:")
print(grapheDual.Edges)
print("Adjacency Matrix")
print(grapheDual.PrimalGraphMatrix())
print("Incidence Matrix ")
print(grapheDual.incidenceMatrix)
print("Incidence Matrix Transpose")
print(grapheDual.incidenceMatrixTranspose())
print(grapheDual)



#G = nx.Graph(g)
#nx.draw(G)
#plt.draw()
