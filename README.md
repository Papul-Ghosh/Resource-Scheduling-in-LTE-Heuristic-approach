# Resource-Scheduling-in-LTE-Heuristic-approach
Resource Scheduling in LTE to minimize interference applying Genetic Algorithm


**Technology used:** Python, Gurobi solver.

**Project Summary:**

The task is to allocate same resource block twice in an optimised way to minimize interference at the receiver of two users using same resource block.

Here we have implemented the Genetic Algorithm as a heuristic approach. For N number of users and M=N/2 number of resources blocks the implemented steps are as follows:
1. Encoding:

The size of the initial population is taken as N, where each of the N chromosomes represents the M number of binary strings that denote the assignment of the users to the resource blocks. For example, for N=4 and M=2, one chromosome can be represented as ['1010', '0101']. Here each of the 2 binary strings denotes a resource that holds 2 communication simultaneously. It is evident that number of 1’s in each string cannot be larger than 2. Moreover, the encoding also takes care of that one user can be allocated to exactly one resource block. The and (&&) operation of any 2 binary strings are always 0.

2. Selection:

Here we have implemented the Tournament Selection Method, where we are randomly picking any 2 chromosomes and comparing their fitness values (ie. interference values). The one minimum interference is considered as the best fit to be chosen for the next generation as per the Search Darwin's theory of evolution by natural selection.

Eg.: Interference of ['1010', '0101'] < Interference of ['1001', '0110']

Therefore ['1010', '0101'] is chosen for the next generation

3. Mutation:
Here we have randomly picked any chromosome and swapped the user allocations to the resource blocks (ie. substrings of each RB) between each binary strings that can be considered as the evolution of the chromosome. During evolution, we have also taken care of the basic constraints of resource allocation.

Eg.: Before mutation: chromosome: ['1001', '0110']

After mutation: chromosome: ['1010', '0101']
