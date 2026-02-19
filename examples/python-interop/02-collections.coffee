# Python Collections

from collections import defaultdict, Counter

# defaultdict - auto-initialize values
wordCounts = defaultdict(-> 0)
words = ["apple", "banana", "apple", "cherry", "apple", "banana"]

for word in words
  wordCounts[word] += 1

print "Word counts: #{wordCounts}"

# Counter - count elements
letters = Counter(["a", "b", "a", "c", "a", "b", "b"])
print "Letter counts: #{letters}"
print "Most common: #{letters.most_common(2)}"

# Working with lists
numbers = [1, 2, 3, 4, 5]

# List methods
numbers.append(6)
print "After append: #{numbers}"

numbers.extend([7, 8, 9])
print "After extend: #{numbers}"

popped = numbers.pop()
print "Popped: #{popped}, remaining: #{numbers}"

# List comprehensions with Python methods
squares = [x ** 2 for x in numbers]
print "Squares: #{squares}"

# Filtering
evens = [x for x in numbers when x % 2 == 0]
print "Evens: #{evens}"

# Sorting
unsorted = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_list = sorted(unsorted)
print "Sorted: #{sorted_list}"

# Reversed
reversed_list = list(reversed(sorted_list))
print "Reversed: #{reversed_list}"

# Dictionary operations
person = {name: "Alice", age: 30, city: "NYC"}

# Keys, values, items
print "Keys: #{person.keys()}"
print "Values: #{person.values()}"

# Get with default
print "Email: #{person.get('email', 'N/A')}"
print "Name: #{person.get('name', 'Unknown')}"

# Update
person.update({email: "alice@example.com", age: 31})
print "Updated: #{person}"
