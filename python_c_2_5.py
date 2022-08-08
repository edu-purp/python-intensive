from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, len, dir):
        self.bow = bow
        self.len = len
        self.dir = dir
        self.lives = len

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.len):
            x_1 = self.bow.x
            y_1 = self.bow.y

            if self.dir == 0:
                x_1 += i

            elif self.dir == 1:
                y_1 += i

            ship_dots.append(Dot(x_1, y_1))

        return ship_dots

    def hit(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)


    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Ship destroyed!")
                    return False
                else:
                    print("You hit it!")
                    return True

        self.field[d.x][d.y] = "."
        print("You missed!")
        return False

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Computer turn: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Your turn: ").split()

            if len(cords) != 2:
                print("Please input the coordinates ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Please input the numbers")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Please shoot inside the board. Board have size 6x6"

class BoardUsedException(BoardException):
    def __str__(self):
        return "You shot this cell before!"

class BoardWrongShipException(BoardException):
    pass


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board


    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("User board:")
            print(self.us.board)
            print("-" * 20)
            print("Computer board:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("User turn")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Computer turn")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("You WIN!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Computer WIN!")
                break
            num += 1

    def start(self):
        self.loop()


g = Game()
g.start()