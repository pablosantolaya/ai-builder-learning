# Exercise 9: Define and call functions

def greet(name, greeting = "Hello"):
    return f"{greeting}, {name}!"

print(greet("Pablo"))

print(greet("Pablo", "Hi"))

print(greet("Pablo", greeting = "Hi"))

# Exercise 10: Function with multiple parameters

def analyze_numbers(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    return {"sum": total, "average": average, "min": minimum, "max": maximum}


numbers_list = [10, 20, 30, 40, 50]
result = analyze_numbers(numbers_list)
print(f"Sum: {result['sum']}, Average: {result['average']}, Min: {result['min']}, Max: {result['max']}")

# Exercise 11: character count function

def char_frequency(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

sentence = "The weather is great today"
frequency = char_frequency(sentence)
print(f"{frequency}")

# Exercise 12: List of dictionaries in function

def top_students(students, threshold):
    good_students = []
    for student in students:
        if student["grade"] > threshold:
            good_students.append(student["name"])
    return good_students

students = [
    {"name": "Alice", "grade": 92},
    {"name": "Bob", "grade": 78},
    {"name": "Carol", "grade": 85},
    {"name": "David", "grade": 95}
]

print(top_students(students, 80))

# Bonus exercise

def word_frequency(text):
    words = text.split()
    word_counter = {}
    for word in words:
        if word in word_counter.keys():
            word_counter[word] += 1
        else:
            word_counter[word]=1
    return word_counter


sentence = "I am a person, I am a human, I am Pablo"
print(word_frequency(sentence))