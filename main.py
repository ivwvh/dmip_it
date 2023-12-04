import os
import keyboard
from typing import List, Tuple
from random import choice, randint
from time import sleep

"""
Необходимо реализовать игру «Ловкий муравьед».
Главный герой – голодный, но очень ловкий муравьед бегает по двумерному полю от
одного муравейника к другому и вылавливает убегающих за границу экрана муравьёв.
Необходимо реализовать консольное приложение-игру с текстовым
псевдографическим интерфейсом (графика может быть реализована при помощи
любых текстовых и псевдографических символов). Пользователь должен управлять
объектом-муравьедом, перемещаемым по двумерному полю (с препятствиями).
Управляемый объект обладает способностью поедать объекты муравьёв,
появляющихся из объектов-муравейников, разбросанных на поле. При появлении
муравьи хаотично перемещаются по полю. Если муравей соприкасается с границей
поля, то он считается упущенным и пропадает с поля. От соприкосновения муравьеда
с муравьём – последний исчезает, а игроку начисляется 1 балл. Муравейники на поле
размещаются случайным образом в количестве до 4 штук. В каждом муравейнике
могут прятаться до 10 муравьёв. Как только на поле все муравьи оказываются съедены
или упущены, игра завершается. По завершению игры результаты игровой сессии
выводятся на экран.

муравей
муравьед
муравейник
поле
клетка поля
"""


ROWS = 20 
COLUMNS = 20
CELL_IMAGE = '.'
PLAYER_IMAGE = 'P'
ANTHILL_IMAGE = 'A'
ANT_IMAGE = 'a'
ANT_IMAGE = 'a'
MAX_ANTHILLS = 10
MIN_ANTHILLS = 1
MAX_ANTS = 5




class GameObject:
    '''
    Базовый класс для создания игровых объектов

    Атрибуты:
        x: int - координата x
        y: int - координата y
    '''
    
    def __init__(self, y, x, image) -> None:
        '''
        Конструктор класса
    
        Аругменты:
            x: int - координата x
            y: int - координата y
            image: str - символ, представляющий объект
        '''
        self.y = y
        self.x = x
        self.image = image


class FieldCell:
    '''
    Класс представляющий клетку поля
    
    Атрибуты:
        x: int - координата x
        y: int - координата y
        image: str - символ, представляющий объект
        content: Any - объект находящийся на клетке
    '''
    
    def __init__(self, x: int, y: int) -> None:
        '''
        Конструктор класса

        Аругменты:
            x: int - координата x
            y: int - координата y
            
        '''
        self.image = CELL_IMAGE
        self.y = y
        self.x = x
        self.content = None

    def draw(self) -> None:
        '''
        Метод выводящитй содеримое клетки на экран
        '''
        if self.content:
            print(self.content.image, end='')
        else:
            print(self.image, end='')


class AntHill(GameObject):
    '''
    Объект представляющий муравейник, является дочерним классом от GameObject


    Атрибуты:
        x: int - координата x
        y: int - координата y

    '''
    
    def __init__(self, y, x) -> None:
        '''
        Конструктор класса

        Аргументы:
            x: int - координата x
            y: int - координата y
            image: str - символ, представляющий объект
        '''
        self.image = ANTHILL_IMAGE
        self.ants = [Ant(0, 0) for _ in range(MAX_ANTS)]
        super().__init__(y, x, self.image)


class Ant(GameObject):
    def __init__(self, x: int, y: int) -> None:
        self.image = ANT_IMAGE
        super().__init__(y, x, self.image)


class Player(GameObject):
    '''
    Объект представляющий игрока, является дочерним классом от GameObject


    Атрибуты:
       x: int - координата x
       y: int - координата y

    '''

    def __init__(self, y, x) -> None:
        '''
        Конструктор классаinput 

        Аргументы:
            x: int - координата x
            y: int - координата y
            image: str - символ, представляющий объект
        '''
        self.image = PLAYER_IMAGE
        self.eaten_ants = 0
        self.ran_away = 0
        super().__init__(y, x, self.image)


class Field:
    '''
    Объект представляющий игровое поле
    
    Атрибуты:
        columns: int - кол-во колонн поля
        rows: int - кол-во рядов поля
        player: Player - игрок
        anthills: List[AntHill] - список всех муравейников и их координат
        cells: List[FieldCell] - список всех клеток и их координат
    '''
    
    def __init__(self,
                 columns: int,
                 rows: int,
                 player: Player) -> None:
        '''
        Конструктор класса 

        Аргументы:
            columns: int - кол-во колонн поля
            rows: int - кол-во рядов поля
            player: Player - игрок
        '''

        self.columns = columns
        self.rows = rows
        self.player = player
        self.anthills = []
        self.cells = []
        self.ants = []

    def generate_field(self) -> None:
        '''
        Метод генерирующий поле со всеми объектами
        '''
        self.cells = [
            [FieldCell(x, y) for x in range(self.columns)] for y in range(self.rows)
        ]
        for anthill in self.anthills:
            self.cells[anthill.y][anthill.x].content = anthill
        for ant in self.ants:
            self.cells[ant.y][ant.x].content = ant
        self.cells[self.player.y][self.player.x].content = self.player

    def draw_field(self) -> None:
        '''
        Метод выводящий поле на экран
        ''' 
        for row in self.cells:
            for cell in row:
                cell.draw()
            print('')

    def generate_anthills(self) -> None:
        '''
        Метод генерирующий муравейники
        '''
        used_cords = [(i.y, i.x) for i in self.anthills if len(self.anthills) > 0]
        anthill_y = randint(0, self.rows - 1)
        anthill_x = randint(0, self.columns - 1)
        if not (anthill_y, anthill_x) in used_cords:
            if not (anthill_y, anthill_x) == (self.player.y, self.player.x):
                self.anthills.append(AntHill(y=anthill_y,
                                             x=anthill_x))
            else:
                return self.generate_anthills()
        else:
            return self.generate_anthills()

        if len(self.anthills) < MAX_ANTHILLS:
            return self.generate_anthills()

    def move_player(self) -> None:
        '''
        Метод перемещающий игрока по полю
        '''
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'right' and self.player.x < self.columns - 1:
                if isinstance(self.cells[self.player.y][self.player.x + 1].content, Ant):
                    cell_content = self.cells[self.player.y][self.player.x + 1].content
                    ant_index = self.ants.index(cell_content)
                    self.ants.pop(ant_index)
                    self.player.eaten_ants += 1
                    self.player.x += 1
                    return

                if not self.cells[self.player.y][self.player.x + 1].content: 
                    self.player.x += 1

            if event.name == 'left' and self.player.x > 0:
                if isinstance(self.cells[self.player.y][self.player.x - 1].content, Ant):
                    cell_content = self.cells[self.player.y][self.player.x - 1].content
                    ant_index = self.ants.index(cell_content)
                    self.ants.pop(ant_index)
                    self.player.eaten_ants += 1
                    self.player.x -= 1
                    return
                if not self.cells[self.player.y][self.player.x - 1].content:
                    self.player.x -= 1

            if event.name == 'up' and self.player.y > 0:
                if isinstance(self.cells[self.player.y - 1][self.player.x].content, Ant):
                    cell_content = self.cells[self.player.y - 1][self.player.x].content
                    ant_index = self.ants.index(cell_content)
                    self.ants.pop(ant_index)
                    self.player.eaten_ants += 1
                    self.player.y -= 1
                    return

                if not self.cells[self.player.y - 1][self.player.x].content:
                    self.player.y -= 1

            if event.name == 'down' and self.player.y < self.rows - 1:
                if isinstance(self.cells[self.player.y + 1][self.player.x].content, Ant):
                    cell_content = self.cells[self.player.y + 1][self.player.x].content
                    ant_index = self.ants.index(cell_content)
                    self.ants.pop(ant_index)
                    self.player.eaten_ants += 1
                    self.player.y += 1
                    return

                if not self.cells[self.player.y + 1][self.player.x].content:
                    self.player.y += 1

    def get_neighbours(self, y: int, x: int) -> list:
        all_neighbours = [
            (y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
            (y, x - 1), (y, x + 1),
            (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)
        ]
        possible_neighbours = []
        for y, x in all_neighbours:
            if x > 0 and x < self.columns and y > 0 and y < self.rows:
                if not self.cells[y][x].content:
                    possible_neighbours.append((y, x))

        return possible_neighbours
    
    def spawn_ants(self) -> None:
        anthill = choice(self.anthills)
        if anthill.ants:
            neighbours = self.get_neighbours(anthill.y,
                                             anthill.x)
            ant = anthill.ants[0]
            if neighbours:
                position = choice(neighbours)
            else:
                return
            ant.y, ant.x = position
            self.ants.append(anthill.ants.pop(0))

    def move_ants(self) -> None:
        for index, ant in enumerate(self.ants):
            match(randint(0, 3)):
                case 0:
                    if ant.x > 0 and ant.x < COLUMNS - 1:
                        if randint(0, 1):
                            if not self.cells[ant.y][ant.x + 1].content:
                                ant.x += 1
                        else:
                            if not self.cells[ant.y][ant.x - 1].content:
                                ant.x -= 1
                    else:
                        self.ants.pop(index)
                        self.player.ran_away += 1
                case 1:
                    if ant.y > 0 and ant.y < ROWS - 1:
                        if randint(0, 1):
                            if not self.cells[ant.y + 1][ant.x].content:
                                ant.y += 1
                        else:
                            if not self.cells[ant.y - 1][ant.x].content:
                                ant.y -= 1
                    else:
                        self.ants.pop(index)
                        self.player.ran_away += 1
                case 3:
                    pass


class Game:
    '''
    Класс представляющий игру
    
    Атрибуты:
        player: Player - игрок
        field: Field - игровое поле
        is_running: bool - переменная отвечающая за то запущена ли игра

    '''

    def __init__(self) -> None:
        '''
        Конструктор класса
        '''
        self.player = Player(y=ROWS // 2,
                             x=COLUMNS // 2)
        self.field = Field(ROWS, COLUMNS, self.player)
        self.field.generate_anthills()
        self.field.generate_field()
        self.field.draw_field()
        self.is_running = True

    def run(self) -> None:
        '''
        Основной цикл событий
        '''
        while self.is_running:

            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            self.field.draw_field()
            self.field.spawn_ants()
            print(f'Набрано очков {self.player.eaten_ants}')
            print(f'Сбежало {self.player.ran_away}')
            sleep(0.08)
            self.field.move_player()
            self.field.move_ants()
            self.field.generate_field()


game = Game()
game.run()
