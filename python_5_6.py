def field_paint():
    print("   0 1 2")
    for col, row in enumerate(field):
        row_info = f" {col} {' '.join(row)}"

        print(row_info)

def check_win():
    win_sit = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)),
               ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for sit in win_sit:
        side = []
        for c in sit:
            side.append(field[c[0]][c[1]])
        if side == ["X", "X", "X"]:
            print("X win")
            return True
        if side == ["0", "0", "0"]:
            print("0 win")
            return True
    return False


def turn():
    while True:
        coord = input("Your turn ").split()

        if len(coord) != 2:
            print("Write only 2 coordinates pls")
            continue

        x, y = coord

        if not (x.isdigit()) or not (y.isdigit()):
            print("Please input only numbers")
            continue

        x, y = int(x), int(y)

        if x < 0 or x > 2 or y < 0 or y > 2:
            print("Please input number inside the field")
            continue

        if field[x][y] != " ":
            print("Please choose free coordinates")
            continue

        return x, y

field = []
for i in range(3):
    field.append([" "," "," "])
count = 0
while True:
    count += 1
    field_paint()

    x, y = turn()

    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"

    if check_win():
        break

    if count >= 9:
        print(" Draw!")
        break
