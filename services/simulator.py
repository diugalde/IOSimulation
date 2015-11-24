import random
from multiprocessing import Process, Queue
import numpy as np


class Simulator:
    def __init__(self):
        self.server_costs = [29.4, 28.3, 12.1, 69.6]

    # config = [3, 3, 4, 6]
    def simulate(self, config, package_amount, simulation_number):
        process_queue = Queue()
        jobs = []
        for i in range(0, 4):
            pid = Process(target=self.simulate_process, args=(package_amount, config[i], i + 1,
                                                              process_queue, simulation_number))
            pid.start()
            jobs.append(pid)
        for i in range(0, 4):
            jobs[i].join()

        simulation_results = [0] * 4
        for i in range(0, 4):
            e = process_queue.get()
            simulation_results[e[0] - 1] = e[1]
        return simulation_results

    def simulate_with_variance(self, config, package_amount, simulation_number):
        process_queue = Queue()
        jobs = []
        for i in range(0, 4):
            pid = Process(target=self.simulate_process_with_variance,
                          args=(package_amount, config[i], i + 1, process_queue, simulation_number))
            pid.start()
            jobs.append(pid)
        for i in range(0, 4):
            jobs[i].join()
        phases_waiting_time = [0] * 4
        phases_packages_waiting_time = [0] * 4
        for i in range(0, 4):
            e = process_queue.get()
            phases_waiting_time[e[0] - 1] = e[1]
            phases_packages_waiting_time[e[0] - 1] = e[2]
        variance = self.calculate_variance(phases_waiting_time, phases_packages_waiting_time, package_amount)
        return variance

    def simulate_process(self, package_amount, server_amount, phase, process_queue, simulation_number):
        queue = self.generate_queue(package_amount, phase, simulation_number)
        servers = [0] * server_amount
        wait_time = 0
        for i in range(0, package_amount):
            free_server = np.argmin(servers)
            wait_time += servers[free_server]
            servers[free_server] += queue[i]
        process_queue.put([phase, wait_time])

    def simulate_process_with_variance(self, package_amount, server_amount, phase, process_queue, simulation_number):
        queue = self.generate_queue(package_amount, phase, simulation_number)
        servers = [0] * server_amount
        packages_waiting_time = []
        wait_time = 0
        for i in range(0, package_amount):
            free_server = np.argmin(servers)
            wait_time += servers[free_server]
            packages_waiting_time.append(servers[free_server])
            servers[free_server] += queue[i]
        process_queue.put([phase, wait_time, packages_waiting_time])

    """
        Phase #1: Exponential.  Lambda = 0.07745307
        Phase #2: Normal.       Median = 85.8762728 - Standard Deviation = 11.9313856926
        Phase #3: Poisson       Lambda = 10.4126.
        Phase #4: Exponential.  Lambda = 0.03311214
    """
    def generate_queue(self, package_amount, phase, seed):
        np.random.seed(1)
        random.seed(1)
        if phase == 1:
            queue = self.generate_random_list(package_amount, lambda: random.expovariate(0.07745307))
        elif phase == 2:
            queue = self.generate_random_list(package_amount, lambda: random.normalvariate(85.8762728, 11.9313856926))
        elif phase == 3:
            #np.random.seed(seed)
            queue = self.generate_random_list(package_amount, lambda: np.random.poisson(10.4126))
        elif phase == 4:
            queue = self.generate_random_list(package_amount, lambda: random.expovariate(0.03311214))
        return queue

    def generate_random_list(self, n, dist):
        l = []
        for i in range(0, n):
            r = dist()
            l.append(r)
        return l

    def get_config_cost(self, config):
        res = 0
        for i in range(0, 4):
            res += (self.server_costs[i] * config[i])
        return res

    def calculate_variance(self, phases_wt, phases_packages_wt, packages_amount):
        mean = (phases_wt[0] + phases_wt[1] + phases_wt[2] + phases_wt[3]) / (packages_amount+0.0)
        sum = 0
        for i in range(0, packages_amount):
            xi = phases_packages_wt[0][i] + phases_packages_wt[1][i] + \
                 phases_packages_wt[2][i] + phases_packages_wt[3][i]
            sum += pow(xi - mean, 2)
        variance = sum / (packages_amount - 1.0)
        return variance
