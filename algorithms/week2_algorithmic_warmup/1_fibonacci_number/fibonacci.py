# Uses python3
def calc_fib(n):
    if (n <= 1):
        return n

    return calc_fib(n - 1) + calc_fib(n - 2)

def calc_fib_fast(n):
    if (n <= 1):
        return n
    
    else:
        seq_list = list(range(n))
        for i in range(2, n):
            seq_list[i] = seq_list[(i - 1)] + seq_list[(i - 2)]
    
        return seq_list[-1] + seq_list[-2]


n = int(input())
print(calc_fib_fast(n))
