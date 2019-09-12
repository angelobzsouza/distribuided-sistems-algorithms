# Ricart-Agrawala Mutual Exclusion Algorithm

This code simulate a situation where two or more nodes wants to use one same critical resouce at same time. The algorithm used to solve the problem was Ricart-Agrawala's adaptation that works in the follow way:

1. If it's not using resource and don't want to do it, respond OK;
2. If it's using resource, responde NO;
3. If it's not using resource but want to do it, compare its own current time to the resquest's time, if its own time is bigger, respond OK, if isn't, respond NO.

PS: This exercise use Total Order Multicas algorithm as base

## Running
1. Open three different terminals
2. Run the application in each one with the following commands

```
python mutualExclusion.py 9000 0
```
```
python mutualExclusion.py 9001 1
```
```
python mutualExclusion.py 9002 2
```

3. The instances will decide alone when want to use one resource, print a message when this happen and when using one.