"""
Implemented efficient min queries of static array.

First we have to precompute mins on segments of the 
array whose lengths are powers of 2. 

Since we have O(log(n)) such lengths, and we can compute
the mins for a given length in O(n) time, this 
precomputation costs O(n log(n)).

We can efficiently precompute the array using dp:
    f(a, b) = min( f(a, a + w - 1), f(a + w, b) )
    w = (b - a + 1) // 2.

Then the range query can be answered in O(1) time:
    min(a, b) = min( min(a, a + k - 1), min(b - k + 1, b) )
    k is the largest power of 2 less than b - a + 1.
"""



class MinOracle:
    def __init__(self, arr):
        self.precomputed = self._min_precompute(arr)

    def min_query(self, a, b):
        """Returns min(arr[a:b+1])."""
        k, temp = 1, (b - a + 1)
        while k < temp:
            k *= 2
        k //= 2
        return min(
                    self.precomputed[(a, a + k - 1)], 
                    self.precomputed[(b - k + 1, b)]
                )

    def _min_precompute(self, arr):
        # init with seg len 1;
        precomputed = {
                    (i, i): arr[i]
                    for i in range(len(arr))
                }

        def f(a, b):
            if (a, b) in precomputed:
                return precomputed[(a, b)]
            w = (b - a + 1) // 2
            precomputed[(a, b)] = min(f(a, a + w - 1), f(a + w, b))
            return precomputed[(a, b)]
        
        # precompute mins on segements
        # with power of 2 lens;
        inc = 2
        while inc < len(arr):
            idx = 0
            while idx + inc - 1< len(arr):
                f(idx, idx + inc - 1)
                idx += 1
            inc *= 2
        inc //= 2
        return precomputed


if __name__ == "__main__":
    import random
    random.seed(0)

    arr = random.choices(range(1000), k=100)
    mo = MinOracle(arr)

    for _ in range(1000):
        a, b = random.sample(range(len(arr)), k=2)
        a, b = min(a, b), max(a, b)
        out, expected = mo.min_query(a, b), min(arr[a:b+1])
        assert out == expected
