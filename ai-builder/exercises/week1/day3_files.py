import json

# Exercise 13: Create a file and write to it

with open("exercises/week1/output/first_file.txt","w") as f:
    f.write("First line of text\n")
    f.write("Second line of text\n")
    f.write("Third line of text\n")
    f.write("Fourth line of text\n")
    f.write("Fifth line of text\n")

with open("exercises/week1/output/first_file.txt","r") as f:
    for i, line in enumerate(f):
        print(f"{i+1}: {line.strip()}")


# Exercise 14: Creating JSON

schedule = {
    "Monday": ["Finance lecture", "Gym", "Study group"],
    "Tuesday": ["AI lab session", "Office hours", "Reading"],
    "Wednesday": ["Strategy seminar", "Team project meeting", "Gym"],
    "Thursday": ["Entrepreneurship workshop", "Library research", "Networking event"],
    "Friday": ["Case study prep", "Guest speaker lunch", "Free afternoon"],
    "Saturday": ["AI Builder session", "Errands"],
    "Sunday": ["Rest", "Week planning", "Light reading"]
}

with open("exercises/week1/output/schedule.json","w") as f:
    json.dump(schedule, f, indent=4)

with open("exercises/week1/output/schedule.json","r") as f:
    loaded = json.load(f)

for activity in loaded["Monday"]:
    print(f" - {activity}")

# Excercise 15: Function to read text file and return dictionary

def analyze_text(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
    
    line_count = len(lines)
    word_count = 0
    characters_count = 0
    frequency = {}

    for line in lines:
        words = line.split()
        word_count += len(words)
        characters_count += len(line.strip())

        for word in words:
            if word in frequency.keys():
                frequency[word] += 1
            else:
                frequency[word] = 1
    
    most_common_word = max(frequency,key=frequency.get)
    
    return {'line_count': line_count, 'word_count': word_count, 'character_count': characters_count, 'most_common_word': most_common_word}

print(analyze_text("exercises/week1/output/first_file.txt"))


    
