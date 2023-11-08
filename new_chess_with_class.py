import chess
import sys


class ChessGame:
    BLACK = "\033[30m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    PIECES_DICT = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "P": "♙", "N": "♘"}

    def __init__(self):
        self.board = chess.Board()

    def turn_piece(self):
        if self.board.turn == chess.WHITE:
            turn = "white"
        else:
            turn = "black"

        return turn

    def input_validation_king_check(self):
        while True:
            move = input("Please enter your move: ")
            try:
                player_move = chess.Move.from_uci(move)

                if player_move in self.board.legal_moves:
                    legal_moves = list(self.board.legal_moves)
                    safe_moves = []

                    # Filter out moves that get the king out of check
                    for move in legal_moves:
                        # Make the move on a temporary board
                        temp_board = self.board.copy()
                        temp_board.push(move)

                        # Check if the king is still in check after the move
                        if not temp_board.is_check():
                            safe_moves.append(move)

                    if not safe_moves:
                        print("It's checkmate! The game is over.")
                        self.board.is_game_over = True
                    if player_move not in safe_moves:
                        print("Invalid move. You must get the king out of check.")
                        print(f"here are the legal moves {safe_moves}")
                        continue
                    else:
                        self.board.push(player_move)
                        break
                else:
                    print("Invalid move, try again!")
                    continue

            except:
                print(
                    f"The move {move} is not in the correct format. Please enter a move in the UCI format."
                )
                continue

    def checking_promotion(self):
        last_move = self.board.pop()

        target_rank = chess.square_rank(last_move.to_square)
        is_promotion_square = target_rank in [0, 7]

        if is_promotion_square:
            edit_move = chess.Move.from_uci(str(last_move) + "q")
            self.board.push(edit_move)
        else:
            self.board.push(last_move)

    def display_board(self):
        print("   a b c d e f g h")
        for i in range(8):
            row = []
            for j in range(8):
                square = chess.square(j, i)
                piece = self.board.piece_at(square)
                if piece:
                    if piece.color == chess.BLACK:
                        row.append(
                            f"{self.BLACK}{self.PIECES_DICT[str(piece).upper()]}{self.RESET}"
                        )
                    else:
                        row.append(
                            f"{self.WHITE}{self.PIECES_DICT[str(piece).upper()]}{self.RESET}"
                        )
                else:
                    if (i + j) % 2 == 0:
                        row.append(".")
                    else:
                        row.append(".")
            print(f"{i+1} {' '.join(row)}")

    def is_draw(self):
        if self.board.is_fivefold_repetition():
            self.board.is_game_over = True

        # Check for seventy-five moves rule
        if self.board.is_seventyfive_moves():
            self.board.is_game_over = True

        # Check for stalemate
        if self.board.is_stalemate():
            self.board.is_game_over = True

        # Check for insufficient material
        if self.board.is_insufficient_material():
            self.board.is_game_over = True

        # If none of the conditions are met, the game is not a draw
        self.board.is_game_over = False

    def play(self):
        # while not self.board.is_game_over():
        self.display_board()

        turn = self.turn_piece()
        print(f"TURN FOR: {turn}")

        self.input_validation_king_check()
        self.checking_promotion()
        self.is_draw()

    def how_to_play(self):
        print(
            "**********************\n"
            "*                    *\n"
            "*     IMPORTANT      *\n"
            "*                    *\n"
            "**********************"
        )

        msg = """You have to use UCI format to play this CLI(command line interface) game. 
The purpose of this game is to play against AI bot which is yet to be created. 
In order to move your pieces, you have to type the square that your piece is at, and the destination square that you want to move to.
For example, if you want to move your pawn from a2 to a4, please type in a2a4 when you want to move. 
                """
        print(msg)


if __name__ == "__main__":
    chess_game = ChessGame()

    chess_game.how_to_play()

    while chess_game.board.is_game_over != True:
        chess_game.play()

# TODO: i have to optimize this code again ... i still have to handle drawing condition
