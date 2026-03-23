def filter_by_field(items, field, value):
    filtered = []
    for item in items:
        if item[field] == value:
            filtered.append(item)

    return filtered


students = [
    {"name": "Pablo", "grade": "A"},
    {"name": "Ana", "grade": "B"},
    {"name": "Marco", "grade": "A"},
    {"name": "Priya", "grade": "C"},
    {"name": "David", "grade": "B"},
]

students_a = filter_by_field(students, "grade", "A")
print(students_a)