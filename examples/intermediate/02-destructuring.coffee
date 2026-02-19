# Destructuring Assignment

# Array destructuring
[a, b, c] = [1, 2, 3]
print "a=#{a}, b=#{b}, c=#{c}"

# Skip elements
temp = [1, 2, 3, 4, 5]
first = temp[0]
third = temp[2]
print "first=#{first}, third=#{third}"

# Splat (rest) at end
[head, tail...] = [1, 2, 3, 4, 5]
print "head=#{head}"
print "tail=#{tail}"

# Splat at start
[rest..., last] = [1, 2, 3, 4, 5]
print "rest=#{rest}"
print "last=#{last}"

# Splat in middle
[first, middle..., last] = [1, 2, 3, 4, 5, 6, 7]
print "first=#{first}, middle=#{middle}, last=#{last}"

# Object destructuring
{name, age} = {name: "Alice", age: 30}
print "name=#{name}, age=#{age}"

# Object with alias
{name: userName, age} = {name: "Bob", age: 25}
print "userName=#{userName}, age=#{age}"

# Destructuring with defaults
{x, y = 10} = {x: 5}
print "x=#{x}, y=#{y}"

# Nested destructuring (simplified)
data = {person: {name: "Charlie", address: {city: "NYC", zip: "10001"}}}
name = data.person.name
city = data.person.address.city
print "name=#{name}, city=#{city}"

# Array of objects (simplified)
arr = [{name: "A"}, {name: "B"}]
first = arr[0].name
second = arr[1].name
print "first=#{first}, second=#{second}"

# In function parameters (simplified)
processUser = (user) ->
  "#{user.name} (#{user.age}) - N/A"

print processUser({name: "Dave", age: 35})

# Multiple assignment
x = y = z = 0
print "x=#{x}, y=#{y}, z=#{z}"
