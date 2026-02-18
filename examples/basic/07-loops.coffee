# Loops in CoffeePy

# while loop
i = 0
while i < 5
  print "while: #{i}"
  i += 1

# while with then
j = 0
while j < 3 then print "while-then: #{j++}"

# until loop (opposite of while)
k = 5
until k == 0
  print "until: #{k}"
  k -= 1

# for...in loop (arrays)
print "for...in:"
for item in ["apple", "banana", "cherry"]
  print "  #{item}"

# for...in with index
print "with index:"
for fruit, index in ["apple", "banana", "cherry"]
  print "  #{index}: #{fruit}"

# for...of loop (objects)
person = {name: "Alice", age: 30, city: "NYC"}
print "for...of:"
for key, value of person
  print "  #{key} = #{value}"

# for...of (keys only)
print "keys only:"
for key of person
  print "  #{key}"

# break
print "break example:"
for x in [1..10]
  break if x > 5
  print "  #{x}"

# continue
print "continue (odd only):"
for x in [1..10]
  continue if x % 2 == 0
  print "  #{x}"

# Range in loop
print "range loop:"
for n in [1..5]
  print "  #{n}"
