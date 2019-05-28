# python3

def max_pairwise_product_fast(numbers):
    rank_1, rank_2 = 0, 0

    for n in numbers:
        if n > rank_1:
            rank_2 = rank_1
            rank_1 = n
            
        elif n > rank_2:
            rank_2 = n
    
    return rank_1 * rank_2


def max_pairwise_product(numbers):
    n = len(numbers)
    max_product = 0
    for first in range(n):
        for second in range(first + 1, n):
            max_product = max(max_product,
                numbers[first] * numbers[second])

    return max_product


if __name__ == '__main__':
    input_n = int(input())
    input_numbers = [int(x) for x in input().split()]
    print(max_pairwise_product_fast(input_numbers))
