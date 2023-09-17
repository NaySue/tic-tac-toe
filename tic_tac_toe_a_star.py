import copy

# Define constants
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1

# A* Node representation
class Node:
    def __init__(self, board, player, move):
        self.board = board
        self.player = player
        self.move = move
        self.children = []

    def is_terminal(self):
        return self.check_winner() != EMPTY or not any(EMPTY in row for row in self.board)

    def check_winner(self):
        for row in self.board:
            if all(cell == PLAYER_X for cell in row):
                return PLAYER_X
            elif all(cell == PLAYER_O for cell in row):
                return PLAYER_O

        for col in range(3):
            if all(self.board[row][col] == PLAYER_X for row in range(3)):
                return PLAYER_X
            elif all(self.board[row][col] == PLAYER_O for row in range(3)):
                return PLAYER_O

        if all(self.board[i][i] == PLAYER_X for i in range(3)) or all(self.board[i][2 - i] == PLAYER_X for i in range(3)):
            return PLAYER_X
        elif all(self.board[i][i] == PLAYER_O for i in range(3)) or all(self.board[i][2 - i] == PLAYER_O for i in range(3)):
            return PLAYER_O

        return EMPTY

    def get_empty_cells(self):
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    empty_cells.append((i, j))
        return empty_cells

# A* Search
def astar_search(node, depth):
    if node.is_terminal():
        if node.check_winner() == PLAYER_X:
            return 1
        elif node.check_winner() == PLAYER_O:
            return -1
        else:
            return 0

    if depth % 2 == 0:  # Maximizing player (X)
        max_eval = float('-inf')
        for child in node.children:
            eval = astar_search(child, depth + 1)
            max_eval = max(max_eval, eval)
        return max_eval

    else:  # Minimizing player (O)
        min_eval = float('inf')
        for child in node.children:
            eval = astar_search(child, depth + 1)
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board):
    root = Node(board, PLAYER_X, None)
    empty_cells = root.get_empty_cells()
     
    if not empty_cells:
        return None  # No available moves
    
    for cell in empty_cells:
        new_board = copy.deepcopy(board)
        new_board[cell[0]][cell[1]] = PLAYER_X
        root.children.append(Node(new_board, PLAYER_O, cell))

    best_move = None
    best_eval = float('-inf')

    for child in root.children:
        eval = astar_search(child, 0)
        if eval > best_eval:
            best_eval = eval
            best_move = child.move

    return best_move

def print_board(board):
    for row in board:
        print(" | ".join(["X" if cell == PLAYER_X else "O" if cell == PLAYER_O else " " for cell in row]))
        print("-" * 9)

def main():
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]

    print("Welcome to Tic-Tac-Toe!")

    while True:
        print_board(board)
        
        # Check for a draw
        if not any(EMPTY in row for row in board):
            print_board(board)
            print("It's a draw!")
            break

        #Player's turn
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == EMPTY:
                    board[row][col] = PLAYER_O
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter row and column as integers.")
        
        # Check for a win after player's move
        winner = Node(board, PLAYER_O, None).check_winner()
        if winner == PLAYER_O:
            print_board(board)
            print("You win!")
            break
        elif winner == PLAYER_X:
            print_board(board)
            print("AI wins!")
            break

        # AI's turn
        print("AI's turn...")
        ai_move = find_best_move(board)
        if ai_move is not None:
            board[ai_move[0]][ai_move[1]] = PLAYER_X
        
        # Check for a win after AI's move
        winner = Node(board, PLAYER_X, None).check_winner()
        if winner == PLAYER_X:
            print_board(board)
            print("AI wins!")
            break
        elif winner == PLAYER_O:
            print_board(board)
            print("You win!")
            break
        
if __name__ == "__main__":
    main()
