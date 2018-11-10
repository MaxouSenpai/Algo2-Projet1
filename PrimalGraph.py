from numpy.random import choice

class PrimalGraph :
    """
    Le graphe primal d’un hypergraphe est un graphe défini sur les
    sommets de l’hypergraphe, avec des arêtes entre sommets contenus
    dans la même hyper-arête .
    """
    def __init__(self,V=set(),dicoV={}) :
        """
        Initialise le graphe primal

        Prend en paramètre :
            V : Ensemble des sommets du graphe primal
            dicoV : Dictionnaire contenant les sommets comme clés et comme valeurs les sommets contenus dans la même hyper-arête
        """
        self.n = len(V)
        # Nombre de sommets
        self.V = V
        self.dicoV = dicoV
        self.E = self.getEdges()
        # Les arêtes entre les sommets du graphe primal

    def getEdges(self) :
        """
        Renvoie les arêtes entre les sommets du graphe primal
        """
        edgesList = []
        # Liste contenant toutes les arêtes du graphe primal
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                if {Vertex,Vertex2} not in edgesList :
                    edgesList.append({Vertex,Vertex2})

        return edgesList


    def getPrimalGraphMatrix(self) :
        """
        Renvoie la matrice du graphe primal
        """
        n = len(self.V)
        Matrix = [[ 0 for _ in range(n)] for _ in range(n)]
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                Matrix[self.stringDigit(Vertex)-1][self.stringDigit(Vertex2)-1] = 1

        return Matrix

    def stringDigit(self,word) :
        """
        Renvoie le nombre contenu dans "word"
        """
        return int("".join([ letter for letter in word if letter.isdigit()]))

    def find_cliques(self,P,R=set(),X=set(),cliques=[]) :
        """
        Renvoie toutes les cliques du graphe primal
        s'il y en a sinon une liste vide , une clique est
        un sous-graphe induit complet .

        Prend en paramètre:
            R : L'ensemble des nœuds d'une clique maximale.
            P : L'ensemble des nœuds possibles dans une clique maximale.
            X : L'ensemble des nœuds exclus.
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
        de taille deux ou plus dans le graphe primal est une hyper-arête
        dans l’hypergraphe H(V,E) sinon False .
        """
        cliques = self.find_cliques(self.V)
        # Cliques maximales
        if cliques :
            print("Les cliques maximales du graphe primal :")
            print("\n".join(str(cliques[i]) for i in range(len(cliques))))
        else :
            print("Pas de cliques maximales")

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
        Renvoie un sous-graphe induit
        """
        #Un sous-graphe induit est un
        #sous-graphe en restreignant le graphe à un sous ensemble de sommets.
        #Formellement, H est un sous-graphe induit de G si, pour tout couple
        #(x,y) de sommets de H, x est connecté à y dans H si et seulement
        #si x est connecté à y dans G.

        newDico = {}
        for Vertex in self.dicoV :
            if Vertex in liste :
                newDico[Vertex] = list(set(self.dicoV[Vertex]) & set(liste))
        return PrimalGraph(set(liste),newDico)

    def is_complete_graph(self) :
        """
        Renvoie True si le graphe est complet sinon False
        """
        #Un graphe complet
        #est un graphe simple dont tous les sommets sont adjacents, c'est-à-dire
        #que tout couple de sommets disjoints est relié par une arête.

        if self.n < 2:
            return True
        graphEdges = len(self.E)
        # Nombre des arêtes du graphe primal
        graphMaxEdges = ((self.n * (self.n - 1)) / 2)
        # Nombre maximal des arêtes qu'un graphe primal peut avoir

        return graphEdges == graphMaxEdges

    def max_cardinality_node(self, choices, wanna_connect):
        """
        Retourne un sommet dans les choix qui a plus de connexions
        en graphe aux sommets dans wanna_connect.
        """

        maxConnections = -1
        # Nombre de connexions maximales
        for choice in choices:
            # Choisir un sommet dans les choix
            connections = len([Vertex for Vertex in self.dicoV[choice] if Vertex in wanna_connect])
            # Nombre de connexions du sommet choisi aux sommets dans wanna_connect
            if connections > maxConnections:
                maxConnections = connections
                maxCardinalityNode = choice
                # Sommet qui a plus de connexions

        return maxCardinalityNode

    def is_chordal(self):
        """
        Étant donné l'ensemble des sommets du graphe primal,lance une recherche
        de cardinalité maximale (en partant d'un sommet arbitraire)
        en essayant de trouver un cycle non-chordal.
        """

        unnumbered = set(self.V)
        # Ensemble des sommets non numéroté
        s = choice(list(self.V))
        # Choisi un sommet arbitraire

        unnumbered.remove(s)
        # Supprime le sommet choisi de l'ensemble non numéroté
        numbered = set([s])
        # Ajout le sommet choisi à l'ensemble des sommets numéroté

        current_treewidth = -1

        while unnumbered:

            Vertex = self.max_cardinality_node(unnumbered, numbered)
            # Sommet qui a plus de connexions aux sommets dans numbered
            unnumbered.remove(Vertex)
            # Supprime le sommet qui a plus de connexions de l'ensemble non numéroté
            numbered.add(Vertex)
            # Ajout le sommet qui a plus de connexions à l'ensemble des sommets numéroté
            clique_wanna_be = set(self.dicoV[Vertex]) & numbered
            #
            subGraph = self.subgraph(list(clique_wanna_be))
            # Un sous-graphe induit des sommets appartenant à clique_wanna_be

            isCompleteGraph = subGraph.is_complete_graph()
            if not isCompleteGraph :
                # Le sous-graphe n'est pas une clique
                return False
            #Else
            # Le graphe semble être chordal maintenant,on continue.

        return True
