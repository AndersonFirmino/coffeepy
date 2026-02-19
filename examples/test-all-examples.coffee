# CoffeePy Test Runner
# Runs all example scripts with delays for demonstration
# Run: python -m coffeepy examples/test-all-examples.coffee

from time import sleep
from os import listdir, path
from subprocess import run

print "================================================"
print "     CoffeePy - Running All Examples"
print "================================================"
print ""

examples_dir = "examples"
categories = ["basic", "intermediate", "advanced", "python-interop"]

total_files = 0
passed = 0
failed = 0

for category in categories
  category_path = path.join(examples_dir, category)
  
  if path.exists(category_path)
    print "----------------------------------------"
    print category
    print "----------------------------------------"
    
    all_files = listdir(category_path)
    coffee_files = [f for f in all_files when f.endswith(".coffee")]
    coffee_files.sort()
    
    for file in coffee_files
      total_files += 1
      file_path = path.join(category_path, file)
      
      print ""
      print "[#{total_files}] #{file}"
      print "-"
      
      try
        result = run(["python", "-m", "coffeepy", file_path], capture_output=true, text=true, timeout=10)
        
        if result.returncode == 0
          passed += 1
          print result.stdout
        else
          failed += 1
          print "ERROR:"
          print result.stderr
      
      catch e
        failed += 1
        print "ERROR: #{e}"
      
      sleep(0.3)

print ""
print "================================================"
print "                  SUMMARY"
print "================================================"
print ""
print "Total: #{total_files}"
print "Passed: #{passed}"
print "Failed: #{failed}"
print ""
if failed == 0
  print "ALL EXAMPLES PASSED!"
else
  print "#{failed} examples failed."
print ""
print "================================================"
