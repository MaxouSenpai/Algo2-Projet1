from random import choice
import sys

class Graph :
    def __init__(self,V={},dicoV={}) :
        self.n = len(V)
        self.V = V
        self.dicoV = dicoV
        self.E = self.getEdges()

    def getEdges(self) :
        lst = []
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                if {Vertex,Vertex2} not in lst :
                    lst.append({Vertex,Vertex2})
        return lst

    def subgraph(self,liste) :
        newDico = {}
        for Vertex in self.dicoV :
            if Vertex in liste :
                newDico[Vertex] = list(set(self.dicoV[Vertex]) & set(liste))
        return Graph(set(liste),newDico)

    def is_complete_graph(self) :

        if self.n < 2:
            return True
        e = len(self.E)
        max_edges = ((self.n * (self.n - 1)) / 2)
        return e == max_edges


    def max_cardinality_node(self, choices, wanna_connect):
        """Returns a the node in choices that has more connections in G
        to nodes in wanna_connect.
        """
        #    max_number = None
        max_number = -1
        for x in choices:
            number = len([y for y in self.dicoV[x] if y in wanna_connect])
            if number > max_number:
                max_number = number
                max_cardinality_node = x
        return max_cardinality_node

    def is_chordal(self, s=None, treewidth_bound=sys.maxsize):
        """ Given a graph G, starts a max cardinality search
        (starting from s if s is given and from an arbitrary node otherwise)
        trying to find a non-chordal cycle.
        """

        unnumbered = set(self.V)
        if s is None:
            s = choice(list(self.V))

        unnumbered.remove(s)
        numbered = set([s])
        #    current_treewidth = None
        current_treewidth = -1

        while unnumbered:  # and current_treewidth <= treewidth_bound:

            v = self.max_cardinality_node(unnumbered, numbered)

            unnumbered.remove(v)
            numbered.add(v)

            clique_wanna_be = set(self.dicoV[v]) & numbered
            subGraph = self.subgraph(list(clique_wanna_be))

            if subGraph.is_complete_graph():
                # The graph seems to be chordal by now. We update the treewidth
                current_treewidth = max(current_treewidth, len(clique_wanna_be))
                if current_treewidth > treewidth_bound:
                    raise TypeError
            else:
                # sg is not a clique,
                return False
        return True
