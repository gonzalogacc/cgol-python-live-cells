# Conway's Game of Life - Sparse Implementation

A Python implementation of Conway's Game of Life using sparse representation.

## Approach

This implementation uses a **sparse representation** where only living cells are stored in memory. Instead of processing every cell on the board, it only evaluates:
- Living cells (to check if they survive)  
- Dead neighbors of living cells (to check if they're born)


## Usage

```bash
python main.py [options]
```

**Options:**
- `-b, --board_size`: Board size (default: 25)
- `-g, --generations`: Number of generations (default: 100)
- `-s, --saturation`: Initial population density 0.0-1.0 (default: 0.4)
- `-f, --freq`: Time between generations (default: 0.2s)
- `-p, --pattern`: .cells file to load pattern, "random" for random board (default: random)

**Examples:**
```bash
# Random sparse simulation
python main.py -b 100 -g 500 -s 0.1 -f 0.05

# Load a glider pattern
python main.py -p glider.cells -b 50 -g 200

# Dense small board
python main.py -b 20 -s 0.6 -g 100
```

## Classes

- **`Cell`**: Represents a cell coordinate with neighbor detection and rule application
- **`Board`**: Manages the set of living cells and neighbor counting  
- **`Simulation`**: Orchestrates the evolution process and handles initialization

## Performance

- **Memory**: Scales with number of living cells, not board size
- **Speed**: Scales with pattern complexity, not board dimensions
- **Best for**: Large sparse boards, gliders, spaceships, oscillators

## Rules

Standard Conway's Game of Life rules:
- Living cell with < 2 neighbors dies (underpopulation)
- Living cell with 2-3 neighbors survives
- Living cell with > 3 neighbors dies (overpopulation)  
- Dead cell with exactly 3 neighbors becomes alive (reproduction)

## Example Patterns

The sparse representation excels with:
- **Gliders** traveling across large empty spaces
- **Oscillators** with small active regions
- **Spaceships** and other moving patterns
- **Large empty universes** with isolated colonies

## TODO

- Port load patterns from cells file
- Some basic optimization