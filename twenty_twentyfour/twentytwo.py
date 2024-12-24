from itertools import pairwise, tee
from collections import defaultdict

def next_secret(secret):
    secret ^= secret << 6 & 0xFFFFFF
    secret ^= secret >> 5 & 0xFFFFFF
    return secret ^ secret << 11 & 0xFFFFFF

def banana_haggling_old(secrets, num_iters):
    sum, price = 0, defaultdict(int)
    for secret in secrets:
        nums = [secret] + [secret := next_secret(secret) for _ in range(num_iters)]
        sum += nums[-1]
        
        diffs = [b%10-a%10 for a,b in pairwise(nums)]
        seen = set()
        for i in range(len(nums)-4):
            pat = tuple(diffs[i:i+4])
            if pat not in seen:
                price[pat] += nums[i+4] % 10
                seen.add(pat)

    return sum, max(price.values())

def nwise(iterable, n):
    """Return overlapping tuples of size n from an iterable."""
    iterables = tee(iterable, n)
    for i, it in enumerate(iterables):
        for _ in range(i):
            next(it, None)
    return zip(*iterables)

def banana_haggling(secrets, num_iters):
    sum, price = 0, defaultdict(int)
    cur_seen = set()
    for secret in secrets:
        nums = [secret] + [secret := next_secret(secret) for _ in range(num_iters)]
        sum += nums[-1]
        
        diffs = [b%10-a%10 for a,b in pairwise(nums)]
        cur_seen.clear()
        for i, pat in enumerate(nwise(diffs, 4)):
            if pat not in cur_seen:
                price[pat] += nums[i+4] % 10
                cur_seen.add(pat)

    return sum, max(price.values())
