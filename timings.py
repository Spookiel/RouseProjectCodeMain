

import chess
import asyncio
import time
import chess.engine
start = time.time()
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
print("loaded engine in", time.time()-start, "seconds")


bo = chess.Board()
bo.push_san("e4")
print(bo)
info  = engine.analyse(bo,chess.engine.Limit(depth=0))
print(info)


def get(board):
    global engine
    info = engine.analyse(board, chess.engine.Limit(depth=20))
    print(info["score"])


start2 = time.time()
get(bo)
print("ANALYSED IN", time.time()-start2)


get(bo)
#asyncio.run(get(bo))