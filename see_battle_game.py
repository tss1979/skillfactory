import random

SIZES = [3, 2, 2, 1, 1, 1, 1]


class BoardOutException(Exception):
    "Возникает когда игрок пытается выстрелить за пределы игрового поля"
    pass


class DoubleShootException(Exception):
    "Возникает когда игрок пытается выстрелить в ячейку, по которой уже производился выстрел"
    pass


class ShipIsNotOnBoardException(Exception):
    "Возникает когда игрок пытается поставить корабль за пределы игрового поля"
    pass


class ShootIsNotOnBoardException(Exception):
    "Возникает когда игрок пытается выстрелить за пределы игрового поля"
    pass


class ShipIsInTouchException(Exception):
    "Возникает когда игрок пытается поставить корабль без отступа от другого корабля"
    pass


class FieldIsOcupiedException(Exception):
    "Возникает когда игрок пытается поставить корабль в поле где уже есть корабль"
    pass


class BrokenBroadException(Exception):
    "Возникает когда созданная компьютером игровая доска не пригодна для игры"
    pass


class WrongDirectionException(Exception):
    "Возникает когда пользователь вводит неверную команду напрвления построения корабля"
    pass


class ContourShootException(Exception):
    "Возникает когда пользователь стреляет в точку где не может быть корабля из-за прикосновения"
    pass


class Dot:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self.__class__.__name__) + f'({ self.x } ,{ self.y })'

    def __eq__(self, other):
        return all([self.x == other.x, self.y == other.y])


class Ship:
    def __init__(self, length: int, begin_dot: Dot, direction: str):
        self.length = int(length)
        self.begin_dot = begin_dot
        self.direction = direction
        self.lifes = length

    @property
    def dots(self):
        '''Устанавливает все значения точек коробля от начально в заданном направлении'''
        if self.length > 1:
            if self.direction == 'down':
                return [Dot(self.begin_dot.x, self.begin_dot.y + i) for i in range(self.length)]
            elif self.direction == 'right':
                return [Dot(self.begin_dot.x + i, self.begin_dot.y) for i in range(self.length)]
            elif self.direction == 'up':
                return [Dot(self.begin_dot.x, self.begin_dot.y - i) for i in range(self.length)]
            elif self.direction == 'left':
                return [Dot(self.begin_dot.x - i, self.begin_dot.y) for i in range(self.length)]
        else:
            return [self.begin_dot]


class Board:
    def __init__(self, hid: bool):
        self.fields = [[' O |' for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.hid = hid
        self.ships_alive = 7
        self.shoot_list = []
        self.all_ships_dots = []

    def add_ship(self, ship: Ship):
        '''Метод принимает аргумент ship класса Ship и бобавляет на доску в случае, если
        между кораблями есть хотя бы 1 пустая клетка, не этих полях нет кораблей и координаты точек
        корабля находятся в пределах игорового поля иначе вызывает соответственное исключение'''

        neibs = self.contour(ship)
        is_neib_fill = any([self.fields[dot.y][dot.x] == ' \u25A0 |' for dot in neibs])
        is_out = any([self._out(dot) for dot in ship.dots])
        is_occupied = any([dot in self.all_ships_dots for dot in ship.dots])
        if not is_out and len(self.ships) <= 7 and not is_neib_fill and not is_occupied:
            self.ships.append(ship)
            self.all_ships_dots.extend(ship.dots)
            for dot in ship.dots:
                self.fields[dot.y][dot.x] = ' \u25A0 |'
        if is_occupied:
            raise FieldIsOcupiedException
        if is_neib_fill:
            raise ShipIsInTouchException
        if is_out:
            raise ShipIsNotOnBoardException


    @staticmethod
    def _out(dot: Dot) -> bool:
        '''Метод принимает аргумент dot класса Dot и проверяет являются ли
        координаты точки координатами в пределах ирового поля возвращает True или False'''
        return dot.x not in [i for i in range(6)] or dot.y not in [i for i in range(6)]

    def contour(self, ship: Ship) -> list:
        '''Метод принимает аргумент ship класса Ship и возвращает список точек класса Dot,
        окружающих корабль но не выходящих за поле'''
        contour_list = []
        neibs = (-1, 0, 1)
        for dot in ship.dots:
            for n in neibs:
                for j in neibs:
                    dot_ex = Dot(dot.x + n, dot.y + j)
                    if dot_ex not in ship.dots and not self._out(dot_ex) and dot_ex not in contour_list:
                        contour_list.append(dot_ex)
        return contour_list

    def print_board(self) -> None:
        '''Метод выводит в консоль графическое представление игровой доски с кораблями и выстрелами'''
        j = 1
        string_el = ''
        if not self.hid:
            for i in range(1, 7):
                if i == 1:
                    print(f'  | {i} ', end='|')
                else:
                    print(f' {i} ', end='|' )
            print('\n')
            for field in self.fields:
                string_el += str(j) + ' |'
                for item in field:
                    string_el += item
                print(f'{string_el}\n')
                string_el = ''
                j += 1

    def shoot(self, x: int, y: int, board = None) -> bool:
        '''Метод принимает координаты точки поля x и y и в случае вызова от лица пользователя
        аргумент board класса если отсутствует принимает значение None в случае попадания в корабль
        соперника возращает True в обратном случае False'''
        dot = Dot(x - 1, y - 1)
        if self._out(dot):
            raise ShootIsNotOnBoardException
        elif dot in self.shoot_list:
            raise DoubleShootException
        else:
            good_shoot = False
            if dot not in self.shoot_list and self.fields[dot.y][dot.x] == ' T |':
                good_shoot = True
                raise ContourShootException
            self.shoot_list.append(dot)
            if dot not in self.all_ships_dots:
                print('Мимо!')
                self.fields[dot.y][dot.x] = ' T |'
                if board:
                    board.fields[dot.y][dot.x] = ' T |'
            else:
                for ship in self.ships:
                    if dot in ship.dots:
                        if ship.lifes > 1:
                            ship.lifes -= 1
                            print('Ранен!')
                            self.fields[dot.y][dot.x] = ' X |'
                            if board:
                                board.fields[dot.y][dot.x] = ' X |'
                        else:
                            print('Убит!')
                            self.ships_alive -= 1
                            self.fields[dot.y][dot.x] = ' X |'
                            if board:
                                board.fields[dot.y][dot.x] = ' X |'
                            for cont in self.contour(ship):
                                self.fields[cont.y][cont.x] = ' T |'
                                if board:
                                    board.fields[cont.y][cont.x] = ' T |'
                        self.all_ships_dots.remove(dot)
                        good_shoot = True
            if board:
                board.print_board()
            else:
                self.print_board()
            return good_shoot


class Player:
    def ask(self):
        pass

    def move(self):
        pass


class AI(Player):
    def __init__(self, my_board, enemy_board):
        self.enemy_board = enemy_board
        self.my_board = my_board

    def ask(self):
        '''Метод возвращает случайные координаты поля доски'''
        return random.randint(1, 6), random.randint(1, 6)

    def move(self):
        '''Метод производит ход компьютера возвращает None'''
        while True:
            try:
                x, y = self.ask()
                return self.enemy_board.shoot(x, y)
            except:
                continue


class User(Player):
    def __init__(self, my_board, enemy_board):
        self.enemy_board = enemy_board
        self.my_board = my_board
        self.clone_board = Board(False)

    def ask(self):
        '''Метод запрашивает у пользователя и возвращает случайные координаты поля доски случае ввода
        значений не являющимися целыми числами выводит сообщение об ошибке'''
        try:
                x = int(input('Ваш выстрел, введите координату по горизонтали от 1 до 6: '))
                y = int(input('Ваш выстрел, введите координату по вертикале от 1 до 6: '))
                return x, y
        except:
                print('Ввести можно только числа от 1 до 6')

    def move(self):
        '''Метод производит ход пользователя'''
        while True:
            try:
                x, y = self.ask()
                return self.enemy_board.shoot(x, y, self.clone_board)
            except ShootIsNotOnBoardException:
                print('Числа должны быть от 1 до 6')
                continue
            except DoubleShootException:
                print('Вы уже стреляли в это поле')
                continue
            except ContourShootException:
                print('В этом поле не может быть корабля иначе он будет соприкосаться с уже подбитым кораблем')
                continue
            except:
                print('Ввести можно только числа от 1 до 6')
                continue


class GameControler:
    @staticmethod
    def check_board(board: Board) -> bool:
        '''Метод принимает аргумент board класса Board и проверяет что
        на доске установлены все корабли возвращает True или False'''
        return len(board.ships) == len(SIZES)

    @staticmethod
    def check_direction(dir: str) -> bool:
        '''Метод принимает аргумент dir - направление, которое ввел пользователь
         и проверяет что это допустимый ввод возвращает True или False'''
        directions = ["влево", "вправо", "вниз", "вверх"]
        return dir.lower().strip() in directions


class Game:
    def __init__(self):
        self.ai_board = None
        self.user_board = None
        self.user = None
        self.ai = None

    def random_board(self) -> None:
        '''Метод расставляет случайныим образом корабли на доске'''
        direction = ['up', 'right', 'down', 'left']
        self.ai_board = Board(True)
        for index, size in enumerate(SIZES):
            i = 0
            while i < 1000:
                i += 1
                try:
                    d = random.choice(direction)
                    x = random.randint(0, 6)
                    y = random.randint(0, 6)
                    ship = Ship(size, Dot(x, y), d)
                    self.ai_board.add_ship(ship)
                    break
                except:
                    continue

    def create_user_board(self) -> None:
        '''Метод запрашивает у пользователя координаты начальной точки и направление построения корабля
        и проверяет возможно ли разместить его на доске если нет поднимает соответствующую ошибку'''
        directions = {
                        'вверх': 'up',
                        'вправо': 'right',
                        'вниз': 'down',
                        'влево': 'left'
                     }
        self.user_board = Board(False)
        self.user_board.print_board()
        for j, size in enumerate(SIZES):
            while len(self.user_board.ships) != j + 1:
                print(f'Ставим корабли размера { size }')
                try:
                    x = int(input('Введите коррдинату начальной точки по горизонтали от 1 до 6: '))
                    y = int(input('Введите коррдинату начальной точки по вертикале от 1 до 6: '))
                    if size == 1:
                        dir = "влево"
                    else:
                        dir = input("""Введите направление куда строить корабль -
                                        если горизонтально, то "влево" или "вправо", если вертикально - "вниз"
                                        или "вверх": """"").lower().strip()
                    if GameControler.check_direction(dir):
                        direction = directions.get(dir)
                        ship = Ship(size, Dot(x - 1, y - 1), direction)
                        self.user_board.add_ship(ship)
                        self.user_board.print_board()
                    else:
                        raise WrongDirectionException
                except ShipIsNotOnBoardException:
                    print('Данные введены неверно - Корабль выходит за пределы поля')
                    continue
                except ShipIsInTouchException:
                    print('Данные введены неверно - Корабль не может соприкасаться с другими кораблями')
                    continue
                except FieldIsOcupiedException:
                    print('Данные введены неверно - В этих ячейках уже есть корабли')
                    continue
                except WrongDirectionException:
                    print('Данные введены неверно - неверно введено направление построения корабля')
                    continue
                except ValueError:
                    print('Коррдината начальной точки должна быть числом от 1 до 6')
                    continue
                except BoardOutException:
                    print('Коррдината начальной точки должна быть числом от 1 до 6')
                    continue
                except:
                    print('Данные введены неверно')
                    continue

    @staticmethod
    def greet():
        '''Метод выводит преветственное сообщение и правила'''
        print("""Игра началась! Для начала тебe нужно расставить 7 кораблей
            1 - трехпалубный 2 - двухпалубного и 4 - однопалубные""")
        print("""Для ввода положения корабля тебе нужно по запросу ввести 1) Коррдинаты начальной точки
            по горизонтали и по вертикали цифрами от 1 до 6 2) выбрать как от этой точке расположить корабль -
            если горизонтально введи - "гор", если вертикально - "вер" и направление куда строить корабль -
            если горизонтально, то "влево" или "вправо", если вертикально - "вниз"  или "вверх"
            смотри чтобы корабль не выходил за пределы поля - такой корабль мы не сможем построить - 
            придется вводить заново""")

    def loop(self) -> None:
        '''Метод производит ход соперников пока не наступает случай окончания игры'''
        step = 'user'
        while self.ai_board.ships_alive >= 1 and self.user_board.ships_alive >= 1:
            if step == 'user':
                print('Ваш ход!')
                step = 'user' if self.user.move() else 'ai'
            if step == 'ai':
                print('Ход вашего соперника!')
                step = 'ai' if self.ai.move() else 'user'


    def start(self) -> None:
        '''Метод запускает игру'''
        self.greet()
        self.random_board()
        if not GameControler.check_board(self.ai_board):
            print('Сожалеем, игра не может быть запущена, ваш соперник не может расставить корабли')
        else:
            self.create_user_board()
            self.user = User(self.user_board, self.ai_board)
            self.ai = AI(self.ai_board, self.user_board)
            self.loop()
            print('Игра закончилась!')
            if self.ai_board.ships_alive == 0:
                print('Вы победили!')
            else:
                print('Вы проиграли!')

game = Game()
game.start()




















