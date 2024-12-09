import pytest

from twenty_twentyfour.four import count_word_in_grid, count_x_mas
from twenty_twentyfour.five import valid_updates, invalid_updates
from twenty_twentyfour.six import count_guard_positions, guard_is_in_loop, count_guard_loops
from twenty_twentyfour.datatypes import CharGrid, Direction

def test_four_first_example():
    example = ('MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX'
    )
    assert count_word_in_grid('XMAS', example) == 18

def test_four_first(data_dir):
    with open(data_dir / 'four.txt') as f:
        assert count_word_in_grid('XMAS', f.readlines()) == 2447

def test_four_second(data_dir):
    with open(data_dir / 'four.txt') as f:
        assert count_x_mas(f.readlines()) == 1868

def test_five_first(data_dir):
    with open(data_dir / 'five.txt') as f:
        restricted_pages = dict()
        for line in f:
            if line.startswith('\n'):
                break
            before, after = line.strip().split('|')
            before, after = before, after
            restrictions = restricted_pages.get(before, list())
            restrictions.append(after)
            restricted_pages[before] = restrictions
        
        updates = [line.strip().split(',') for line in f]
    assert valid_updates(updates, restricted_pages) == 5762


def test_five_second(data_dir):
    with open(data_dir / 'five.txt') as f:
        restricted_pages = dict()
        for line in f:
            if line.startswith('\n'):
                break
            before, after = line.strip().split('|')
            before, after = before, after
            restrictions = restricted_pages.get(before, list())
            restrictions.append(after)
            restricted_pages[before] = restrictions
        
        updates = [line.strip().split(',') for line in f]

    assert invalid_updates(updates, restricted_pages) == 4130

def test_six_example(data_dir):
    with open(data_dir / 'six_example.txt') as f:
        source = f.readlines()
    assert count_guard_positions(source) == 41

def test_six_first(data_dir):
    with open(data_dir / 'six.txt') as f:
        source = f.readlines()
    assert count_guard_positions(source) == 4722

def test_not_in_loop(data_dir):
    with open(data_dir / 'six_example.txt') as f:
        source = f.readlines()
    start_pos = (4, 6)
    grid = CharGrid(source)
    assert guard_is_in_loop(grid, start_pos, Direction.NORTH) == False

@pytest.mark.parametrize("input_file", [
    'six_loop1.txt',
    'six_loop2.txt',
    'six_loop3.txt',
    'six_loop4.txt',
    'six_loop5.txt',
    'six_loop6.txt',
])
def test_in_loop(input_file, data_dir):
    with open(data_dir / input_file) as f:
        source = f.readlines()
    start_pos = (4, 6)
    grid = CharGrid(source)
    assert guard_is_in_loop(grid, start_pos, Direction.NORTH)

def test_six_second(data_dir):
    with open(data_dir / 'six.txt') as f:
        source = f.readlines()
    assert count_guard_loops(source) == 1602