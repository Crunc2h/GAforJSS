class FactoryManager:

    def __init__(self, machines, num_of_machines_per_stage, num_of_stages, jobs):

        self.stop_flag = False
        self.schedule = None

        self.machines = machines
        self.jobs = jobs
        self.num_of_stages = num_of_stages
        self.num_of_machines_per_stage = num_of_machines_per_stage
        self.num_of_jobs = len(jobs)

        self.current_time = 0

    def get_tardiness(self):
        total_tardiness = 0
        for job in self.jobs:
            total_tardiness += job.processing_time - job.due_time if job.processing_time - job.due_time > 0 else 0
        return total_tardiness


    def time_step(self):

        for machine in self.machines:
            machine.check_machine_process(self.current_time)

        for job in self.jobs:

            if job.being_processed:
                continue
            if job.job_done:
                continue

            current_job_stage = job.current_stage

            available_machines = [machine for machine in self.machines if machine.num_stage == current_job_stage
                                  and machine.processing_job is False]

            if len(available_machines) == 0:
                continue

            available_machine_ids = [machine.num_machine for machine in available_machines]

            if job.current_target_machine_id in available_machine_ids:
                target_machine = [machine for machine in available_machines if machine.num_machine == job.current_target_machine_id][0]
                target_machine.process_job(job, self.current_time)

        self.current_time += 1

    def update_stop_flag(self):

        return all([job.job_done for job in self.jobs])

    def assign_target_machine_ids(self):

        for job in self.jobs:
            target_machines_per_stage = []
            for i in range(self.num_of_stages):
                chromosome_segment = self.schedule[i]
                for f in range(self.num_of_machines_per_stage):
                    machine_job_processing_order = chromosome_segment[f]
                    if job.id + 1 in machine_job_processing_order:
                        target_machines_per_stage.append(f)
            job.target_machine_ids = target_machines_per_stage
            job.update_target_machine_id()

    def reset_factory(self, schedule):

        for job in self.jobs:

            job.current_stage = 0
            job.processing_time = 0
            job.current_target_machine_id = 0
            job.start_times = []
            job.end_times = []
            job.target_machine_ids = None
            job.job_done = False

        self.schedule = schedule
        self.assign_target_machine_ids()
        self.current_time = 0
        self.stop_flag = False

    def run(self, schedule):

        self.reset_factory(schedule)
        self.assign_target_machine_ids()

        while self.stop_flag is False:
            self.time_step()
            self.stop_flag = self.update_stop_flag()

        total_tardiness = self.get_tardiness()

        return self.current_time, total_tardiness