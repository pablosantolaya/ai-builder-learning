# Exercise 1: Lists
cities = ["Madrid", "Dublin", "Virginia", "Lausanne", "Boston"]

print(f"First city: {cities[0]}\nLast city: {cities[-1]}\nMiddle city: {cities[len(cities) // 2]}")
cities.append("Barcelona")
cities.remove("Virginia")

print(f"Updated cities list: {cities}")

# Exercise 2: Dictionaries
person = {
    "name": "Pablo",
    "age": 30,
    "courses": ["Data Science", "Machine Learning"],
    "grades": ["A", "B"]
}

print(f"Name: {person['name']}\nAge: {person['age']}")

person["courses"].append("Deep Learning")
person["grades"].append("A+")

person["grades"][1] = "A"
print(f"Updated courses: {person['courses']}\nUpdated grades: {person['grades']}")

# Exercise 7: List from list
numbers = [1, 2, 3, 4, 5]
even_numbers = []
for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
print(f"Even numbers: {even_numbers}")

# Excercise 8: Course grades dictionary
course_grades = {
    "Data Science": 95,
    "Machine Learning": 85,
    "Deep Learning": 90
}

average_grade = sum(course_grades.values()) / len(course_grades)
max_grade = max(course_grades.values())
max_grade_course = max(course_grades, key=course_grades.get)

print(f"Average grade: {average_grade}\nHighest grade: {max_grade} in {max_grade_course}")
