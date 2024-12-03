# one report per line
# each report is list of levels
# a report is safe if levels are 1) all increasing or all decreasing
# adn 2) adjacent levels differ by at least one and at most three

from typing import List
def report_safe(report: List) -> bool:
    if len(report) <= 1:
        return True

    overall_direction = None
    for idx in range(len(report) - 1):
        cur, next = report[idx], report[idx + 1]
        diff = cur - next
        abs_diff = abs(diff)
        if abs_diff < 1 or abs_diff > 3:
            return False
        
        cur_direction = diff // abs_diff
        if overall_direction is None:
            overall_direction = cur_direction
        elif overall_direction != cur_direction:
            return False
        
    return True

def safe_report_count(filepath: str) -> int:
    result = 0
    with open(filepath) as file:
        for line in file:
            report = [int(el) for el in line.split()]
            if report_safe(report):
                result += 1
    return result
            
    

if __name__ == '__main__':
    print(safe_report_count("two.txt"))