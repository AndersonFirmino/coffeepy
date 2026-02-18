# Classes - Basic

class Person
  constructor: (@name, @age) ->
  
  greet: -> "Hello, I'm #{@name}"
  
  birthday: ->
    @age += 1
    print "#{@name} is now #{@age}"

# Create instance
alice = new Person("Alice", 30)
print alice.greet()
alice.birthday()

# Access properties
print "Name: #{alice.name}"
print "Age: #{alice.age}"

# Modify properties
alice.age = 31
print "New age: #{alice.age}"

# Another class
class Rectangle
  constructor: (@width, @height) ->
  
  area: -> @width * @height
  
  perimeter: -> 2 * (@width + @height)
  
  isSquare: -> @width == @height

rect = new Rectangle(5, 10)
print "Area: #{rect.area()}"
print "Perimeter: #{rect.perimeter()}"
print "Is square: #{rect.isSquare()}"

square = new Rectangle(5, 5)
print "Square is square: #{square.isSquare()}"
