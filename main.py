from enum import Enum

Relation = Enum('Relation', ['UP_LEFT', 'UP', 'UP_RIGHT', 'LEFT', 'RIGHT', 'DOWN_LEFT', 'DOWN', 'DOWN_RIGHT', 'NONE'])

class Point:
    def __init__(self, r: int, c: int):
        self.r = r
        self.c = c

    def __str__(self):
        return f'Point<r:{self.r},c:{self.c}>'
    
    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    def getRelation(self, first: Point, second: Point) -> Relation:
        if first.r == second.r:
            


def isValidPoint(puzzle: list[list[str]], point: Point) -> bool:
    return point.r >= 0 and point.c >= 0 and point.r <= len(puzzle) and point.c <= len(puzzle[0])


# def findWord(puzzle: list[list[str]], word: str) -> list[Point]:
#     for r in puzzle:
#         for c in r:
#             if c == word[0]:


def getSurrounding(puzzle: list[list[str]], p: Point) -> list[Point]:
    points = []
    for r in range(p.r-1, p.r+2):
        for c in range(p.c-1, p.c+2):
            if not (Point(r,c) == p) and isValidPoint(puzzle, Point(r, c)):
                points.append(Point(r, c))

    return points


def get_puzzle(path: str) -> list[list[str]]:
    board = []
    with open(path, encoding="utf8") as f:
        for r in f.readlines():
            row = list(r.strip())
            board.append(row)

    return board

def main():
    puzzle = get_puzzle("./puzzle.txt")
    print(puzzle)

    point = Point(1,2)
    print(point.r)

    for p in getSurrounding(puzzle, Point(1, 1)):
        print(p)

main()
