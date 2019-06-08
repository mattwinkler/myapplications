# Uses python3
import sys

def lcm_naive(a, b):
    for l in range(1, a*b + 1):
        if l % a == 0 and l % b == 0:
            return l

    return a*b

def primes(n): 
    
    result = []
    # Print the number of two's that divide n 
    while n % 2 == 0: 
        result.append(2) 
        n = int(n / 2)
          
    # n must be odd now, so a skip of 2 ( i = i + 2) can be used 
    for i in range(3, int(n**(1/2.0)) + 1, 2): 
          
        # while i divides n , print i and divide n 
        while n % i == 0: 
            result.append(i) 
            n = int(n / i)
              
    # Condition if n is a prime number greater than 2 
    if n > 2: 
        result.append(n)

    return result

def count_elements(arr):
    result = {}
    for elem in arr:
        elem_str = str(elem)
        if elem_str in result:
            result[elem_str] += 1
        else:
            result[elem_str] = 1
    return result

def find_max_element_count(counts_a, counts_b):
    result = []
    for k, v in counts_a.items():
        b_count = counts_b.get(k, 0)
        max_count = max(v, b_count)
        result.append((int(k), max_count))
        if k in counts_b:
            del counts_b[k]

    for k, v in counts_b.items():
        result.append((int(k), v))

    return result

def calculate_result(max_counts):
    result = 1
    for elem in max_counts:
        elem_result = elem[0] ** elem[1]
        result *= elem_result
    return result

def lcm_fast(a, b):
    primes_a = primes(a)
    primes_b = primes(b)
    counts_a = count_elements(primes_a)
    counts_b = count_elements(primes_b)
    max_counts = find_max_element_count(counts_a, counts_b)
    return calculate_result(max_counts)

if __name__ == '__main__':
    input_data = sys.stdin.read()
    a, b = map(int, input_data.split())
    print(lcm_fast(a, b))

