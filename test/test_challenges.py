from twenty_twentyfour.four import count_word_in_grid, count_x_mas
from twenty_twentyfour.five import valid_updates, invalid_updates

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
