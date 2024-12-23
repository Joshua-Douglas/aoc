# if engraved w/0 then change to 1
# if engrabed w/even number of digits then replace with two stones.
    # Left Stone has left half of digits
    # Right Stone has right half of digits
# otherwise multiply stone number by 2024
# 0 1 10 99 999
# 1 2024 1 0 9 9 2021976
from typing import List, Optional, Tuple


def blink_stone(stone: str) -> Tuple[str, Optional[str]]:
    first, second = None, None
    if stone == '0':
        first = '1'
    elif len(stone) % 2 == 0:
        middle_idx = len(stone) // 2
        first, second = stone[:middle_idx], stone[middle_idx:]
    else:
        first = int(stone)*2024
    return str(int(first)), str(int(second)) if second else None
    
def blink_stones(stones: List[str], maintain_order = True) -> List[str]:
    for idx in reversed(range(len(stones))):
        original_stone = stones[idx]
        new_left, new_right = blink_stone(original_stone)
        stones[idx] = new_left
        if new_right:
            if maintain_order:
                stones.insert(idx + 1, new_right)
            else:
                stones.append(new_right)
    return stones

stone_count_memo = dict()

def stone_count_after_blink(stone: str, blinks: int) -> int:
    global stone_count_memo
    if (stone,blinks) in stone_count_memo:
        return stone_count_memo[(stone, blinks)]

    left_stone, right_stone = blink_stone(stone)

    if (blinks == 1) and right_stone:
        return 2
    elif blinks == 1:
        return 1
    
    left_count = stone_count_after_blink(left_stone, blinks-1)
    right_count = stone_count_after_blink(right_stone, blinks-1) if right_stone else 0
    stone_count_memo[(stone, blinks)] = left_count+right_count
    return left_count + right_count

def stones_count_after_blink(stones: List[str], blinks:int) -> int:
    result = 0
    for stone in stones:
        result += stone_count_after_blink(stone, blinks)
    return result

def stones_after_blink(stones: List[str], blinks: int, maintain_order: bool = False) -> int:
    for _ in range(blinks):
        stones = blink_stones(stones, maintain_order)
    return len(stones)

