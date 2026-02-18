# Arithmetic Operations

# Basic math
a = 10
b = 3

print "Addition: #{a + b}"        # 13
print "Subtraction: #{a - b}"     # 7
print "Multiplication: #{a * b}"  # 30
print "Division: #{a / b}"        # 3.33...
print "Modulo: #{a % b}"          # 1
print "Power: #{a ** b}"          # 1000

# Augmented assignment
x = 10
x += 5   # x = 15
print "After += 5: #{x}"

x -= 3   # x = 12
print "After -= 3: #{x}"

x *= 2   # x = 24
print "After multiply: #{x}"

x /= 4   # x = 6
print "After divide: #{x}"

# Increment/Decrement
counter = 0
counter++  # counter = 1
counter++  # counter = 2
counter--  # counter = 1
print "Counter: #{counter}"

# Order of operations
result = 2 + 3 * 4    # 14 (not 20)
print "2 + 3 * 4 = #{result}"

result = (2 + 3) * 4  # 20
print "(2 + 3) * 4 = #{result}"
