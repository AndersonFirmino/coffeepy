# Comprehensions

# Array comprehensions
numbers = [1, 2, 3, 4, 5]

# Transform
doubled = [x * 2 for x in numbers]
print "Doubled: #{doubled}"

# Filter with when
evens = [x for x in [1..10] when x % 2 == 0]
print "Evens: #{evens}"

# Transform and filter
largeEvens = [x * 10 for x in [1..20] when x % 2 == 0]
print "Large evens: #{largeEvens}"

# With index
items = ["a", "b", "c"]
indexed = ["#{i}: #{items[i]}" for i in [0..2]]
print "Indexed: #{indexed}"

# Nested comprehensions
matrix = [[x * y for x in [1, 2, 3]] for y in [1, 2]]
print "Matrix: #{matrix}"

# From range
squares = [x * x for x in [1..5]]
print "Squares: #{squares}"

# Object comprehensions
# Basic
squaredObj = {x: x * x for x in [1, 2, 3, 4, 5]}
print "Squared object: #{squaredObj}"

# From object
prices = {apple: 1.50, banana: 0.75, cherry: 2.00}
withTax = {k: v * 1.1 for k, v of prices}
print "With tax: #{withTax}"

# With filter
expensive = {k: v for k, v of prices when v > 1.00}
print "Expensive: #{expensive}"

# Practical example: Filter active users
users = [{name: "Alice", active: true}, {name: "Bob", active: false}, {name: "Charlie", active: true}]

activeNames = [user.name for user in users when user.active]
print "Active users: #{activeNames}"

# Create lookup object
lookup = {}
for user in users
  lookup[user.name] = user
print "Lookup: #{lookup}"
