import pytest

from twenty_twentyfour.four import count_word_in_grid, count_x_mas
from twenty_twentyfour.five import valid_updates, invalid_updates
from twenty_twentyfour.six import count_guard_positions, guard_is_in_loop, count_guard_loops
from twenty_twentyfour.seven import get_calibrations, sum_valid_calibrations, get_elephant_operators, concat
from twenty_twentyfour.eight import calc_antinodes, count_antinodes, count_harmonic_antinodes
from twenty_twentyfour.nine import assign_file_ids, noncontinguous_defrag, disk_checksum, contiguous_defrag
from twenty_twentyfour.ten import search, count_paths
from twenty_twentyfour.eleven import blink_stones, stones_after_blink, stones_count_after_blink
from twenty_twentyfour.twelve import calc_plot_dimensions, calc_fencing_cost
from twenty_twentyfour.thirtheen import solve_linear_system_integer_solutions, find_token_cost
from twenty_twentyfour.fourteen import predict_botpos, read_input, quadrant_bot_count, bot_safety_factor

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

def test_eight_example_harmonic(data_dir):
    with open(data_dir / 'eight_example.txt') as f:
        source = f.readlines()
    assert count_harmonic_antinodes(source) == 34

def test_eight_example_harmonic(data_dir):
    with open(data_dir / 'eight.txt') as f:
        source = f.readlines()
    assert count_harmonic_antinodes(source) == 934

def test_nine_assign_file_ids_odd_len():
    example_input = '2333133121414131402'    
    assert assign_file_ids(example_input) == [
        (0,2,3),
        (1,3,3),
        (2,1,3),
        (3,3,1),
        (4,2,1),
        (5,4,1),
        (6,4,1),
        (7,3,1),
        (8,4,0),
        (9,2,0)
    ]
def test_nine_assign_file_ids_even_len():
    example_input = '23331331214141314023'    
    assert assign_file_ids(example_input) == [
        (0,2,3),
        (1,3,3),
        (2,1,3),
        (3,3,1),
        (4,2,1),
        (5,4,1),
        (6,4,1),
        (7,3,1),
        (8,4,0),
        (9,2,3)
    ]

def test_nine_noncontinguous_defrag():
    example_input = '2333133121414131402'
    indexed_input = assign_file_ids(example_input)
    assert noncontinguous_defrag(indexed_input) == [
        (0,2,0),
        (9,2,0),
        (8,1,0),
        (1,3,0),
        (8,3,0),
        (2,1,0),
        (7,3,0),
        (3,3,0),
        (6,1,0),
        (4,2,0),
        (6,1,0),
        (5,4,0),
        (6,2,14)
    ]


def test_nine_continguous_defrag():
    example_input = '2333133121414131402'
    indexed_input = assign_file_ids(example_input)
    assert contiguous_defrag(indexed_input) == [
        (0,2,0),
        (9,2,0),
        (2,1,0),
        (1,3,0),
        (7,3,1),
        (4,2,1),
        (3,3,4),
        (5,4,1),
        (6,4,5),
        (8,4,2)
    ]

def test_nine_example_first():
    example_input = '2333133121414131402'
    indexed_input = assign_file_ids(example_input)
    defraged_map = noncontinguous_defrag(indexed_input)
    assert disk_checksum(defraged_map) == 1928

def test_nine_example_second():
    example_input = '2333133121414131402'
    indexed_input = assign_file_ids(example_input)
    defraged_map = contiguous_defrag(indexed_input)
    assert disk_checksum(defraged_map) == 2858

def test_nine_example_second_2():
    example_input = '12101'
    indexed_input = assign_file_ids(example_input)
    defraged_map = contiguous_defrag(indexed_input)
    assert disk_checksum(defraged_map) == 4

def test_nine_first(data_dir):
    with open(data_dir / 'nine.txt') as f:
        input = f.readline()
    indexed_input = assign_file_ids(input)
    defraged_map = noncontinguous_defrag(indexed_input)
    assert disk_checksum(defraged_map) == 6344673854800

def test_nine_second(data_dir):
    with open(data_dir / 'nine.txt') as f:
        input = f.readline()
    indexed_input = assign_file_ids(input)
    defraged_map = contiguous_defrag(indexed_input)    
    assert disk_checksum(defraged_map) == 6360363199987

def test_ten_example_first_small():
    source_str = (
        '0123',
        '1234',
        '8765',
        '9876',
    )
    assert count_paths(source_str) == 1

def test_ten_example_first_medium():
    source_str = (
        '89010123',
        '78121874',
        '87430965',
        '96549874',
        '45678903',
        '32019012',
        '01329801',
        '10456732'
    )
    assert count_paths(source_str) == 36

@pytest.mark.parametrize('start, count', [
    ((2,0), 5),
    ((4,0), 6),
    ((4,2), 5),
    ((6,4), 3),
    ((2,5), 1),
    ((5,5), 3),
    ((0,6), 5),
    ((6,6), 3),
    ((1,7), 5)
])
def test_ten_search(start, count):
    source_str = (
        '89010123',
        '78121874',
        '87430965',
        '96549874',
        '45678903',
        '32019012',
        '01329801',
        '10456732'
    )
    g = CharGrid(source_str)
    assert search(g, start) == count


@pytest.mark.parametrize('start, count', [
    ((2,0), 20),
    ((4,0), 24),
    ((4,2), 10),
    ((6,4), 4),
    ((2,5), 1),
    ((5,5), 4),
    ((0,6), 5),
    ((6,6), 8),
    ((1,7), 5)
])
def test_ten_distinct(start, count):
    source_str = (
        '89010123',
        '78121874',
        '87430965',
        '96549874',
        '45678903',
        '32019012',
        '01329801',
        '10456732'
    )
    g = CharGrid(source_str)
    assert search(g, start, True) == count


def test_ten_first(data_dir):
    with open(data_dir / 'ten.txt') as f:
        source = f.readlines()
    assert count_paths(source) == 822

def test_ten_second(data_dir):
    with open(data_dir / 'ten.txt') as f:
        source = f.readlines()
    assert count_paths(source, include_distinct_paths=True) == 1801

@pytest.mark.parametrize('orig, new', [
    (['125', '17'], ['253000', '1', '7']),
    (['253000', '1', '7'], ['253','0','2024','14168']),
    (['253','0','2024','14168'], ['512072', '1', '20', '24', '28676032']),
    (['512072', '1', '20', '24', '28676032'], ['512', '72', '2024', '2', '0', '2', '4', '2867', '6032']),
    (['512', '72', '2024', '2', '0', '2', '4', '2867', '6032'], ['1036288', '7', '2', '20', '24', '4048', '1', '4048', '8096', '28', '67', '60', '32']),
    (['1036288', '7', '2', '20', '24', '4048', '1', '4048', '8096', '28', '67', '60', '32'], ['2097446912', '14168', '4048', '2', '0', '2', '4', '40', '48', '2024', '40', '48', '80', '96', '2', '8', '6', '7', '6', '0', '3', '2'])
])
def test_eleven_blink(orig, new):
    assert blink_stones(orig) == new

def test_eleven_blink_count():
    assert stones_after_blink(['125', '17'], 6) == 22
    assert stones_after_blink(['125', '17'], 25) == 55312

def test_eleven_part_one():
    input = ['554735', '45401', '8434', '0', '188', '7487525', '77', '7']
    # assert stones_after_blink(input, 25, maintain_order=False) == 209412
    assert stones_count_after_blink(input, 25) == 209412

def test_eleven_part_two():
    input = ['554735', '45401', '8434', '0', '188', '7487525', '77', '7']
    assert stones_count_after_blink(input, 75) == 248967696501656

@pytest.mark.parametrize('start_pos, area, perimeter, sides', [
    ((0,0), 4, 10, 4),((1,0), 4, 10, 4),((2,0), 4, 10, 4),((3,0), 4, 10, 4), #A A A A
    ((0,1), 4, 8, 4), ((1,1), 4, 8, 4), ((2,1), 4, 10, 8), ((3,1), 1, 4, 4), #B B C D
    ((0,2), 4, 8, 4), ((1,2), 4, 8, 4), ((2,2), 4, 10, 8),((3,2), 4, 10, 8), #B B C C
    ((0,3), 3, 8, 4), ((1,3), 3, 8, 4), ((2,3), 3, 8, 4), ((3,3), 4, 10, 8), #E E E C
])
def test_twelve_dim_calc_simple(start_pos, area, perimeter, sides):
    source_str = (
        'AAAA',
        'BBCD',
        'BBCC',
        'EEEC'
    )
    g = CharGrid(source_str)
    assert calc_plot_dimensions(g, start_pos) == (area, perimeter, sides)

@pytest.mark.parametrize('start_pos, area, perimeter, sides', [
    ((0,0), 12, 18, 10), #R
    ((4,0), 4, 8, 4),   #I
    ((6,0), 14, 28, 22), #C
    ((8,0), 10, 18, 12), #F
    ((0,3), 13, 20, 10), #V
    ((6,3), 11, 20, 12), #J
    ((7,4), 1, 4, 4), #C
    ((9,9), 13, 18, 8), #E
    ((1,8), 14, 22, 16), #I
    ((0,8), 5, 12, 6),  #M
    ((5,9), 3, 8, 6)    #S
])
def test_twelve_dim_calc_example(start_pos, area, perimeter, sides):
    source_str = (
        'RRRRIICCFF',
        'RRRRIICCCF',
        'VVRRRCCFFF',
        'VVRCCCJFFF',
        'VVVVCJJCFE',
        'VVIVCCJJEE',
        'VVIIICJJEE',
        'MIIIIIJJEE',
        'MIIISIJEEE',
        'MMMISSJEEE'
    )
    g = CharGrid(source_str)
    assert calc_plot_dimensions(g, start_pos) == (area, perimeter, sides)

def test_twelve_example_cost():
    source_str = (
        'RRRRIICCFF',
        'RRRRIICCCF',
        'VVRRRCCFFF',
        'VVRCCCJFFF',
        'VVVVCJJCFE',
        'VVIVCCJJEE',
        'VVIIICJJEE',
        'MIIIIIJJEE',
        'MIIISIJEEE',
        'MMMISSJEEE'
    )
    assert calc_fencing_cost(source_str) == 1930
    assert calc_fencing_cost(source_str, True) == 1206

def test_twelve_complex_examples():
    source_str = (
        'EEEEE',
        'EXXXX',
        'EEEEE',
        'EXXXX',
        'EEEEE'
    )
    second_source = (
        'AAAAAA',
        'AAABBA',
        'AAABBA',
        'ABBAAA',
        'ABBAAA',
        'AAAAAA'
    )
    g = CharGrid(source_str)
    second_g = CharGrid(second_source)
    assert calc_plot_dimensions(g, (0,0)) == (17, 36, 12)
    assert calc_plot_dimensions(g, (1,1)) == (4, 10, 4)
    assert calc_plot_dimensions(g, (1,3)) == (4, 10, 4)
    #assert calc_plot_dimensions(second_g, (0,0)) == (17, 36, 12)
    #assert calc_plot_dimensions(second_g, (1,1)) == (4, 10, 4)
    #assert calc_plot_dimensions(second_g, (1,3)) == (4, 10, 4)
    assert calc_fencing_cost(source_str, True) == 236
    assert calc_fencing_cost(second_source, True) == 368

def test_twelve_part1_cost(data_dir):
    with open(data_dir / 'twelve.txt') as f:
        source = f.readlines()
    assert calc_fencing_cost(source) == 1549354

def test_twelve_part2_cost(data_dir):
    with open(data_dir / 'twelve.txt') as f:
        source = f.readlines()
    assert calc_fencing_cost(source, True) == 937032

@pytest.mark.parametrize('a1, b1, c1, a2, b2, c2, solution', [
    (94, 22, 8400, 34, 67, 5400, (80, 40)),
    (26, 67, 12748, 66, 21, 12176, None),
    (17, 84, 7870, 86, 37, 6450, (38, 86)),
    (69, 27, 18641, 23, 71, 10279, None),
])
def test_thirteen_linear(a1, b1, c1, a2, b2, c2, solution):
    assert solve_linear_system_integer_solutions(a1, b1, c1, a2, b2, c2) == solution

def test_thirteen_example_part_one(data_dir):
    assert find_token_cost(data_dir / 'thirteen_example.txt') == 480

def test_thirteen_part_one(data_dir):
    assert find_token_cost(data_dir / 'thirteen.txt') == 31589

def test_thirteen_part_two(data_dir):
    assert find_token_cost(data_dir / 'thirteen.txt', 10000000000000) == 98080815200063

def test_fourteen_input_read(data_dir):
    pos, vel = read_input(data_dir / 'fourteen_ex.txt')
    assert pos[0] == (0,4)
    assert vel[0] == (3,-3)
    assert pos[-1] == (9,5)
    assert vel[-1] == (-3,-3)

def test_fourteen_bot_prediction(data_dir):
    pos, vel = read_input(data_dir / 'fourteen_ex.txt')
    positions = predict_botpos(7, 11, 100, pos, vel)
    expected_str = ('00000020010',
'00000000000',
'10000000000',
'01100000000',
'00000100000',
'00012000000',
'01000010000')
    assert positions == CharGrid(expected_str)
    assert quadrant_bot_count(positions) == (1,3,4,1)
    assert bot_safety_factor(positions) == 12

def test_fourteen_part_one(data_dir):
    pos, vel = read_input(data_dir / 'fourteen.txt')
    positions = predict_botpos(103, 101, 100, pos, vel)
    assert bot_safety_factor(positions) == 231852216

def test_fourteen_part_two(data_dir):
    pos, vel = read_input(data_dir / 'fourteen.txt')
    cur_step = -1
    positions = ''
    while '1111111111111111111111111111111' not in str(positions):
        cur_step += 1
        positions = predict_botpos(103, 101, cur_step, pos, vel)
    assert cur_step == 8159