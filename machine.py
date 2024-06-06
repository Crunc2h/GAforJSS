class Machine:

    def __init__(self, num_stage, num_machine):

        self.num_stage = num_stage
        self.num_machine = num_machine

        self.processing_job = False
        self.current_job = None

        self.job_start_time = 0
        self.job_end_time = 0

    def process_job(self, job, job_start_time):

        self.processing_job = True
        self.current_job = job
        self.job_start_time = job_start_time
        self.job_end_time = job_start_time + self.current_job.get_job_processing_time(self.num_machine)
        self.current_job.start_job_processing(self.num_machine, job_start_time, self.job_end_time)

    def check_machine_process(self, current_time):

        if self.current_job is not None:
            if current_time == self.job_end_time:
                self.current_job.end_job_processing()
                self.current_job = None
                self.processing_job = False