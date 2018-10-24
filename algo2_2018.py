import matplotlib.pyplot as plt
import numpy as np
import Tree

def max_subtree(t):
    plt.figure("max_subtree",figsize=(20,10))
    ax = plt.axes()
    ax.set_aspect("equal")
    plt.axis([-1.25,2.25,-0.5,1.2])
    plt.axis('off')

    if t.maxContribution() > 0:

        t.show(ax)

    else:
        plt.text(0.5,0.5,"Il n’existe pas de sous-arbre de poids positif contenant r",horizontalalignment="center",verticalalignment="center",fontsize=20)
        print(t)
    plt.show()

def randomTree(max_nodes=15):
    res = ['r',np.random.randint(-100,100),[]]
    random_array = list(np.random.randint(-100,100,max_nodes-1))
    makeRandomTree(random_array,res,65)
    return res

def makeRandomTree(random_array,temp,letter):
    nb_of_children = np.random.randint(0,len(random_array)//2)

    for i in range(nb_of_children):
        temp[2].append([chr(letter),random_array.pop(0),[]])
        letter+=1

    for i in range(nb_of_children):
        letter = makeRandomTree(random_array,temp[2][i],letter)

    return letter

def main():

    t = Tree.Tree(randomTree())
    max_subtree(t)

main()
