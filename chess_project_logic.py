converted = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
reverted = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
def convert(num1,num2):
    # converts numerical coordinates to chess notation i.e. (5,5) -> 'E5'
    return converted[num1] + str(num2)
    
# converts chess notation to two-element list of numerical coordinates for easier access
def cart_list(coords):
    return [reverted[coords[0]], int(coords[1])]

class Player:
    def __init__(self, color, board):
        # assigns player to GameBoard
        self.held = None
        self.color, self.board = color, board
        self.pieces, self.captured = [], []

        # being in check will limit the player's moves
        self.in_check = False

            # attributes for castling
        self.king_moved, self.left_rook_moved, self.right_rook_moved = False, False, False

    def move(self, start, end):
        if self.board.game_over:
            return

        # Moves a piece from start position to end position if the move is legal.
        chessboard = self.board.squares
        piece = chessboard[start]

        # Check if player has a piece on the selected square
        if self.board.turn == self and piece and (piece.color == self.color):
            if type(piece) == King and GameBoard.check_castle(self.board, self, start, end):

                if self.color == 'white':
                    row_num = str(1)
                if self.color == 'black':
                    row_num = str(8)

                # move king
                chessboard[end] = chessboard[start]
                chessboard[start] = None
                piece.coords = end

                if 'c' in end:
                    rook_start, rook_end = 'a' + row_num, 'd' + row_num
                    chessboard['d' + row_num] = chessboard['a' + row_num]
                    chessboard['a' + row_num] = None

                if 'g' in end:
                    rook_start, rook_end = 'h' + row_num, 'f' + row_num
                    chessboard['f' + row_num] = chessboard['h' + row_num]
                    chessboard['h' + row_num] = None

                print(f"{self.color} moved king from {start} to {end}")
                print(f"{self.color} moved rook from {rook_start} to {rook_end}")

                self.board.turn = self.opp
                self.held = None
                return 'Castle'

                # Check if piece is able to move to destination

            if end in piece.possible_moves():
                # Update board s.t. piece moves
                current_state = chessboard.copy()
                current_list1 = self.pieces[:]
                current_list2 = self.opp.pieces[:]

                new_piece = type(piece)(end, piece.player)

                if type(piece) == King:
                    self.king = new_piece

                if chessboard[end]:
                    self.opp.pieces.remove(chessboard[end])
                chessboard[end] = new_piece
                chessboard[start] = None


                self.pieces.remove(piece)

                # Check if moving piece will result in a self-check
                if GameBoard.check_check(self, self.king.coords):
                    self.board.squares = current_state
                    self.pieces = current_list1
                    self.opp.pieces = current_list2

                    if type(new_piece) == King:
                        self.king = piece
                    return

                print(f"{self.color} moved {chessboard[end]} from {start} to {end}")
                self.board.turn = self.opp
                self.in_check = False
                self.held = None

                # if piece is king or rook, change player's attributes s.t. we know the piece has been moved (for castling)
                if type(piece) == King:
                    piece.player.king_moved = True

                if type(piece) == Rook:
                    if start[0] == 'a':
                        piece.player.left_rook_moved = True
                    if start[0] == 'h':
                        piece.player.right_rook_moved = True

                  # Check if moving piece checks opponent
                if GameBoard.check_check(self.opp, self.opp.king.coords):
                    self.opp.in_check = True
                    if GameBoard.check_mate(self.opp):
                        print('checkmate')
                        return 'Checkmate'
                        self.board.game_over = True
                    else:
                        print('check')
                        return 'Check'

                # Check if moving piece results in stalemate i.e. opponent cannot move any pieces
                if GameBoard.check_stale(self.opp):
                    print('stalemate')
                    return 'Stalemate'
                    self.board.game_over = True

        return

class GameBoard:
    def __init__(self):
        self.game_over = False
     # Sets up the board and pieces for a new game.
        # Creates a dictionary to store squares with two attributes: numerical coordinates and pieces. 
        self.squares = {}
        for x in range(1, 9):
            for y in range(1, 9):
                self.squares[converted[x] + str(y)] =  None
        # Initializes two Player instances. 
        self.white, self.black = Player("white", self), Player("black", self)
        self.white.opp, self.black.opp = self.black, self.white
        self.turn = self.white
        # Places pieces. 
        def setup(s, player):
            if "7" in s or "2" in s:
                self.squares[s] = Pawn(s, player)
            elif "b" in s or "g" in s:
                self.squares[s] = Knight(s, player)
            elif "c" in s or "f" in s:
                self.squares[s] = Bishop(s, player)
            elif "a" in s or "h" in s:
                self.squares[s] = Rook(s, player)
            elif "d" in s:
                self.squares[s] = Queen(s, player)
            elif "e" in s:
                self.squares[s] = King(s, player)
                player.king = self.squares[s]
                
        for s in self.squares:
            if s[1] == "1" or s[1] == "2":
                setup(s, self.white)
            if s[1] == "7" or s[1] == "8":
                setup(s, self.black)
                
    def check_castle(self, player, start, end):
        """
        >>> b=GameBoard()
        >>> white,black=b.white,b.black
        >>> white.move('e2','e3')
        white moved pawn from e2 to e3
        >>> black.move('e7','e6')
        black moved pawn from e7 to e6
        >>> white.move('f1','d3')
        white moved bishop from f1 to d3
        >>> black.move('f8','d6')
        black moved bishop from f8 to d6
        >>> white.move('g1','f3')
        white moved knight from g1 to f3
        >>> black.move('g8','f6')
        black moved knight from g8 to f6
        >>> white.move('e1','g1')
        white moved king from e1 to g1
        white moved rook from h1 to f1
        'Castle'
        """
        
        if player.color == 'white': 
            row_num = str(1)
        if player.color == 'black':
            row_num = str(8)

        # check if our move from start to end is a castle 
        if self.squares[start] == player.king: 
            
            # king cannot have been moved; player cannot be in check 
            if not player.king_moved and not player.in_check: 
                
                if 'c' in end and not player.left_rook_moved: 
                    if not (self.squares['b' + row_num] or self.squares['c' + row_num] or self.squares['d' + row_num]):
                        return True 
                elif 'g' in end and not player.right_rook_moved: 
                    if not (self.squares['f' + row_num] or self.squares['g' + row_num]):
                        return True 
        return 
    
    def check_check(player, king_coords):
        # Check if the specified player is in check
        for i in player.opp.pieces: 
            # iterate through opponent's pieces to check if any can 'capture' player's king
            lst_moves = i.possible_moves() 
            if type(i) == Pawn: 
                
                x1, y1 = i.cart[0], i.cart[1]
                if i.color == 'white':
                    y2 = y1 + 1
                if i.color == 'black':
                    y2 = y1 - 1
                capture_moves = [convert(x, y2) for x in [x1+1,x1-1] if x in range(1, 9)] 
                lst_moves.extend(capture_moves) 
            
            if lst_moves and king_coords in lst_moves:
                return True 
        return False 
        
        
    def king_stuck(player, piece):
        # determine how many moves the king has (i.e. w/out going in check)
        # if king_stuck returns 0 then king is stuck on its square 
        # subfunction for check_mate, check_stale 
        
        saved_moves = piece.possible_moves() 
        saved_count = len(saved_moves)
        saved_coords = piece.coords
        king_coords = player.king.coords
                
        # iterate through king's available moves and test if they put king in check
        for move in saved_moves: 
            
            # move king
            capture = False 
            if player.board.squares[move]: 
                saved_capture = player.board.squares[move]
                capture = True 
                        
            player.board.squares[saved_coords] = None 
            player.board.squares[move] = piece
            
            # in check? 
            if GameBoard.check_check(player, move): 
                saved_count -= 1
            
            # reset 
            player.board.squares[saved_coords] = piece 
            player.board.squares[move] = None 
                    
            if capture:
                player.board.squares[move] = saved_capture 
                        
        return saved_count 
        
    def check_stale(player):
        """
        >>> b=GameBoard()
        >>> white,black=b.white,b.black
        >>> white.move('e2','e3')
        white moved pawn from e2 to e3
        >>> black.move('a7','a5')
        black moved pawn from a7 to a5
        >>> white.move('d1','h5')
        white moved queen from d1 to h5
        >>> black.move('a8','a6')
        black moved rook from a8 to a6
        >>> white.move('h5','a5')
        white moved queen from h5 to a5
        >>> black.move('h7','h5')
        black moved pawn from h7 to h5
        >>> white.move('h2','h4')
        white moved pawn from h2 to h4
        >>> black.move('a6','h6')
        black moved rook from a6 to h6
        >>> white.move('a5','c7')
        white moved queen from a5 to c7
        >>> black.move('f7','f6')
        black moved pawn from f7 to f6
        >>> white.move('c7','d7')
        white moved queen from c7 to d7
        check
        'Check'
        >>> black.move('e8','f7')
        black moved king from e8 to f7
        >>> white.move('d7','b7')
        white moved queen from d7 to b7
        >>> black.move('d8','d3')
        black moved queen from d8 to d3
        >>> white.move('b7','b8')
        white moved queen from b7 to b8
        >>> black.move('d3','h7')
        black moved queen from d3 to h7
        >>> white.move('b8','c8')
        white moved queen from b8 to c8
        >>> black.move('f7','g6')
        black moved king from f7 to g6
        >>> white.move('c8','e6')
        white moved queen from c8 to e6
        stalemate
        'Stalemate'
        """
        
    # Check if the player is in a stalemate.
    
        # if king in check, not a stalemate 
        if GameBoard.check_check(player, player.king.coords):
            return False 
        king_len = len(player.king.possible_moves())
        
        # Check if all of king's possible moves result in check 
        if player.king.possible_moves(): 
            king_len = GameBoard.king_stuck(player, player.king)

        if king_len == 0: 
            
            saved_pieces = len(player.pieces) - 1
            king_removed = player.pieces[:]
            king_removed.remove(player.king)
            
            # iterate through player's other pieces
            for piece in king_removed: 
                saved_moves = piece.possible_moves() 
                saved_count = len(saved_moves)
                saved_coords = piece.coords

                # similar logic as king_stuck
                # determine whether moving a piece to a square will put the king in check 
                for move in saved_moves: 
                    
                    # move piece 
                    capture = False 
                    if player.board.squares[move]: 
                        saved_capture = player.board.squares[move]
                        capture = True 
                        
                    player.board.squares[saved_coords] = None 
                    player.board.squares[move] = piece
                    
                    # king in check? 
                    if GameBoard.check_check(player, player.king.coords): 
                        saved_count -= 1

                    # reset 
                    player.board.squares[saved_coords] = piece 
                    player.board.squares[move] = None 
                    
                    if capture:
                        player.board.squares[move] = saved_capture 
                        
                        
                if saved_count <= 0:
                    saved_pieces -= 1
            
            # if no pieces can be moved (w/out putting the king in check), there is a stalemate 
            if saved_pieces == 0:
                return True 
                        
        return False 
    
    def check_mate(player):
        """
        >>> b=GameBoard()
        >>> white,black=b.white,b.black
        >>> white.move('e2','e4')
        white moved pawn from e2 to e4
        >>> black.move('e7','e5')
        black moved pawn from e7 to e5
        >>> white.move('d1','h5')
        white moved queen from d1 to h5
        >>> black.move('b8','c6')
        black moved knight from b8 to c6
        >>> white.move('f1','c4')
        white moved bishop from f1 to c4
        >>> black.move('g8','f6')
        black moved knight from g8 to f6
        >>> white.move('h5','f7')
        white moved queen from h5 to f7
        checkmate
        'Checkmate'
        """
    # Check if the player is in checkmate.
        king_coords = player.king.coords
        
        # if king not in check, not a checkmate 
        if not GameBoard.check_check(player, king_coords):
            return False 
        
        # check if king can move out of check 
        if player.king.possible_moves(): 
            king_len = GameBoard.king_stuck(player, player.king) 
                
            if king_len == 0:
                saved_pieces = len(player.pieces) - 1
                king_removed = player.pieces[:]
                king_removed.remove(player.king)
                 
                # iterate through player's other pieces 
                for piece in king_removed: 
                    saved_moves = piece.possible_moves() 
                    saved_coords = piece.coords
                
                    for move in saved_moves: 
                        
                        # move 
                        capture = False 
                        if player.board.squares[move]: 
                            saved_capture = player.board.squares[move]
                            capture = True 
                        
                        player.board.squares[saved_coords] = None 
                        player.board.squares[move] = piece
                    
                        # if a piece can move to block the check, not in checkmate 
                        if not GameBoard.check_check(player, king_coords): 
                            return False 

                        player.board.squares[saved_coords] = piece 
                        player.board.squares[move] = None 
                        
                return True  
        
        return False

class Piece:
    def __init__(self, coords, player):
        self.player = player
        self.player.pieces.append(self)

        # to shorten code
        self.color = self.player.color
        self.board = self.player.board.squares

        # position
        self.coords = coords
        self.cart = cart_list(coords)

    # function to verify that piece is not capturing a piece of its own color
    # input: numerical coords in list of 2 elems; output: boolean
    def not_capture_self(self, coords):
        coords = convert(coords[0], coords[1])
        if (not self.board[coords]) or self.board[coords].color != self.color:
            return True

            # function to verify that piece does not move off board

    # input: numerical coords in list of 2 elems; output: boolean
    def on_board(coords):
        if [n for n in coords if n < 1 or n > 8]:
            return False
        return True


class Pawn(Piece):
    def __repr__(self):
        return 'pawn'

    def possible_moves(self):
        # returns a list of squares that the piece could move to, not accounting for checks.
        lst = []

        # x1, y1 are initial x,y positions
        x1, y1 = self.cart[0], self.cart[1]
        if y1 in [1, 8]:
            return lst

        # white and black pawns move in opposite directions. normally pawns move one square 'forward' ( = y2)
        if self.color == 'white':
            y2 = y1 + 1
            # pawns in initial position can move forward 2 spaces (but no capturing or jumping over pieces)
            if y1 == 2 and not self.board[convert(x1, y2)] and not self.board[convert(x1, 4)]:
                lst.append(convert(x1, 4))

        # same logic as above but for black color
        elif self.color == 'black':
            y2 = y1 - 1
            if y1 == 7 and not self.board[convert(x1, y2)] and not self.board[convert(x1, 5)]:
                lst.append(convert(x1, 5))

        # can move one square forward and diagonally but only for captures.
        captures = [convert(x, y2) for x in [x1 + 1, x1 - 1] if
                    x in range(1, 9) and self.board[convert(x, y2)] and self.color != self.board[convert(x, y2)].color]
        if captures:
            lst.extend(captures)

        # move one square forward
        if not self.board[convert(x1, y2)]:
            lst.append(convert(x1, y2))

        return lst

    def promote(self, type):
        # pawn must be on the opposite edge of the board. self.cart[1] is y-position
        def promotable():
            if self.color == 'white' and self.cart[1] == 8:
                return True
            if self.color == 'black' and self.cart[1] == 1:
                return True
            return

        if promotable():
            print(f'Promoted to {type}')
            # switches the pawn out for a piece of the specified type
            self.board[self.coords] = type(self.coords, self.player)


class Knight(Piece):
    def __repr__(self):
        return 'knight'

    def possible_moves(self):
        lst = []

        # helper function for "L" pattern
        def make_range(n, i):
            return [n + i, n - i]

        x1, y1 = self.cart[0], self.cart[1]

        # move two squares horizontally then one square vertically
        for x2 in make_range(x1, 2):
            for y2 in make_range(y1, 1):
                if Piece.on_board([x2, y2]) and self.not_capture_self([x2, y2]):
                    lst.append(convert(x2, y2))

        # move two squares vertically then one square horizontally
        for y2 in make_range(y1, 2):
            for x2 in make_range(x1, 1):
                if Piece.on_board([x2, y2]) and self.not_capture_self([x2, y2]):
                    lst.append(convert(x2, y2))

        return lst


class Bishop(Piece):
    def __repr__(self):
        return 'bishop'

    def possible_moves(self):

        lst = []
        x1, y1 = self.cart[0], self.cart[1]

        # check all diagonals up until a diagonal is blocked by a piece or we go off the board
        def not_blocked(coords):
            if Piece.on_board(coords) and self.not_capture_self(coords) and not capture_stop:
                return True

                # up and right

        x2, y2 = x1 + 1, y1 + 1
        capture_stop = False
        while not_blocked([x2, y2]):
            lst.append(convert(x2, y2))
            if self.board[convert(x2, y2)]:
                capture_stop = True
            x2 += 1
            y2 += 1

            # up and left
        x2, y2 = x1 - 1, y1 + 1
        capture_stop = False
        while not_blocked([x2, y2]):
            lst.append(convert(x2, y2))
            if self.board[convert(x2, y2)]:
                capture_stop = True
            x2 -= 1
            y2 += 1

            # down and right
        x2, y2 = x1 + 1, y1 - 1
        capture_stop = False
        while not_blocked([x2, y2]):
            lst.append(convert(x2, y2))
            if self.board[convert(x2, y2)]:
                capture_stop = True
            x2 += 1
            y2 -= 1

            # down and left
        x2, y2 = x1 - 1, y1 - 1
        capture_stop = False
        while not_blocked([x2, y2]):
            lst.append(convert(x2, y2))
            if self.board[convert(x2, y2)]:
                capture_stop = True
            x2 -= 1
            y2 -= 1
        return lst


class Rook(Piece):
    def __repr__(self):
        return 'rook'

    def possible_moves(self):
        lst = []
        x1, y1 = self.cart[0], self.cart[1]

        # check all vertical/horizontal moves up until a row/column is blocked by a piece or we go off the board
        def not_blocked(coords):
            if Piece.on_board(coords) and self.not_capture_self(coords) and not capture_stop:
                return True

                # up

        y2 = y1 + 1
        capture_stop = False
        while not_blocked([x1, y2]):
            lst.append(convert(x1, y2))
            if self.board[convert(x1, y2)]:
                capture_stop = True
            y2 += 1

            # down
        y2 = y1 - 1
        capture_stop = False
        while not_blocked([x1, y2]):
            lst.append(convert(x1, y2))
            if self.board[convert(x1, y2)]:
                capture_stop = True
            y2 -= 1

            # left
        x2 = x1 - 1
        capture_stop = False
        while not_blocked([x2, y1]):
            lst.append(convert(x2, y1))
            if self.board[convert(x2, y1)]:
                capture_stop = True
            x2 -= 1

        # right
        x2 = x1 + 1
        capture_stop = False
        while not_blocked([x2, y1]):
            lst.append(convert(x2, y1))
            if self.board[convert(x2, y1)]:
                capture_stop = True
            x2 += 1

        return lst


class Queen(Piece):
    def __repr__(self):
        return 'queen'

    # queen can move wherever a bishop or rook could move
    def possible_moves(self):
        return Bishop.possible_moves(self) + Rook.possible_moves(self)


class King(Piece):
    def __init__(self, coords, player):
        super().__init__(coords, player)
        self.player.king = self

    def __repr__(self):
        return 'king'

    def possible_moves(self):
        x, y = self.cart[0], self.cart[1]
        lst1 = [[x + 1, y + 1], [x + 1, y], [x + 1, y - 1], [x, y + 1], [x, y - 1], [x - 1, y + 1], [x - 1, y],
                [x - 1, y - 1]]
        lst2 = []

        for coords in lst1:
            if Piece.on_board(coords) and self.not_capture_self(coords):
                lst2.append(convert(coords[0], coords[1]))

        return lst2