from job_creator import JobCreator
from job import Job
from factory_creator import FactoryCreator
from genetic_job_shop_scheduler import GenJobSS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

NUM_OF_STAGES = 6
NUM_OF_MACHINES_PER_STAGE = 3
NUM_OF_JOBS = 5
MEAN_PROCESSING_TIME = 6
MAX_PROCESSING_TIME = 9
MIN_PROCESSING_TIME = 3
STD = 3


csv_file = pd.read_csv('JobPtimes.csv')

stage_values = []
for row in csv_file.iterrows():
    stage_values.append(row[1].values)


due_dates = csv_file['60']
csv_file = csv_file.drop(['60'], axis=1)

def convert_job_timetable(desired_shape, timetables):
    new_timetables = []
    for stage_timetable in timetables:
        new_timetable = np.array([stage_timetable])
        timetable = np.vstack([new_timetable for i in range(desired_shape[0])])
        new_timetables.append(timetable.T)
    return new_timetables

new_job_values = convert_job_timetable((3,6), stage_values)
converted_job_values = []
for i in range(len(new_job_values)):
    new_job = Job(id=i,
                  due_time=due_dates[i],
                  timetable=new_job_values[i],
                  max_stage=6)
    converted_job_values.append(new_job)

jobs = JobCreator.create_jobs(NUM_OF_MACHINES_PER_STAGE,
                              NUM_OF_STAGES,
                              NUM_OF_JOBS,
                              MEAN_PROCESSING_TIME,
                              MAX_PROCESSING_TIME,
                              MIN_PROCESSING_TIME,
                              STD)




factory = FactoryCreator.create_factory(NUM_OF_MACHINES_PER_STAGE, NUM_OF_STAGES, converted_job_values)


gen_job_ss = GenJobSS(factory=factory,
                      initial_generation_search_length=5,
                      num_of_searchs_before_termination=500,
                      num_of_generations=10,
                      population_size=100,
                      crossover_rate=0.5,
                      mutation_probability=0.01,
                      initial_mutation_probability=0.45,
                      mutation_probability_convergence_percentage=0.5,
                      boundary_swap_probability=0.01,
                      initial_bs_probability=0.1,
                      bs_probability_convergence_percentage=0.1)

avg_ct, avg_tdns, best_solution = gen_job_ss.run_ga()
'''
plt.plot(avg_ct)
plt.xlabel('Generations')
plt.ylabel('Completion Time')
plt.title('Average Completion Time Acroos Generations')
plt.show()
'''

[print(job.processing_time) for job in converted_job_values]

tasks = {}
for i in range(len(factory.jobs)):
    job = factory.jobs[i]
    for f in range(NUM_OF_STAGES):
        tasks[f"Job {job.id + 1}"] = {"start":job.start_times[f], "end":job.end_times[f]}

    # Generate Gantt Chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.tab10.colors
yticks = []
yticklabels = []

for i in range(len(best_solution.chromosome)):
    for f in range(len(best_solution.chromosome[i])):
        yticks.append(len(yticks))
        yticklabels.append(f'Stage {i + 1} Machine {f + 1}')
        for n in range(len(best_solution.chromosome[i][f])):
            job = [_job for _job in factory.jobs if _job.id + 1 == best_solution.chromosome[i][f][n]][0]
            end_time = job.end_times[i]
            start_time = job.start_times[i]
            id = job.id

            ax.barh(len(yticks) - 1, end_time - start_time, left=start_time,
                    color=colors[id % len(colors)], edgecolor='black', height=0.4)

            ax.text(start_time + (end_time - start_time) / 2, len(yticks) - 1,
                    f'Job {id + 1}', ha='center', va='center', color='white', fontsize=8)

ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)
ax.set_xlabel('Time')
ax.set_title('Gantt Chart of Job Processing')
plt.tight_layout()
plt.show()

































