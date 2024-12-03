import heapq

def list_distance(filepath: str):
    first_ids, second_ids = list(), list()

    with open(filepath) as file:
        for line in file:
            first_str, second_str = line.split()
            heapq.heappush(first_ids, int(first_str))
            heapq.heappush(second_ids, int(second_str))
    
    if len(first_ids) != len(second_ids):
        raise ValueError("The file contained unequal length columns of location IDs")
    
    result = 0
    while len(first_ids) > 0:
        first = heapq.heappop(first_ids)
        second = heapq.heappop(second_ids)
        result += abs(first - second)

    return result

if __name__ == '__main__':
    # 3569916
    print(list_distance("one.txt"))