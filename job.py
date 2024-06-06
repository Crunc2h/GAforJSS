from schedule_chromosome import ScheduleChromosome


class Job:

    def __init__(self, id, timetable, due_time, max_stage):

        self.id = id
        self.max_stage = max_stage
        self.stage_timetable = timetable
        self.due_time = due_time

        self.target_machine_ids = None
        self.being_processed = False
        self.job_done = False

        self.current_target_machine_id = 0
        self.current_stage = 0
        self.processing_time = 0

        self.start_times = []
        self.end_times = []

    def get_job_processing_time(self, num_machine):

        return self.stage_timetable[self.current_stage][num_machine]

    def get_machine_times_of_stage(self):

        return self.stage_timetable[self.current_stage]

    def update_target_machine_id(self):

        self.current_target_machine_id = self.target_machine_ids[self.current_stage]

    def start_job_processing(self, num_machine, job_start_time, job_end_time):

        self.being_processed = True
        self.processing_time += self.get_job_processing_time(num_machine)
        self.start_times.append(job_start_time)
        self.end_times.append(job_end_time)


    def end_job_processing(self):

        if self.current_stage == self.max_stage - 1:
            self.being_processed = False
            self.job_done = True
        else:
            self.being_processed = False
            self.current_stage += 1
            self.update_target_machine_id()
























