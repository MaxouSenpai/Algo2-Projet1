################################
#   Maxime Hauwaert : 461714   #
#   Yahya Bakkali   : 445166   #
################################

from PrimalGraph import PrimalGraph
import matplotlib.pyplot as plt
import numpy as np

class Hypergraph :
    def __init__(self,V=set(),E={},incidenceMatrix = []) :
        """
        Initialise l'hypergraphe

        Prend en paramètre :
            V : Ensemble des sommets de l'hypergraphe
            E : Dictionnaire contenant les hyper-arêtes comme clés et les sommets qui appartiennent à cette hyper-arête comme valeurs
            incidenceMatrix : La matrice d'incidence de l'hypergraphe
        """
        self.V = V
        self.E = E
        self.incidenceMatrix = incidenceMatrix
        self.dicoV = self.getDicoV()
        # Dictionnaire contenant les sommets comme clés et les sommets contenus dans la même hyper-arête
        self.primalGraph = self.primalGraph_OfaHypergraph()
        # Le graphe primal de l'hypergraphe

    def getVertices(self) :
        """
        Renvoie les sommets de l'hypergraphe.
        """
        return self.V

    def getEdges(self) :
        """
        Renvoie les arêtes entre les sommets de l'hypergraphe.
        """
        edgesList = []
        # Liste contenant toutes les arêtes de l'hypergraphe
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                if {Vertex,Vertex2} not in edgesList :
                    edgesList.append({Vertex,Vertex2})

        return edgesList

    def getDicoV(self) :
        """
        Renvoie un dictionnaire avec les sommets de l'hypergraphe comme clés
        et comme valeur les autres sommets qui se trouvent dans
        la même hyper-arête.
        """
        dicoV = { Vertex :[] for Vertex in self.V }

        for hyperedge in self.E :
            # Une hyper-arête dans E
            x = len(self.E[hyperedge])
            if x > 1 :
                for i in range(x) :
                    Vertex = self.E[hyperedge][i]
                    # Sommet qui se trouve dans l'hyper-arête

                    for j in range(i+1,x) :
                        Vertex2 = self.E[hyperedge][j]
                        # Un autre sommet qui se trouve dans la même hyper-arête

                        if Vertex2 not in dicoV[Vertex] :
                            dicoV[Vertex].append(Vertex2)
                        if Vertex not in dicoV[Vertex2] :
                            dicoV[Vertex2].append(Vertex)
        return dicoV


    def primalGraph_OfaHypergraph(self) :
        """
        Renvoie le graphe primal de l'hypergraphe
        """
        return PrimalGraph(self.V,self.dicoV)

    def is_alphaAcyclique(self) :
        """
        Renvoie True si le graphe est α-acyclique sinon False
        """
        #Un hypergraphe est α-acyclique si son graphe primal est cordal et
        #que toute clique maximale (au sens de l’inclusion) de taille deux
        #ou plus dans le graphe primal est une hyper-arête dans l’hypergraphe.

        return self.primalGraph.checkCliques(self.E) and self.primalGraph.is_chordal()

    def getIncidenceMatrixTranspose(self) :
        """
        Renvoie la transposée de la matrice d'incidence
        """
        n = len(self.incidenceMatrix[0])

        MatrixTranspose = [[row[i] for row in self.incidenceMatrix] for i in range(n)]

        return MatrixTranspose

    def generateDualGraph(self) :
        """
        Renvoie l'hypergraphe dual de l'hypergraphe
        """
        #Générer l'hypergraphe dual H* (V*,E*) de l'hypergraphe H (V,E) revient à faire :
        #H* = (V*,E*) où V* = E et pour chaque sommet v dans V,
        #nous avons une hyper-arête dans E* de la forme Ev = {X ⊆ E : v ∈ X}.

        incidenceMatrixTranspose = self.getIncidenceMatrixTranspose()
        # Transposée de la matrice d'incidence
        n = len(incidenceMatrixTranspose)
        m = len(incidenceMatrixTranspose[0])

        V = set("E" + str(i+1) for i in range(n))
        # V* = E
        E = {"Ev" + str(j+1):["E" + str(i+1) for i in range(n) if incidenceMatrixTranspose[i][j]] for j in range(m) }
        # Une hyper-arête dans E* de la forme Ev = {X ⊆ E : v ∈ X}

        return Hypergraph(V,E,incidenceMatrixTranspose)

    def show(self,isHT):
        """
        Lance l'affichage de l'hypergraphe
        """
        plt.figure("SUPER INTERFACE DE OUF",figsize=(20,10))
        ax = plt.axes()
        ax.set_aspect("equal")
        plt.axis("off")
        plt.axis([0,1,0,1.2])
        plt.text(0.5,1.3,"This Hypergraph is an Hyper Tree" if isHT else "This Hypergraph is not an Hyper Tree" ,horizontalalignment="center",verticalalignment="center",fontsize=30,color="black")

        self.showPrimalGraph(ax,-0.6)
        self.showIncidenceGraph(ax,0.6)

    def showIncidenceGraph(self,ax,dx):
        """
        Lance l'affichage du graphe d'incidence
        """
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
        """
        Lance l'affichage du graphe primal
        """
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
