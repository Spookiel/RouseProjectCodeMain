

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


def stockfishEval(board):
        global mainEngine
        info = mainEngine.analyse(board, chess.engine.Limit(depth=0))
        return info["score"]

class myBoard(chess.Board):

    def __init__(self):
        super().__init__()
        self.cache = {}
        self.ai_col = 0 #Assumes the AI is white


    def clear_cache(self):
        self.cache = {}
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
        # Negative score means that black is better, otherwise white is better



    def minimax(self, depth, maxWhite):
        if depth==0 or not self.legal_moves:
            self.cache[self.epd()] =  self.evaluatePos()
            return self.cache[self.epd()]


        best = -1e8 if maxWhite else 1e8

        for move in self.legal_moves:
            self.push(move)

            possible_score  = self.minimax(depth-1, ~maxWhite)
            self.cache[self.epd()] = possible_score

            if maxWhite:
                best = max(best, possible_score)
            else:
                best = min(best, possible_score)

            self.pop()

        self.cache[self.epd()] = best

        return best

    def minimaxab(self, depth, maxWhite,alpha,beta):
        global calls,hits
        calls += 1
        brepr = self.epd()
        if self.cache.get(brepr, None):
            hits += 1
            return self.cache[brepr]
        if depth==0 or not self.legal_moves:
            self.cache[brepr] =  self.evaluatePos()
            return self.cache[brepr]
            #return self.evaluatePos()

        best = -1e8 if maxWhite else 1e8


        for move in self.legal_moves:
            self.push(move)

            possible_score  = self.minimaxab(depth-1, ~maxWhite, alpha, beta)
            self.cache[self.epd()] = possible_score

            if maxWhite:
                best = max(best, possible_score)
                alpha = max(alpha, best)
            else:
                best = min(best, possible_score)
                beta = min(beta, best)

            self.pop()
            if beta <= alpha:
                break

            # Trying to implement fail hard
            """
            if maxWhite:
                if best >= beta:
                    return beta
            else:
                if best <= alpha:
                    return alpha"""

        self.cache[self.epd()] = best

        return best


    def hash_board(self):
        pass
        return self.epd()

    def basic_ai_turn(self, timelimit):
        #This AI will use iterative deepening to find the best states
        return 1


    def minimaxtest(self):

        #This test will look 1 and 2 moves ahead and assumes the AI is playing as black

        glob_score = -1e8
        bmove = None
        for cur_move in self.legal_moves:
            self.push(cur_move)

            loc_score = self.minimax(3,1-self.ai_col)
            print(cur_move, loc_score)
            if loc_score > glob_score:
                glob_score = loc_score
                bmove = cur_move
            self.pop()

        print("CHOSEN MOVE", bmove)

        self.push(bmove)

    def minimaxabtest(self):

        #This test will look 1 and 2 moves ahead and assumes the AI is playing as black
        alpha = -1e8
        beta = 1e8
        glob_score = -1e8 if not self.ai_col else 1e8
       # print(moveOrder)
        bmove = None
        for cur_move in self.legal_moves:
            self.push(cur_move)
            #print(len(list(self.legal_moves)), "CUR MOVES CACHED", len(self.cache))
            depth = 5 #if self.ply() < 16 else 4
            loc_score = self.minimaxab(depth,1-self.ai_col, alpha, beta)
            print(cur_move, loc_score, glob_score)
            if not self.ai_col and loc_score > glob_score:
                glob_score = loc_score
                bmove = cur_move
            if self.ai_col and loc_score < glob_score:
                glob_score = loc_score
                bmove = cur_move
            self.pop()

        print("CHOSEN MOVE", bmove)

        self.push(bmove)



    #The AI will use iterative deepening to ensure that states are considered in a bfs manner
    # Because due to turn time limits, the AI will only be able to consider up to a certain depth

#chess.STARTING_FEN = "rn1qkbnr/pp1bpppp/8/1B4N1/8/4p3/PPPP1PPP/R1BQK2R w KQkq - 1 7"
tBoard = myBoard()
tBoard.reset_board()
#tBoard.set_fen("r1b1k2r/pppp1p2/2n3pp/1Bb1p3/8/5q2/PPPP2PP/RNB1K1NR w kq - 0 11")
#tBoard.push_san("e4")
#print(stockfishEval(tBoard))

print(tBoard)
while True:

    tBoard.minimaxabtest()
    print(tBoard)
    myMove = input("ENTER MOVE: ")
    tBoard.push_san(myMove)
    print()
    print(tBoard)
    print("CALLS MADE", calls, "WITH", len(tBoard.cache), "STORED AND HITS: ", hits)