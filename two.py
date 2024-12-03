# one report per line
# each report is list of levels
# a report is safe if levels are 1) all increasing or all decreasing
# adn 2) adjacent levels differ by at least one and at most three

from typing import List, Optional
def unsafe_report_level(report: List[int]) -> Optional[int]:
    if len(report) <= 1:
        return True, None

    overall_direction = None
    for idx in range(len(report) - 1):
        cur, next = report[idx], report[idx + 1]
        diff = cur - next
        abs_diff = abs(diff)
        if abs_diff < 1 or abs_diff > 3:
            return idx
        
        cur_direction = diff // abs_diff
        if overall_direction is None:
            overall_direction = cur_direction
        elif overall_direction != cur_direction:
            return idx
        
    return None

def safe_report_count(filepath: str, enable_dampener: bool) -> int:
    result = 0
    with open(filepath) as file:
        for line in file:
            report = [int(el) for el in line.split()]
            unsafe_idx = unsafe_report_level(report)
            if unsafe_idx is None:
                result += 1
            elif enable_dampener:
                last_safe_idx = max(unsafe_idx - 2, 0)
                for remove_idx in (unsafe_idx - 1, unsafe_idx, unsafe_idx + 1):
                    if (remove_idx < 0) or (remove_idx >= len(report)):
                        continue
                    cleaned_report = report[last_safe_idx:remove_idx] + report[remove_idx + 1:] 
                    if unsafe_report_level(cleaned_report) is None:
                        result += 1
                        break
    return result

if __name__ == '__main__':
    # 606
    print(safe_report_count("two.txt", enable_dampener=False))
    # 644 
    print(safe_report_count("two.txt", enable_dampener=True))