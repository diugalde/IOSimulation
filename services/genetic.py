from abc import ABCMeta, abstractmethod
import random
from services.simulator import Simulator


class Genetic(metaclass=ABCMeta):

    def __init__(self):
        self.generation_package_amount = 0
        self.current_generation = 1
        self.simulator = Simulator()
        self.max_servers = []
        self.best_individuals = []

    def get_individual(self):
        individual = []
        for i in range(0, 4):
            individual.append(random.randint(1, self.max_servers[i]))
        return individual

    def get_first_generation(self, size):
        population = []
        for i in range(0, size):
            population.append(self.get_individual())
        return population

    @abstractmethod
    def mutate(self, individual):
        pass

    @abstractmethod
    def crossover(self, individual1, individual2):
        pass

    def get_next_generation(self, population, best_individual):
        size = len(population)
        new_population = []
        for i in range(0, size):
            cross = self.crossover(population[i], best_individual)
            mutatation_probability = random.random()
            if mutatation_probability < 0.05:
                cross = self.mutate(cross)
            new_population.append(cross)
        self.current_generation += 1
        return new_population

    @abstractmethod
    def get_fitness(self):
        pass

    def get_best_individual(self, population):
        max_grade = -10000000
        best_ind = []
        for ind in population:
            grade = self.get_fitness(ind)
            if grade > max_grade:
                max_grade = grade
                best_ind = ind
        return [best_ind, grade]

    def start(self, generations):
        generations_copy = generations
        size = 80
        population = self.get_first_generation(size)
        while generations > 0:
            print("Generacion #" + str((generations_copy-generations)+1))
            best_individual = self.get_best_individual(population)
            self.best_individuals.append(best_individual)
            population = self.get_next_generation(population, best_individual[0])
            generations -= 1
        optimum = self.get_optimum_individual()
        optimum_cost = self.simulator.get_config_cost(optimum[0])
        optimum_diff = 999999999.0/(optimum[1]*optimum_cost)
        print("Optimum: " + str(optimum[0]))
        print("Cost: " + str(optimum_cost))
        print("Diff: " + str(optimum_diff))

    def get_optimum_individual(self):
        best_grade = -10000
        best_individual = []
        best_individual_index = -1
        for i in range(0, len(self.best_individuals)):
            if self.best_individuals[i][1] > best_grade:
                best_grade = self.best_individuals[i][1]
                best_individual = self.best_individuals[i]
                best_individual_index = i
        print("Indice del mejor individuo: " + str(best_individual_index))
        return best_individual
