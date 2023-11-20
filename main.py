import os
import keyboard

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


class FieldCell:
    def __init__(self, x: int, y: int, image='.') -> None:
        self.image = CELL_IMAGE
        self.y = y
        self.x = x
        self.content = None

    def __str__(self):
        return self.image

    def draw(self) -> None:
        if self.content:
            print(self.content.image, end='')
        else:
            print(self.image, end='')


class Player:
    def __init__(self, x=0, y=0, image='@') -> None:
        self.x = x
        self.y = y
        self.image = PLAYER_IMAGE

    def move(self) -> None:
        pass

    def __str__(self) -> str:
        return self.image


class Field:
    def __init__(self,
                 columns: int,
                 rows: int,
                 player: Player) -> None:
        self.columns = columns
        self.rows = rows
        self.player = player
        self.cells = []

    def move_player(self) -> None:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'right' and self.player.x < COLUMNS - 1:
                self.player.x += 1
            if event.name == 'left' and self.player.x > 0:
                self.player.x -= 1
            if event.name == 'up' and self.player.y > 0:
                self.player.y -= 1
            if event.name == 'down' and self.player.y < ROWS - 1:
                self.player.y += 1

    def generate_field(self) -> list:
        self.cells = [
            [FieldCell(x, y) for x in range(self.columns)] for y in range(self.rows)
        ]
        self.cells[self.player.y][self.player.x].content = self.player

    def draw_field(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.draw()
            print('')


class Game:
    def __init__(self) -> None:
        self.player = Player(y=ROWS // 2,
                             x=COLUMNS // 2)
        self.field = Field(ROWS, COLUMNS, self.player)
        self.is_running = True

    def run(self) -> None:
        while self.is_running:
            self.field.draw_field()
            self.field.move_player()
            self.update()
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

    def update(self) -> None:
        self.field.generate_field()


game = Game()
game.run()
'''player = Player()
field = Field(COLUMNS, ROWS, player=player)
player.x, player.y = field.columns // 2, field.rows // 2
field.generate_field()
field.draw_field()'''
