# Exercise 1: Variables and f-strings

name = 'Pablo'
age = 30
university = 'MIT Sloan School of Management'

print(f"My name is {name}, I am {age} years old, and I study at {university}.")


# Exercise 2: Temperature converter
celsius = 25

fahrenheit = celsius * 9/5 + 32
print(f"{celsius} degrees Celsius is equal to {fahrenheit} degrees Fahrenheit.")

# Exercise 3: String manipulation

full_name = "Pablo Santolaya"

first_name = full_name.split()[0]
last_name = full_name.split()[1]

print(f"First name: {first_name}")
print(f"Last name: {last_name}")

# Exercise 4: String metadata

sentence = "Python is a great programming language."
sentence_length = len(sentence)
sentence_words = sentence.split()
number_of_words = len(sentence_words)
sentence_upper = sentence.upper()
sentence_reversed = sentence[::-1]

print(f"Sentence: {sentence}\n Length: {sentence_length}\n Number of words: {number_of_words}\n Uppercase: {sentence_upper}\n Reversed: {sentence_reversed}")