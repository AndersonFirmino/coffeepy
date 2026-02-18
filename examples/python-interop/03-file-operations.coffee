# File Operations

import os
from os.path import exists, join

# Create test file
testFile = "test_data.txt"

# Write file
content = """Hello from CoffeePy!
This is line 2.
And line 3.
"""

# Using Python's open
f = open(testFile, "w")
f.write(content)
f.close()

print "File written: #{testFile}"

# Read file
f = open(testFile, "r")
readContent = f.read()
f.close()

print "Content read:"
print readContent

# Check if file exists
print "File exists: #{exists(testFile)}"

# Get file info
print "File size: #{os.path.getsize(testFile)} bytes"

# Read lines
f = open(testFile, "r")
lines = f.readlines()
f.close()

print "Lines: #{lines}"

# Process each line
print "Processing lines:"
for line, i in lines
  print "  Line #{i}: #{line.trim()}"

# Clean up
os.remove(testFile)
print "File removed: #{testFile}"
print "Still exists: #{exists(testFile)}"
