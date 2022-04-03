def power(a, b):
    return pow(a, b)


def n_th_fibonacci(n):
    a, b = 0, 1
    c = 1

    while c < n:
        a, b = b, a + b
        c += 1
    return a


def factorial(n):
    p = 1
    for i in range(1, n + 1):
        p *= i

    return p
