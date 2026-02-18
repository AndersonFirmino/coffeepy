# Switch Statements

day = "Mon"

# Basic switch
result = switch day
  when "Mon" then "Monday"
  when "Tue" then "Tuesday"
  when "Wed" then "Wednesday"
  when "Thu" then "Thursday"
  when "Fri" then "Friday"
  when "Sat", "Sun" then "Weekend"
  else "Unknown"

print "Day: #{result}"

# Switch with multiline body
action = switch day
  when "Mon"
    "Start of work week"
  when "Fri"
    "End of work week"
  when "Sat", "Sun"
    "Relax time"
  else
    "Midweek"

print "Action: #{action}"

# Switch without value (case-like)
score = 75
grade = switch
  when score >= 90 then "A"
  when score >= 80 then "B"
  when score >= 70 then "C"
  when score >= 60 then "D"
  else "F"

print "Grade: #{grade}"

# Multiple conditions
x = 15
category = switch
  when x < 0 then "negative"
  when x == 0 then "zero"
  when x > 0 and x < 10 then "small positive"
  when x >= 10 and x < 100 then "medium positive"
  else "large positive"

print "Category: #{category}"

# Type checking simulation
value = [1, 2, 3]
type = switch
  when value is null then "null"
  when typeof value == "object" then "object"
  else "other"

print "Type: #{type}"
