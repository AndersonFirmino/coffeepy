# Generators with yield
# Create Python generators that can be iterated

# Simple generator
gen = ->
  yield 1
  yield 2
  yield 3

print "Simple generator:"
g = gen()
print "  First: #{g.__next__()}"
print "  Second: #{g.__next__()}"
print "  Third: #{g.__next__()}"

# Generator with for loop
gen2 = ->
  for i in [1..5]
    yield i * 2

print "\nGenerator with for loop:"
for x in gen2()
  print "  #{x}"

# Generator with condition
evens = ->
  for i in [1..10]
    if i % 2 == 0
      yield i

print "\nEven numbers:"
for n in evens()
  print "  #{n}"

# Infinite generator (be careful!)
counter = (start) ->
  n = start
  while true
    yield n
    n += 1

print "\nCounter (first 5):"
c = counter(10)
for i in [1..5]
  print "  #{c.__next__()}"

# Generator with filtering
positive = (numbers) ->
  for n in numbers
    if n > 0
      yield n

print "\nPositive numbers:"
for p in positive([-3, -1, 0, 2, 5, -4, 8])
  print "  #{p}"

# Fibonacci generator
fib = ->
  a = 0
  b = 1
  while true
    yield a
    temp = a
    a = b
    b = temp + b

print "\nFibonacci (first 10):"
f = fib()
for i in [1..10]
  print "  #{f.__next__()}"
