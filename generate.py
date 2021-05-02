from collections import deque
import pickle
import chess
import chess.engine

mainEngine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
MAINBOARD = chess.Board()


BOOK = {}


q = deque()
q.append(MAINBOARD.copy())
while q:
    nextBoard = q.popleft()
    #print(nextBoard, end="\n--------------------\n")
    #print(len(BOOK))
    if len(BOOK)%100==0:
        print(len(BOOK))
    if len(BOOK)%1000==0:
        pickle.dump(BOOK, open("openings.p", "wb"))
    best = mainEngine.play(nextBoard, chess.engine.Limit(depth=10))
    BOOK[nextBoard.fen()] = best.move

    #Now we need to add every possible black response to this move
    nextBoard.push(best.move)
    for newMove in nextBoard.legal_moves:
        nextBoard.push(newMove)
        q.append(nextBoard.copy())
        nextBoard.pop()
