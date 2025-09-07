dictionary = input().split()
text = input().split()
dictionary_set = set(dictionary)


def shorten_word(word):
    for i in range(1, len(word) + 1):
        if word[:i] in dictionary_set:
            return word[:i]
    return word


result = [shorten_word(word) for word in text]
print(' '.join(result))