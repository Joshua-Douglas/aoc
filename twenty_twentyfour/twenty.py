from twenty_twentyfour.datatypes import CharGrid, Direction
from itertools import product
                
def valid_cheats(track, max_dist):
    for start_idx, (start_x, start_y) in enumerate(track):
        # Look ahead by at least 3 positions to consider shortcuts
        for end_idx in range(start_idx + 3, len(track)):
            end_x, end_y = track[end_idx]
            manhattan_dist = abs(end_x - start_x) + abs(end_y - start_y)
            # Calculate the number of steps between the two points on the track
            steps_on_track = end_idx - start_idx
            # Check if a valid cheat exists
            if manhattan_dist <= max_dist and steps_on_track > manhattan_dist:
                steps_saved = steps_on_track - manhattan_dist
                yield steps_saved

def get_path(grid: CharGrid):
    start_pos = None
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x,y] == 'S':
            start_pos = (x, y)
            break

    track = [None, start_pos]
    while grid[x,y] != 'E':
        for dir in (Direction.WEST, Direction.EAST, Direction.NORTH, Direction.SOUTH): 
            next_x, next_y = grid.step_coord((x,y), dir)

            # Check if the neighbor is valid and not the previous position
            if (next_x, next_y) != track[-2] and grid[next_x, next_y] != '#':
                x, y = next_x, next_y
                track.append((x, y))
                break
    return track[1:]