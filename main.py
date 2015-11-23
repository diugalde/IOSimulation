import time
from services.simulator import Simulator
from multiprocessing import Process


class Main:

    def main(self):
        simulator = Simulator()
        start = time.time()
        for i in range(0, 50):
            config = [1000, 1000, 1000, 1000]
            simulator.simulate(config)
        end = time.time()
        print("Duro: " + str(end-start))


s = Main()
s.main()


