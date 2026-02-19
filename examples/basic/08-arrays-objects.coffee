# Arrays and Objects

# Array literal
fruits = ["apple", "banana", "cherry"]
print "First: #{fruits[0]}"
print "Second: #{fruits[1]}"

# Array modification
fruits[1] = "blueberry"
print "Modified: #{fruits}"

# Object literal
person = {name: "Alice", age: 30, city: "New York"}

# Access properties
print "Name: #{person.name}"
print "Age: #{person.age}"

# Bracket notation
print "City: #{person.city}"

# Modify object
person.email = "alice@example.com"
print "Email: #{person.email}"

# Nested structures
company = {name: "Tech Corp", employees: [{name: "Alice", role: "Engineer"}, {name: "Bob", role: "Designer"}]}

print "Company: #{company.name}"
print "First employee: #{company.employees[0].name}"

# Array of objects
tasks = [{id: 1, title: "Task 1", done: false}, {id: 2, title: "Task 2", done: true}, {id: 3, title: "Task 3", done: false}]

print "Task 2 done: #{tasks[1].done}"

# Mixed array
mixed = [1, "two", true, null, {key: "value"}]
print "Mixed: #{mixed}"
