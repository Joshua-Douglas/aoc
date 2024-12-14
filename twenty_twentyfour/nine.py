from typing import List, Tuple
import math
from itertools import batched

def noncontinguous_defrag(disk_map: List[Tuple[int, int, int]]) -> str:
    '''
    Take a dense diskmap where each element represents
    (file_id, no_file_blocks, no_empty_blocks) and return the
    defragmented diskmap, by moving file_blocks into the empty
    memory blocks. This algorithm will not maintain contiguous
    memory, and will greedily place file blocks into the first 
    available empty memory block.
    '''
    result = []
    l_idx, r_idx = 0, len(disk_map) - 1
    empty_block_count = 0
    r_file_id, r_file_size, r_empty = disk_map[r_idx]
    while l_idx < r_idx:
        l_file_id, l_file_size, l_empty = disk_map[l_idx]
        empty_block_count += l_empty
        result.append((l_file_id, l_file_size, 0))
        
        while l_empty > 0:
            num_moves = min(r_file_size, l_empty)
            result.append((r_file_id, num_moves, 0))
            l_empty -= num_moves
            r_file_size -= num_moves
            if r_file_size <= 0: # update to == later
                r_idx -= 1
                r_file_id, r_file_size, r_empty = disk_map[r_idx]
                empty_block_count += r_empty
        l_idx += 1
        if (l_idx == r_idx) and (r_file_size > 0):
            if result[-1][0] == r_file_id:
                result[-1] = result[-1][0], result[-1][1] + r_file_size, result[-1][2]
            else:
                result.append((r_file_id, r_file_size, 0))
            
    result[-1] = result[-1][0], result[-1][1], empty_block_count
    return result

def disk_checksum_old(disk_map: Tuple[int,int,int]):
    result = 0
    memory_id = 0
    for file_id, file_size, _ in disk_map:
        for i in range(file_size):
            result += file_id * memory_id
            memory_id += 1
    return result

def disk_checksum_nodiv(disk_map: Tuple[int,int,int]):
    result = 0
    memory_id = 0
    for file_id, file_size, _ in disk_map:
        result += sum(file_id * m_id for m_id in range(memory_id, memory_id+file_size))
        memory_id += file_size
    return result

def disk_checksum(disk_map: Tuple[int, int, int]) -> int:
    result = 0
    memory_id = 0
    for file_id, file_size, _ in disk_map:
        # Sum of memory IDs for the current file
        memory_sum = file_size * memory_id + file_size * (file_size - 1) // 2
        result += file_id * memory_sum
        memory_id += file_size
    return result

def assign_file_ids(disk_map) -> List[Tuple[int,int,int]]:
    '''
    Provide a unique file_id to each of the file blocks provided
    in the dense disk map. The dense disk map is expected to have
    the repeating format '{no_file_blocks}{no_empty_blocks}'. 
    The returned disk map will have the format 
    '{file_id}{no_file_blocks}{no_empty_blocks}', with file_ids 
    starting at 0 and increasing by 1 for each encountered file.
    '''
    result = list()
    for id, idx in enumerate(range(0, len(disk_map) - 1, 2)):
        file_size = disk_map[idx]
        empty_blocks = disk_map[idx + 1]
        result.append((id, int(file_size), int(empty_blocks)))
    if len(result) % 2 != 0:
        result.append(((id+1), int(disk_map[-1]), 0))
    return result