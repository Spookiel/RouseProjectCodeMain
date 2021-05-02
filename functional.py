

import chess
import pickle
import chess.engine
import chess.polyglot
import sys
import time
mainEngine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

calls = 0
hits = 0



class Manager:


    def __init__(self, mainBoard=None):

        self.__MAINBOARD = mainBoard

        self.__MAINENGINE = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

        self.__tpcache = {}
        self.__CACHEHITS = 0
        self.__CALLS = 0
        self.__STOP_DEPTH = 2
        self.__LAST_START_TIME = None
        self.__TIME_LIMIT = 2

    @property
    def MAINBOARD(self):
        return self.__MAINBOARD

    @property
    def LAST_START_TIME(self):
        return self.__LAST_START_TIME

    @LAST_START_TIME.setter
    def LAST_START_TIME(self, val):
        self.__LAST_START_TIME = val

    def flip_square(self, sq):
        return sq^0x38


    def stockfishEval(self):

        board_info = self.__MAINENGINE.analyse(self.__MAINBOARD, chess.engine.Limit(depth=self.__STOP_DEPTH))
        return board_info["score"].relative.score(mate_score=1000000)

    def __check_time(self):
        return time.time() - self.__LAST_START_TIME > self.__TIME_LIMIT

    def __basic_minimax(self, depth, maxWhite):

        if self.__check_time():
            return -1e8 if maxWhite else 1e8

        if depth==self.__STOP_DEPTH or not self.MAINBOARD.legal_moves:
            final_score = self.stockfishEval()
            self.__tpcache[MAINBOARD.epd()] = final_score
            return final_score


        best_score = -1e8 if maxWhite else 1e8
        for new_move in self.MAINBOARD.legal_moves:

            self.MAINBOARD.push(new_move)

            got = self.__tpcache.get(MAINBOARD.epd(), None)

            if got is None:

                pot_score = self.__basic_minimax(depth - 1, ~maxWhite)
            else:
                pot_score = got
            self.MAINBOARD.pop()
            try:
                if maxWhite:
                    # Then we're trying to find the best move for white
                    if pot_score > best_score:
                        best_score = pot_score
                else:
                    if pot_score < best_score:
                        best_score = pot_score
            except Exception as e:
                print(e, pot_score, best_score)
                print(self.MAINBOARD)
                print("FAILED FOR UNKNOWN REASON")
                print("TERMINATING ENGINE BINARY")
                sys.exit(1)

        self.__tpcache[self.MAINBOARD.epd()] = best_score
        return best_score

    def basic_move(self):
        # Looking for the best move for the current turn of the board
        cur_turn = int(MAINBOARD.turn)

        best_move = None
        best_score = -1e8 if cur_turn else 1e8

        for cur_move in MAINBOARD.legal_moves:

            self.MAINBOARD.push(cur_move)
            cdepth = self.__STOP_DEPTH+1
            self.LAST_START_TIME = time.time()

            while self.__check_time():
                self.__basic_minimax(cdepth, 1-cur_turn)
                cdepth += 1

            new_score = self.__tpcache[MAINBOARD.epd()]

            # If cur turn is true, then we are trying to maximise for white

            if cur_turn and new_score > best_score:
                best_score = new_score
                best_move = cur_move
            elif not cur_turn and new_score < best_score:
                best_score = new_score
                best_move = cur_move
            self.MAINBOARD.pop()

        print("CHOSEN", best_move, "WITH SCORE", best_score)
        return best_move

def get_basic_move():
    #Looking for the best move for the current turn of the board
    cur_turn = int(MAINBOARD.turn)



    best_move = None
    best_score = -1e8 if cur_turn else 1e8

    for cur_move in MAINBOARD.legal_moves:

        MAINBOARD.push(cur_move)

        minimaxBasic(3, 1 - cur_turn)


        new_score = tpcache[MAINBOARD.epd()]
        print(cur_move, new_score, "CACHED", len(tpcache), "WITH", CALLS, "FUNCTION CALLS AND", CACHEHITS, "CACHE HITS")

        #If cur turn is true, then we are trying to maximise for white

        if cur_turn and new_score > best_score:
            best_score = new_score
            best_move = cur_move
        elif not cur_turn and new_score < best_score:
            best_score = new_score
            best_move = cur_move
        MAINBOARD.pop()

    print("CHOSEN", best_move, "WITH SCORE", best_score)
    MAINBOARD.push(best_move)


def flip_square(sq):
    return sq^0x38


def stockfishEval(board):
        global mainEngine
        info = mainEngine.analyse(board, chess.engine.Limit(depth=2))
        #print(info["score"].relative.score())
        return info["score"].relative.score(mate_score=100000)

tpcache  = {}

#The steps I need to do are write a minimax function
# Write the interface with the stockfish evaluation
# Then use optimisation tricks to improve the pruning

MAINBOARD = chess.Board()
TESTBOARD = chess.Board()
CALLS, CACHEHITS = 0,0


def minimaxAlphaBeta(depth, maxWhite, alpha, beta):
    global MAINBOARD,CALLS, CACHEHITS
    CALLS += 1
    if depth==2:# or not MAINBOARD.legal_moves:

        final_score = stockfishEval(MAINBOARD)
        #final_score = evaluatePos(MAINBOARD)
        tpcache[MAINBOARD.epd()] = final_score
        return final_score

    #Then we need to check for each legal move, we need to calculate the best and worst scores for that move
    best_score = -1e8 if maxWhite else 1e8
    for new_move in MAINBOARD.legal_moves:

        #Check if we can go down here
        MAINBOARD.push(new_move)

        got = tpcache.get(MAINBOARD.epd(), None)

        if got is None:

            pot_score = minimaxAlphaBeta(depth-1, ~maxWhite,alpha,beta)
            tpcache[got] = pot_score
        else:
            CACHEHITS += 1
            pot_score = got
        MAINBOARD.pop()
        if maxWhite:
            #Then we're trying to find the best move for white
            if pot_score > best_score:
                best_score = pot_score
                alpha = max(alpha, best_score)


        else:
            if pot_score < best_score:
                best_score = pot_score
                beta = min(best_score, best_score)

        if beta <= alpha:
            break

        if maxWhite:
            if best_score >= beta:
                return beta
        else:
            if best_score <= alpha:
                return alpha
    tpcache[MAINBOARD.epd()] = best_score
    return best_score

#To get the relative score of the position, where postive is better for white and negative is better for black
TESTSCORE  = stockfishEval(TESTBOARD)









def get_advanced_move():
    #Looking for the best move for the current turn of the board
    cur_turn = int(MAINBOARD.turn)



    best_move = None
    best_score = -1e8 if cur_turn else 1e8
    #minimaxAlphaBeta(6, cur_turn, -1e8, 1e8)
    for cur_move in MAINBOARD.legal_moves:

        MAINBOARD.push(cur_move)

        minimaxAlphaBeta(5, 1 - cur_turn, -1e8, 1e8)


        new_score = tpcache[MAINBOARD.epd()]
        #print(cur_move, new_score, "CACHED", len(tpcache))
        print(cur_move, new_score, "CACHED", len(tpcache), "WITH", CALLS, "FUNCTION CALLS AND", CACHEHITS, "CACHE HITS")
        #If cur turn is true, then we are trying to maximise for white
        #If a move is found which leads to mate, then just set it as the best move and break
        if cur_turn and new_score > best_score:
            best_score = new_score
            best_move = cur_move
        elif not cur_turn and new_score < best_score:
            best_score = new_score
            best_move = cur_move
        MAINBOARD.pop()

    print("CHOSEN", best_move, "WITH SCORE", best_score)
    MAINBOARD.push(best_move)



# Add an openings book to speed up the first 5 moves of the game or so

best = mainEngine.play(MAINBOARD, chess.engine.Limit(depth=10))
print(best)
print(MAINBOARD)

BEST_LOOK = pickle.load(open("openings.p", "rb"))
with chess.polyglot.open_reader("komodo.bin") as reader:
    while True:
        #get_basic_move()
        try:
            got = reader.find(MAINBOARD).move
        except:

            got = BEST_LOOK.get(MAINBOARD.fen(), None)
        if not got:
            get_advanced_move()
        else:
            print("CHOSEN", got)
            MAINBOARD.push(got)
        print(MAINBOARD)
        print(MAINBOARD.fen())
        new_move = input("ENTER MOVE: ")
        MAINBOARD.push_san(new_move)






