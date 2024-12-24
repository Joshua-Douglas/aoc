import heapq

l1 = sorted([3, 4, 2, 1, 3, 3])
l2 = sorted([4, 3, 5, 3, 9, 3])

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

def similarity_score(filepath: str):
    '''
    Calculate the similarity score of two lists, where each 
    element's similarity is measured as (value * frequency_in_other_list)
    '''
    first_ids, second_freq = list(), dict()

    with open(filepath) as file:
        for line in file:
            first, second = line.split()
            first, second = int(first), int(second)
            first_ids.append(first)
            frequency = second_freq.get(second, 0)
            second_freq[second] = frequency + 1
    
    result = 0
    for location_id in first_ids:
        freq = second_freq.get(location_id, 0)
        result += location_id * freq

    return result