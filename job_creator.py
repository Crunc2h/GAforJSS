import random
import numpy as np
from scipy.stats import truncnorm
from job import Job

SEED = 42
np.random.seed(SEED)
random.seed(SEED)


class JobCreator:

    @staticmethod
    def create_jobs(machine_per_stage, num_of_stages, num_of_jobs, mean_processing_time, max_processing_time, min_processing_time, std):
        jobs = []
        job_timetables = [JobCreator.create_random_job_timetable(machine_per_stage,
                                                                 num_of_stages,
                                                                 mean_processing_time,
                                                                 max_processing_time,
                                                                 min_processing_time,
                                                                 std) for i in range(num_of_jobs)]

        for i in range(len(job_timetables)):
            job_due_time = int(mean_processing_time * random.uniform(2, 3))
            job = Job(id=i, timetable=job_timetables[i], due_time=job_due_time, max_stage=num_of_stages)
            jobs.append(job)

        return jobs

    @staticmethod
    def create_random_job_timetable(machine_per_stage, num_of_stages, job_min_processing_time, job_max_processing_time, job_mean_processing_time, std):
        timetable = np.zeros((num_of_stages, machine_per_stage))
        for i in range(timetable.shape[0]):
            for f in range(timetable.shape[1]):
                timetable[i][f] = JobCreator.get_truncated_normal(job_mean_processing_time, std, job_min_processing_time, job_max_processing_time)
        return timetable

    @staticmethod
    def get_truncated_normal(mean, sd, low, upp):
        a = (low - mean) / sd
        b = (upp - mean) / sd

        truncated_norm = truncnorm(a, b, loc=mean, scale=sd)

        return int(truncated_norm.rvs())