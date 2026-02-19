# Advanced Operators

# Existential operator (?)
value = null
result = value ? "default"
print "null ? default: #{result}"  # "default"

value = "exists"
result = value ? "default"
print "exists ? default: #{result}"  # "exists"

# Safe access (?.)
user = {name: "Alice", address: {city: "NYC"}}
print "City: #{user?.address?.city}"  # "NYC"

nullUser = null
print "Null city: #{nullUser?.address?.city}"  # null (no error)

# Existential assignment (?=)
config = {}
config.debug ?= false
print "Debug: #{config.debug}"  # false

config.debug ?= true
print "Debug still: #{config.debug}"  # false (not overwritten)

# Logical assignment (||=)
name = ""
name ||= "Anonymous"
print "Name: #{name}"  # "Anonymous"

name = "Bob"
name ||= "Charlie"
print "Name: #{name}"  # "Bob" (not overwritten)

# Logical assignment (&&=)
count = 10
count &&= count * 2
print "Count: #{count}"  # 20

count = 0
count &&= count * 2
print "Count: #{count}"  # 0 (falsy, not updated)

# is and isnt aliases
a = 5
b = 5
c = 10

print "a is b: #{a is b}"       # true
print "a isnt c: #{a isnt c}"   # true
print "a is c: #{a is c}"       # false

# is not combination
print "a is not b: #{not (a is b)}"  # false
print "a is not c: #{not (a is c)}"  # true

# Chained comparisons
x = 15
print "1 < x < 20: #{1 < x < 20}"       # true
print "0 <= x <= 100: #{0 <= x <= 100}" # true
print "10 < x < 15: #{10 < x < 15}"     # false

# Practical examples
# Default values
getConfig = (options) ->
  options ?= {}
  options.host ?= "localhost"
  options.port ?= 8080
  options.debug ?= false
  options

config = getConfig()
print "Default config: #{config}"

config = getConfig({port: 3000})
print "Custom port: #{config}"

# Conditional update
items = []
if len(items) == 0
  items.append("first")
print "Items: #{items}"
