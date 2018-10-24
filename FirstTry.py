from random import random,randint
import networkx as nx
import matplotlib.pyplot as plt

class Graph :
    def __init__(self,V={},E={},incidenceMatrix = []) :
        self.V = V
        self.E = E
        self.incidenceMatrix = incidenceMatrix if incidenceMatrix != [] else self.IncidenceGraphMatrix()
        self.dicoV = self.MakeGraph()
        self.Vertices = self.getVertices()
        self.Edges = self.getEdges()
        self.PrimalGraph = self.PrimalGraphMatrix()
        self.incidenceMatrixTranspose = self.incidenceMatrix_Transpose()

    def getVertices(self) :
        return self.V

    def getEdges(self) :
        lst = []
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                if {Vertex,Vertex2} not in lst :
                    lst.append({Vertex,Vertex2})
        return lst

    def MakeGraph(self) :
        dicoV = {}
        for elem in self.V :
            dicoV[elem] = []

        for hyperarete in self.E :
            x = len(self.E[hyperarete])
            if x > 1 :
                for i in range(x) :
                    for j in range(i+1,x) :
                        if self.E[hyperarete][i] not in dicoV[self.E[hyperarete][j]] :
                            dicoV[self.E[hyperarete][j]].append(self.E[hyperarete][i])
                        if self.E[hyperarete][j] not in dicoV[self.E[hyperarete][i]] :
                            dicoV[self.E[hyperarete][i]].append(self.E[hyperarete][j])
        return dicoV

    def PrimalGraphMatrix(self) :
        n = len(self.V)
        Matrix = [[ 0 for _ in range(n)] for _ in range(n)]
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                Matrix[self.stringDigit(Vertex)-1][self.stringDigit(Vertex2)-1] = 1

        return Matrix

    def IncidenceGraphMatrix(self) :
        IncidenceMatrix = [[0 for _ in range(len(self.E))] for _ in range(len(self.V)) ]
        for hyperarete in self.E :
            for Vertex in self.E[hyperarete] :
                IncidenceMatrix[self.stringDigit(Vertex)-1][self.stringDigit(hyperarete)-1] = 1

        return IncidenceMatrix

    def incidenceMatrix_Transpose(self) :
        n = len(self.incidenceMatrix)
        m = len(self.incidenceMatrix[0])
        MatrixTranspose = [[0 for i in range(n)] for j in range(m)]
        for i in range(n) :
            for j in range(m) :
                MatrixTranspose[j][i] = self.incidenceMatrix[i][j]

        return MatrixTranspose

    def generateDualGraph(self) :
        V = set()
        E = {}
        for i in range(len(self.incidenceMatrixTranspose)) :
            Vertex = "E" + str(i+1)
            V.add(Vertex)
            for j in range(len(self.incidenceMatrixTranspose[0])) :
                hyperarete = "Ev" + str(j+1)
                if hyperarete not in E :
                    E[hyperarete] = []
                if self.incidenceMatrixTranspose[i][j] == 1 :
                    E[hyperarete].append(Vertex)

        return Graph(V,E)

    def stringDigit(self,str) :
        res = ""
        for letter in str :
            if letter.isdigit() :
                res += letter
        return int(res)

def printMatrix(Matrix) :
    n = len(Matrix)
    m = len(Matrix[0])
    print("\n".join([" ".join([str(Matrix[i][j]) for j in range(m)]) for i in range(n)]))

def random_graph_generator(n,m):
    V = set(["v" + str(i) for i in range(1,n+1)])
    E = {}
    for i in range(1,m+1) :
        E["E" + str(i)] = []

    incidenceMatrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if random() < 0.5:

                Vertex = "v" + str(i+1)
                hyperarete = "E" + str(j+1)
                E[hyperarete].append(Vertex)

                incidenceMatrix[i][j] = 1
    ### PRINT Matrix
    printMatrix(incidenceMatrix)
    ### PRINT E
    for elem in E :
        print(elem + " :" , E[elem])

    return Graph(V,E,incidenceMatrix)
"""
V = {"v1","v2","v3","v4","v5","v6","v7"}

v = { "v1" : ["v2","v3"],
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
"""
graphe = random_graph_generator(randint(1,15),randint(1,15))
print("Vertices of graph:")
print(graphe.Vertices)
print("Edges of graph:")
print(graphe.Edges)
print("Adjacency Matrix")
printMatrix(graphe.PrimalGraph)

print("Incidence Matrix ")
printMatrix(graphe.incidenceMatrix)
print("Incidence Matrix Transpose")
printMatrix(graphe.incidenceMatrixTranspose)
print("\n\n\n\n")

grapheDual = graphe.generateDualGraph()
print("Vertices of dual graph:")
print(grapheDual.Vertices)
print("Edges of dual graph:")
print(grapheDual.Edges)
print("Adjacency Matrix")
printMatrix(grapheDual.PrimalGraph)
print("Incidence Matrix ")
printMatrix(grapheDual.incidenceMatrix)
print("Incidence Matrix Transpose")
printMatrix(grapheDual.incidenceMatrixTranspose)


#G = nx.Graph(g)
#nx.draw(G)
#plt.draw()
