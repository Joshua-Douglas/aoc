from functools import cmp_to_key
from typing import Dict, List

def page_comparator_factory(restricted_pages: Dict[str, List[str]]) -> int:
    '''
    Sort manual by the page order restriction rules. Do not reorder pages that
    are not currently violating any ordering rule.

    This require a O(rules) search for each page, so it scales with the number
    of restrictions. We could update this algorithm to do an O(1) search if we
    stored the restrictions as a dense matrix, using a bitarray. This might actually
    more more memory efficient than a dictionary of lists for a small page count, 
    but it would not scale to very large page counts.    
    '''
    def page_comparator(first: str, second: str):
        if (first in restricted_pages) and (second in restricted_pages[first]):
            return -1
        elif (second in restricted_pages) and (first in restricted_pages[second]):
            return 1
        return 0
    return page_comparator

def valid_page_order(update: List[str], restricted_pages: Dict[str, List[str]]) -> bool:
    page_sort_key_func = page_comparator_factory(restricted_pages)
    for idx in range(len(update) - 1):
        if page_sort_key_func(update[idx], update[idx + 1]) > 0:
            return False
    return True

def valid_updates(updates: List[str], restricted_pages: Dict[str, List[str]]) -> int:
    '''
    Return sum of the middle page from all the valid ordered updated manuals.
    '''
    result = 0
    for update in updates:
        if valid_page_order(update, restricted_pages):
            result += int(update[(len(update) // 2)])
    return result

def invalid_updates(updates: List[str], restricted_pages: Dict[str, List[str]]) -> int:
    '''
    Find all incorrectly ordered updates, reorder them to the correct order, and
    return the sum of the corrected manual's middle page.
    '''
    result = 0
    page_sort_key_func = page_comparator_factory(restricted_pages)
    page_sort_comparator = cmp_to_key(page_sort_key_func)
    for update in updates:
        if not valid_page_order(update, restricted_pages):
            update = sorted(update, key=page_sort_comparator)
            result += int(update[(len(update) // 2)])
    return result