import os
import keyboard
from random import randint
import abc

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


ROWS = 10
COLUMNS = 10
CELL_IMAGE = '.'
PLAYER_IMAGE = 'P'
ANTHILL_IMAGE = 'A'
ANT_IMAGE = 'a'
MAX_ANTHILLS = 4
MIN_ANTHILLS = 1


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
        Конструктор класса

        Аргументы:
            x: int - координата x
            y: int - координата y
            image: str - символ, представляющий объект
        '''
        self.image = PLAYER_IMAGE
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

    def generate_field(self) -> None:
        '''
        Метод генерирующий поле со всеми объектами
        '''
        self.cells = [
            [FieldCell(x, y) for x in range(self.columns)] for y in range(self.rows)
        ]
        for anthill in self.anthills:
            self.cells[anthill.y][anthill.x].content = anthill
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
                if not self.cells[self.player.y][self.player.x + 1].content:  # возможно плохой подход - муравей тоже может быть content` ом клетки
                    self.player.x += 1
            if event.name == 'left' and self.player.x > 0:
                if not self.cells[self.player.y][self.player.x - 1].content:
                    self.player.x -= 1
            if event.name == 'up' and self.player.y > 0:
                if not self.cells[self.player.y - 1][self.player.x].content:
                    self.player.y -= 1
            if event.name == 'down' and self.player.y < self.rows - 1:
                if not self.cells[self.player.y + 1][self.player.x].content:
                    self.player.y += 1


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
            self.field.move_player()
            self.field.generate_field()


game = Game()
game.run()
