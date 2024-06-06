import random
import copy
from schedule_chromosome import ScheduleChromosome


class GenJobSS:

    def __init__(self,
                 factory,
                 num_of_generations,
                 num_of_searchs_before_termination,
                 initial_generation_search_length,
                 population_size,
                 crossover_rate,
                 mutation_probability,
                 initial_mutation_probability,
                 mutation_probability_convergence_percentage,
                 boundary_swap_probability,
                 initial_bs_probability,
                 bs_probability_convergence_percentage
                 ):

        self.factory = factory
        self.num_of_jobs = factory.num_of_jobs
        self.num_of_machines_per_stage = factory.num_of_machines_per_stage
        self.num_of_stages = factory.num_of_stages

        self.initial_random_search_length = initial_generation_search_length
        self.num_of_searchs_before_termination = num_of_searchs_before_termination
        self.num_of_generations = num_of_generations
        self.crossover_rate = crossover_rate
        self.population_size = population_size

        self.mutation_probability = mutation_probability
        self.initial_mutation_probability = initial_mutation_probability
        self.mutation_probability_convergence_percentage = mutation_probability_convergence_percentage

        self.boundary_swap_probability = boundary_swap_probability
        self.initial_bs_probability = initial_bs_probability
        self.bs_probability_convergence_percentage = bs_probability_convergence_percentage

        self.current_generation = None

    def run_ga(self):

        self.current_generation = self.select_initial_generation()

        mutation_probability_decay_rate = GenJobSS.get_probability_decay_rate(initial_probability=self.initial_mutation_probability,
                                                                              specified_probability=self.mutation_probability,
                                                                              num_of_generations=self.num_of_generations,
                                                                              probability_convergence_percentage=self.mutation_probability_convergence_percentage)

        boundary_swap_probability_decay_rate = GenJobSS.get_probability_decay_rate(initial_probability=self.initial_bs_probability,
                                                                                   specified_probability=self.boundary_swap_probability,
                                                                                   num_of_generations=self.num_of_generations,
                                                                                   probability_convergence_percentage=self.bs_probability_convergence_percentage)

        current_mutation_probability = self.initial_mutation_probability
        current_boundary_swap_probability = self.initial_bs_probability

        average_tardiness_values = []
        average_completion_time_values = []

        for i in range(self.num_of_generations):

            self.current_generation = GenJobSS.simulate_generation(factory=self.factory,
                                                                   generation=self.current_generation)

            best_members_in_generation = GenJobSS.tournament_selection(generation=self.current_generation)
            worst_member_in_generation = self.current_generation[0]

            for member in self.current_generation:

                if member.makespan > worst_member_in_generation.makespan:
                    worst_member_in_generation = member

            chosen_offspring = None
            search_count = 0

            while chosen_offspring is None and search_count < self.num_of_searchs_before_termination:

                sampled_parents = random.sample(best_members_in_generation, 2)
                offspring_1, offspring_2 = self.create_offsprings_from_selection(parent_1=sampled_parents[0],
                                                                                 parent_2=sampled_parents[1],
                                                                                 crossover_rate=self.crossover_rate,
                                                                                 mutation_probability=current_mutation_probability,
                                                                                 boundary_swap_probability=current_boundary_swap_probability)
                offspring_1, offspring_2 = self.simulate_generation(generation=[offspring_1, offspring_2],
                                                                    factory=self.factory)

                better_offspring = offspring_1 if offspring_1.makespan <= offspring_2.makespan else offspring_2
                chosen_offspring = better_offspring \
                    if better_offspring.makespan < worst_member_in_generation.makespan \
                    else None
                search_count += 1

            if chosen_offspring is None and search_count > self.num_of_searchs_before_termination:
                self.num_of_generations = i
                break
            elif chosen_offspring is None:
                continue
            else:
                self.current_generation[worst_member_in_generation.index_in_generation] = chosen_offspring

            if current_mutation_probability > self.mutation_probability:
                current_mutation_probability = GenJobSS.apply_probability_decay(current_mutation_probability,
                                                                                mutation_probability_decay_rate)

            if current_boundary_swap_probability > self.boundary_swap_probability:
                current_boundary_swap_probability = GenJobSS.apply_probability_decay(current_boundary_swap_probability,
                                                                                     boundary_swap_probability_decay_rate)

            average_completion_time = GenJobSS.get_average_completion_time_in_gen(self.current_generation)
            average_tardiness = GenJobSS.get_average_tardiness_in_gen(self.current_generation)

            average_completion_time_values.append(average_completion_time)
            average_tardiness_values.append(average_tardiness)

            print(f"Generation #{i + 1} --- Average Completion Time = {average_completion_time} | Average Tardiness = {average_tardiness}")

        best_solution = self.get_best_member_in_generation(self.current_generation)

        print("===========================REPORT===========================\n")
        print(f"Best solution found in {self.num_of_generations} generations is schedule with {best_solution.makespan} completion time and {best_solution.tardiness} tardiness.")

        for job in self.factory.jobs:
            print(f"Job {job.id + 1} Due Time ===> {job.due_time} || Job Completion Time ===> {job.processing_time}")
            for m in range(len(job.start_times)):
                print(f"Stage {m + 1} || START => {job.start_times[m]} | END => {job.end_times[m]}")
            print("------------------------------")

        print('\n')
        for i in range(len(best_solution.chromosome)):
            print(f"=====Stage{i + 1}=====")
            for f in range(len(best_solution.chromosome[i])):
                print(f"Machine {f + 1} Job Order ==> {best_solution.chromosome[i][f]}")

        return average_completion_time_values, average_tardiness_values, best_solution

    def select_initial_generation(self):
        generations = []
        for i in range(self.initial_random_search_length):
            gen = self.initialize_generation(num_of_jobs=self.num_of_jobs,
                                             num_of_machines_per_stage=self.num_of_machines_per_stage,
                                             num_of_stages=self.num_of_stages,
                                             population_size=self.population_size)
            GenJobSS.simulate_generation(gen, self.factory)
            generations.append(gen)

        best_generation = generations[0]
        for gen in generations:
            if GenJobSS.get_average_completion_time_in_gen(gen) < GenJobSS.get_average_completion_time_in_gen(best_generation):
                best_generation = gen
        return best_generation

    def create_offsprings_from_selection(self, parent_1, parent_2, crossover_rate, mutation_probability, boundary_swap_probability):
        parent_1_dna_boundaries, parent_1_dna_segments = GenJobSS.convert_chromosome_segments_to_dna(parent_1.chromosome)
        parent_2_dna_boundaries, parent_2_dna_segments = GenJobSS.convert_chromosome_segments_to_dna(parent_2.chromosome)

        mutation = False if random.random() >= mutation_probability else True

        if mutation:
            offspring_1_dna_segments, offspring_2_dna_segments = GenJobSS.perform_mutation(parent_1_dna_segments, parent_2_dna_segments)
        else:
            offspring_1_dna_segments, offspring_2_dna_segments = self.perform_crossover(parent_1_dna_segments, parent_2_dna_segments, crossover_rate)

        offspring_1_boundaries, offspring_2_boundaries = self.perform_boundary_swapping(parent_1_dna_boundaries, parent_2_dna_boundaries, boundary_swap_probability)

        offspring_1_chromosome = self.reconstruct_chromosome_segments_from_dna(offspring_1_boundaries, offspring_1_dna_segments)
        offspring_2_chromosome = self.reconstruct_chromosome_segments_from_dna(offspring_2_boundaries, offspring_2_dna_segments)

        offspring_1 = ScheduleChromosome(num_of_jobs=self.num_of_jobs,
                                         num_of_stages=self.num_of_stages,
                                         machines_per_stage=self.num_of_machines_per_stage,
                                         assigned_encoded_schedule=offspring_1_chromosome)

        offspring_2 = ScheduleChromosome(num_of_jobs=self.num_of_jobs,
                                         num_of_stages=self.num_of_stages,
                                         machines_per_stage=self.num_of_machines_per_stage,
                                         assigned_encoded_schedule=offspring_2_chromosome)

        return offspring_1, offspring_2

    @staticmethod
    def perform_boundary_swapping(parent_1_boundaries, parent_2_boundaries, boundary_swap_chance):

        boundary_count = len(parent_1_boundaries)
        boundary_length = len(parent_1_boundaries[0])

        offspring_1_boundaries = []
        offspring_2_boundaries = []

        for i in range(boundary_count):
            offspring_1_boundary = []
            offspring_2_boundary = []

            for f in range(boundary_length):
                if random.random() <= boundary_swap_chance:
                    offspring_1_boundary.append(parent_2_boundaries[i][f])
                else:
                    offspring_1_boundary.append(parent_1_boundaries[i][f])

                if random.random() <= boundary_swap_chance:
                    offspring_2_boundary.append(parent_1_boundaries[i][f])
                else:
                    offspring_2_boundary.append(parent_2_boundaries[i][f])

            offspring_1_boundary.sort()
            offspring_2_boundary.sort()

            offspring_1_boundaries.append(offspring_1_boundary)
            offspring_2_boundaries.append(offspring_2_boundary)

        return offspring_1_boundaries, offspring_2_boundaries

    @staticmethod
    def perform_mutation(parent_1_dna, parent_2_dna):

        parent_1_dna = copy.deepcopy(parent_1_dna)
        parent_2_dna = copy.deepcopy(parent_2_dna)

        number_of_segments = len(parent_1_dna)
        dna_segment_length = len(parent_1_dna[0])

        offspring_1_segments = []
        offspring_2_segments = []

        for i in range(number_of_segments):
            parent_1_random_index = random.randint(0, dna_segment_length - 1)
            parent_2_random_index = random.randint(0, dna_segment_length - 1)

            ph_parent_1 = parent_1_dna.copy()
            ph_parent_2 = parent_2_dna.copy()

            ph_parent_1[i][parent_1_random_index] = parent_2_dna[i][parent_2_random_index]
            ph_parent_2[i][parent_2_random_index] = parent_1_dna[i][parent_1_random_index]

            offspring_1_segment = ph_parent_1[i]
            offspring_2_segment = ph_parent_2[i]

            offspring_1_segments.append(offspring_1_segment)
            offspring_2_segments.append(offspring_2_segment)

        return offspring_1_segments, offspring_2_segments

    @staticmethod
    def perform_crossover(parent_1_dna, parent_2_dna, crossover_rate):

        parent_1_dna = copy.deepcopy(parent_1_dna)
        parent_2_dna = copy.deepcopy(parent_2_dna)

        number_of_segments = len(parent_1_dna)
        dna_segment_length = len(parent_1_dna[0])
        crossover_length = int(dna_segment_length * crossover_rate) if int(
            dna_segment_length * crossover_rate) > 0 else 1

        offspring_1_segments = []
        offspring_2_segments = []

        for i in range(number_of_segments):
            parent_1_random_starting_index = random.randint(0, dna_segment_length - 1)
            parent_2_random_starting_index = random.randint(0, dna_segment_length - 1)

            crossover_gene_1, indices_1 = GenJobSS.extract_crossover_gene_from_dna(parent_1_dna[i],
                                                                                   parent_1_random_starting_index,
                                                                                   crossover_length, dna_segment_length)
            crossover_gene_2, indices_2 = GenJobSS.extract_crossover_gene_from_dna(parent_2_dna[i],
                                                                                   parent_2_random_starting_index,
                                                                                   crossover_length, dna_segment_length)

            parent_1_dna[i][indices_1[0]: indices_1[1]] = crossover_gene_2
            parent_2_dna[i][indices_2[0]: indices_2[1]] = crossover_gene_1

            offspring_1_segment = parent_1_dna[i]
            offspring_2_segment = parent_2_dna[i]

            offspring_1_segments.append(offspring_1_segment)
            offspring_2_segments.append(offspring_2_segment)

        return offspring_1_segments, offspring_2_segments

    @staticmethod
    def extract_crossover_gene_from_dna(parent_dna_segment, random_starting_index, crossover_length, dna_segment_length):
        direction = 1 if random.random() >= 0.5 else -1
        if direction == -1:
            if random_starting_index - crossover_length >= 0:
                crossover_gene = parent_dna_segment[random_starting_index - crossover_length:random_starting_index]
                indices = (random_starting_index - crossover_length, random_starting_index)
            else:
                crossover_gene = parent_dna_segment[random_starting_index:random_starting_index + crossover_length]
                indices = (random_starting_index, random_starting_index + crossover_length)
        else:
            if random_starting_index + crossover_length <= dna_segment_length:
                crossover_gene = parent_dna_segment[random_starting_index:random_starting_index + crossover_length]
                indices = (random_starting_index, random_starting_index + crossover_length)
            else:
                crossover_gene = parent_dna_segment[random_starting_index - crossover_length:random_starting_index]
                indices = (random_starting_index - crossover_length, random_starting_index)

        return crossover_gene, indices

    @staticmethod
    def reconstruct_chromosome_segments_from_dna(offspring_boundaries, offspring_segments):
        boundary_length = len(offspring_boundaries[0])
        num_of_stages = len(offspring_segments)
        num_of_machines_per_stage = boundary_length + 1
        chromosome = []

        for i in range(num_of_stages):
            current_boundary_list = offspring_boundaries[i]
            current_stage_job_orders = offspring_segments[i]
            machine_job_orders_of_stage = []
            for f in range(num_of_machines_per_stage):
                if f == 0:
                    current_machine_job_orders = current_stage_job_orders[0:current_boundary_list[f]]
                elif f == num_of_machines_per_stage - 1:
                    current_machine_job_orders = current_stage_job_orders[current_boundary_list[f - 1]:]
                else:
                    current_machine_job_orders = current_stage_job_orders[
                                                 current_boundary_list[f - 1]:current_boundary_list[f]]

                machine_job_orders_of_stage.append(current_machine_job_orders)

            chromosome.append(machine_job_orders_of_stage)

        return chromosome

    @staticmethod
    def convert_chromosome_segments_to_dna(chromosome):
        boundaries, segments = [], []
        for chromosome_segment in chromosome:
            segment = []
            boundary = []
            index_in_array = 0
            for i in range(len(chromosome_segment)):
                machine_job_processing_orders = chromosome_segment[i]
                for job_process_priority in machine_job_processing_orders:
                    segment.append(job_process_priority)
                    index_in_array += 1

                if i != len(chromosome_segment) - 1:
                    boundary.append(index_in_array)

            boundaries.append(boundary)
            segments.append(segment)

        return boundaries, segments

    @staticmethod
    def tournament_selection(generation, selection_size=4, sample_best_fraction=0.1):
        num_best_candidates = int(len(generation) * sample_best_fraction)
        best_candidates = []

        while len(best_candidates) < num_best_candidates:
            population_sample = random.sample(generation, selection_size)

            winner_candidate = population_sample[0]
            for chromosome in population_sample:
                if chromosome.makespan < winner_candidate.makespan:
                    winner_candidate = chromosome

            best_candidates.append(winner_candidate)

        return best_candidates

    @staticmethod
    def simulate_generation(generation, factory):
        for i in range(len(generation)):
            generation[i].makespan, generation[i].tardiness = factory.run(generation[i].chromosome)
            generation[i].index_in_generation = i
        return generation

    @staticmethod
    def initialize_generation(num_of_jobs, num_of_machines_per_stage, num_of_stages, population_size):
        return [ScheduleChromosome(num_of_jobs=num_of_jobs,
                                   machines_per_stage=num_of_machines_per_stage,
                                   num_of_stages=num_of_stages) for i in range(population_size)]

    @staticmethod
    def get_best_member_in_generation(generation):
        best_member = generation[0]
        for member in generation:
            if member.makespan < best_member.makespan:
                best_member = member
        return best_member

    @staticmethod
    def get_average_completion_time_in_gen(generation):
        sum_completion_time = 0
        for member in generation:
            sum_completion_time += member.makespan
        return sum_completion_time / len(generation)

    @staticmethod
    def get_average_tardiness_in_gen(generation):
        sum_tardiness = 0
        for member in generation:
            sum_tardiness += member.tardiness
        return sum_tardiness / len(generation)

    @staticmethod
    def get_probability_decay_rate(initial_probability, specified_probability, num_of_generations, probability_convergence_percentage):
        if initial_probability > specified_probability:
            return (initial_probability - specified_probability) / (num_of_generations * probability_convergence_percentage)
        else:
            raise Exception(f"!!!ERROR -- Specified probability {specified_probability} is bigger than the initial probability {initial_probability}!!!")

    @staticmethod
    def apply_probability_decay(current_probability, decay_rate):
        return current_probability - decay_rate
