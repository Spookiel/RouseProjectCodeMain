
from math import log,e, sqrt, inf
explore_weight = 0
class MCTS:
    def __init__(self,numsims):
        self.numsims = numsims


    def simulate(self, boardState):

        rootNode = Node(boardState)



        # What we need to do is simulate some moves into the future and check the board state in that position, and then feed back the state
        # Steps should be something like this

        #

class Node:
    def __init__(self):
        pass


