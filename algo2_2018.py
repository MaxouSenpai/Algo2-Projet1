import copy
import networkx as nx
import matplotlib.pyplot as plt

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
        return self.name + " : " + str(self.weight)

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

    def show(self,figure):
        G1 = nx.DiGraph()
        pos = self.makeGraph(G1)
        plt.figure(figure)
        nx.draw_networkx_nodes(G1,pos,node_size=1000,node_color='red',alpha=0.5)
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

def max_subtree(t):
    c = copy.deepcopy(t)
    print(str(c.contribution()) + " ---> " + str(c))

    t.show("Before")

    c.show("After")

    plt.show()

def test_hypertree(t):
    pass

def main():

    n = [-1]
    l = [-1]
    m = [3,n]
    i = [4]
    j = [-5,l,m]
    c = [4]
    d = [-1,i,j]
    e = [-1]
    a = [-5,c,d,e]

    k = [1]
    f = [-1]
    g = [-2,k]
    h = [2]
    b = [-1,f,g,h]

    r = [2,a,b]

    t = Tree(r)
    max_subtree(t)
    test_hypertree(t)

main()
