import random
from services.genetic import Genetic


class GeneticLowestVariance(Genetic):

    def __init__(self):
        super(GeneticLowestVariance, self).__init__()
        self.generation_package_amount = 1000
        self.max_servers = [10, 57, 8, 23]

    def mutate(self, individual):
        r = random.random()
        mutation = random.randint(1, 5)
        if r < 0.10419040459173522:
            individual[0] += mutation
        elif r < 0.6825783837678314:
            individual[1] += mutation
        elif r < 0.7642436262960646:
            individual[2] += mutation
        else:
            individual[3] += mutation
        return individual

    def crossover(self, individual1, individual2):
        cross = []
        for i in range(0, 4):
            if i == 0:
                a = random.randint(0, 2)
            if i == 1:
                a = random.randint(0, 11)
            elif i == 2:
                a = random.randint(0, 1)
            elif i == 3:
                a = random.randint(0, 4)
            gen = ((individual1[i] + individual2[i])//2) + a
            cross.append(gen)
        return cross

    def get_fitness(self, individual):
        variance = self.simulator.simulate_with_variance(individual, self.generation_package_amount,
                                                         self.current_generation)
        grade = 999999999.0/variance
        return grade