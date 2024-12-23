from array import array 
from typing import Optional, Iterable, Union
from enum import Enum

Point = tuple[int, int]

class Direction(Enum):
    '''
    2D Coordinate directions, assuming top-left origin.
    '''
    NORTHWEST = (-1, -1)
    NORTH = (0, -1)
    NORTHEAST = (1, -1)
    EAST = (1, 0)
    WEST = (-1, 0)
    SOUTHEAST = (1, 1)
    SOUTH = (0, 1)
    SOUTHWEST = (-1, 1)

    def __lt__(self, other):
        return self.value < other.value

class CharGrid:
    '''
    Equal width character grid, with top-left origin.
    Movement will step out of bounds, unless wrap_grid
    is set to True.
    '''
    def __init__(self, source: Iterable[str], wrap_grid: bool = False):
        self.height = 0
        self.width = 0
        self._grid = array('u')
        self.wrap = wrap_grid
        for line in source:
            line = line.strip()
            if (self.width > 0) and (self.width != len(line)):
                raise ValueError(f"Different size grid widths found {self.width} & {len(line)}")
            self.width = len(line)
            self.height += 1
            self._grid.extend(line)
    
    @staticmethod
    def empty_grid(height: int, width: int, init_char: str, wrap_grid: bool = False):
        if 0 > len(init_char) > 1:
            raise ValueError(f"Expected single character initializer but found {init_char}")
        def _empty_row(h, w, c):
            cur_height = 0
            row = c * w
            while cur_height < h:
                yield row
                cur_height += 1
        return CharGrid(_empty_row(height, width, init_char), wrap_grid)

    def index(self, x: int, y: int) -> Optional[int]:
        if self.wrap:
            x, y = x % self.width, y % self.height
        if self.inbound(x, y):
            return x + (y * self.width)
        return None

    def __getitem__(self, coord: Point) -> Optional[str]:
        x, y = coord
        idx = self.index(x, y)
        if idx is not None:
            return self._grid[idx]
        return None

    def __setitem__(self, coord: Point, value: str) -> None:
        x, y = coord
        idx = self.index(x, y)
        self._grid[idx] = value

    def __str__(self) -> str:
        lines = (
            ''.join(self._grid[row * self.width:(row + 1) * self.width])
            for row in range(self.height)
        )
        return '\n'.join(lines)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CharGrid):
            raise NotImplementedError()
        return (
            self.width == other.width and
            self.height == other.height and
            self._grid == other._grid
        )

    def inbound(self, x: int, y: int) -> bool:
        if (0 <= x <= (self.width - 1)) and (0 <= y <= self.height - 1):
            return True
        return False
    
    def step_coord(self, coord: Point, dir: Union[Direction, Point], steps: int = 1) -> Optional[Point]:
        start_x, start_y = coord
        step_x, step_y = dir.value if isinstance(dir, Direction) else dir
        step_x, step_y = step_x * steps, step_y * steps
        return start_x + step_x, start_y + step_y

    def step(self, coord: Point, dir: Union[Direction, Point], steps: int = 1) -> Optional[Point]:
        next_x, next_y = self.step_coord(coord, dir, steps)
        return self[next_x, next_y]

class StringCharIterator:
    def __init__(self, string):
        self.string = string
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.string):
            raise StopIteration
        char = self.string[self.index]
        self.index += 1
        return char

    def reset(self):
        self.index = 0
    
    def has_next(self):
        return self.index < len(self.string)