from random import random,randint,choice
from Graph import Graph
from cover_hypertree import *
import matplotlib.pyplot as plt
import numpy as np

class Hypergraph :
    def __init__(self,V={},E={},incidenceMatrix = []) :

        self.V = V
        # Ensemble des sommets de l'hypergraphe
        self.E = E
        # Dictionnaire contient les hyper-arêtes comme clés et les sommets qui appartiennent à cette hyper-arête comme valeurs
        self.incidenceMatrix = incidenceMatrix if incidenceMatrix != [] else self.getIncidenceGraphMatrix()
        # Matrice d'incidence de l'hypergraphe
        self.dicoV = self.getDicoV()
        # Dictionnaire contient les sommets comme clés et les sommets contenus dans la même hyper-arête
        self.incidenceMatrixTranspose = self.getIncidenceMatrixTranspose()
        # Transposée de la matrice d'incidence

    def getVertices(self) :
        """
        Renvoie les sommets d'hypergraphe.
        """
        return self.V

    def getEdges(self) :
        """
        Renvoie les arêtes entre les sommets d'hypergraphe.
        """
        edgesList = []
        # Liste qui contient tous les arêtes d'hypergraphe
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                if {Vertex,Vertex2} not in edgesList :
                    edgesList.append({Vertex,Vertex2})

        return edgesList

    def getDicoV(self) :
        """
        Renvoie un dictionnaire avec les sommets d'hypergraphe comme clés,
        et comme valeur des clés les autres sommets qui se trouvent dans
        la même hyper-arête.
        """
        dicoV = { Vertex :[] for Vertex in self.V }

        for hyperedge in self.E :
            x = len(self.E[hyperedge])
            if x > 1 :
                for i in range(x) :
                    for j in range(i+1,x) :
                        if self.E[hyperedge][j] not in dicoV[self.E[hyperedge][i]] :
                            dicoV[self.E[hyperedge][i]].append(self.E[hyperedge][j])
                        if self.E[hyperedge][i] not in dicoV[self.E[hyperedge][j]] :
                            dicoV[self.E[hyperedge][j]].append(self.E[hyperedge][i])
        return dicoV

    def getPrimalGraphMatrix(self) :
        n = len(self.V)
        Matrix = [[ 0 for _ in range(n)] for _ in range(n)]
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                Matrix[self.stringDigit(Vertex)-1][self.stringDigit(Vertex2)-1] = 1

        return Matrix

    def getIncidenceGraphMatrix(self) :

        IncidenceMatrix = [[0 for _ in range(len(self.E))] for _ in range(len(self.V)) ]
        for hyperedge in self.E :
            for Vertex in self.E[hyperedge] :
                IncidenceMatrix[self.stringDigit(Vertex)-1][self.stringDigit(hyperedge)-1] = 1

        return IncidenceMatrix

    def getIncidenceMatrixTranspose(self) :

        n = len(self.incidenceMatrix[0])

        MatrixTranspose = [[row[i] for row in self.incidenceMatrix] for i in range(n)]

        return MatrixTranspose

    def generateDualGraph(self) :
        """
        Générer l'hypergraphe dual H* (V*,E*) de l'hypergraphe H (V,E) ,
        H* = (V*,E*) où V* = E et pour chaque sommet v dans V
        nous avons une hyper-arête dans E* de la forme Ev = {X ⊆ E : v ∈ X}.
        """
        n = len(self.incidenceMatrixTranspose)
        m = len(self.incidenceMatrixTranspose[0])

        V = set("E" + str(i+1) for i in range(n))
        # V* = E
        E = { "Ev" + str(j+1) : [] for j in range(m)}
        # Une hyper-arête dans E* de la forme Ev = {X ⊆ E : v ∈ X}


        for i in range(n) :
            Vertex = "E" + str(i+1)

            for j in range(m) :
                hyperedge = "Ev" + str(j+1)

                if self.incidenceMatrixTranspose[i][j] == 1 :
                    E[hyperedge].append(Vertex)

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
        """
        Renvoie True si toute clique maximale (au sens de l’inclusion)
        de taille deux ou plus dans le graphe primale est une hyper-arête
        dans l’hypergraphe H(V,E) sinon False .
        """
        cliques = self.find_cliques(self.V)
        # Cliques maximales
        print("Les cliques maximales du graphe :")
        print("\n".join(str(cliques[i]) for i in range(len(cliques))))

        check = True
        E_values = [set(liste) for liste in self.E.values()]

        for clique in cliques :
            check = clique in E_values
            if not check :
                break

        return check

    def stringDigit(self,word) :

        return int("".join([ letter for letter in word if letter.isdigit()]))

    def show(self,isHT):
        plt.figure("SUPER INTERFACE DE OUF",figsize=(20,10))
        ax = plt.axes()
        ax.set_aspect("equal")
        plt.axis("off")
        plt.axis([0,1,0,1.2])
        plt.text(0.5,1.3,"This Hypergraph is an Hyper Tree" if isHT else "This Hypergraph is not an Hyper Tree" ,horizontalalignment="center",verticalalignment="center",fontsize=30,color="black")

        self.showPrimalGraph(ax,-0.6)
        self.showIncidenceGraph(ax,0.6)
        plt.show()

    def showIncidenceGraph(self,ax,dx):
        plt.text(0.5+dx,1.15,"Incidence graph of a dual hypergraph" ,horizontalalignment="center",verticalalignment="center",fontsize=20,color="black")
        pos = dict()

        if len(self.V) > 0:
            y = 1
            dy = 1/len(self.V)

            for v in self.V:
                pos[v] = y
                ax.add_artist(plt.Circle((0+dx, y), 0.03, color="red",clip_on=False))
                plt.text(0+dx,y,v,horizontalalignment="center",verticalalignment="center",fontsize=10,color="black")
                y-= dy

        if len(self.E.keys()) > 0:
            y = 1
            dy = 1/len(self.E.keys())
            color = ["deeppink","pink", "orange", "gold", "darkkhaki", "purple", "green", "lime", "blue", "cyan", "turquoise", "navy", "brown", "chocolate", "darkslategray"]
            i = 0

            for e in self.E.keys():
                ax.add_artist(plt.Circle((1+dx, y), 0.03, color="red",clip_on=False))
                plt.text(1+dx,y,e,horizontalalignment="center",verticalalignment="center",fontsize=10,color="black")

                for v in self.E[e]:
                    line = plt.Line2D([0.97+dx,0.023+dx], [y,pos[v]],color=color[i],linewidth=5,alpha=0.5,clip_on=False)
                    ax.add_line(line)

                y -= dy
                i+=1

    def showPrimalGraph(self,ax,dx):
        plt.text(0.5+dx,1.15,"Primal graph of a dual hypergraph" ,horizontalalignment="center",verticalalignment="center",fontsize=20,color="black")

        if len(self.V) > 0: # Prevent division by zero
            o = 360/len(self.V)
            angle = 90
            pos = dict()
            color = ["deeppink","pink", "orange", "gold", "darkkhaki", "purple", "green", "lime", "blue", "cyan", "turquoise", "navy", "brown", "chocolate", "darkslategray"]

            for v in self.V:
                x = 0.5 + dx + np.cos(np.deg2rad(angle))*0.5
                y = 0.5 + np.sin(np.deg2rad(angle))*0.5
                pos[v] = (x,y)
                ax.add_artist(plt.Circle((x, y), 0.075, color="red",clip_on=False))
                plt.text(x,y,v,horizontalalignment="center",verticalalignment="center",fontsize=20,color="black")
                angle-=o

            for c in range(len(self.E.keys())):

                e = list(self.E.keys())[c]

                if len(self.E[e]) > 1:

                    for i in range(len(self.E[e])):

                        origin = pos[self.E[e][i]]

                        for j in range(i+1,len(self.E[e])):
                            temp = pos[self.E[e][j]]
                            line = plt.Line2D([origin[0],temp[0]], [origin[1],temp[1]],color = color[c],linewidth = 5,alpha = 0.5,clip_on=False)
                            ax.add_line(line)


def random_graph_generator():
    """
    Une fonction qui génère aléatoirement un hypergraphe de taille
    raisonnable (maximum 15 sommets et hyper-arêtes) .
    """
    n = randint(1,15)
    # Nombre du sommet
    V = set("v" + str(i) for i in range(1,n+1))

    max_hyperedge = 2**n - 1
    # Maximum d'hyper-arêtes qu'on peut obtenir avec n sommets
    m = randint(1,15)
    # Nombre d'hyper-arêtes
    while m > max_hyperedge :
        m = randint(1,15)

    MatrixTranspose = []
    i = 0
    while i < m :
        row = [ 0 if random() < 0.5 else 1 for j in range(n)]
        # Génère une hyper-arête
        if row not in MatrixTranspose :
            # Vérifier qu'il existe par la même hyper-arête deux fois
            MatrixTranspose.append(row)
            i += 1

    n = len(MatrixTranspose[0])

    incidenceMatrix = [[row[i] for row in MatrixTranspose] for i in range(n)]

    E = {"E" + str(j+1):["v" + str(i+1) for i in range(n) if incidenceMatrix[i][j]] for j in range(m) }

    return Hypergraph(V,E,incidenceMatrix)

def test_hypertree(hypergraph) :
    """
    Une fonction qui prend en paramètre un hypergraphe affichera
    à l'écran son hypergraphe dual sous les deux formats et si
    oui ou non il s’agit d’un hypertree.

    Si c'est un hypertree il affichera s'il existe une couverture
    exacte pour cet hypertree .
    (si la réponse est oui, la fonction affichera également la couverture).
    """
    hypergraphDual = hypergraph.generateDualGraph()
    hypergraphDual_Primal = Graph(hypergraphDual.V,hypergraphDual.dicoV)
    isHT = hypergraphDual.checkCliques() and hypergraphDual_Primal.is_chordal()
    # Tester si l'hypergraphe dual est α-acyclique
    if isHT :
        solution = cover_hypertree(hypergraph)
        # Chercher s'il existe une couverture exacte pour l'hypergraphe

    hypergraphDual.show(isHT)
    # Interface graphique (GUI)


def testPrint(graphe) :
    print("Vertices of graph :\n",graphe.getVertices())
    print("\nEdges of graph :\n",graphe.getEdges())
    print("\nAdjacency Matrix :")
    printMatrix(graphe.getPrimalGraphMatrix())
    print("\nIncidence Matrix :")
    printMatrix(graphe.incidenceMatrix)
    print("\nIncidence Matrix Transpose")
    printMatrix(graphe.incidenceMatrixTranspose)
    print("\n\n\n")

graphe = random_graph_generator()
testPrint(graphe)
grapheDual = graphe.generateDualGraph()
testPrint(grapheDual)

test_hypertree(graphe)
