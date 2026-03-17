#Bonus Exercise: Nested Dictionaries

cities = {
    "Madrid": {"country": "Spain", "years": 25},
    "Dublin": {"country": "Ireland", "years": 1},
    "Virginia": {"country": "USA", "years": 1},
    "Lausanne": {"country": "Switzerland", "years": 1},
    "Boston": {"country": "USA", "years": 2}
}

cities_2y =[]
for city in cities.keys():
    if cities[city].get("years") >= 2:
        cities_2y.append(city)

print(f"Cities: {cities_2y}")

print(f"{cities.items()}")
