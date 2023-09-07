# check castle
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
        """

# check checks, stalemate
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
        """

#check checkmate
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
        """