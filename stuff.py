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
