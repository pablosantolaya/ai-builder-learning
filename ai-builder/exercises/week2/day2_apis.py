import requests
import json

# Week 2 Excercise 5
response = requests.get("https://api.github.com")

status_code = response.status_code
response_json = response.json()

print(list(response_json.items())[:3])
print(status_code)
print(type(response_json))

# Week 2 Exercise 6
def get_repo_count(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code ==404:
        print("User not found")
        return None
    else:
        json_github = response.json()
        return json_github["public_repos"]

print(get_repo_count("pablosantolaya"))
print(get_repo_count("thisuserdoesnotexist99999"))

# Week 2 Excercise 7
def fetch_random_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 404:
            print("Request error, please try again")
            return None
        else:
            response_json = response.json()
            quote_entry = response_json[0]
            json_quote = quote_entry["q"]
            json_author = quote_entry["a"]
            return {"quote": json_quote, "author": json_author}

    except requests.exceptions.RequestException:
        print("Network error, please try again")
        return None

def save_quote(quote_dict, filepath):
    with open(filepath,"w") as f:
        json.dump(quote_dict, f, indent = 4)

quote = fetch_random_quote()
print(quote)
save_quote(quote,"exercises/week2/output/quote.json")

# Bonus excercise
def agify_func(name):
    try:
        url = f"https://api.agify.io?name={name}"
        response = requests.get(url)
        if response.status_code == 404:
            print("Request error, please try again")
            return None
        else:
            response_dict = response.json()
            age = response_dict["age"]
            name = response_dict["name"]

        return {"name":name, "age":age}
    
    except requests.exceptions.RequestException:
        print("Network error, please try again")
        return None

def save_json_agify(quote_dic,filepath):
    with open(filepath,"w") as f:
        json.dump(quote_dic,f, indent=4)

names = ["Pablo", "Maria", "John", "Yuki"]
results = []

for name in names:
    result = agify_func(name)
    if result is not None:
        results.append(result)

print(results)
save_json_agify(results,"exercises/week2/output/name_age.json")
