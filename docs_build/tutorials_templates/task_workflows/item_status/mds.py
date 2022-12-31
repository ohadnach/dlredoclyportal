def func1():
    """
    ## Item Status
    To flag for finishing work on an item in a task, the worker assigns a status to the item.
    The Dataloop system has default statuses, as well as the option to add custom statuses
    Default statuses for annotation tasks: COMPLETE and DISCARD
    Default statuses for QA tasks: APPROVE and DISCARD

    ### 1. Set status on an item in task
    """


def func2():
    """
    ### 2. Set status on multiple items
    #### 1. Using dataset and filter (recommended for using with multiple items from different tasks)
   """


def func3():
    """
    #### 2. Use task entity (recommended for items of the same task)
   """


def func4():
    """
    ### 3. Clear status from an item (no-status)
    Clearing a status from an item will make it available again for work in the respective task, and the worker (annotator)
    will see the item in the assignment (either QA or annotations).
    """


def func5():
    """
    ### 4. Create a task with item actions (statuses options)
    """


def func6():
    """
    <div style="background-color: lightblue; color: black; width: 50%; padding: 10px; border-radius: 15px 5px 5px 5px;"><b>Note</b><br>
    Changing the statuses in the task doesn't change the status on any items that already received a status.
    """
