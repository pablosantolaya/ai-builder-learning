# Excersice 29a

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_num = []

for num in numbers:
    if num % 2 == 0:
        even_num.append(num)

even_number = [num for num in numbers if num % 2 == 0]

print(even_num)
print(even_number)

# Excersice 29b
cities = ["madrid", "boston", "london", "paris"]

cities_upper = []

for city in cities:
    cities_upper.append(city.upper())

cities_upper_2 = [city.upper() for city in cities]

print(cities_upper)
print(cities_upper_2)

# Exercise 29c
students = [
    {"name": "Pablo", "grade": 92},
    {"name": "Ana", "grade": 78},
    {"name": "Marco", "grade": 85},
    {"name": "Priya", "grade": 61},
]

passed_students = []

for student in students:
    if student["grade"] > 80:
        passed_students.append(student)

passed_student_2 = [student for student in students if student["grade"] > 80]

# Excercise 29d
emails = [
    {"from": "boss@company.com", "subject": "URGENT: Q3 report", "read": False},
    {"from": "friend@gmail.com", "subject": "Lunch tomorrow?", "read": True},
    {"from": "cto@company.com", "subject": "DEADLINE: Review by Friday", "read": False},
    {"from": "newsletter@news.com", "subject": "Weekly digest", "read": True},
]

unread_title = []

for email in emails:
    if email["read"] is False:
        unread_title.append(email["subject"])

unread_title_2 = [email["subject"] for email in emails if email["read"] is False]


from datetime import datetime, date , timedelta
# Exercise 30a
today = date.today()
print(today.strftime("%B %d, %Y"))

# Exercise 30b
deadline = datetime.strptime("2026-05-29", "%Y-%m-%d").date()
diff = deadline -date.today()
days_to = diff.days

# Exercise 30c
period = ""
time_str = "14:30"
hour = int(time_str.split(":")[0])
if hour < 12:
    period = "morning"
elif hour < 17:
    period = "afternoon"
else:
    period = "night"

# Excercise 30d:
today_date = date.today()

dates = []

for i in range(7):
    delta_time = timedelta(days=i)
    day = today_date + delta_time
    day_parsed = day.strftime("%A, %B %d")
    dates.append(day_parsed)

print(dates)

# Excercise 31
emails = [
    {"from": "boss@company.com", "subject": "Q3 report", 
     "date": "2026-03-20", "body": "Please review by end of week"},
    {"from": "cto@company.com", "subject": "URGENT: server down", 
     "date": "2026-03-23", "body": "Production is down, need fix ASAP"},
    {"from": "friend@gmail.com", "subject": "Lunch tomorrow?", 
     "date": "2026-03-22", "body": "Are you free for lunch?"},
    {"from": "pm@company.com", "subject": "DEADLINE: submit proposal", 
     "date": "2026-03-21", "body": "Proposal due Friday"},
    {"from": "newsletter@news.com", "subject": "Weekly digest", 
     "date": "2026-03-19", "body": "Your weekly roundup"},
]

# Excercise 31a
sorted_emails = sorted(emails, key = lambda email: email["date"], reverse=True)

# Excercise 31b
keywords = ["URGENT", "DEADLINE", "ASAP"]
for email in emails:
    if any(keyword in email["subject"].upper() for keyword in keywords):
        email["priority"] = "high"
    else:
        email["priority"] = "normal"

# Exercise 31c
high_prio = [email for email in emails if email["priority"] == "high"]
high_prio_sort = sorted(high_prio, key = lambda item:item["date"], reverse=True)