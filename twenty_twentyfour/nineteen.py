from functools import cache

@cache
def towel_solve(available, pattern):
    if not pattern:
        return [[]]
    
    result = []
    for towel in available:
        if pattern.startswith(towel):
            solutions = towel_solve(available, pattern[len(towel):])
            for remaining_solutions in solutions:
                result.append([towel] + remaining_solutions)

    return result

def towels_solve(available, patterns):
    result = dict()
    for pattern in patterns:
        result[pattern] = towel_solve(available, pattern)
    return result, sum(1 for pattern in patterns if len(result[pattern]) > 0)

def read_towels(filepath: str):
    with open(filepath) as f:
        available = f.readline().strip().split(', ')
        f.readline()
        towels = list()
        for line in f:
            towels.append(line.strip())
    return tuple(available), towels

@cache
def towel_counts(available, pattern):
    if not pattern:
        return 1
    result = 0
    for towel in available:
        if pattern.startswith(towel):
            result += towel_counts(available, pattern[len(towel):])
    return result