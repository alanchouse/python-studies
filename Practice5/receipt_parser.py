import re

# 1. W3Schools Examples (search, findall, split, sub)
txt = "The rain in Spain"
print("W3S Example:", re.search("^The.*Spain$", txt).group())

text_base = "Hello 123 World 456"
print("Search:", re.search(r"\d+", text_base).group())
print("Findall:", re.findall(r"\d+", text_base))
print("Split:", re.split(r"\s", text_base))
print("Sub:", re.sub(r"World", "Python", text_base))

# 2. Problem Set Tasks
# Task 1-2: ab* and ab{2,3}
print("Task 1:", bool(re.fullmatch(r"ab*", "abbb")))
print("Task 2:", bool(re.fullmatch(r"ab{2,3}", "abb")))

# Task 3: lowercase with underscore
print("Task 3:", re.findall(r"[a-z]+_[a-z]+", "hello_world test_case Python_Code"))

# Task 4: Upper followed by lower
print("Task 4:", re.findall(r"[A-Z][a-z]+", "Apple Banana apple"))

# Task 5: a...b
print("Task 5:", bool(re.fullmatch(r"a.*b", "axxxxb")))

# Task 6: Replace space, comma, dot with colon
print("Task 6:", re.sub(r"[ ,.]", ":", "Hello, world. Test"))

# Task 7: Snake to Camel
s = "snake_case_string"
print("Task 7:", "".join(x.capitalize() for x in s.split("_")))

# Task 8: Split at uppercase
print("Task 8:", re.findall(r"[A-Z][^A-Z]*", "SplitAtUppercase"))

# Task 9: Insert spaces
print("Task 9:", re.sub(r"([a-z])([A-Z])", r"\1 \2", "InsertSpacesBetweenWords"))

# Task 10: Camel to Snake
c = "CamelCaseString"
s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', c)
print("Task 10:", re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower())

# 3. Practical Exercise: Receipt Parsing
print("\n--- RECEIPT PARSING ---")
try:
    with open('raw.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    # Date and Time
    dt = re.search(r'Время: (\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})', data)
    if dt: print("Date/Time:", dt.group(1))

    # All prices
    prices = re.findall(r'(\d+[\s\d]*[.,]\d{2})', data)
    print("Prices found:", prices)

    # Product names
    products = re.findall(r'\d+\.\n(.*?)\n', data)
    print("Products:", products[:5])

    # Total amount
    total = re.search(r'ИТОГО:\s*([\d\s,.]+)', data)
    if total: print("TOTAL:", total.group(1).strip())

except FileNotFoundError:
    print("raw.txt not found")