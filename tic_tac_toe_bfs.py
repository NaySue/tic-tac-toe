import numpy as np
import curses
from collections import deque
import random

class Node:
    def __init__(self):
        self.id = -1
        self.data = None
        self.children = []
        
class Tree:
    def __init__(self):
        self.root = None

    def set_root(self, node: Node):
        self.root = node

    def add(self, node: Node, parent: int):
        if self.root is not None:
            queue = deque([self.root])
            while queue:
                curr_node = queue.popleft()
                queue.extend(curr_node.children)
                if curr_node.id == parent:
                    curr_node.children.append(node)
                    return
        else:
            self.set_root(node)

    def print(self):
        if self.root is not None:
            queue = deque([self.root])
            while queue:
                curr_node = queue.popleft()
                queue.extend(curr_node.children)
                children_ids = [child.id for child in curr_node.children]
                print(str(curr_node.id) + " - " + str(children_ids))
                
def check_winner(board):
    rows = [board[0], board[1], board[2]]
    cols = [[board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]]]
    diags = [[board[0][0], board[1][1], board[2][2]],
             [board[0][2], board[1][1], board[2][0]]]

    lines = rows + cols + diags

    for line in lines:
        if np.count_nonzero(line == 1) == 3:
            return 1
        elif np.count_nonzero(line == -1) == 3:
            return -1

    return 0

def generate(mat, player, lvl, tree, parent=None):
    winner = check_winner(mat)
    if np.count_nonzero(mat == 0) == 0 or np.abs(winner) == 1:
        # Base case: game over or board filled
        node = Node()
        node.id = lvl
        node.data = mat.copy()
        if parent != None:
            tree.add(node, parent)
        return

    for i in range(mat.size):
        if mat.flat[i] == 0:
            aux = mat.copy().flatten()
            aux[i] = player
            tmp = np.array(aux).reshape((3, 3))
            node = Node()
            node.id = lvl
            node.data = tmp
            if parent != None:
                tree.add(node, parent)
            generate(tmp, -player, lvl + 1, tree, node.id)
            
def bfs(tree, start_state):
    queue = deque([(tree.root, 1)])  # (node, level)
    while queue:
        curr_node, level = queue.popleft()
        print("Level:", level)
        print(curr_node.data)

        if level % 2 == 0:
            # AI's turn
            best_score = float('-inf')
            best_child = None
            for child in curr_node.children:
                score = minimax(child, False)
                if score > best_score:
                    best_score = score
                    best_child = child
            if best_child:
                curr_node = best_child
                print("AI's move:")
                print(curr_node.data)
                print()

        if np.count_nonzero(curr_node.data == 0) == 0 or np.abs(check_winner(curr_node.data)) == 1:
            # Game over or board filled
            break

        queue.extend((child, level + 1) for child in curr_node.children)
        
def minimax(node, maximizing_player):
    winner = check_winner(node.data)
    if np.count_nonzero(node.data == 0) == 0 or np.abs(winner) == 1:
        return winner

    if maximizing_player:
        best_score = float('-inf')
        for child in node.children:
            score = minimax(child, False)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for child in node.children:
            score = minimax(child, True)
            best_score = min(best_score, score)
        return best_score
    
def draw_board(stdscr, board):
    stdscr.clear()
    stdscr.addstr("Tic-Tac-Toe\n")
    stdscr.addstr("-----------\n")
    for row in board:
        stdscr.addstr("| ")
        for cell in row:
            if cell == 1:
                stdscr.addstr("X ")
            elif cell == -1:
                stdscr.addstr("O ")
            else:
                stdscr.addstr("  ")
        stdscr.addstr("|\n")
    stdscr.addstr("-----------\n")
    stdscr.refresh()

def play_game(stdscr, game_tree):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input

    board = np.zeros((3, 3), dtype=int)
    current_state = game_tree.root

    # Randomly choose who starts
    player_starts = random.choice([True, False])
    if player_starts:
        turn_message = "Your turn. Press 1-9 to make a move. Press 'q' to quit."
    else:
        turn_message = "AI's turn. Press 'q' to quit."

    while True:
        draw_board(stdscr, board)

        # Player's turn
        if np.count_nonzero(board == 0) > 0 and np.abs(check_winner(board)) != 1:
            key = stdscr.getch()
            if key == ord('q'):
                break

            row, col = divmod(key - ord('1'), 3)
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == 0:
                board[row][col] = 1
                current_state = current_state.children[row * 3 + col]

        draw_board(stdscr, board)

        # AI's turn
        if np.count_nonzero(board == 0) > 0 and np.abs(check_winner(board)) != 1:
            bfs(game_tree, current_state)

            best_child = None
            for child in current_state.children:
                if (child.data == current_state.data).all():
                    best_child = child
                    break

            if best_child is not None:
                current_state = best_child
                board = current_state.data
                curses.napms(500)  # Pause for AI move

    curses.napms(2000)  # Pause before exiting
    
def main(stdscr):
    # Create a new tree
    game_tree = Tree()

    # Generate game states
    initial_state = np.zeros((3, 3), dtype=int)
    generate(initial_state, 1, 1, game_tree)

    # Play the game
    play_game(stdscr, game_tree)

# Run the game
curses.wrapper(main)        