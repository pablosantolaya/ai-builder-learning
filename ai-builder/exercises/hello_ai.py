# This line was added on test-branch to practice Git branching
from datetime import datetime, date

print("Hello, I'm Pablo and I'm learning to build AI tools.")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

days_left = (date(2026, 5, 29) - date.today()).days
print(f"\nDays until end of semester (May 29, 2026): {days_left}")

if days_left > 30:
    print("You have plenty of time — keep building, stay consistent!")
else:
    print("The finish line is close — push through and finish strong!")
