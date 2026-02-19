# Safe Access Operator (?.)
# Returns null instead of throwing error when property doesn't exist

# Basic usage - property exists
user = {name: "Alice", age: 30}
print "Name: #{user?.name}"      # → Alice
print "Age: #{user?.age}"        # → 30

# Property doesn't exist - returns null (no error!)
print "Email: #{user?.email}"    # → null

# With null object
user2 = null
print "Null user: #{user2?.name}" # → null

# Chained safe access
data = {user: {profile: {city: "NYC"}}}
print "City: #{data?.user?.profile?.city}"  # → NYC

# Chained with null in middle
data2 = {user: null}
print "City2: #{data2?.user?.profile?.city}"  # → null

# Practical use case - optional config
config = {debug: true}
print "Debug: #{config?.debug ? false}"  # → true
print "Verbose: #{config?.verbose ? false}"  # → false
