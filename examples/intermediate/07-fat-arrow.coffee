# Fat Arrow and Binding

# Problem: regular arrow loses 'this' context
class Button
  constructor: (@label) ->
  
  # Regular arrow - 'this' may be lost
  regularClick: ->
    print "Clicked: #{@label}"
  
  # Fat arrow - 'this' is always bound
  boundClick: =>
    print "Bound click: #{@label}"

# Example with callback simulation
class Timer
  constructor: (@name) ->
    @count = 0
  
  # Fat arrow preserves 'this'
  start: =>
    @count += 1
    print "#{@name}: count = #{@count}"

timer = new Timer("MyTimer")
callback = timer.start

# This works because of fat arrow
callback()  # "MyTimer: count = 1"
callback()  # "MyTimer: count = 2"

# Class with event handlers
class EventEmitter
  constructor: ->
    @listeners = {}
  
  on: (event, handler) =>
    @listeners[event] ?= []
    @listeners[event].push(handler)
  
  emit: (event, data) =>
    handlers = @listeners[event] ? []
    for handler in handlers
      handler(data)

emitter = new EventEmitter()
emitter.on("test", (msg) -> print "Received: #{msg}")
emitter.emit("test", "Hello!")

# Counter with bound methods
class Counter
  constructor: (@initial = 0) ->
    @count = @initial
  
  increment: =>
    @count += 1
    @count
  
  decrement: =>
    @count -= 1
    @count
  
  reset: =>
    @count = @initial
    @count

counter = new Counter(10)
inc = counter.increment
dec = counter.decrement

print inc()  # 11
print inc()  # 12
print dec()  # 11
