# Explanation of the approach taken

Interpret the problem as a search problem, since I suspect this is NP-Complete. This problem has a highly combinatorial search space and you are asked to list all feasible solutions in the space. Therefore, the most logical choice was to implement a CSP. The problem is modeled as a matrix of domains, where the domain of the index (i,j) are composed by all the possible pieces that could go in that position. By modeling the problem as a search problem, each rotation of the different pieces was considered different values for the domain. As it is necessary to list all the feasible solutions of the space, the implemented CSP has only the metaheristics "constraint propagation" and "variable selection", as the rest are more oriented to find a feasible element than to reduce the size of the space. Finally, when it was indicated that the direction of the puzzle does not matter, the first piece that could go in the first corner was selected and the search was started.

To run the script use the following command

```bash
$> python script.py 4x4.txt
```

# Any other significant enhancement not listed on the requirements

The find method of the implemented CSP supports passing an incomplete puzzle as a parameter, in which case an attempt will be made to complete it.

```bash
$> python script.py 4x4.txt --base my_puzzle.txt --pretty 1
```

# How could you improve the algorithm in the future

The most costly features of the proposed solutions are 1) the total exploration of the space (features of the problem) and 2) during the constraint propagation process an exponential amount of matrices are created. A more recursive, object-oriented implementation could be tested in the future. The time cost would not be affected since the main process would still be a DFS, but the control of the domains per the instances may reduce this problem #2.

Another idea could be in the case where the constraints of the problem change and not all feasible elements of the space are requested. If you ask for a solution or a semi-optimal, you could try other heuristics, in particular I think that the "ant colony optimization" could work because the structure of the problem would facilitate transformation to a graph.

# What Went Well

I easily recognized the dimensions of the problem, which quickly led me to the idea of using metaheuristics and modeling it as a search problem.

# How long did you spend solving this problem?

The implementation took me about 3 hours. Although I knew the idea of CSP, its optimizations and its use cases, I had never implemented it. For that reason I wasted a lot of time at the end fixing details.
