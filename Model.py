
import csv

class Model:

# instance variables
    def __init__(self):
        self.allNodes = {}
        self.allNodes2 = []
        self.allNodes2.append((23.142, 11.736))
        self.number_of_routes = 6
    def BuildModel(self):
        file1 = "Instance.csv"
        with open(file1) as csvfile:
            spamreader = csv.reader(csvfile)
            count = 0
            self.allNodes = {(23.142, 11.736): (0, 0, 0, 0)}
            for row in spamreader:
                count = count + 1
                if count > 11:
                    key = int(row[0])
                    x = float(row[1])
                    y = float(row[2])
                    demand = int(row[3])
                    service_time = int(row[4])
                    profit = int(row[5])
                    self.allNodes[(x, y)] = (key, demand, service_time, profit)
                    self.allNodes2.append((x, y))
class Route:
    def __init__(self, dp):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.time = 0
        self.capacity = 0
        self.profit = 0
