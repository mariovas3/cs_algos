"""
    Given sorted array and target number,
    return index of leftmost element that is
    greater than or equal to the target.
"""


def find_ge_idx(arr: list, target: int) -> int:
    if not arr or arr[-1] < target:
        return -1
    if arr[0] >= target:
        return 0
    
    l, h = 0, len(arr) - 1
    while l < h:
        mid = l + (h - l) // 2
        if arr[mid] >= target:
            if arr[mid-1] < target:
                return mid
            h = mid
        else:
            if arr[mid+1] >= target:
                return mid + 1
            l = mid + 1
    return -1


if __name__ == "__main__":
    import random
    random.seed(0)
    a = sorted(random.choices(range(-9, 10), k=40))
    print(find_ge_idx(a, 3), a, sep='\n')

