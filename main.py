from enum import Enum

Relation = Enum('Relation', ['UP_LEFT', 'UP', 'UP_RIGHT', 'LEFT', 'RIGHT', 'DOWN_LEFT', 'DOWN', 'DOWN_RIGHT', 'SAME'])

class WordNotFoundException(Exception):
    pass

class Point:
    def __init__(self, r: int, c: int):
        self.r = r
        self.c = c

    def __str__(self):
        return f'Point<r:{self.r},c:{self.c}>'
    
    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    def is_valid(self, puzzle: list[list[str]]) -> bool:
        return self.r in range(len(puzzle)) and self.c in range(len(puzzle[0]))

    def get_related(self, r: Relation):
        match r:
            case Relation.UP:
                return Point(self.r-1, self.c)
            case Relation.DOWN:
                return Point(self.r+1, self.c)
            case Relation.RIGHT:
                return Point(self.r, self.c+1)
            case Relation.LEFT:
                return Point(self.r, self.c-1)
            case Relation.UP_LEFT:
                return Point(self.r-1, self.c-1)
            case Relation.UP_RIGHT:
                return Point(self.r-1, self.c+1)
            case Relation.DOWN_LEFT:
                return Point(self.r+1, self.c-1)
            case Relation.DOWN_RIGHT:
                return Point(self.r+1, self.c+1)
            

def get_point_value(puzzle: list[list[str]], point: Point) -> str:
    return puzzle[point.r][point.c]

def get_points_values(puzzle: list[list[str]], points: list[Point]) -> list[str]:
    return [get_point_value(puzzle, point) for point in points]

def get_relation(first: Point, second: Point) -> Relation:
    if first == second:
        return Relation.SAME
    if first.c == second.c:
        return Relation.UP if first.r > second.r else Relation.DOWN
    if first.r == second.r:
        return Relation.RIGHT if first.c < second.c else Relation.LEFT
    if first.c < second.c:
        return Relation.DOWN_LEFT if first.r > second.c else Relation.DOWN_RIGHT
    if first.c > second.c:
        return Relation.UP_LEFT if first.r < second.c else Relation.UP_RIGHT
    


def try_find(puzzle: list[list[str]], first: Point, relation: Relation, word: list[str]) -> list[Point]:
    """This function will go as far as it can as long as the word matches."""
    # NOTE: If you wanted to make this project work for funky crossword dimensions, you'd probably want to move is_valid_point check here
    solution = []

    p = first
    for l in word:
        if p.is_valid(puzzle) and get_point_value(puzzle, p) == l:
            solution.append(p)
            p = p.get_related(relation)
        else:
            raise WordNotFoundException

    return solution


def find_word(puzzle: list[list[str]], word: str) -> list[Point]:
    for rc, r in enumerate(puzzle):
        for cc, c in enumerate(r):
            if c == word[0]:
                first = Point(rc, cc)
                for p in get_surrounding(puzzle, first):
                    if get_point_value(puzzle, p) == word[1]:
                        second = p
                        relation = get_relation(first, second)
                        try:
                            a = try_find(puzzle, first, relation, list(word))
                            return a
                        except WordNotFoundException:
                            continue

    raise WordNotFoundException


def get_surrounding(puzzle: list[list[str]], p: Point) -> list[Point]:
    points = []
    for r in range(p.r-1, p.r+2):
        for c in range(p.c-1, p.c+2):
            if not (Point(r,c) == p) and Point(r, c).is_valid(puzzle):
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


    f = find_word(puzzle, "COT")
    for p in f:
        print(f"p: {p}, v: {get_point_value(puzzle, p)}")

main()
