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

    def show(self,figure=1):
        G1=nx.DiGraph()
        self.makeGraph(G1)
        pos = hierarchy_pos(G1,self.name)
        plt.figure(figure)
        nx.draw_networkx_nodes(G1,pos,node_size=700)
        nx.draw_networkx_edges(G1,pos,width=4)
        nx.draw_networkx_labels(G1,pos,font_size=20,font_family='sans-serif')
        plt.axis('off')

    def makeGraph(self,G):
        for child in self.children:
            G.add_edge(self.name,child.name,weight=child.weight)
            child.makeGraph(G)

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
    #if parent != None:   #this should be removed for directed graphs.
    #    neighbors.remove(parent)  #if directed, then parent not in neighbors.
    if len(neighbors)!=0:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx+0.075, vert_gap = vert_gap,
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos,
                                parent = root)
    return pos

def max_subtree(t):
    c = copy.deepcopy(t)
    print(str(c.contribution()) + " ---> " + str(c))
    """
    G1=nx.DiGraph()
    t.makeGraph(G1)
    #pos = nx.circular_layout(G1)
    pos = hierarchy_pos(G1,t.name)
    print(pos)
    plt.figure(1)
    nx.draw_networkx_nodes(G1,pos,node_size=700)
    nx.draw_networkx_edges(G1,pos,width=6)
    nx.draw_networkx_labels(G1,pos,font_size=20,font_family='sans-serif')
    plt.axis('off')
    #plt.figure(1)
    #nx.draw(G1)
    """
    t.show()
    """
    G=nx.DiGraph()
    c.makeGraph(G)
    #pos = nx.circular_layout(G)
    pos = hierarchy_pos(G,c.name)
    plt.figure(2)
    nx.draw_networkx_nodes(G,pos,node_size=700)
    nx.draw_networkx_edges(G,pos,width=6)
    nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
    #nx.draw(G)
    #labels = nx.get_edge_attributes(G,'weight')
    #print(labels)
    #labels = nx.get_node_attributes(G,'A')
    #print(labels)
    #nx.draw_networkx_edge_labels(G,pos,edge_label=labels)
    #nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display
    """
    c.show(2)

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
    #print(t)
    max_subtree(t)
    test_hypertree(t)

main()
