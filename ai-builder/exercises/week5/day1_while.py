import random

def unreliable_function():
    return random.random() < 0.5

def retry(max_attempts):
    attempt = 0
    status_final = False
    while attempt < max_attempts:
        status = unreliable_function()
        print(f"Attempt: {attempt + 1}: {'Success' if status else 'Failed'}")
        if status:
            status_final = True
            break
        attempt += 1
    return status_final

items = []

while True:
    print("\n1) Add item")
    print("2) View items")
    print("3) Quit")    
    choice = input("Enter choice: ")
    
    if choice == "1":
        item = input("Enter new item:")
        items.append(item)
    elif choice == "2":
        print(items)
    elif choice == "3":
        break