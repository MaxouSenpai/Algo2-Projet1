import matplotlib.pyplot as plt
import numpy as np
from numpy.random import random,randint,choice
from Tree import Tree
from Hypergraph import Hypergraph
from cover_hypertree import *

def max_subtree(t):
    """
    Fonction qui prend en paramètre un arbre enraciné en r
    dont les sommets sont pondérés et affichera à l’écran les sommets qui constituent
    un sous-arbre enraciné en r de poids maximum.
    Les noeuds qui constituent le sous-arbre de poids maximum seront colorés en rouge
    et les autres seront colorés en gris.
    """
    nodes_to_desactivate = []
    t.show(nodes_to_desactivate,True if t.maxContribution(nodes_to_desactivate) > 0 else False)

def test_hypertree(hypergraph) :
    """
    Fonction qui prend en paramètre un hypergraphe, affichera
    à l'écran son hypergraphe dual sous les deux formats et si
    oui ou non il s’agit d’un hypertree.

    Si c'est un hypertree il affichera s'il existe une couverture
    exacte pour cet hypertree .
    (si la réponse est oui, la fonction affichera également la couverture).
    """
    hypergraphDual = hypergraph.generateDualGraph()
    isHT = hypergraphDual.is_alphaAcyclique()
    # Tester si l'hypergraphe dual est α-acyclique
    if isHT :
        solution = cover_hypertree(hypergraph)
        # Chercher s'il existe une couverture exacte pour l'hypergraphe

    hypergraphDual.show(isHT)
    # Interface graphique (GUI)

def random_tree_generator(max_nodes=15):
    res = ['r',np.random.randint(-100,100),[]]
    random_array = list(np.random.randint(-100,100,np.random.randint(0,max_nodes)))
    letter = 65

    for node in random_array:
        temp_node = [chr(letter),node,[]]
        letter += 1
        placed = False
        temp_dir = res[2]

        while not placed:
            if len(temp_dir) == 0:
                temp_dir.append(temp_node)
                placed = True

            else:
                choice = np.random.randint(0,2) # 0 : new child , 1 : new_dir

                if choice == 0:
                    temp_dir.insert(np.random.randint(0,len(temp_dir)),temp_node)
                    placed = True

                else:
                    temp_dir = temp_dir[np.random.randint(0,len(temp_dir))][2]

    return Tree(res)

def random_graph_generator():
    """
    Fonction qui génère aléatoirement un hypergraphe de taille
    raisonnable (maximum 15 sommets et hyper-arêtes) .
    """
    n = randint(1,16)
    # Nombre du sommets
    V = set("v" + str(i) for i in range(1,n+1))

    max_hyperedge = 2**n - 1
    # Maximum d'hyper-arêtes qu'on peut obtenir avec n sommets
    m = randint(1,16)
    # Nombre d'hyper-arêtes
    while m > max_hyperedge :
        m = randint(1,16)

    MatrixTranspose = []
    i = 0
    while i < m :
        row = [ 0 if random() < 0.5 else 1 for j in range(n)]
        # Génère une hyper-arête
        if row not in MatrixTranspose :
            # Vérifier qu'il n'existe pas la même hyper-arête deux fois
            MatrixTranspose.append(row)
            i += 1

    n = len(MatrixTranspose[0])

    incidenceMatrix = [[row[i] for row in MatrixTranspose] for i in range(n)]

    E = {"E" + str(j+1):["v" + str(i+1) for i in range(n) if incidenceMatrix[i][j]] for j in range(m) }

    return Hypergraph(V,E,incidenceMatrix)

def main():
    max_subtree(random_tree_generator())
    test_hypertree(random_graph_generator())
    plt.show()

if __name__ == "__main__":
    main()
