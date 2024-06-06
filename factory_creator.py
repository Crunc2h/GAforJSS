from factory_manager import FactoryManager
from machine import Machine


class FactoryCreator:

    @staticmethod
    def create_factory(machine_per_stage, num_of_stages, jobs):
        machines = FactoryCreator.create_machines(machine_per_stage, num_of_stages)
        factory_manager = FactoryCreator.create_factory_manager(machines, machine_per_stage, num_of_stages, jobs)
        return factory_manager

    @staticmethod
    def create_machines(machine_per_stage, num_of_stages):
        machines = []
        for i in range(num_of_stages):
            for f in range(machine_per_stage):
                machines.append(Machine(i, f))
        return machines

    @staticmethod
    def create_factory_manager(machines, machine_per_stage, max_stages, jobs):
        return FactoryManager(machines, machine_per_stage, max_stages, jobs)