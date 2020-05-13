import numpy as np
import random

def startingpos(board):
    boardnew = board.copy()
    black1 = board[0].copy()
    black2 = board[0].copy()
    white1 = board[0].copy()
    white2 = board[0].copy()
    for i in range(len(black1)//2):
        black1[2*i] = 1
        black2[2*i+1] = 1
        white1[2*i] = -1
        white2[2*i+1] = -1
    if len(board[0]) % 2 == 1:
        boardnew[-1] = white1
        boardnew[-2] = white2
    else:
        boardnew[-1] = white2
        boardnew[-2] = white1
    boardnew[0] = black1
    boardnew[1] = black2
    return boardnew

class board(object):
    def __init__(self, board_size):
        self.board_size = board_size
        self.blankboard = np.zeros([self.board_size, self.board_size])
        self.board = startingpos(np.zeros([self.board_size, self.board_size]))
        self.player = -1

    def makemove(self, piece, number):
        board, nextmove = move(self.board, piece, number, self.player)
        print("MOVING NEXT:", nextmove)
        board = checkforking(board)
        self.board = board
        self.player = nextmove
        victor = checkwin(self.board)
        stalemate = checkstalemate(self.board, self.player)
        return victor, stalemate

    def reset(self):
        self.board = startingpos(np.zeros([self.board_size, self.board_size]))
        self.player=-1


#game = board(board_size)

def isinboard(board, space):
    boarddim = len(board[0])
    if space[0] >= boarddim or space[0] < 0 or space[1] >= boarddim or space[1] < 0:
        return False
    else:
        return True


def ismovelegal(board, tile, direction, player):
    b = sum(sum(np.isin(board,3))) + sum(sum(np.isin(board,-3))) + sum(sum(np.isin(board,4))) + sum(sum(np.isin(board,-4)))
    if b != 0:
        mid_hop=True
        if abs(board[tile[0], tile[1]]) == 1 or abs(board[tile[0], tile[1]]) == 2:
            return False
    if abs(board[tile[0], tile[1]]) == 2 or abs(board[tile[0], tile[1]])==4:
        king = True
    else:
        king = False
    movespace = tile + direction
    takespace = tile + 2*direction
    if mid_hop==True:
        if board[movespace[0],movespace[1]]==0:
            return False
    if isinboard(board, tile) == False:
        #print("Tile not in board")
        return False
    if isinboard(board, movespace) == False:
        #print("Move not in board")
        return False
    if player == -1:
        if king == False and direction[0] == 1:
            #print("Backwards move attempted")
            return False

        if board[tile[0], tile[1]] != -1 and board[tile[0], tile[1]] != -2 and board[tile[0], tile[1]] != -3 and board[tile[0], tile[1]] != -4:
            #print("Piece not selected")
            return False
        else:
            if board[movespace[0], movespace[1]] == 0:
                return True
            elif board[movespace[0], movespace[1]] == 1 or board[movespace[0], movespace[1]] == 2:
                if isinboard(board, takespace) == False:
                    #print("Illegal movement attempted")
                    return False
                elif board[takespace[0], takespace[1]] == 0:
                    return True
                else:
                    #print("Illegal movement attempted")
                    return False

            pass
    elif player == 1:
        if king == False and direction[0] == -1:
            #print("Backwards move attempted")
            return False

        if board[tile[0], tile[1]] != 1 and board[tile[0], tile[1]] != 2 and board[tile[0], tile[1]] != 3 and board[tile[0], tile[1]] != 4:
           # print("Piece not selected")
            return False
        else:
            if board[movespace[0], movespace[1]] == 0:
                return True
            elif board[movespace[0], movespace[1]] == -1 or board[movespace[0], movespace[1]] == -2:
                if isinboard(board, takespace) == False:
                    #print("Hop not in board")
                    return False
                elif board[takespace[0], takespace[1]] == 0:
                    return True
                else:
                    #print("Illegal movement attempted")
                    return False

def get_legal_moves(board,player):
    moves = [np.array([-1,-1]), np.array([-1,1]), np.array([1,1]), np.array([1,-1])]
    n = len(board)
    moves_considered = []
    for i in range(n):
        for j in range(n):
            for d in [0,1,2,3]:
                if ismovelegal(board, np.array([i,j]) ,  moves[d], player):
                    moves_considered.append( ( (i,j),d) )
    return moves_considered

def get_random_move(board,player):
    moves_considered = get_legal_moves(board,  player)
    n = len(moves_considered)
    if n>0:
        return moves_considered[random.randint(0,n-1) ]
    else:
        return 0

##
def move(board1, piece, number, player):
    board = board1
    counter = board[piece[0], piece[1]]
    if counter == 3:
        counter = 1
    elif counter == 4:
        counter = 2
    elif counter == -3:
        counter = -1
    elif counter == -4:
        counter = -2
    #print(counter)

    if number == 0:
        move = np.array([-1, -1])
    elif number == 1:
        move = np.array([-1, 1])
    elif number == 2:
        move = np.array([1,1])
    elif number == 3:
        move = np.array([1, -1])
    else:
        #print("ILLEGAL MOVE")
        return (board, player)
    legal = ismovelegal(board, piece, move, player)
    if legal == False:
        #print("ILLEGAL MOVE")
        return (board, player)

    if abs(counter)==1.0 or abs(counter)==3.0:
        takecounter = 3*player
    elif abs(counter)==2.0 or abs(counter)==4.0:
        takecounter = 4*player

    moveloc = piece + move
    takeloc = piece + 2*move
    if board[moveloc[0], moveloc[1]] != 0:
        board[piece[0], piece[1]] = 0
        board[moveloc[0], moveloc[1]] = 0
        board[takeloc[0], takeloc[1]] = takecounter
        more_hops = check_further_moves(board, takeloc, player)
        #print("MORE HOPS:", more_hops)
        if len(more_hops)==0:
            #print("no more hops")
            board[takeloc[0], takeloc[1]] = counter
            return (board, -player)
        else:
            return (board, player)
    else:
        board[piece[0], piece[1]] = 0
        board[moveloc[0], moveloc[1]] = counter

        return(board, -player)

def checkforking(board):
    kings1 = [i for i,x in enumerate(board[-1]) if x == 1]
    kings_1 = [i for i,x in enumerate(board[0]) if x == -1]
    for i,x in enumerate(kings1):
        board[-1][x] = 2
    for i,x in enumerate(kings_1):
        board[0][x]=-2
    return board

def check_further_moves(board, piece, player):
    moves = [np.array([-1,-1]), np.array([-1,1]), np.array([1,1]), np.array([1,-1])]
    #print(piece)
    #print(abs(board[piece[0], piece[1]]))
    if abs(board[piece[0], piece[1]])==1 or abs(board[piece[0], piece[1]])==3:
        if player == -1:
            a=0
            b=2
        else:
            a=2
            b=4
    else:
        a=0
        b=4
    movespaces = [(moves[i], piece+moves[i]) for i in range(a,b)]
    #print("MOVESPACES:", movespaces)
    #for x in movespaces:
        #print(x[0], x[1], ismovelegal(board, piece, x[0], player))
    available_hops = [i for i,x in enumerate(movespaces) if ismovelegal(board, piece, x[0], player) and board[x[1][0], x[1][1]]==-player]
    #print("AVAILABLE HOPS:", available_hops)
    return available_hops

def checkwin(board):
    piecesp = board.copy()
    piecesm = board.copy()
    piecesp[piecesp<0]=0
    piecesm[piecesm>0]=0
    #print(piecesp)
    #print(piecesm)
    mwin = sum(sum(piecesp))
    pwin = sum(sum(piecesm))
    if mwin == 0:
        print("VICTORY!")
        return -1
    elif pwin == 0:
        print("VICTORY!")
        return 1
    else:
        return 0

def checkstalemate(board, player):
    moves = [np.array([-1,-1]), np.array([-1,1]), np.array([1,1]), np.array([1,-1])]
    print("Player:", player)
    pieces = np.argwhere(player*board > 0)
    #print(pieces)
    for piece in pieces:
        for move in moves:
            #print(piece, move, player, ismovelegal(board, piece, move, player))
            if ismovelegal(board, piece, move , player):
                return False
    return True
