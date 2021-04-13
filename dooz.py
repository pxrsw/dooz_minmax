from math import inf as infinity
from random import choice

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def result(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def is_game_finish(state):
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

# array i az  [behtarin row, behtarin col, behtarin score] barmigardoone
def minimax(state, depth, player):

# computer ra min va ensan ro max gharar migozarim
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

# agar bazi tamoom shode bood ya avalin nobat 
    if depth == 0 or is_game_finish(state):
        score = result(state)
        return [-1, -1, score]

# halghe mizanim rooye hame khane haye ghabele entekhab
    for cell in empty_cells(state):
        # be ezaye har khane ye khali an ra dar an gharar midanim va score e an ra hesab mikonim va say mikonim in joori behtain ravesh ra entekhab konim
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

# agar ke in khane behtar az khaneii bood ta alan peyda kardim an ra jaygozin mikonim ta dar akhar behtarin khane ra return konim
        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def print_board(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
# agar bazi tamoo shode bashe ke hichi
    depth = len(empty_cells(board))
    if depth == 0 or is_game_finish(board):
        return
# dar gheyre in soorat:
    print(f'Computer turn [{c_choice}]')
    print_board(board, c_choice, h_choice)

    if depth == 9:
        # agar dar avalin nobat bood be soorate random entekhab mikonim
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        # algorithm e minmax moshakhas mikone ke computer che khaneii ro entekhab kone
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or is_game_finish(board):
        return

    # Dictionary baraye tabdile adadi ke ensan vared mikone be aan khane az matrix
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    print(f'Human turn [{h_choice}]')
    print_board(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1

        except (KeyError, ValueError):
            print('Bad choice')


def main():
    h_choice = '' 
    c_choice = ''
    first = ''

    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'


    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # halgheye asli e bazi
    while len(empty_cells(board)) > 0 and not is_game_finish(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # chap e natijeye payani
    if wins(board, HUMAN):
        print(f'Human turn [{h_choice}]')
        print_board(board, c_choice, h_choice)
        print('YOU WIN!')
   
    elif wins(board, COMP):
        print(f'Computer turn [{c_choice}]')
        print_board(board, c_choice, h_choice)
        print('YOU LOSE!')
    
    else:
        print_board(board, c_choice, h_choice)
        print('DRAW!')

    exit()

if __name__ == '__main__':
    main()