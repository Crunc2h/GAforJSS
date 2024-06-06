import random


class ScheduleChromosome:

    def __init__(self,
                 machines_per_stage,
                 num_of_stages,
                 num_of_jobs,
                 random_init=True,
                 assigned_encoded_schedule=None):

        if random_init:
            self.chromosome = self.create_encoded_schedule(num_of_jobs=num_of_jobs,
                                                           machines_per_stage=machines_per_stage,
                                                           num_of_stages=num_of_stages)
        else:
            self.chromosome = assigned_encoded_schedule

        self.makespan = None
        self.tardiness = None
        self.index_in_generation = None

    @staticmethod
    def create_encoded_schedule(num_of_jobs, machines_per_stage, num_of_stages):

        chromosome_segments = []

        for i in range(num_of_stages):
            jobs_per_machine = [[] for i in range(machines_per_stage)]
            available_jobs = random.sample(range(1, num_of_jobs + 1), num_of_jobs)

            for f in range(num_of_jobs):
                chosen_job = random.choice(available_jobs)
                random.choice(jobs_per_machine).append(chosen_job)
                available_jobs.pop(available_jobs.index(chosen_job))
            chromosome_segments.append(jobs_per_machine)

        return chromosome_segments














