# Comparison Operators

a = 10
b = 20

# Basic comparisons
print "a == b: #{a == b}"   # false
print "a != b: #{a != b}"   # true
print "a < b: #{a < b}"     # true
print "a <= b: #{a <= b}"   # true
print "a > b: #{a > b}"     # false
print "a >= b: #{a >= b}"   # false

# is and isnt aliases
print "a is b: #{a is b}"       # false (same as ==)
print "a isnt b: #{a isnt b}"   # true (same as !=)

# Chained comparisons
x = 15
print "1 < x < 20: #{1 < x < 20}"     # true
print "10 <= x <= 20: #{10 <= x <= 20}" # true

# Logical operators
t = true
f = false

print "t and f: #{t and f}"   # false
print "t or f: #{t or f}"     # true
print "not t: #{not t}"       # false

# Combined
age = 25
isAdult = age >= 18
print "Is adult: #{isAdult}"  # true

# Membership with in
numbers = [1, 2, 3, 4, 5]
print "3 in numbers: #{3 in numbers}"  # true
print "10 in numbers: #{10 in numbers}" # false

# Membership with of
person = {name: "Alice", age: 30}
print "name of person: #{'name' of person}"  # true
print "email of person: #{'email' of person}" # false
