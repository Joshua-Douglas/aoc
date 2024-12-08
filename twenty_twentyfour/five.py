def valid_page_order(update, page, idx, restricted_pages):
    if page not in restricted_pages:
        return True
    
    for restriction_check_idx in range(idx):
        if update[restriction_check_idx] in restricted_pages[page]:
            return False
    return True

def valid_updates(restricted_pages, updates):
    result = 0
    for update in updates:
        if all(valid_page_order(update, page, idx, restricted_pages) for idx, page in enumerate(update)):
            result += int(update[(len(update) // 2)])
    return result