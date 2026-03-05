import sys
from copy import deepcopy

def read_input(filename):
    with open(filename) as f:
        lines = [l.strip() for l in f if l.strip()]
    h, n, k = map(int, lines[0].split())
    tubes = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        tubes.append(row)
    # Add empty tubes
    for _ in range(k):
        tubes.append([])
    return h, n, k, tubes

def is_goal(tubes, h):
    for tube in tubes:
        if len(tube) == 0:
            continue
        if len(tube) != h:
            return False
        if len(set(tube)) != 1:
            return False
    return True

def heuristic(tubes, h):
    """
    Lower bound: count balls not in a uniform tube.
    For each tube, count how many balls need to move out
    (any ball that is not the same color as the bottom ball, or is in a mixed tube).
    More precisely: for each tube, the cost is h - (length of longest same-color
    prefix from bottom). But we need a proper admissible heuristic.
    
    Admissible heuristic: each "misplaced group" requires at least one move.
    We count the number of color-contiguous groups across all tubes minus
    the number of colors (since each color needs exactly 1 group in the end).
    """
    # Count contiguous groups per tube
    total_groups = 0
    for tube in tubes:
        if not tube:
            continue
        groups = 1
        for i in range(1, len(tube)):
            if tube[i] != tube[i-1]:
                groups += 1
        total_groups += groups
    
    # Number of non-empty tubes
    num_colors = len(set(b for tube in tubes for b in tube))
    # Each color should end up as 1 group, so minimum moves >= total_groups - num_colors
    return max(0, total_groups - num_colors)

def get_moves(tubes, h):
    moves = []
    for i, src in enumerate(tubes):
        if not src:
            continue
        top = src[-1]
        for j, dst in enumerate(tubes):
            if i == j:
                continue
            if len(dst) >= h:
                continue
            # Can move if dst is empty or top of dst matches top of src
            if not dst or dst[-1] == top:
                moves.append((i, j))
    return moves

def is_useless_move(tubes, i, j, h):
    """Prune: moving from a uniform tube to an empty tube is useless."""
    src = tubes[i]
    dst = tubes[j]
    if not dst and len(set(src)) == 1:
        return True
    return False

def ida_star(tubes, h):
    def search(tubes, g, bound, path, last_move):
        f = g + heuristic(tubes, h)
        if f > bound:
            return f, None
        if is_goal(tubes, h):
            return -1, path[:]
        
        minimum = float('inf')
        
        moves = get_moves(tubes, h)
        for (i, j) in moves:
            if is_useless_move(tubes, i, j, h):
                continue
            # Avoid immediate reversal
            if last_move and last_move == (j, i):
                continue
            
            # Apply move
            ball = tubes[i][-1]
            tubes[i].pop()
            tubes[j].append(ball)
            path.append((i, j))
            
            t, result = search(tubes, g + 1, bound, path, (i, j))
            
            # Undo move
            tubes[j].pop()
            tubes[i].append(ball)
            path.pop()
            
            if result is not None:
                return -1, result
            if t < minimum:
                minimum = t
        
        return minimum, None
    
    bound = heuristic(tubes, h)
    path = []
    
    while True:
        t, result = search(tubes, 0, bound, path, None)
        if result is not None:
            return result
        if t == float('inf'):
            return None  # No solution
        bound = t

def main():
    if len(sys.argv) < 2:
        print("Usage: solver <input_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    h, n, k, tubes = read_input(filename)
    
    solution = ida_star(tubes, h)
    
    if solution is None:
        print("No solution found")
        return
    
    for (i, j) in solution:
        src_label = chr(ord('a') + i)
        dst_label = chr(ord('a') + j)
        print(f"{src_label}->{dst_label}")

if __name__ == "__main__":
    main()