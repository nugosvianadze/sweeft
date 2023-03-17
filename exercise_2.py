
"""Exercise 2"""

def bigger_is_greater(w):
    n = len(w)
    # find the rightmost pair of adjacent characters where the left one is smaller
    i = n - 2
    while i >= 0 and w[i] >= w[i+1]:
        i -= 1
    if i < 0:
        return "no answer"
    # find the smallest character greater than w[i] among the characters to the right of i
    j = n - 1
    while j > i and w[j] <= w[i]:
        j -= 1
    # swap w[i] and w[j]
    w = list(w)
    w[i], w[j] = w[j], w[i]
    # sort the substring to the right of i in ascending order
    w[i+1:] = sorted(w[i+1:])
    return ''.join(w)

# read the input and run the test cases
T = int(input())
for i in range(T):
    w = input().strip()
    result = bigger_is_greater(w)
    print(result)