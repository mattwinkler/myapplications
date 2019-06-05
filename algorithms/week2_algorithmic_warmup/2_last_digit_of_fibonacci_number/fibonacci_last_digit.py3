# Uses python3
import sys

def get_fibonacci_last_digit_naive(n):
    if n <= 1:
        return n

    previous = 0
    current  = 1

    for _ in range(n - 1):
        previous, current = current, previous + current

    return current % 10

def get_fibonacci_last_digit_fast(n):
    if n <= 1:
        return n

    else:
        seq_list = [0, 1]
        for i in range(2, 60):
            fib_value = seq_list[(i - 1)] + seq_list[(i - 2)]
            seq_list.append(fib_value % 10)

        remainder = n % 60
        return seq_list[remainder]

if __name__ == '__main__':
    input_n = input()
    n = int(input_n)
    print(get_fibonacci_last_digit_fast(n))
