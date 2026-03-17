import json

# Week 2 Exercise 1: Intro to errors management

# number1 = input("What is the first number? ")
# number2 = input("What is the second number? ")

number1 = 10
number2 = 5

try:
    number1 = float(number1)
    number2 = float(number2)

    result = number1 / number2

except ValueError:
    print("The input format is not supported")

except ZeroDivisionError:
    print("Division by 0 is not supported")

else:
    print(result)


#Week 2 Exercise 2: JSON reading exceptions

def safe_load_json(filepath):
    
    try:
        with open(filepath, "r") as f:
            json_value = json.load(f)
        return json_value
    
    except FileNotFoundError:
        print("File not found. Please provide valid path.")
        return {}
    
    except json.JSONDecodeError:
        print("File format is not valid. Please ensure the file is a valid JSON")
        return {}

    
data = safe_load_json("input/test_broken.json")
print(data)

data = safe_load_json("inventedpath/valid_json.json")
print(data)

data = safe_load_json("input/valid_json.json")
print(data)


# Week 2 Exercise 3: Install and import libraries
import requests
import dotenv

print(f"requests version: {requests.__version__}")

# Week 2 Exercise 4: Environment Variables
from dotenv import load_dotenv
import os

load_dotenv()

name = os.getenv("MY_NAME")
university = os.getenv("MY_UNIVERSITY")
end_date = os.getenv("SEMESTER_END")
no_var = os.getenv("MISSING")

print(f"the parameters are {name}, {university} and {end_date}. {no_var} is missing")