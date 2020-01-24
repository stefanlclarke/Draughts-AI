import numpy as np

#Parameters
board_size = 6

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
        self.moving = 1
        
    def makemove(self, piece, number, player):
        board, nextmove = move(self.board, piece, number, player)
        self.board = board
        self.moving = nextmove
        
        
game = board(board_size)

def isinboard(board, space):
    boarddim = len(board[0])
    if space[0] >= boarddim or space[0] < 0 or space[1] >= boarddim or space[1] < 0:
        return False
    else:
        return True
    
        
def ismovelegal(board, tile, direction, player):
    if abs(board[tile[0], tile[1]]) == 2:
        king = True
    else:
        king = False
    movespace = tile + direction
    takespace = tile + 2*direction
    if isinboard(board, tile) == False:
        print("Tile not in board")
        return False
    if isinboard(board, movespace) == False:
        print("Move not in board")
        return False
    if player == -1:
        if king == False and direction[0] == 1:
            print("Backwards move attempted")
            return False
        
        if board[tile[0], tile[1]] != -1 and board[tile[0], tile[1]] != -2:
            print("Piece not selected")
            return False
        else:
            if board[movespace[0], movespace[1]] == 0:
                return True
            elif board[movespace[0], movespace[1]] == 1 or board[movespace[0], movespace[1]] == 2:
                if isinboard(board, takespace) == False:
                    print("Illegal movement attempted")
                    return False
                elif board[takespace[0], takespace[1]] == 0:
                    return True
                else:
                    print("Illegal movement attempted")
                    return False
            
            pass
    elif player == 1:
        if king == False and direction[0] == -1:
            print("Backwards move attempted")
            return False
        
        if board[tile[0], tile[1]] != 1 and board[tile[0], tile[1]] != 2:
            print("Piece not selected")
            return False
        else:
            if board[movespace[0], movespace[1]] == 0:
                return True
            elif board[movespace[0], movespace[1]] == -1 or board[movespace[0], movespace[1]] == -2:
                if isinboard(board, takespace) == False:
                    print("Illegal movement attempted")
                    return False
                elif board[takespace[0], takespace[1]] == 0:
                    return True
                else:
                    print("Illegal movement attempted")
                    return False
                
def move(board1, piece, number, player):
    board = board1.copy()
    counter = board[piece[0], piece[1]]
    if number == 1:
        move = np.array([-1, -1])
    elif number == 2:
        move = np.array([-1, 1])
    elif number == 3:
        move = np.array([1,1])
    elif number == 4:
        move = np.array([1, -1])
    else:
        print("ILLEGAL MOVE")
        return (board, player)
    legal = ismovelegal(board, piece, move, player)
    if legal == False:
        print("ILLEGAL MOVE")
        return (board, player)
    else:
        moveloc = piece + move
        takeloc = piece + 2*move
        if board[moveloc[0], moveloc[1]] != 0:
            board[piece[0], piece[1]] = 0
            board[moveloc[0], moveloc[1]] = 0
            board[takeloc[0], takeloc[1]] = counter
            return (board, player)
        else:
            board[piece[0], piece[1]] = 0
            board[moveloc[0], moveloc[1]] = counter
            return(board, -player)
            

        
