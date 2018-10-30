import matplotlib.pyplot as plt

class Tree:
    """docstring for Tree."""

    def __init__(self,data):

        self.name = data[0]

        self.weight = data[1]

        self.children = []

        for child in data[2]:
            self.children.append(Tree(child))

    def maxContribution(self,state=[]):
        res = self.weight

        for child in self.children:
            temp = child.maxContribution(state)
            if temp <= 0:
                state.append(child)
            else:
                res += temp
        return res

    def show(self,ax,state=[],current_state=True,x=0.5,y=1,space=0.25,width=3):

        current_state = current_state and self not in state
        ax.add_artist(plt.Circle((x, y), 0.075, color="red" if current_state else "silver",clip_on=False))
        plt.text(x,y,str(self.name)+'\n'+str(self.weight),horizontalalignment="center",verticalalignment="center",fontsize=20)

        if len(self.children) > 0: # Prevent division by 0
            dx = width/len(self.children)
            nx = x - width/2 - dx/2

            for child in self.children:
                nx += dx
                ax.arrow(x, y-0.075, nx-x, 0.15+y-space-y,head_width=0.05, head_length=0.05,fc="k", ec="k",length_includes_head=True,clip_on=False)
                child.show(ax,state,current_state,nx,y-space,space,dx+0.075)
