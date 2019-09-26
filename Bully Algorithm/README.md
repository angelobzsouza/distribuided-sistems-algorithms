# Bully Algorithm (Leader Election)

This code simulate the bully algorithm to elect a new leader in the distributed system. Every time a process receive a election message, it send messages to all process next to it. If dosn't receive any answer, send message to all indicating that it's the new leader. Every time a process know that some other process is dead, it's start a new election.

There is a simple menu to help to understand the algorithm operation.

## Running
1. Open five different terminals
2. Run the application in each one with the following commands

```
python bullyAlgorithm.py 9000 0
```
```
python bullyAlgorithm.py 9001 1
```
```
python bullyAlgorithm.py 9002 2
```
```
python bullyAlgorithm.py 9003 3
```
```
python bullyAlgorithm.py 9004 4
```

3. The instances will decide alone when want to resource and prints messages to show what is happen in process.