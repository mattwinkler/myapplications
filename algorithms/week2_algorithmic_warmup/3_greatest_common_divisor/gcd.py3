# Uses python3
import sys

def gcd_naive(a, b):
    current_gcd = 1
    for d in range(2, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            if d > current_gcd:
                current_gcd = d

    return current_gcd

def gcd_fast(a, b):
	sm, bg = min(a, b), max(a, b)
	r = bg % sm
	
	if r == 0: 
		return sm
	
	else:
		return gcd_fast(sm, r)

if __name__ == "__main__":
    input_data = sys.stdin.read()
    a, b = map(int, input_data.split())
    print(gcd_fast(a, b))
