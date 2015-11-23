import random
from multiprocessing import Process, Queue
import numpy as np


class Simulator:

    def __init__(self):
        self.server_costs = [29.4, 28.3, 12.1, 69.6]

    # config = [3, 3, 4, 6]
    def simulate(self, config, simulation_number):
        process_queue = Queue()
        jobs = []
        for i in range(0, 4):
            pid = Process(target=self.simulate_process, args=(config[i], i+1, process_queue, simulation_number))
            pid.start()
            jobs.append(pid)
        for i in range(0, 4):
            jobs[i].join()

        simulation_results = [0] * 4
        for i in range(0, 4):
            e = process_queue.get()
            simulation_results[e[0]-1] = e[1]

    def simulate_process(self, server_amount, phase, process_queue, simulation_number):
        package_amount = 1000
        queue = self.generate_queue(package_amount, phase, simulation_number)
        servers = [0] * server_amount
        wait_time = 0
        for i in range(0, package_amount):
            free_server = np.argmin(servers)
            wait_time += servers[free_server]
            servers[free_server] += queue[i]
        process_queue.put([phase, wait_time/package_amount])

    """
        Phase #1: Exponential.  Lambda = 0.07745307
        Phase #2: Normal.       Median = 85.8762728 - Standard Deviation = 11.9313856926
        Phase #3: Poisson       Lambda = 10.4126. /  Binomial:  n = 21   -    p = 0.495838
        Phase #4: Exponential.  Lambda = 0.03311214
    """
    def generate_queue(self, package_amount, phase, seed):
        if phase == 1:
            queue = self.generate_random_list(package_amount, lambda: random.expovariate(0.07745307))
        elif phase == 2:
            queue = self.generate_random_list(package_amount, lambda: random.normalvariate(85.8762728, 11.9313856926))
        elif phase == 3:
            # queue = self.generate_random_list(package_amount, lambda: self.random_binomial(21, 0.495838))
            np.random.seed(seed)
            queue = self.generate_random_list(package_amount, lambda: self.random_poisson(10.4126))
        elif phase == 4:
            queue = self.generate_random_list(package_amount, lambda: random.expovariate(0.03311214))
        return queue

    def generate_random_list(self, n, dist):
        l = []
        for i in range(0, n):
            r = dist()
            l.append(r)
        return l

    def random_poisson(self, lamb):
        return np.random.poisson(lamb, 1)[0]

    def random_binomial(self, n, p):
        return np.random.binomial(n, p, 1)[0]

    def get_config_cost(self, config):
        res = 0
        for i in range(0, 4):
            res += (self.server_costs[i]*config[i])
        return res

    # def generate_configs_
