from decimal import Decimal
import math
import os
from re import split


class DistributionCalculator:

    """
        Reads a file with numbers until EOF. Returns an array with the file content.
        data_type = 0 -> Reading file with integers.
        data_type = 1 -> Reading file with doubles.
        data_type = 2 -> Reading file with fractions.
    """
    @staticmethod
    def read_data(file_name, data_type):
        array = []
        with open(os.getcwd()+'/data/' + file_name) as file:
            if data_type == 2:
                for line in file:
                    operands = split('/', line)
                    a = Decimal(operands[0])
                    b = Decimal(operands[1])
                    array.append(a/b)
            elif data_type == 1:
                for line in file:
                    array.append(Decimal(line))
            else:
                for line in file:
                    array.append(int(line))
        return array

    @staticmethod
    def get_avg(array):
        n = Decimal(len(array))
        res = Decimal(0)
        for i in array:
            res += i
        return res/n

    @staticmethod
    def get_standard_deviation(array, avg):
        average = Decimal(avg)
        res = Decimal(0)
        n = Decimal(len(array))-1
        for i in array:
            res += pow(i-average, 2)
        return math.sqrt(res/n)

    @staticmethod
    def print_data_array(array):
        print("Printing array...")
        for i in array:
            print(i)
        print()

    @staticmethod
    def create_intervals(array, n):
        res = []
        quantity = Decimal(n)
        for i in array:
            res

    @staticmethod
    def get_chi(observed_array, expected_array):
        n = len(observed_array)
        chi = 0
        for i in range(0, n):
            temp = ((observed_array[i] - expected_array[i]) ** 2)/expected_array[i]
            chi += temp
        return chi

    @staticmethod
    def exponential(x):
        median = 1.0/30.20040211331461845189765
        return median * (math.e ** (-median * x))

    @staticmethod
    def binomial(x):
        p = 10.4126/10000.0



    @staticmethod
    def poisson(x, fact_array):
        lamb = 10.4126
        res = ((lamb**x) * (math.e ** -lamb))/(fact_array[x]+0.0)
        if x == 1:
            print("Res:",end=" ")
            print(res*10000)
        return res

    @staticmethod
    def normal(x):
        median = 10.4126
        dev = 2.775631757486089
        return (1 / (dev * math.sqrt(2 * math.pi))) * math.e ** (-0.5 * (((x - median) / dev) ** 2))

    @staticmethod
    def simpson(f, a, b, n):
        h = (b-a)/n
        k = 0.0
        x = a + h
        for i in range(1, int(n/2 + 1)):
            k += 4*f(x)
            x += 2*h

        x = a + 2*h
        for i in range(1, int(n/2)):
            k += 2*f(x)
            x += 2*h
        return (h/3)*(f(a)+f(b)+k)

    @staticmethod
    def get_expected_frequency(interval_size):
        res = []
        if interval_size > 0:
            a = 0
            b = interval_size
            for i in range(0, 40):
                temp = DistributionCalculator.simpson(DistributionCalculator.normal, a, b, 40)
                res.append(temp*10000)
                a += interval_size
                b += interval_size
        else:
            fact_array = DistributionCalculator.get_factorial(22)
            for i in range(0, 22):
                temp = DistributionCalculator.poisson(i, fact_array)
                res.append(temp*10000)
        return res

    @staticmethod
    def get_fofe(obs_array, exp_array):
        res = []
        n = len(obs_array)
        for i in range(0, n):
            res.append(obs_array[i] - exp_array[i])
        return res

    @staticmethod
    def get_acum(fofe):
        maximum = -100000000
        array = []
        res = 0
        for n in fofe:
            res += n
            maximum = max(maximum, math.fabs(res))
            array.append(res)
        print(maximum)
        return array

    @staticmethod
    def get_factorial(n):
        res = [1]
        for i in range(1, n+1):
            res.append(res[i-1]*i)
        return res





