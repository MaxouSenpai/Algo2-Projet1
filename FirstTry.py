import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
class Graph :
    def __init__(self,V={},E={},incidenceMatrix=[]) :
        self.Vertex = 7
        self.V = V
        self.E = E
        self.Vertices = self.getVertices()
        self.Edges = self.getEdges()
        self.PrimalGraph = self.PrimalGraphMatrix()
        self.incidenceMatrix = incidenceMatrix if incidenceMatrix != [] else self.incidence_Matrix()

    def getVertices(self) :
        return [Vertex for Vertex in self.V]

    def getEdges(self) :
        lst = []
        for Vertex in self.V :
            for Vertex2 in self.V[Vertex] :
                if {Vertex,Vertex2} not in lst :
                    lst.append({Vertex,Vertex2})
        return lst

    def PrimalGraphMatrix(self) :
        Matrix = [[ 0 for _ in range(self.Vertex)] for _ in range(self.Vertex)]
        for Vertex in self.V :
            for Vertex2 in self.V[Vertex] :
                Matrix[int(Vertex[-1])-1][int(Vertex2[-1])-1] = 1
        return np.array(Matrix)

    def incidence_Matrix(self) :
        Matrix = [[0 for _ in range(len(self.E))] for _ in range(len(self.V)) ]
        for hyperarete in self.E :
            for Vertex in self.E[hyperarete] :
                Matrix[int(Vertex[-1])-1][int(hyperarete[-1])-1] = 1

        return np.array(Matrix)


    def incidenceMatrixTranspose(self) :
        return np.transpose(self.incidenceMatrix)

    @staticmethod
    def generateDualGraph(incidenceMatrix) :
        V = {}
        E = {}
        for i in range(len(incidenceMatrix)) :
            Vertex = "E" + str(i+1)
            V[Vertex] = []
            for j in range(len(incidenceMatrix[0])) :
                hyperarete = "Ev" + str(j+1)
                if hyperarete not in E :
                    E[hyperarete] = []
                if incidenceMatrix[i][j] == 1 :
                    E[hyperarete].append(Vertex)

        for hyperarete in E :
            x = len(E[hyperarete])
            if x > 1 :
                for i in range(x) :
                    for j in range(i+1,x) :
                        if E[hyperarete][j] not in V[E[hyperarete][i]] :
                            V[E[hyperarete][i]].append(E[hyperarete][j])
                        if E[hyperarete][i] not in V[E[hyperarete][j]] :
                            V[E[hyperarete][j]].append(E[hyperarete][i])

        return Graph(V,E,incidenceMatrix)

    def __str__(self) :
        for elem in self.V :
            print(elem + " :" , self.V[elem])
        return ""




V = { "v1" : ["v2","v3"],
      "v2" : ["v1","v3"],
      "v3" : ["v1", "v2","v5","v6"],
      "v4" : [],
      "v5" : ["v3","v6"],
      "v6" : ["v3","v5"],
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
print(graphe.PrimalGraph)
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
print(grapheDual.PrimalGraph)
print("Incidence Matrix ")
print(grapheDual.incidenceMatrix)
print("Incidence Matrix Transpose")
print(grapheDual.incidenceMatrixTranspose())
print(grapheDual)




#G = nx.Graph(g)
#nx.draw(G)
#plt.draw()
