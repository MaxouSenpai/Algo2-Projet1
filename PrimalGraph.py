from random import choice
import sys

class PrimalGraph :
    """
    Le graphe primal d’un hypergraphe est un graphe défini sur les
    sommets de l’hypergraphe, avec des arêtes entre sommets contenus
    dans la même hyper-arête .
    """
    def __init__(self,V={},dicoV={}) :
        self.n = len(V)
        # Nombre du sommets
        self.V = V
        # Ensemble des sommets de l'hypergraphe
        self.dicoV = dicoV
        # Dictionnaire contient les sommets comme clés et les sommets contenus dans la même hyper-arête
        self.E = self.getEdges()
        # Les arêtes entre les sommets d'hypergraphe

    def getEdges(self) :
        lst = []
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                if {Vertex,Vertex2} not in lst :
                    lst.append({Vertex,Vertex2})
        return lst

    def find_cliques(self,P,R=set(),X=set(),cliques=[]) :
        """
        Renvoie toutes les cliques du graphe primal
        s'il y en sinon une liste vide , une clique est
        un sous-graphe induit complet .

        R: = est l'ensemble des nœuds d'une clique maximale.
        P: = est l'ensemble des nœuds possibles dans une clique maximale.
        X: = est l'ensemble des nœuds exclus.
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

    def checkCliques(self,E) :
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
        E_values = [set(liste) for liste in E.values()]
        # Liste contenant toutes les hyper-arêtes de l’hypergraphe

        for clique in cliques :
            check = clique in E_values
            # Vérifier si la clique est une hyper-arête dans l’hypergraphe
            if not check :
                break

        return check

    def subgraph(self,liste) :
        """
        Renvoie un sous-graphe induit , Un sous-graphe induit est un
        sous-graphe en restreignant le graphe à un sous ensemble de sommets.
        Formellement, H est un sous-graphe induit de G si, pour tout couple
        ( x , y ) de sommets de H, x est connecté à y dans H si et seulement
        si x est connecté à y dans G.
        """
        newDico = {}
        for Vertex in self.dicoV :
            if Vertex in liste :
                newDico[Vertex] = list(set(self.dicoV[Vertex]) & set(liste))
        return PrimalGraph(set(liste),newDico)

    def is_complete_graph(self) :
        """
        Renvoie True si le graphe est complet sinon False, un graphe complet
        est un graphe simple dont tous les sommets sont adjacents, c'est-à-dire
        que tout couple de sommets disjoints est relié par une arête.
        """
        if self.n < 2:
            return True
        graphEdges = len(self.E)
        graphMaxEdges = ((self.n * (self.n - 1)) / 2)

        return graphEdges == graphMaxEdges

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
