import cProfile
import random
from copy import deepcopy
from time import sleep, perf_counter
from typing import Self


class Cell:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x}:{self.y}"

    def __lt__(self, other):
        # Lexicographic: compare x first, then y if x values are equal
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def neighbours(self, board_size: int) -> set[Self]:
        x = self.x
        y = self.y
        # board_size = board_size

        neighbours = []
        for ny in [-1, 0, 1]:
            for nx in [-1, 0, 1]:
                if ny == nx == 0:
                    # skip centre
                    continue

                px, py = x+nx, y+ny

                if 0<=px<board_size and 0<=py<board_size:
                    neighbours.append(Cell(x=px, y=py))
        return set(neighbours)

    def apply_rules(self, is_alive: bool, number_of_neighbours: int):
        if is_alive:
            new_value = 2 <= number_of_neighbours <= 3
        else:
            new_value = number_of_neighbours == 3
        return new_value

class Board:
    _board_size: int

    def __init__(self, board_size: int):
        self._board_size = board_size
        self._board = set() # Board is a set of live cells

    @property
    def size(self):
        return self._board_size

    def from_cells(self, cells: list[Cell]) -> None:
        self._board.update(cells)

    def neighbour_count(self, neighbours: set[Cell]) -> int:
        return len(neighbours & self._board)

    def get_live_cells(self):
        return self._board

    def print_board(self):
        print(chr(27) + "[2J")
        print(chr(27) + "[1;1f")
        board_string = ""
        for y in range(self.size):
            line = ""
            for x in range(self.size):
                if Cell(x=x, y=y) in self._board:
                    line += 'O'
                else:
                    line += ' '
            board_string+=f"{line}\n"
        print(board_string)

class Simulation:

    def __init__(self, board_size: int):
        self.board = Board(board_size)

        self.to_visit_live = set()
        self.to_visit_neighbours = set()

        self.visited = set()

    def init_random_board(self, pop_density: float = .2):
        self.board.from_cells(list(self.random_cells(int(self.board.size*self.board.size*pop_density))))

    def random_cells(self, cell_number: int) -> set[Cell]:
        cells = set()
        for _ in range(cell_number):
            cells.add(Cell(x=random.choice(range(self.board.size)), y=random.choice(range(self.board.size))))
        return cells

    def run_step(self):
        """ Run a single step """

        self.to_visit_live.clear()
        self.to_visit_neighbours.clear()

        # Temp board to store the step being computed
        temp_board = Board(self.board.size)

        # set the live cells to be processed
        for cell in self.board.get_live_cells():
            self.to_visit_live.add(cell)

        # If there are empty neighbours to be computed in case they become alive
        # add to the second list. These are all dead at the beginning otherwise
        # they would ne in the other set
        for cell in self.to_visit_live:
            for neighbour in cell.neighbours(self.board.size):
                if neighbour not in self.to_visit_live:
                    self.to_visit_neighbours.add(neighbour)

        for cell in self.to_visit_live:
            number_of_neighbours = self.board.neighbour_count(cell.neighbours(self.board.size))
            if cell.apply_rules(True, number_of_neighbours):
                temp_board._board.add(cell)

        for cell in self.to_visit_neighbours:
            number_of_neighbours = self.board.neighbour_count(cell.neighbours(self.board.size))
            if cell.apply_rules(False, number_of_neighbours):
                temp_board._board.add(cell)

        self.board._board = temp_board._board

def main(board_size: int, freq: float, periods: int, random_pop_density: float, pattern: str = 'random'):
    sim = Simulation(board_size)
    sim.init_random_board(random_pop_density)
    for _ in range(periods):
        sim.run_step()
        sim.board.print_board()
        sleep(freq)

if __name__ == "__main__":

    # cProfile.run('main(20, 101, .2)', sort='cumtime')
    t1_start = perf_counter()
    main(200, 101, .2)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:", t1_stop - t1_start)

