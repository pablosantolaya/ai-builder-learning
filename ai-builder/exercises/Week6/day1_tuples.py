def analyze_numbers(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers)/len(numbers)
    return minimum, maximum, average

stats = [85, 92, 78, 95, 88]

min_score, max_score, avg_score = analyze_numbers(stats)

print(f"Minimum Score: {min_score}")
print(f"Maximum Score: {max_score}")
print(f"Average Score: {avg_score:.2f}")