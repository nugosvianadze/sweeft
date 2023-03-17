
n = int(input())  # read the number of words

# initialize a dictionary to store the count of each word
word_count = {}

# read the words and count their occurrences
for i in range(n):
    word = input().strip()
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

# output the number of distinct words
print(len(word_count))

# output the count of each word in the order of appearance
for word in word_count:
    print(word_count[word], end=' ')
print()