# Complete Application Example

# A simple task management system
from datetime import datetime
from json import dumps, loads

class Task
  constructor: (@title, @priority = "medium") ->
    @id = this._generateId()
    @createdAt = datetime.now()
    @completed = false
  
  _generateId: ->
    from random import randint
    randint(1000, 9999)
  
  complete: ->
    @completed = true
    @completedAt = datetime.now()
  
  toString: ->
    status = if @completed then "[x]" else "[ ]"
    "#{status} #{@title} (#{@priority})"

class TaskManager
  constructor: ->
    @tasks = []
  
  addTask: (title, priority) ->
    task = new Task(title, priority)
    @tasks.append(task)
    task
  
  completeTask: (id) ->
    for task in @tasks
      if task.id == id
        task.complete()
        return true
    false
  
  getPending: ->
    [task for task in @tasks when not task.completed]
  
  getCompleted: ->
    [task for task in @tasks when task.completed]
  
  getByPriority: (priority) ->
    [task for task in @tasks when task.priority == priority]
  
  listAll: ->
    for task in @tasks
      print task.toString()
  
  summary: ->
    total = len(@tasks)
    completed = len(@getCompleted())
    pending = total - completed
    
    """
    Task Summary
    ============
    Total: #{total}
    Completed: #{completed}
    Pending: #{pending}
    """

# Use the task manager
manager = new TaskManager()

# Add tasks
manager.addTask("Learn CoffeePy", "high")
manager.addTask("Build an app", "high")
manager.addTask("Write documentation", "medium")
manager.addTask("Fix bugs", "low")
manager.addTask("Deploy to production", "high")

print "All tasks:"
manager.listAll()

print "\nPending tasks:"
for task in manager.getPending()
  print "  #{task.toString()}"

print "\nHigh priority:"
for task in manager.getByPriority("high")
  print "  #{task.toString()}"

print "\n" + manager.summary()
