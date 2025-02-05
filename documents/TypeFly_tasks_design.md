Here is the exact text extracted verbatim from the image you provided:

---

**Table 1: Benchmark tasks used in the reported evaluation.**  
We define 5 types of tasks to test TypeFly's capabilities thoroughly. Tasks 1-3 test TypeFly's basic ability to reason and plan; Tasks 4-6 test using Remote LLM in execution to generate offline plans for the undetermined targets; Tasks 7-8 test several more complex planning scenarios; Tasks 9-10 test the TypeFly's ability of exception handling; Last task evaluates the safety of MiniSpec to generate a plan with termination.

| Categories                  | ID  | Task Description                                                                                   | Scene Setup                                                                                   |
|-----------------------------|------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Basic Planning**          | 1   | Go and take a picture of the chair.                                                              | a chair in sight                                                                            |
|                             | 2   | Could you find an apple? If so, go to it.                                                        | an apple in the scene                                                                       |
|                             | 3   | Go to the largest item you can see right now.                                                    | a person, apple, and keyboard in sight                                                     |
| **LLM in Execution**        | 4   | Find something yellow and sweet.                                                                 | banana and lemon on the table behind the drone                                             |
|                             | 5   | Can you find something for cutting paper on the table? The table is on your left.               | table on the left with a pair of scissors                                                  |
|                             | 6   | Find a chair and go to the object that is closest to the chair.                                  | a chair on the back with an apple on the chair and a bottle behind the chair               |
| **Complex Planning**        | 7   | Move up for 1m and check the top of the cabinet, if you see anything red and sweet, take a picture of it. Otherwise, return to the original position. | an apple on top of the cabinet                                                             |
|                             | 8   | Can you find something for me to eat? If you can, go for it and return. Otherwise, find and go to something drinkable. | only coke on the left table without any other food                                         |
| **Incremental Planning & Replanning** | 9   | Turn around and go to the apple.                                                                | an apple on the table behind the drone with a chair blocking in between                    |
|                             | 10  | If you can see more than two people behind you, then turn to the tallest one that is behind you. | 3 people in sight and 2 other people in the back of the drone                              |
| **Safety of MiniSpec**      | 11  | Turn around in a 45-degree step until you see a person with a cup in hand.                       | none                                                                                       |

--- 

Let me know if you need further assistance!