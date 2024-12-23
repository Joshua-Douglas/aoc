from typing import Optional, Iterator, List

def unsafe_report_level(report: Iterator[int]) -> Optional[int]:
    try:
        cur = next(report)
    except StopIteration:
        return None
    
    overall_direction = None
    idx = 0
    for el in report:
        next_el = el
        diff = cur - next_el
        abs_diff = abs(diff)
        if abs_diff < 1 or abs_diff > 3:
            return idx
        cur_direction = diff // abs_diff
        if overall_direction is None:
            overall_direction = cur_direction
        elif overall_direction != cur_direction:
            return idx
        
        cur = next_el
        idx += 1        
    return None

def generate_clean_report(report: List[int], start_idx: int, idx_to_remove: int):
    for count, el in enumerate(report, start=start_idx):
        idx = count - start_idx
        if idx != idx_to_remove:
            yield el

def safe_report_count(filepath: str, enable_dampener: bool) -> int:
    result = 0
    with open(filepath) as file:
        for line in file:
            report = [int(el) for el in line.split()]
            unsafe_idx = unsafe_report_level((iter(report)))
            if unsafe_idx is None:
                result += 1
            elif enable_dampener:
                # Restart unsafe level search starting at last known safe pair of 
                # levels. Generate three potential cleaned reports - by removing the
                # level where the safety issue was found and its neighbors.
                last_safe_idx = max(unsafe_idx - 2, 0)
                for remove_idx in (unsafe_idx - 1, unsafe_idx, unsafe_idx + 1):
                    clean_report_generator = generate_clean_report(report, last_safe_idx, remove_idx)
                    if unsafe_report_level(clean_report_generator) is None:
                        result += 1
                        break
    return result

if __name__ == '__main__':
    # 606
    print(safe_report_count("two.txt", enable_dampener=False))
    # 644 
    print(safe_report_count("two.txt", enable_dampener=True))