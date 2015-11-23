import time
from services.simulator import Simulator
from multiprocessing import Process


class Main:

    def main(self):
        simulation_amount = 100000
        simulator = Simulator()
        start = time.time()
        jobs = []
        for i in range(0, simulation_amount):
            config = [100, 100, 100, 100]
            pid = Process(target=simulator.simulate, args=(config, i))
            pid.start()
            jobs.append(pid)
        for i in range(0, simulation_amount):
            jobs[i].join()
        end = time.time()
        print("Duro: " + str(end-start))


s = Main()
s.main()


