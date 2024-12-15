from typing import List, Tuple

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

def contiguous_defrag(disk_map: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Defragment the disk map by moving file blocks from the right into empty spaces on the left,
    only if the file block completely fits into the empty space.
    """
    r_idx = len(disk_map) - 1
    defrag_start_idx  = 0
    while r_idx >= 0:
        r_file_id, r_file_size, r_empty = disk_map[r_idx]
        all_left_blocks_defragged = False
        for l_idx in range(defrag_start_idx, r_idx):
            l_file_id, l_file_size, l_empty = disk_map[l_idx]

            all_left_blocks_defragged = all_left_blocks_defragged and (l_empty == 0)
            if all_left_blocks_defragged:
                defrag_start_idx = l_idx
            
            if (r_file_size <= l_empty):
                disk_map[l_idx] = l_file_id, l_file_size, 0
                del disk_map[r_idx]
                disk_map.insert(l_idx+1, (r_file_id, r_file_size, l_empty - r_file_size)) 
                prev_id, prev_size, prev_empty = disk_map[r_idx]
                disk_map[r_idx] = prev_id, prev_size, prev_empty + r_file_size + r_empty
                break
        else:
            r_idx -= 1
    return disk_map

def disk_checksum(disk_map: Tuple[int, int, int]) -> int:
    result = 0
    memory_id = 0
    for file_id, file_size, empty_size in disk_map:
        # Sum of memory IDs for the current file
        memory_sum = file_size * memory_id + file_size * (file_size - 1) // 2
        result += file_id * memory_sum
        memory_id += file_size + empty_size
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
    if len(disk_map) % 2 != 0:
        result.append(((id+1), int(disk_map[-1]), 0))
    return result