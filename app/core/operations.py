from functools import lru_cache


@lru_cache
def power(a, b):
    return pow(a, b)


@lru_cache
def n_th_fibonacci(n):
    a, b = 0, 1
    c = 1

    while c < n:
        a, b = b, a + b
        c += 1
    return a


@lru_cache
def factorial(n):
    p = 1
    for i in range(1, n + 1):
        p *= i

    return p
