
def check_row(param, row):
    if param in row and row.count(param) == len(row):
        return True
def check_step(field, param):
    first_diog = [x for i, el in enumerate(field) for j, x in enumerate(el) if j == i]
    second_diog = [x for i, el in enumerate(field) for j, x in enumerate(el) if i == abs(j - (len(el) - 1))]
    for i, el in enumerate(field):
        col = [x[i] for x in field]
        if check_row(param, el) or check_row(param, col):
            return True
    if check_row(param, first_diog) or check_row(param, second_diog):
        return True

    else:
        return False

def print_field(field):
    print(f'    0   1   2')
    for i, el in enumerate(field):
        print(f'{i} | {el[0]} | {el[1]} | {el[2]} |')

def enter_coordinates(field, param_to_move):
    j = 0
    while j <= 3:
        j += 1
        try:
            a = int(input('Введите координату по вертикале в диапазоне от 0 до 3: '))
            b = int(input('Введите координату по горизонтале в диапазоне от 0 до 3: '))
            if field[b][a] == '-':
                field[b][a] = param_to_move
                return True
            else:
                print('В это поле сходить нельзя, оно уже занято')
                continue
        except:
            print('Неверные пераметры ввода')
            continue
    else:
        print('Мы не смогли начать игру, вы вводите неверные параметры')
        return False

def start_game():
    field = [['-' for _ in range(3)] for _ in range(3)]
    param_to_move = 'X'
    i = 0
    print('Начинаем игру')
    print_field(field)
    while i <= 9:
        i += 1
        print(f'Ход { param_to_move }')
        if enter_coordinates(field, param_to_move) and not check_step(field, param_to_move):
            print_field(field)
            param_to_move = 'X' if param_to_move == 'O' else 'O'
        else:
            print_field(field)
            print(f'{ param_to_move } - Выйграли')
            print('Игра закончилась')
            break

start_game()
