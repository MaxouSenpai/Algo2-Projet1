from random import random,randint,choice
import matplotlib.pyplot as plt
import numpy as np

class Hypergraph :
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
        """
        MatrixTranspose = [[0 for i in range(n)] for j in range(m)]
        for i in range(n) :
            for j in range(m) :
                MatrixTranspose[j][i] = self.incidenceMatrix[i][j]
        """
        MatrixTranspose = []
        for i in range(m):
            MatrixTranspose.append([row[i] for row in self.incidenceMatrix])

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

        return Hypergraph(V,E)

    def find_cliques(self,P,R=set(),X=set(),cliques=[]) :
        """
        R := is the set of nodes of a maximal clique.
        P := is the set of possible nodes in a maximal clique.
        X := is the set of nodes that are excluded.
        """

        if not P and not X  :
            if len(R) >= 2 and R not in cliques :
                cliques.append(R)
        else :
            pivot = choice(list(P.union(X)))
            for vertex in P.difference(self.dicoV[pivot]) :
                newP = P.intersection(self.dicoV[vertex])
                newR = R.union({vertex})
                newX = X.intersection(self.dicoV[vertex])
                self.find_cliques(newP,newR,newX,cliques)
                P.difference({vertex})
                X.union({vertex})
        return cliques

    def checkCliques(self) :
        cliques = self.find_cliques(self.V)
        print(cliques)
        check = True
        E_values = list(self.E.values())

        for clique in cliques :
            check = sorted(list(clique)) in E_values
            if not check :
                break

        return check


    def stringDigit(self,str) :
        res = ""
        for letter in str :
            if letter.isdigit() :
                res += letter
        return int(res)

    def show(self):
        ax = plt.axes()
        ax.set_aspect("equal")
        plt.axis([-0.1,1.1,-0.1,1.1])
        plt.axis("off")
        #plt.draw()

        if len(self.V) > 0: # Prevent division by zero
            o = 360/len(self.V)
            angle = 90
            pos = dict()

            for v in self.V:
                x = 0.5 + np.cos(np.deg2rad(angle))*0.5
                y = 0.5 + np.sin(np.deg2rad(angle))*0.5
                pos[v] = (x,y)
                ax.add_artist(plt.Circle((x, y), 0.075, color="red"))
                plt.text(x,y,v,horizontalalignment="center",verticalalignment="center",fontsize=20,color="black")
                angle-=o

            color = ['b','g','y','k','r','c','m']

            for c in range(len(self.E.keys())):

                e = list(self.E.keys())[c]

                if len(self.E[e]) > 1:

                    for i in range(len(self.E[e])):

                        origin = pos[self.E[e][i]]

                        for j in range(i+1,len(self.E[e])):
                            temp = pos[self.E[e][j]]
                            line = plt.Line2D([origin[0],temp[0]], [origin[1],temp[1]],color = color[c],linewidth = 10,alpha = 0.5)
                            ax.add_line(line)
                            plt.pause(0.5)
                            line.set_linewidth(5)
                            plt.pause(0.5)
                elif len(self.E[e]) == 1: # Circle
                    pass
                plt.pause(1)
            plt.show()

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

    return Hypergraph(V,E,incidenceMatrix)

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


V = {"v1","v2","v3","v4","v5","v6","v7"}

dicoV = { "v1" : ["v2","v3"],
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
test = Hypergraph(V,E)
#plt.figure("Test :-D",figsize=(20,10))
#ax = plt.axes()
#ax.set_aspect("equal")
#plt.axis([-0.1,1.1,-0.1,1.1])
#plt.axis("off")
test.show()
#ax.add_line(plt.Line2D([0,1], [0,1],color="green"))
#plt.plot(0, 1, '-g')  # solid green
#plt.show()
print(test.checkCliques())
