import matplotlib.pyplot as plt

class Tree:
    """Classe Arbre"""

    def __init__(self,data):
        """
        Premet d'initialiser l'arbre

        Prend en paramètre :
            data : Les données brutes de l'arbre.
                Modèle : [name,weight,children]
                où children = [[name_1,weight_1,children_1],...,[name_n,weight_n,children_n]]
        """

        self.name = data[0]
        self.weight = data[1]
        self.children = []

        for child in data[2]:
            self.children.append(Tree(child))

    def maxContribution(self,nodes_to_desactivate=[]):
        """
        Permet d'ajouter à la liste "state" les noeuds à désactiver

        Prend en paramètre :
            nodes_to_desactivate : Liste des noeuds à désactiver

        Retourne :
            res : La contribution max du noeud courrant
        """

        res = self.weight

        for child in self.children:
            temp = child.maxContribution(nodes_to_desactivate)
            if temp <= 0:
                # Si la contribution du fils courrant est nulle où négative on ajoute le fils à la liste "nodes_to_desactivate"
                nodes_to_desactivate.append(child.name)
            else:
                res += temp
        return res

    def show(self,ax,nodes_to_desactivate=[],current_state=True,x=0.5,y=1,space=0.25,width=3):
        """
        Permet d'afficher l'arbre :
            Les noeuds activés en rouge
            Les noeuds désactivés en gris

        Prend en paramètre :
            ax : Les axes
            nodes_to_desactivate : La liste du nom des noeuds à désactiver
            current_state : L'état du père du noeud courrant
            x : La position x du noeud courant
            y : La position y du noeud courant
            space : La différence Y entre un père et son fils
            width : L'espace X disponible pour cette branche
        """

        current_state = current_state and self.name not in nodes_to_desactivate
        # Si son père est désactivé alors lui aussi est désactivé

        ax.add_artist(plt.Circle((x, y), 0.075, color="red" if current_state else "silver",clip_on=False))
        plt.text(x,y,str(self.name)+'\n'+str(self.weight),horizontalalignment="center",verticalalignment="center",fontsize=20)

        if len(self.children) > 0: # Prevent division by 0
            dx = width/len(self.children)
            nx = x - width/2 - dx/2

            for child in self.children:
                nx += dx
                ax.arrow(x, y-0.075, nx-x, 0.15+y-space-y,head_width=0.05, head_length=0.05,fc="k", ec="k",length_includes_head=True,clip_on=False)
                child.show(ax,nodes_to_desactivate,current_state,nx,y-space,space,dx+0.075)
