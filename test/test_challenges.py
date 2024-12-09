import pytest

from twenty_twentyfour.four import count_word_in_grid, count_x_mas
from twenty_twentyfour.five import valid_updates, invalid_updates
from twenty_twentyfour.six import count_guard_positions, guard_is_in_loop, count_guard_loops
from twenty_twentyfour.seven import get_calibrations, sum_valid_calibrations, get_elephant_operators, concat
from twenty_twentyfour.eight import calc_antinodes, count_antinodes

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

def test_seven_example(data_dir):
    calibrations = get_calibrations(data_dir / 'seven_example.txt')
    assert sum_valid_calibrations(calibrations) == 3749

def test_seven(data_dir):
    calibrations = get_calibrations(data_dir / 'seven.txt')
    assert sum_valid_calibrations(calibrations) == 1038838357795

@pytest.mark.parametrize("a, b, expected", [
    (12, 34, 1234), 
    (5, 7, 57), 
    (0, 123, 123), 
    (-12, 34, 1234), 
    (-5, -7, 57), 
    (100, 200, 100200),
])
def test_concat(a, b, expected):
    assert concat(a, b) == expected

def test_seven_example_second(data_dir):
    calibrations = get_calibrations(data_dir / 'seven_example.txt')
    assert sum_valid_calibrations(calibrations, get_elephant_operators()) == 11387

def test_seven_second(data_dir):
    calibrations = get_calibrations(data_dir / 'seven.txt')
    assert sum_valid_calibrations(calibrations, get_elephant_operators()) == 254136560217241

@pytest.mark.parametrize("antenna1, antenna2, antinode1, antinode2", [
    ((4,3), (5,5), (3,1), (6,7)),
    ((5,5), (8,4), (2,6), (11,3))
])
def test_antinode_calc(antenna1, antenna2, antinode1, antinode2):
    actual_antinodes = calc_antinodes(antenna1, antenna2)
    assert antinode1 in actual_antinodes
    assert antinode2 in actual_antinodes

def test_eight_example(data_dir):
    with open(data_dir / 'eight_example.txt') as f:
        source = f.readlines()
    assert count_antinodes(source) == 14
    
def test_eight_first(data_dir):
    with open(data_dir / 'eight.txt') as f:
        source = f.readlines()
    assert count_antinodes(source) == 293