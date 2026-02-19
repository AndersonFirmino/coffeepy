# Classes - Inheritance

class Animal
  constructor: (@name) ->
  
  speak: -> "#{@name} makes a sound"
  
  move: -> "#{@name} moves"

class Dog extends Animal
  constructor: (name, @breed) ->
    @name = name
  
  speak: -> "#{@name} the #{@breed} barks!"
  
  fetch: -> "#{@name} fetches the ball"

class Cat extends Animal
  constructor: (name, @lives = 9) ->
    @name = name
  
  speak: -> "#{@name} meows"
  
  landOnFeet: -> "#{@name} lands on its feet"

# Test inheritance
dog = new Dog("Rex", "German Shepherd")
print dog.speak()      # Overrides Animal.speak
print dog.move()       # Inherited from Animal
print dog.fetch()      # Dog's own method

cat = new Cat("Whiskers", 7)
print cat.speak()
print cat.landOnFeet()

# instanceof simulation
print "Dog name: #{dog.name}"
print "Dog breed: #{dog.breed}"
print "Cat lives: #{cat.lives}"

# Another inheritance example
class Vehicle
  constructor: (@brand, @model) ->
  
  info: -> "#{@brand} #{@model}"
  
  start: -> "Starting engine..."

class Car extends Vehicle
  constructor: (brand, model, @doors = 4) ->
    @brand = brand
    @model = model
  
  info: -> "#{@brand} #{@model} (#{@doors} doors)"
  
  honk: -> "Beep beep!"

class Motorcycle extends Vehicle
  constructor: (brand, model, @type = "sport") ->
    @brand = brand
    @model = model
  
  info: -> "#{@brand} #{@model} [#{@type}]"
  
  rev: -> "Vroom vroom!"

car = new Car("Toyota", "Camry", 4)
print car.info()
print car.start()
print car.honk()

bike = new Motorcycle("Kawasaki", "Ninja", "sport")
print bike.info()
print bike.rev()
