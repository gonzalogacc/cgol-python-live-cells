from cwgol import Cell, Board, Simulation


def test_cell_sorting():
    cells = [
        Cell(x=1, y=1),
        Cell(x=1, y=2),
        Cell(x=11, y=1),
        Cell(x=2, y=1)
    ]

    # # Sort to correct order
    cells.sort()

    assert cells[0].y == 1
    assert cells[1].y == 2

def test_cell_in_dict():
    cells = [
        Cell(x=1, y=1),
        Cell(x=1, y=2),
        Cell(x=11, y=1),
        Cell(x=2, y=1),
        Cell(x=11, y=1), #dup
    ]

    cell_dict = {cell: i for i, cell in enumerate(cells)}

    # Cell
    assert len(cell_dict) == 4
    assert cell_dict[cells[-1]] == 4

def test_board():
    cells = [
        Cell(x=5, y=2),
        Cell(x=5, y=2), #dup
        Cell(x=1, y=1),
        Cell(x=1, y=2),
        Cell(x=2, y=3),
        Cell(x=4, y=2),
    ]
    board_size = 5
    board = Board(board_size)
    assert board.size == board_size

    board.from_cells(cells)
    assert len(board._board) == len(cells) - 1
    for cell in cells:
        assert cell in board._board

def test_cell_neighbours():
    """
      0 1 2 3 4 5 6
    0 . . . . . . .
    1 . X . . . . .
    2 . . N N N . .
    3 . . N C N . .
    4 . . N N N . .
    5 . . . . . . .
    6 . . . . . . .
    """
    cells = [
        Cell(x=2, y=2),  # top-left
        Cell(x=3, y=2),  # top
        Cell(x=4, y=2),  # top-right
        Cell(x=2, y=3),  # left
        Cell(x=4, y=3),  # right
        Cell(x=2, y=4),  # bottom-left
        Cell(x=3, y=4),  # bottom
        Cell(x=4, y=4),  # bottom-right
        Cell(x=1, y=1),  # bottom-right
    ]

    central = Cell(x=3, y=3)
    nn = central.neighbours(5)
    assert set(nn).issubset(cells)
    assert cells[-1] not in set(nn)

def test_top_left_cell_neighbours():
    """
      0 1 2 3 4
    0 C N . . .
    1 N N . . .
    2 X . . . . <- non neighbour
    3 . . . . .
    4 . . . . .
    """
    cells = [
        Cell(x=1, y=0),  # right
        Cell(x=0, y=1),  # bottom
        Cell(x=1, y=1),  # bottom-right
        Cell(x=2, y=0), # Non neighbour
    ]

    central = Cell(x=0, y=0)
    nn = central.neighbours(5)
    assert set(nn).issubset(cells)
    assert cells[-1] not in set(nn)

def test_middle_right_cell_neighbours():
    """
      0 1 2 3 4
    0 . . . . .
    1 . . . N N
    2 . . . N C
    3 . . . N N
    4 . . . . X
    """
    cells = [
        Cell(x=3, y=1),  # top-left
        Cell(x=4, y=1),  # top
        Cell(x=3, y=2),  # left
        Cell(x=3, y=3),  # bottom-left
        Cell(x=4, y=3),  # bottom
        Cell(x=4, y=4),  # opposite corner
    ]
    central = Cell(x=4, y=2)
    nn = central.neighbours(5)
    assert set(nn).issubset(cells)
    assert cells[-1] not in set(nn)

def test_bottom_right_cell_neighbours():
    """
      0 1 2 3 4
    0 X . . . .
    1 . . . . .
    2 . . . . .
    3 . . . N N
    4 . . . N C
    """
    cells = [
        Cell(x=3, y=3),  # top-left
        Cell(x=4, y=3),  # top
        Cell(x=3, y=4),  # left
        Cell(x=0, y=0)   # opposite corner
    ]
    central = Cell(x=4, y=4)
    nn = central.neighbours(5)
    assert set(nn).issubset(cells)
    assert cells[-1] not in set(nn)

def test_neighbour_count():
    """
      0 1 2 3 4 5 6
    0 F . . . . . .
    1 . F . X . . .
    2 . . N N N . .
    3 . F N C N F .
    4 . . N N N . .
    5 . . . F . . .
    6 . . . . . . F
    """
    central = Cell(x=3, y=3)
    cells = [
        Cell(x=2, y=2),  # top-left
        Cell(x=3, y=2),  # top
        Cell(x=4, y=2),  # top-right
        Cell(x=2, y=3),  # left
        Cell(x=4, y=3),  # right
        Cell(x=2, y=4),  # bottom-left
        Cell(x=3, y=4),  # bottom
        Cell(x=4, y=4),  # bottom-right
        Cell(x=1, y=1),  # too far diagonally
        Cell(x=3, y=1),  # 2 cells away vertically
        Cell(x=5, y=3),  # 2 cells away horizontally
        Cell(x=1, y=3),  # 2 cells away horizontally
        Cell(x=3, y=5),  # 2 cells away vertically
        Cell(x=0, y=0),  # far away
        Cell(x=6, y=6)   # far away
    ]

    board = Board(10)
    board.from_cells(cells)
    nc = board.neighbour_count(central.neighbours(10))
    assert nc == 8

    """
      0 1 2 3 4 5 6
    0 . . . F . . .
    1 . F . . . . .
    2 . . . N . . .
    3 F . N C . . .
    4 . . . . . . .
    5 . . . . . F .
    6 . . . F . . .
    """
    cells = [
        Cell(x=2, y=3),  # left
        Cell(x=3, y=2),  # top
        Cell(x=1, y=1),  # far diagonal
        Cell(x=5, y=5),  # far diagonal
        Cell(x=0, y=3),  # 3 cells away horizontally
        Cell(x=3, y=6)   # 3 cells away vertically
    ]

    board = Board(10)
    board.from_cells(cells)
    nc = board.neighbour_count(central.neighbours(10))
    assert nc == 2

    """
      0 1 2 3 4 5 6 7 8 9
    0 F . . . . . . . . .
    1 . . . . . . F . . .
    2 . . . F . . . . . .
    3 . . . . . . . . . .
    4 . . . . . . . . . .
    5 . . . . . . . . . .
    6 . . . . . . . . . F
    7 . . . . . . . . . .
    8 . . . . . . . . N N
    9 . . . . . . . F N C
    """
    cells = [
        Cell(x=8, y=8),  # top-left
        Cell(x=9, y=8),  # top
        Cell(x=8, y=9),  # left
        Cell(x=0, y=0),  # far corner (opposite)
        Cell(x=2, y=3),  # far away
        Cell(x=6, y=1),  # far away
        Cell(x=7, y=9),  # 2 cells away horizontally
        Cell(x=9, y=6)   # 3 cells away vertically
    ]
    central = Cell(x=9, y=9)
    board = Board(10)
    board.from_cells(cells)
    nc = board.neighbour_count(central.neighbours(10))
    assert nc == 3

def test_simulation():
    sim = Simulation(5)
    print()
    for _ in range(5):
        sim.board.print_board()
        sim.run_step()
        print()
