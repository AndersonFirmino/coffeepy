# Demonstration of all new CoffeePy features
# Run: python -m coffeepy examples/all-new-features.coffee

print "=================================================="
print "         CoffeePy v1.1 - New Features Demo"
print "=================================================="

# ============================================
# 1. SAFE ACCESS (?.)
# ============================================
print ""
print "1. SAFE ACCESS OPERATOR (?.)"
print "------------------------------"

user = {name: "Alice", age: 30}

print "Existing property: #{user?.name}"
print "Missing property: #{user?.email}"
print "Null object: #{null?.anything}"

data = {user: {name: "Bob"}}
print "Chained: #{data?.user?.name}"

# ============================================
# 2. BETTER ERROR MESSAGES
# ============================================
print ""
print "2. BETTER ERROR MESSAGES"
print "------------------------------"

print "Try undefined var to see better errors with context!"

# ============================================
# 3. GENERATORS
# ============================================
print ""
print "3. GENERATORS (yield)"
print "------------------------------"

# Simple generator
countdown = ->
  start = 5
  for i in [start..1]
    yield i

print "Countdown from 5:"
for n in countdown()
  print "  #{n}"

# Generator with transformation
doubler = ->
  items = [1,2,3,4,5]
  for item in items
    yield item * 2

print ""
print "Doubled values:"
for x in doubler()
  print "  #{x}"

# ============================================
# 4. RANGE IMPROVEMENTS
# ============================================
print ""
print "4. RANGE IN FOR LOOPS"
print "------------------------------"

print "Range [1..5]:"
for i in [1..5]
  print "  #{i}"

print ""
print "Range with step [0..10 by 2]:"
for i in [0..10 by 2]
  print "  #{i}"

print ""
print "Descending [5..1]:"
for i in [5..1]
  print "  #{i}"

# ============================================
# 5. ALL FEATURES TOGETHER
# ============================================
print ""
print "5. COMBINED: Safe Access + Generators"
print "------------------------------"

# Generator that yields safe access results
getNames = ->
  users = [{name: "Alice"}, {age: 25}, {name: "Bob"}]
  for user in users
    name = user?.name
    yield name ? "Unknown"

print "Names with safe access in generator:"
for name in getNames()
  print "  #{name}"

# ============================================
# SUMMARY
# ============================================
print ""
print "=================================================="
print "All features working!"
print "=================================================="
