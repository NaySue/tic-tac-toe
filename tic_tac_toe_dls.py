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
            stack = deque([self.root])
            while stack:
                curr_node = stack.pop()
                stack.extend(curr_node.children)
                if curr_node.id == parent:
                    curr_node.children.append(node)
                    return
        else:
            self.set_root(node)

    def print(self):
        if self.root is not None:
            stack = deque([self.root])
            while stack:
                curr_node = stack.pop()
                stack.extend(curr_node.children)
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
    if np.count_nonzero(mat == 0) == 0 or np.abs(winner) == 1 or lvl == 4:  # Limit the depth to 4 (adjust as needed)
        # Base case: game over, board filled, or depth limit reached
        node = Node()
        node.id = lvl
        node.data = mat.copy()
        if parent is not None:
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
            if parent is not None:
                tree.add(node, parent)
            generate(tmp, -player, lvl + 1, tree, node.id)

def dls(tree, start_state):
    stack = deque([(tree.root, 1)])  # (node, level)
    while stack:
        curr_node, level = stack.pop()
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

        stack.extend((child, level + 1) for child in curr_node.children)

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
    screen_height, screen_width = stdscr.getmaxyx()
    board_height, board_width = 7, 11
    start_y, start_x = (screen_height - board_height) // 2, (screen_width - board_width) // 2

    tic_tac_toe_str = "Tic-Tac-Toe"
    stdscr.addstr(start_y, start_x, tic_tac_toe_str)
    stdscr.addstr(start_y + 1, start_x, "-----------")

    for i in range(3):
        stdscr.addstr(start_y + i * 2 + 2, start_x, "|", curses.A_BOLD)
        for j in range(3):
            cell = "X" if board[i][j] == 1 else "O" if board[i][j] == -1 else " "
            stdscr.addstr(start_y + i * 2 + 2, start_x + 2 + j * 4, f" {cell} ", curses.A_BOLD)
            stdscr.addstr(start_y + i * 2 + 2, start_x + 4 + j * 4, "|", curses.A_BOLD)

    stdscr.addstr(start_y + 6, start_x, "-----------")
    stdscr.refresh()


def curses_main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input
    curses.start_color()  # Enable color support if available
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Define a color pair


def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()  # Enable color support if available
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Define a color pair

    
    # Create a new tree
    game_tree = Tree()

    # Generate game states
    initial_state = np.zeros((3, 3), dtype=int)
    generate(initial_state, 1, 1, game_tree)

    # Play the game
    curses.curs_set(0)  # Hide the cursor

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
        stdscr.addstr(turn_message + "\n")

        # Player's turn
        if player_starts:
            stdscr.addstr("Player's turn\n")
            if np.count_nonzero(board == 0) > 0 and np.abs(check_winner(board)) != 1:
                key = None
                while key is None:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                    key = key - ord('1')
                    if 0 <= key < 9:
                        row, col = key // 3, key % 3
                        if board[row][col] == 0:
                            board[row][col] = 1
                            current_state = current_state.children[row * 3 + col]
                            player_starts = False
                            turn_message = "AI's turn. Press 'q' to quit."
                        else:
                            key = None
                    else:
                        key = None

        draw_board(stdscr, board)

        # AI's turn
        if not player_starts:
            if np.count_nonzero(board == 0) > 0 and np.abs(check_winner(board)) != 1:
                dls(game_tree, current_state)

                best_child = None
                for child in current_state.children:
                    if (child.data == current_state.data).all():
                        best_child = child
                        break

                if best_child is not None:
                    current_state = best_child
                    board = current_state.data
                    player_starts = True
                    turn_message = "Your turn. Press 1-9 to make a move. Press 'q' to quit."
                    
        # Wait for the player to press a key before the next turn
        key = stdscr.getch()
        if key == ord('q'):
            break

    curses.wrapper(main)

if __name__ == "__main__":
    curses.wrapper(main)