# A GA solution for JSSP
- Job-shop scheduling, the job-shop problem (JSP) or job-shop scheduling problem (JSSP) is an optimization problem in computer science and operations research. It is a variant of optimal job scheduling. 
In a general job scheduling problem, we are given n jobs J1, J2, ..., Jn of varying processing times, which need to be scheduled on m machines with varying processing power, while trying to minimize the makespan – the total length of the schedule (that is, when all the jobs have finished processing).

- I made a small simulation of the job processing process in a factory and coded a genome representation of specific job schedules. It works by initializing a specified number of randomized schedule genomes, selecting the best makespan from all of the generations and crossbreeding them, rinse and repeat until finding a better result through crossbreeding becomes impractical in computation time or specified generation is reached before that happens.

  [For further reading](https://www.researchgate.net/publication/242081421_A_JOB-SHOP_SCHEDULING_PROBLEM_JSSP_USING_GENETIC_ALGORITHM_GA)
