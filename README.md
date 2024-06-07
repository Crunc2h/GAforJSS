# A GA solution for JSSP
- Job-shop scheduling, the job-shop problem (JSP) or job-shop scheduling problem (JSSP) is an optimization problem in computer science and operations research. It is a variant of optimal job scheduling. 
In a general job scheduling problem, we are given n jobs J1, J2, ..., Jn of varying processing times, which need to be scheduled on m machines with varying processing power, while trying to minimize the makespan – the total length of the schedule (that is, when all the jobs have finished processing).

- I made a small simulation of the job processing process in a factory and coded a genome representation of specific job schedules. It works by initializing a specified number of randomized schedule genomes, selecting the best makespan from all of the generations and crossbreeding them, rinse and repeat until finding a better result through crossbreeding becomes impractical in computation time or specified generation is reached before that happens.

- My own addition to the solution was to add border mutations to the crossover process. Let Parent A possess an array of genes(a genome) [Gene A, Gene B, Gene C] and let Parent B possess [Gene D, Gene F, Gene E]. Each gene in itself is an array that represents which job is to be assigned at which machine at which stage and order (ex. Gene A[Stage 1[Machine 1 -> J1, J2, J3 & Machine 2 -> J4, J5, J6], Stage 2[Machine 3 -> J3, J5, J6 & Machine 4 -> J1, J4, J2]] and so on.) In crossover, a randomized section of the genes are taken from each parent and mixed to get a child genome. I made it so that during the splicing of the genome, borders to be spliced at may be interchanged between Parent A and Parent B, resulting in better exploration of the solution space. I observed close to %12 improvement on resulting tardiness and makespan values, which might seem small but it is a result that may shave off a week or two in the industrial scales and %16 improvement on computation time for the solution convergence. (Of course, all of this is empirical, I don't claim this to be a scientific discovery)

  [For further reading](https://www.researchgate.net/publication/242081421_A_JOB-SHOP_SCHEDULING_PROBLEM_JSSP_USING_GENETIC_ALGORITHM_GA)
