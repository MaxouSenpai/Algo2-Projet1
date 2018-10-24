import matplotlib.pyplot as plt

class Tree():
    """docstring for Tree."""

    def __init__(self,data,x=0.5,y=1,space=0.25,width=3):

        self.name = data[0]

        self.weight = data[1]

        self.x = x
        self.y = y

        self.state = True

        self.children = []

        if len(data[2]) > 0: # Prevent division by 0

            dx = width/len(data[2])
            nx = x - width/2 - dx/2

            for child in data[2]:
                nx += dx
                temp = Tree(child,nx,y-space,space,dx+0.075)
                self.children.append(temp)

    def maxContribution(self):
        res = self.weight

        for child in self.children:
            temp = child.maxContribution()
            if temp <= 0:
                child.state = False
            else:
                res += temp
        return res

    def show(self,ax,state=True):

        state = state and self.state
        ax.add_artist(plt.Circle((self.x, self.y), 0.075, color="red" if state else "silver"))
        plt.text(self.x,self.y,str(self.name)+'\n'+str(self.weight),horizontalalignment="center",verticalalignment="center",fontsize=20)

        for child in self.children:
            ax.arrow(self.x, self.y-0.075, child.x-self.x, 0.15+child.y-self.y,head_width=0.05, head_length=0.05,fc="k", ec="k",length_includes_head=True)
            child.show(ax,state)
