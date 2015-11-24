import random
from services.genetic import Genetic

class GeneticLowestCost(Genetic):

    def __init__(self):
        super(GeneticLowestCost, self).__init__()
        self.generation_package_amount = 600
        self.max_servers = [9, 63, 18, 9]

    def mutate(self, individual):
        r = random.random()
        mutation = random.randint(5, 15)
        if r < 0.09282857278824626:
            individual[0] += mutation
        elif r < 0.7274850937265904:
            individual[1] += mutation
        elif r < 0.9082784984512393:
            individual[2] += mutation
        else:
            individual[3] += mutation
        return individual

    def crossover(self, individual1, individual2):
        cross = []
        for i in range(0, 4):
            if i == 1:
                a = random.randint(0, 15)
            elif i == 2:
                a = random.randint(0, 6)
            else:
                a = random.randint(0, 3)
            gen = ((individual1[i] + individual2[i])//2) + a
            if gen > self.generation_package_amount:
                return self.get_individual()
            cross.append(gen)
        return cross

    def get_fitness(self, individual):
        sr = self.simulator.simulate(individual, self.generation_package_amount, self.current_generation)
        mean = (sr[0] + sr[1] + sr[2] + sr[3]) / (self.generation_package_amount)
        config_cost = self.simulator.get_config_cost(individual)
        diff = abs(45-mean)
        grade = (999999999.0/diff)/config_cost
        return grade

    def start(self, generations):
        generations_copy = generations
        size = 80
        population = self.get_first_generation(size)
        while generations > 0:
            print("Generacion #" + str((generations_copy-generations)+1))
            best_individual = self.get_best_individual(population)
            print(best_individual)
            self.best_individuals.append(best_individual)
            population = self.get_next_generation(population, best_individual[0])
            generations -= 1
        optimum = self.get_optimum_individual()
        optimum_cost = self.simulator.get_config_cost(optimum[0])
        optimum_diff = 999999999.0/(optimum[1]*optimum_cost)
        print("Optimum: " + str(optimum[0]))
        print("Cost: " + str(optimum_cost))
        print("Diff: " + str(optimum_diff))
