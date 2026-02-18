# Conditional Statements

temperature = 25

# if/then/else inline
status = if temperature > 30 then "hot" else "comfortable"
print "Status: #{status}"

# Multiline if/else
if temperature > 30
  print "It is hot outside!"
else if temperature > 20
  print "It is nice and warm."
else if temperature > 10
  print "It is a bit cool."
else
  print "It is cold!"

# Postfix if
x = 10
print "x is positive" if x > 0

# unless (opposite of if)
ready = false
print "Not ready yet" unless ready

# unless with else
isRaining = false
unless isRaining
  print "No umbrella needed"
else
  print "Bring an umbrella!"

# Complex conditions
age = 25
hasLicense = true

if age >= 18 and hasLicense
  print "You can drive!"
else
  print "You cannot drive."

# Multiple conditions
score = 85
grade = 
  if score >= 90 then "A"
  else if score >= 80 then "B"
  else if score >= 70 then "C"
  else if score >= 60 then "D"
  else "F"

print "Grade: #{grade}"
