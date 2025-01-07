import chess
import chess.engine
import time
import sys
import math
import logging

# Set up logging
logging.basicConfig(
    filename='engine_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.debug("Starting the chess engine")
version = "Grendel.MCTS.2.024"



import chess
import chess.engine
import random
import math
import time

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.visits = 0
        self.wins = 0
        self.children = []

    def is_terminal(self):
        return self.board.is_game_over()

    def is_fully_expanded(self):
        return len(self.children) == len(list(self.board.legal_moves))

class MCTS:
    def __init__(self, board, time_limit=1.0):
        self.board = board
        self.time_limit = time_limit
        self.root = MCTSNode(board)

    def search(self):
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            node = self.select(self.root)
            if not node.is_terminal():
                self.expand(node)
            winner = self.simulate(node)
            self.backpropagate(node, winner)

        best_move = self.get_best_move(self.root)
        return best_move

    def select(self, node):
        while not node.is_terminal() and node.is_fully_expanded():
            node = self.best_uct_child(node)
        return node

    def expand(self, node):
        for move in node.board.legal_moves:
            child_board = node.board.copy()
            child_board.push(move)
            child_node = MCTSNode(child_board, parent=node, move=move)
            node.children.append(child_node)

    def simulate(self, node):
        board_copy = node.board.copy()
        while not board_copy.is_game_over():
            legal_moves = list(board_copy.legal_moves)
            move = random.choice(legal_moves)
            board_copy.push(move)
        return 1 if board_copy.is_checkmate() and board_copy.turn == chess.BLACK else -1 if board_copy.is_checkmate() else 0

    def backpropagate(self, node, winner):
        while node is not None:
            node.visits += 1
            if winner == 1:  # White wins
                node.wins += 1
            elif winner == -1:  # Black wins
                node.wins -= 1
            node = node.parent

    def best_uct_child(self, node):
        best_uct = -math.inf
        best_child = None
        for child in node.children:
            uct_value = (child.wins / (child.visits+0.0000001)) + math.sqrt(2 * math.log(node.visits) / (child.visits+0.00000001))
            if uct_value > best_uct:
                best_uct = uct_value
                best_child = child
        return best_child

    def get_best_move(self, root):
        best_move = None
        best_visits = -1
        for child in root.children:
            if child.visits > best_visits:
                best_visits = child.visits
                best_move = child.move
        return best_move

class MyChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.start_time = None
        self.killer_moves = [{} for _ in range(100)]

    def evaluate(self, board):
        pass

        
        
        
                    
        
    def search(self, depth, alpha, beta, is_maximizing):
        
        pass
    def find_best_move(self, max_time = 10):
        pass
       
                

                

    def send(self, message):
        """Send a message to the GUI."""
        print(message, flush=True)
        logging.debug(f"sent message {message}")

    def handle_command(self, command):
        """Process UCI commands from the GUI."""
        logging.debug(f"received command {command}")
        if command == "uci":
            self.uci()
        elif command == "isready":
            self.isready()
        elif command.startswith("position"):
            self.position(command)
        elif command.startswith("go"):
            self.go(command)
        elif command == "quit":
            self.quit()
        elif command == "ucinewgame":
            self.start()
        else:
            self.send(f"Unknown command: {command}")
    def killer_move_heuristic(self, move, depth):
        if move in self.killer_moves[depth]:
            return 100
        else:
            return 0
    def move_heuristic(self, move):
        """Heuristic to rank moves. For now, it ranks captures higher."""
        if self.board.is_capture(move):
            return 10  # Arbitrary value for captures
        else:
            return 1 
    def uci(self):
        """Respond to the 'uci' command."""
        self.send(f"id name {version}")
        self.send(f"id author Sreek")
        self.send("uciok")
    def start(self):
        self.board.reset()
        self.send("readyok")

    def isready(self):
        """Respond to the 'isready' command."""
        self.send("readyok")

    def position(self, command):
        """Set the board position."""
        if "startpos" in command:
            self.board.reset()
            moves = command.split(" moves ")[-1] if "moves" in command else ""
        elif "fen" in command:
            fen, moves = command.split(" moves ") if "moves" in command else (command.split("fen ")[1], "")
            self.board.set_fen(fen.strip())
        else:
            moves = ""

        for move in moves.split():
            self.board.push_uci(move)

    def go(self, command):
        mcts = MCTS(self.board, time_limit=5.0)  # 2 seconds for the search
        best_move = mcts.search() # Fixed depth search

        if best_move:
            self.send(f"bestmove {best_move.uci()}")
        else:
            self.send("bestmove (none)")
        logging.debug(f"sent move {best_move.uci()}")
            
    def quit(self):
        """Handle the 'quit' command to exit."""
        self.send("bye")
        sys.exit()

def main():
    engine = MyChessEngine()
    while True:
        try:
            command = input().strip()
            engine.handle_command(command)
        except EOFError:
            break

if __name__ == "__main__":
    main()