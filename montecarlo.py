
from math import log,e, sqrt, inf
import chess.engine
import chess.polyglot
mainEngine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
import chess
import random

explore_weight = 0

def select(node, state):

    while not node.untriedMoves and node.children:
        node = node.UCT_select()
        state.push(node.move)
    return node, state

def expand(node, state, limdepth=4):

    for i in range(limdepth):
        if not node.untriedMoves:
            break
        newMove = random.choice(node.untriedMoves)

        state.push(newMove)
        node = node.addChild(newMove, state)
    return node, state

def rollout(state, limdepth=4):

        for i in range(limdepth):
            g = list(state.legal_moves)
            if not g:
                break
            state.push(random.choice(g))
        return state


def stockfishEval(board):
    global mainEngine
    info = mainEngine.analyse(board, chess.engine.Limit(depth=2))
    # print(info["score"].relative.score())
    return info["score"].relative.score(mate_score=100000)

REACHED=0
def getOutcome(state):
    global mainEngine, REACHED
    REACHED += 1
    return stockfishEval(state)
def backprop(state, node):
    while node!=None:
        node.update(getOutcome(state))
        node = node.parent
    return node, state


def UCT_play(root, numsims):
    rootNode = Node(state=root)

    for i in range(numsims):
        node = rootNode
        state =  root.copy()

        node, state = select(node, state)
        node, state = expand(node, state)
        state = rollout(state)
        node, state = backprop(state, node)

    return sorted(rootNode.children, key=lambda c: c.visits)[-1].move


class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.children = set()
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.untriedMoves = list(state.legal_moves)
        self.justPlayed = state.turn # True means white to move


    def UCT_select(self):
        best = max(self.children, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))
        return best

    def addChild(self, moveMade, newState):

        nextChild = Node(move=moveMade, parent=self, state=newState)
        self.untriedMoves.remove(moveMade)
        self.children.add(nextChild)
        return nextChild

    def update(self, res):
        self.visits += 1
        self.wins += res




mainState = chess.Board()

ROOT = Node(state=mainState)

while not mainState.is_game_over():

    move = UCT_play(mainState, 500)
    mainState.push(move)
    print(move, REACHED)
    print(mainState)
    got = input("ENTER MOVE: ")

    mainState.push_san(got)






