def hierarchy_pos(G, root, width=1, vert_gap = 0.2, vert_loc = 0, xcenter = 0.5,
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    print(neighbors)
    if len(neighbors)!=0:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx+0.075, vert_gap = vert_gap,
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos,
                                parent = root)
    return pos

    def show(self,figure,title,x_offset=0):
        G1 = nx.DiGraph()
        pos = self.makeGraph(G1,x_offset)
        plt.figure(figure,figsize=(20,10))
        temp = pos[self.getNodeName()]
        plt.text(temp[0],temp[1]+0.02,title,horizontalalignment="center",fontsize=20)
        nx.draw_networkx_nodes(G1,pos,node_size=650,node_color='red',alpha=0.5)
        nx.draw_networkx_edges(G1,pos,width=2,arrowstyle="-|>",arrowsize=15,edge_color='blue',alpha=0.25)
        nx.draw_networkx_labels(G1,pos,font_size=10,font_family='sans-serif',font_color='black')
        plt.axis('off')

    def makeGraph(self, G, pos = {}, x = 0.5, y = 0, space = 0.2, width = 1):

        pos[self.getNodeName()] = (x,y)

        if len(self.children) != 0:

            dx = width/len(self.children)
            nx = x - width/2 - dx/2

            for child in self.children:
                G.add_edge(self.getNodeName(),child.getNodeName())
                nx += dx
                pos = child.makeGraph(G,pos,nx,y-space,space,dx+0.075)

        return pos


        def makeGraph(self, G, x_offset = 0, pos = {}, x = 0.5, y = 0, space = 0.2, width = 1):

        pos[self.getNodeName()] = (x+x_offset,y)

        if len(self.children) != 0:

            dx = width/len(self.children)
            nx = x - width/2 - dx/2

            for child in self.children:
                G.add_edge(self.getNodeName(),child.getNodeName())
                nx += dx
                pos = child.makeGraph(G,x_offset,pos,nx,y-space,space,dx+0.075)

        return pos

class Tree(object):
    """docstring for Tree."""

    STATIC = 65

    def __init__(self,arg): # Patern : [weight,[else],...,[else]]
        super(Tree, self).__init__()
        self.weight = arg[0]
        self.children = []
        self.name = chr(Tree.STATIC)
        Tree.STATIC+=1
        for t in arg[1:]:
            temp = Tree(t)
            self.children.append(temp)

    def __str__(self):
        res = "(" + self.name + " : " + str(self.weight)
        for child in self.children:
            res += str(child)
        return res+")"

    def getNodeName(self):
        return self.name + "\n" + str(self.weight)

    def contribution(self):
        res = self.weight
        i = 0
        while i < len(self.children):
            temp = self.children[i].contribution()
            if temp <= 0:
                self.children.pop(i)
            else:
                res += temp
                i+=1
        return res

    def show(self,background):
        G = nx.DiGraph()
        background.makeGraph(G)
        pos = background.makePos()
        plt.figure("max_subtree",figsize=(20,10))
        nx.draw_networkx_nodes(G,pos,node_size=650,node_color="silver",alpha=0.5)
        nx.draw_networkx_edges(G,pos,width=2,arrowstyle="-|>",arrowsize=15,edge_color='blue',alpha=0.25)
        nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif',font_color='black')
        G = nx.DiGraph()
        self.makeGraph(G)
        nx.draw_networkx_nodes(G,pos,node_size=650,node_color="red",alpha=0.5)
        plt.axis('off')

    def makeGraph(self, G):
        for child in self.children:
            G.add_edge(self.getNodeName(),child.getNodeName())
            child.makeGraph(G)

    def makePos(self,pos = {}, x = 0.5, y = 0, space = 0.2, width = 1):

        pos[self.getNodeName()] = (x,y)

        if len(self.children) != 0:

            dx = width/len(self.children)
            nx = x - width/2 - dx/2

            for child in self.children:
                nx += dx
                pos = child.makePos(pos,nx,y-space,space,dx+0.075)

        return pos

"""
r = ['r',3,[['a',-3,[['c',1,[]]]],['b',3,[]]]]
t = Tree(r)
t.maxContribution()
plt.figure("max_subtree",figsize=(20,10))
ax = plt.axes()
ax.set_aspect("equal")
t.show(ax)
plt.axis([-0.25,1.25,-0.25,1.25])
plt.axis('off')
plt.show()
"""

#t = Tree(r)
#t = Tree(randomTree())
#t = Tree([-10,[2],[3]])
#max_subtree(t)


#test_hypertree(t)

#circle = plt.Circle((0, 0), 2, color='r')
#fig = plt.subplot()
#fig = plt.figure()
#ax = plt.gca()
#ax = fig.add_subplot(111)
#plt.axis('equal')
#ax.add_artist(circle)
#ax.add_artist(plt.Circle((0.5, 0.5), 0.2, color='r'))
#ax.arrow(0, 0, 0.5, 0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')
#ax.set_aspect("equal")
#plt.show()
"""
n = ['n',-1,[]]
l = ['l',-1,[]]
m = ['m',3,[n]]
i = ['i',4,[]]
j = ['j',-5,[l,m]]
c = ['c',4,[]]
d = ['d',-1,[i,j]]
e = ['e',-1,[]]
a = ['a',-5,[c,d,e]]

k = ['k',1,[]]
f = ['f',-1,[]]
g = ['g',-2,[k]]
h = ['h',2,[]]
b = ['b',-1,[f,g,h]]

r = ['r',2,[a,b]]
"""
from random import random,randint
import matplotlib.pyplot as plt
import numpy as np

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

    def show(self,ax):
        if len(self.V) > 0: # Prevent division by zero
            o = 360/len(self.V)
            angle = 90

            for v in self.V:
                x = np.cos(np.deg2rad(angle))*0.5
                y = np.sin(np.deg2rad(angle))*0.5
                print(x,y,angle,o)
                ax.add_artist(plt.Circle((x, y), 0.075, color="red"))
                angle-=o

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
#graphe = random_graph_generator(randint(1,15),randint(1,15))
graphe = random_graph_generator(1,1)
plt.figure("Test :-D",figsize=(20,10))
ax = plt.axes()
ax.set_aspect("equal")
plt.axis([-0.5,1.5,-0.5,1.5])
graphe.show(ax)
plt.show()
"""
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
"""

#G = nx.Graph(g)
#nx.draw(G)
#plt.draw()

"""
    def show(self):
        plt.figure(figsize=(20,10))
        ax = plt.axes()
        plt.axis([0,1,3.5,1])
        ax.set_aspect('equal')
        plt.axis("off")

        pos = dict()
        color = ["deeppink","pink", "orange", "gold", "darkkhaki", "purple", "green", "lime", "blue", "cyan", "turquoise", "navy", "brown", "chocolate", "darkslategray"]

        y = 1

        for v in self.V:

            pos[v] = y
            ax.add_artist(plt.Circle((0.2-3, y), 0.1, color="red",clip_on=False))
            plt.text(0.2-3,y,v,horizontalalignment="center",verticalalignment="center",fontsize=10,color="black")
            y-= 0.3

        y = 1

        for e in self.E.keys():

            ax.add_artist(plt.Circle((0.8+3, y), 0.1, color="red",clip_on=False))
            plt.text(0.8+3,y,e,horizontalalignment="center",verticalalignment="center",fontsize=10,color="black")

            for v in self.E[e]:
                line = plt.Line2D([0.7-3.4,0.3+3.4], [y,pos[v]],color=(np.random.random(),np.random.random(),np.random.random()),linewidth=5,alpha=0.5,clip_on=False)
                ax.add_line(line)

            y -= 0.3

        plt.show()
"""
