# Ranges and Slices

# Inclusive range (..)
oneToFive = [1..5]
print "1..5: #{oneToFive}"

# Exclusive range (...)
oneToFour = [1...5]
print "1...5: #{oneToFour}"

# Descending range
countdown = [5..1]
print "5..1: #{countdown}"

# Range with step
evens = [0..10 by 2]
print "0..10 by 2: #{evens}"

odds = [1..10 by 2]
print "1..10 by 2: #{odds}"

# Ranges with variables
start = 5
end = 10
range = [start..end]
print "Variable range: #{range}"

# Slicing arrays
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Inclusive slice
print "numbers[2..4]: #{numbers[2..4]}"   # [3, 4, 5]

# Exclusive slice
print "numbers[2...5]: #{numbers[2...5]}" # [3, 4]

# From start
print "numbers[..3]: #{numbers[..3]}"     # [1, 2, 3, 4]

# To end
print "numbers[7..]: #{numbers[7..]}"     # [8, 9, 10]

# Negative ranges for countdown
print "Negative step [10..0 by -2]: #{[10..0 by -2]}"

# Using ranges in loops
print "Loop with range:"
for i in [1..5]
  print "  Item #{i}"
