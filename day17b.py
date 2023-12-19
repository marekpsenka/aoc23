import fileinput
from indexed_priority_queue import IndexedPriorityQueue  # type: ignore
from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict
import math


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    def opposite(self) -> "Direction":
        match self:
            case Direction.Up:
                return Direction.Down
            case Direction.Down:
                return Direction.Up
            case Direction.Right:
                return Direction.Left
            case Direction.Left:
                return Direction.Right


Point = tuple[int, int]


def move(p: Point, dir: Direction) -> Point:
    match dir:
        case Direction.Up:
            return (p[0] - 1, p[1])
        case Direction.Down:
            return (p[0] + 1, p[1])
        case Direction.Left:
            return (p[0], p[1] - 1)
        case Direction.Right:
            return (p[0], p[1] + 1)


def within_bounds(i: int, j: int, max_i: int, max_j: int) -> bool:
    if i < 0:
        return False
    elif i >= max_i:
        return False
    elif j < 0:
        return False
    elif j >= max_j:
        return False
    else:
        return True


@dataclass(frozen=True)
class State:
    p: Point
    last_dir: Direction
    steps_in_last_dir: int

    def possible_dirs(self) -> set[Direction]:
        if self.steps_in_last_dir >= 1 and self.steps_in_last_dir < 4:
            return {self.last_dir}
        dirs = {Direction.Up, Direction.Down, Direction.Right, Direction.Left}
        dirs.remove(self.last_dir.opposite())
        if self.steps_in_last_dir == 10:
            dirs.remove(self.last_dir)

        return dirs

    def derive(self, new_p: Point, new_dir: Direction) -> "State":
        if new_dir == self.last_dir:
            return State(new_p, new_dir, self.steps_in_last_dir + 1)
        else:
            return State(new_p, new_dir, 1)


input = list(
    map(lambda line: list(map(int, str.rstrip(line))), fileinput.input())
)

max_i = len(input)
max_j = len(input[0])


pq = IndexedPriorityQueue()
init_state = State((0, 0), Direction.Right, 0)
pq.push(init_state, 0)
minimum = None
current_lowest: defaultdict[State, float] = defaultdict(lambda: math.inf)
current_lowest[init_state] = 0

while not len(pq) == 0:
    s, heat_loss = pq.pop()
    if s.p == (max_i - 1, max_j - 1):
        minimum = heat_loss
        break

    for dir in s.possible_dirs():
        new_p = move(s.p, dir)
        if not within_bounds(new_p[0], new_p[1], max_i, max_j):
            continue

        new_heat_loss = current_lowest[s] + input[new_p[0]][new_p[1]]
        new_s = s.derive(new_p, dir)

        if new_heat_loss < current_lowest[new_s]:
            current_lowest[new_s] = new_heat_loss
            pq.push(new_s, new_heat_loss)

print(minimum)
