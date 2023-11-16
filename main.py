
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


ROWS = 5
COLUMNS = 5


class FieldCell:
    def __init__(self, x: int, y: int, image='.') -> None:
        self.image = image
        self.y = y
        self.x = x
        self.content = None 

    def __str__(self):
        return self.image


class Player:
    def __init__(self, x=0, y=0, image='@') -> None:
        self.x = x
        self.y = y
        self.image = image

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

    def generate_field(self) -> None:
        self.cells = [
            [FieldCell(x, y) for x in range(self.columns)] for y in range(self.rows)
        ]
        self.cells[self.player.y][self.player.x].content = self.player 

    def draw_field(self) -> None:
        for row in self.cells:
            for cell in row:
                if cell.content:
                    print(cell.content.image, end='')
                else:
                    print('.', end='')
            print('\n')


player = Player()
field = Field(COLUMNS, ROWS, player=player)
player.x, player.y = field.columns // 2, field.rows // 2
field.generate_field()
field.draw_field()
