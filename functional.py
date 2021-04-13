

import chess

import chess.engine

mainEngine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

piece = { 'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000 }
pst = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}
calls = 0
hits = 0
def flip_square(sq):
    return sq^0x38





def evaluatePos(self):

        # We need to evaluate the current position for white, and then the current position for black

    white_total = 0
    black_total = 0
    for sq in range(64):

        found_piece = self.piece_at(sq)
        if found_piece is None:
            continue
        #Otherwise we have found a piece
        piece_repr = found_piece.__str__().upper()
        if found_piece.color:
            # This is a white piece
            bpiece = flip_square(sq)
                #print(piece_repr, pst[piece_repr][bpiece])
            white_total += piece[piece_repr]+pst[piece_repr][bpiece]
        else:
            #bpiece = flip_square(sq)
            black_total += piece[piece_repr]+pst[piece_repr][sq]
    return white_total-black_total

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



def minimaxBasic(depth, maxWhite):
    global MAINBOARD
    if depth==1 or not MAINBOARD.legal_moves:

        final_score = stockfishEval(MAINBOARD)
        tpcache[MAINBOARD.epd()] = final_score
        return final_score

    #Then we need to check for each legal move, we need to calculate the best and worst scores for that move
    best_score = -1e8 if maxWhite else 1e8
    for new_move in MAINBOARD.legal_moves:

        #Check if we can go down here
        MAINBOARD.push(new_move)

        got = tpcache.get(MAINBOARD.epd(), None)

        if got is None:

            pot_score = minimaxBasic(depth-1, ~maxWhite)
        else:
            pot_score = got
        MAINBOARD.pop()
        try:
            if maxWhite:
                #Then we're trying to find the best move for white
                if pot_score > best_score:
                    best_score = pot_score
            else:
                if pot_score < best_score:
                    best_score = pot_score
        except Exception as e:
            print(e, pot_score, best_score)
            print(MAINBOARD)
            input()
    tpcache[MAINBOARD.epd()] = best_score
    return best_score

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


MAINBOARD.set_fen("r3r1k1/ppp2ppp/5P1n/3p4/1n1P4/2NP1Nq1/PP3P2/R1B2RK1 w - - 3 19")
print(MAINBOARD)

while True:
    #get_basic_move()
    get_advanced_move()
    print(MAINBOARD)
    print(MAINBOARD.fen())
    new_move = input("ENTER MOVE: ")
    MAINBOARD.push_san(new_move)






