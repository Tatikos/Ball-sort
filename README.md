# Ball Sort Puzzle - IDA* Solver

## Description

Solves the Ball Sort Puzzle using the IDA* (Iterative Deepening A*) search algorithm.

## Files

- `solver.py` — Main solver script (Python 3)
- `ballsort.txt` — Example input file

## Requirements

- Python 3.6 or higher (no external libraries needed)

## Compilation

No compilation needed — Python is an interpreted language.

## Running

```bash
python3 solver.py <input_file>
```

### Example

```bash
python3 solver.py ballsort.txt
```

## Input Format

The input file must follow this structure:

```
h n k
<tube 1 balls, bottom to top, space-separated>
<tube 2 balls, bottom to top, space-separated>
...
<tube n balls, bottom to top, space-separated>
```

Where:
- `h` = tube capacity
- `n` = number of colors (and filled tubes)
- `k` = number of empty tubes

## Output Format

Each line of output shows one move: `X->Y`, where `X` is the source tube and `Y` is the destination tube. Tubes are labeled `a`, `b`, `c`, ... in order.

## Algorithm

The solver uses **IDA*** (Iterative Deepening A*):

- **Heuristic**: Counts the total number of contiguous color groups across all tubes, minus the number of distinct colors. This is admissible because each color must ultimately form exactly one group.
- **Pruning**: 
  - Skips moves that reverse the immediately preceding move.
  - Skips moving a uniform (already-sorted) tube into an empty tube (wasteful).

## Constraints

- 1 ≤ n ≤ 9
- 1 ≤ n + k ≤ 26