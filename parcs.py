from Pyro4 import expose
import random

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n = self.read_input()
        step = n / len(self.workers)

        # map
        mapped = []
        lastelementi = len(self.workers) - 1

        for i in range(0, lastelementi):
            mapped.append(self.workers[i].mymap(i * step, i * step + step))
        mapped.append(self.workers[lastelementi].mymap(lastelementi * step, n))

        print('Map finished: ', mapped)

        # reduce
        reduced = self.myreduce(mapped, n)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b):
        points_in_circle = 0
        for i in range(a, b):
            points_in_circle += Solver.hits_count()
        return points_in_circle

    @staticmethod
    @expose
    def myreduce(mapped, n_points):
        all_points = 0
        for x in mapped:
            all_points += x.value
        return 4.0 * float(all_points) / n_points

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()

    @staticmethod
    def hits_count():
        x, y = random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)
        if (x ** 2 + y ** 2) <= 1.0:
            return 1
        return 0
