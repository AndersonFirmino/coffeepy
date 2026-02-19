# String Interpolation and Templates

name = "Alice"
age = 30

# Basic interpolation
print "Hello, #{name}!"
print "You are #{age} years old."

# Expressions in interpolation
print "Next year you'll be #{age + 1}"
print "2 + 2 = #{2 + 2}"
print "Your name has #{len(name)} characters"

# Multiple interpolations
print "#{name} is #{age} years old and lives in #{'NYC'}"

# Block strings
message = """
Dear #{name},

Thank you for joining our service.
Your account is now active.

Best regards,
The Team
"""
print message

# Single-quoted block strings (no interpolation)
literal = '''
This has #{no} interpolation
'''
print literal

# Complex expressions
items = [1, 2, 3, 4, 5]
print "Sum of #{items} is #{sum(items)}"

# Conditional in interpolation
score = 85
print "You #{if score >= 60 then 'passed' else 'failed'}"

# Ternary-like
status = "Status: #{if age >= 18 then 'Adult' else 'Minor'}"
print status
