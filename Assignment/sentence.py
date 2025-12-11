'''Q1:Write a Python program that takes a sentence from the user and prints:
Number of characters
Number of words
Number of vowels'''

def sentence_check(sentence):
    num_char = len(sentence)

    words = sentence.split()
    num_words = len(words)

    num_vowels = 0
    vowels = "aeiouAEIOU"
    for char in sentence:
        if char in vowels:
            num_vowels +=1

    print(f"Number of characters= {num_char}")
    print(f"Number of words= {num_words}")
    print(f"Number of vowels= {num_vowels}")

