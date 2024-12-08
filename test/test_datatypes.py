import pytest

from twenty_twentyfour.datatypes import CharGrid, Direction, StringCharIterator

FOUR_BY_THREE_GRID = (
        'abcd',
        'efgh',
        'ijkl'
    )
UNEVEN_GRID = (
    'abcd',
    'efgh',
    'lmnop'
)

def test_width_height():
    g = CharGrid(FOUR_BY_THREE_GRID)
    assert g.width == 4
    assert g.height == 3

def test_uneven_grid():
    with pytest.raises(ValueError):
        CharGrid(UNEVEN_GRID)

def test_empty_grid():
    g = CharGrid(list())
    assert g.height == 0
    assert g.width == 0

def test_indexing():
    g = CharGrid(FOUR_BY_THREE_GRID)
    assert g[0,0] == 'a'
    assert g[1,0] == 'b'
    assert g[2,0] == 'c'
    assert g[3,0] == 'd'
    assert g[0,1] == 'e'
    assert g[1,1] == 'f'
    assert g[2,1] == 'g'
    assert g[3,1] == 'h'
    assert g[0,2] == 'i'
    assert g[1,2] == 'j'
    assert g[2,2] == 'k'
    assert g[3,2] == 'l'

@pytest.mark.parametrize("x, y, expected", [
    (-1, 0, False),
    (0, -1, False),
    (0,0,True),
    (4,0,False),
    (3,0,True),
    (0,3,False),
    (0,2,True),
    (4,3,False),
    (3,2,True)
])
def test_inbounds(x, y, expected):
    g = CharGrid(FOUR_BY_THREE_GRID)
    assert g.inbound(x,y) == expected

@pytest.mark.parametrize("x,y", [
    (-1, 0),
    (0, -1),
    (4,0),
    (0,3),
    (4,3),
])
def test_outofbounds_indexing(x,y):
    g = CharGrid(FOUR_BY_THREE_GRID)
    assert g[x,y] == None


FOUR_BY_THREE_GRID = (
        'abcd',
        'efgh',
        'ijkl'
    )

@pytest.mark.parametrize("x,y,direction,steps,expected", [
    (1, 1, Direction.NORTHWEST, 0, 'f'),
    (1, 1, Direction.NORTHWEST, 1, 'a'),
    (1, 1, Direction.NORTH, 1, 'b'),
    (1, 1, Direction.NORTHEAST, 1, 'c'),
    (1, 1, Direction.WEST, 1, 'e'),
    (1, 1, Direction.EAST, 1, 'g'),
    (1, 1, Direction.SOUTHWEST, 1, 'i'),
    (1, 1, Direction.SOUTH, 1, 'j'),
    (1, 1, Direction.SOUTHEAST, 1, 'k'),
    (1, 1, Direction.NORTHWEST, 2, None), #f -> NORTHEAST -> a
    (1, 1, Direction.NORTH, 2, None),
    (1, 1, Direction.NORTHEAST, 2, None),
    (1, 1, Direction.WEST, 2, None),
    (1, 1, Direction.EAST, 2, 'h'),
    (1, 1, Direction.SOUTHWEST, 2, None),
    (1, 1, Direction.SOUTH, 2, None),
    (1, 1, Direction.SOUTHEAST, 2, None),
    (1, 1, Direction.EAST, 3, None),
    # negative steps work fine
    (1, 1, Direction.NORTHWEST, -1, 'k'),
    (1, 1, Direction.NORTH, -1, 'j'),
    (1, 1, Direction.NORTHEAST, -1, 'i'),
    (1, 1, Direction.WEST, -1, 'g'),
    (1, 1, Direction.EAST, -1, 'e'),
    (1, 1, Direction.SOUTHWEST, -1, 'c'),
    (1, 1, Direction.SOUTH, -1, 'b'),
    (1, 1, Direction.SOUTHEAST, -1, 'a'),
])
def test_step(x, y, direction, steps, expected):
    g = CharGrid(FOUR_BY_THREE_GRID)
    assert g.step((x,y), direction, steps) == expected

def test_iteration():
    iterator = StringCharIterator("hello")
    result = [char for char in iterator]
    assert result == ['h', 'e', 'l', 'l', 'o'], "Iteration over string failed"

def test_reset():
    iterator = StringCharIterator("world")
    first_pass = [char for char in iterator]
    iterator.reset()
    second_pass = [char for char in iterator]
    assert first_pass == second_pass, "Reset did not work correctly"

def test_empty_string():
    iterator = StringCharIterator("")
    result = [char for char in iterator]
    assert result == [], "Iterator should return no characters for an empty string"

def test_partial_iteration():
    iterator = StringCharIterator("abc")
    first_char = next(iterator)
    assert first_char == 'a', "First character is incorrect"
    second_char = next(iterator)
    assert second_char == 'b', "Second character is incorrect"

def test_stop_iteration():
    iterator = StringCharIterator("x")
    next(iterator)  # Consume the only character
    with pytest.raises(StopIteration):
        next(iterator)  # Should raise StopIteration

def test_reset_after_partial_iteration():
    iterator = StringCharIterator("reset")
    next(iterator)  # Consume the first character
    iterator.reset()  # Reset the iterator
    result = [char for char in iterator]
    assert result == ['r', 'e', 's', 'e', 't'], "Reset after partial iteration failed"

def test_has_next():
    iterator = StringCharIterator("abc")

    # Initially, the iterator should have the next element
    assert iterator.has_next() is True

    # Consume one character
    next(iterator)
    assert iterator.has_next() is True

    # Consume all characters
    next(iterator)
    next(iterator)
    assert iterator.has_next() is False

    # Reset the iterator
    iterator.reset()
    assert iterator.has_next() is True