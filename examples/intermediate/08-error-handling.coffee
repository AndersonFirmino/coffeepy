# Error Handling

# Basic try/catch
try
  result = 10 / 0
  print "Result: #{result}"
catch error
  print "Caught error: #{error}"

# try/catch/finally
resource = null
try
  resource = "acquired"
  print "Resource: #{resource}"
  throw "Something went wrong!"
catch error
  print "Error: #{error}"
finally
  print "Cleanup"
  resource = null

print "Resource after: #{resource}"

# Nested try/catch
try
  try
    throw "Inner error"
  catch innerError
    print "Inner caught: #{innerError}"
    throw "Re-throwing: #{innerError}"
catch outerError
  print "Outer caught: #{outerError}"

# Practical example: JSON parsing
from json import loads, dumps

parseJSON = (str) ->
  try
    data = loads(str)
    {success: true, data: data}
  catch error
    {success: false, error: error}

result1 = parseJSON('{"name": "Alice"}')
print "Valid JSON: #{result1}"

result2 = parseJSON('not valid json')
print "Invalid JSON: #{result2}"

# Multiple error types
processValue = (value) ->
  try
    if value is null
      throw "Value is null"
    if typeof value != "number"
      throw "Value must be a number"
    if value < 0
      throw "Value must be positive"
    sqrt(value)
  catch error
    -1

print "sqrt(16): #{processValue(16)}"
print "sqrt(-4): #{processValue(-4)}"
print "sqrt(null): #{processValue(null)}"

# Using finally for cleanup
class FileHandler
  open: -> print "File opened"
  close: -> print "File closed"
  read: -> 
    print "Reading..."
    "data"

processFile = ->
  handler = new FileHandler()
  try
    handler.open()
    data = handler.read()
    print "Got data: #{data}"
  finally
    handler.close()

processFile()
