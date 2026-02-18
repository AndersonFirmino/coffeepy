# Functions in CoffeePy

# Basic function
greet = -> "Hello!"
print greet()  # "Hello!"

# Function with parameter
double = (x) -> x * 2
print double(5)  # 10

# Multiple parameters
add = (a, b) -> a + b
print add(3, 4)  # 7

# Implicit call (no parens needed)
square = (x) -> x * x
print square 5  # 25

# Multiline function
calculateArea = (width, height) ->
  area = width * height
  "The area is #{area}"

print calculateArea(5, 10)

# Default parameters
greetPerson = (name = "World") -> "Hello, #{name}!"
print greetPerson()       # "Hello, World!"
print greetPerson("Alice") # "Hello, Alice!"

# Multiple default parameters
configure = (host = "localhost", port = 8080) ->
  "Connecting to #{host}:#{port}"

print configure()              # "localhost:8080"
print configure("example.com") # "example.com:8080"

# Rest parameters (splat)
sum = (numbers...) ->
  total = 0
  for n in numbers
    total += n
  total

print sum(1, 2, 3)      # 6
print sum(1, 2, 3, 4, 5) # 15

# Closures
createCounter = ->
  count = 0
  ->
    count += 1
    count

counter = createCounter()
print counter()  # 1
print counter()  # 2

# Higher-order functions
applyTwice = (fn, x) -> fn(fn(x))
doubleIt = (x) -> x * 2
print applyTwice(doubleIt, 3)  # 12 (3 * 2 * 2)
