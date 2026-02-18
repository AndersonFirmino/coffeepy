# Python Standard Library - Basics

# OS module
import os
print "Current directory: #{os.getcwd()}"
print "Environment USER: #{os.getenv('USER')}"
print "Path separator: #{os.sep}"

# os.path
from os.path import join, exists, basename, dirname
path = join("folder", "subfolder", "file.txt")
print "Joined path: #{path}"

# DateTime
from datetime import datetime, timedelta
now = datetime.now()
print "Now: #{now}"
print "Year: #{now.year}"
print "Month: #{now.month}"

tomorrow = now + timedelta(days=1)
print "Tomorrow: #{tomorrow}"

nextWeek = now + timedelta(weeks=1)
print "Next week: #{nextWeek}"

# Math
from math import sqrt, pi, sin, cos, floor, ceil
print "Pi: #{pi}"
print "Sqrt of 16: #{sqrt(16)}"
print "Sin(0): #{sin(0)}"
print "Floor(3.7): #{floor(3.7)}"
print "Ceil(3.2): #{ceil(3.2)}"

# Random
from random import random, randint, choice, shuffle
print "Random float: #{random()}"
print "Random int 1-10: #{randint(1, 10)}"
print "Choice: #{choice([1, 2, 3, 4, 5])}"

items = [1, 2, 3, 4, 5]
shuffle(items)
print "Shuffled: #{items}"

# JSON
from json import dumps, loads
data = {name: "Alice", age: 30, active: true}
jsonStr = dumps(data)
print "JSON: #{jsonStr}"

parsed = loads(jsonStr)
print "Parsed name: #{parsed.name}"

# String formatting
print "Formatted: #{'%s is %d years old'.format('Bob', 25)}"
