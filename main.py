import random
import time
from services.distributionCalculator import DistributionCalculator
from services.geneticLowestCost import GeneticLowestCost
from services.simulator import Simulator
from multiprocessing import Process


class Main:

    def first_objective(self, package_amount):
        simulator = Simulator()
        start = time.time()
        min_mean = 100000000000
        best_config = []
        simulation_amount = 0
        for i in range(1, 31):
            for j in range(1, 32):
                for w in range(1, 73):
                    for o in range(1, 14):
                        config = [i, j, w, o]
                        if simulator.get_config_cost(config) <= 1000:
                            simulation_amount += 1
                            sr = simulator.simulate(config, package_amount, i+j+w+o)
                            mean = (sr[0] + sr[1] + sr[2] + sr[3]) / (4.0*package_amount)
                            if mean < min_mean:
                                min_mean = mean
                                best_config = config

        end = time.time()
        print("Duro: " + str(end-start))
        print("Media minima: " + str(min_mean))
        print("Mejor configuracion: " + str(best_config))
        print("Costo de la configuracion: " + str(simulator.get_config_cost(best_config)))
        print("Cantidad de simulaciones: " + str(simulation_amount))

    # Main for the second objective.
    def second_objective(self):
        start = time.time()
        genetic = GeneticLowestCost()
        genetic.start(300)
        end = time.time()
        print("-------------------------------------------------------")
        print("Duro: " + str(end-start))

    def main(self):
        server_costs = [29.4, 28.3, 12.1, 69.6]
        phase = 4
        inc = 1
        s = Simulator()
        config = [107, 860, 235, 121]
        initial_mean = 69331.61131299718
        sr = s.simulate(config, 1000, 1)
        mean = (sr[0] + sr[1] + sr[2] + sr[3]) / (1000.0*4)
        diff = initial_mean-mean
        grade = diff/(server_costs[phase-1]*inc)
        print(grade)
        print(mean)

s = Main()
s.second_objective()
#s.main()


