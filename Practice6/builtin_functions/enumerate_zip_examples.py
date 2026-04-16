players = ["S1mple", "ZywOo", "NiKo"]
ratings = [1.25, 1.30, 1.20]

print("--- Using zip and enumerate ---")
for index, (name, score) in enumerate(zip(players, ratings), start=1):
    print(f"{index}. {name} has a rating of {score}")

# Type conversion demonstration
str_val = "100"
int_val = int(str_val)
print(f"\nConverted {type(str_val)} to {type(int_val)}")