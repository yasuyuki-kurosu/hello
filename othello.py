EMPTY = '.'
BLACK = 'B'
WHITE = 'W'

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def init_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE
    return board

def print_board(board):
    print('  ' + ' '.join(str(i) for i in range(8)))
    for i, row in enumerate(board):
        print(str(i) + ' ' + ' '.join(row))

def is_on_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_moves(board, player):
    opponent = BLACK if player == WHITE else WHITE
    valid = {}
    for x in range(8):
        for y in range(8):
            if board[x][y] != EMPTY:
                continue
            flips = []
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                temp = []
                if is_on_board(nx, ny) and board[nx][ny] == opponent:
                    while is_on_board(nx, ny) and board[nx][ny] == opponent:
                        temp.append((nx, ny))
                        nx += dx
                        ny += dy
                    if is_on_board(nx, ny) and board[nx][ny] == player:
                        flips.extend(temp)
            if flips:
                valid[(x, y)] = flips
    return valid

def apply_move(board, move, flips, player):
    x, y = move
    board[x][y] = player
    for fx, fy in flips:
        board[fx][fy] = player

def score(board):
    b = sum(row.count(BLACK) for row in board)
    w = sum(row.count(WHITE) for row in board)
    return b, w

def main():
    board = init_board()
    player = BLACK
    while True:
        print_board(board)
        moves = valid_moves(board, player)
        if not moves:
            other_moves = valid_moves(board, BLACK if player == WHITE else WHITE)
            if not other_moves:
                break
            else:
                print(f"{player} has no valid moves. Skipping turn.")
                player = BLACK if player == WHITE else WHITE
                continue
        print(f"{player}'s move. Enter row col (e.g., 2 3):")
        try:
            line = input().strip()
            if line.lower() in ('q', 'quit'):
                print('Game quit.')
                return
            x, y = map(int, line.split())
            if (x, y) not in moves:
                print('Invalid move.')
                continue
        except Exception:
            print('Invalid input.')
            continue
        apply_move(board, (x, y), moves[(x, y)], player)
        player = BLACK if player == WHITE else WHITE

    b, w = score(board)
    print_board(board)
    print(f"Game over. Black: {b}  White: {w}")
    if b > w:
        print('Black wins!')
    elif w > b:
        print('White wins!')
    else:
        print('Draw.')

if __name__ == '__main__':
    main()
