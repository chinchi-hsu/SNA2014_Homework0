import sys;
import math;
import copy;
import statistics;
import random;
import networkx;

class IndependentCascadeModel:
    def __init__(self, graph):
        self.graph = graph;

    def run(self, seedSet):
        activeNodeCount = 0;
        activeNodeSet = copy.deepcopy(seedSet);
        visitedNodeSet = copy.deepcopy(seedSet);

        while len(visitedNodeSet) > 0:
            nextVisitedNodeSet = set();

            for node in visitedNodeSet:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in activeNodeSet:
                        dice = random.random();
                        if dice <= self.graph.edge[node][neighbor][0]:
                            activeNodeSet.add(neighbor);
                            nextVisitedNodeSet.add(neighbor);
                            activeNodeCount += 1;

            visitedNodeSet = nextVisitedNodeSet;

        return activeNodeCount;

def main():
    edgeFileName = sys.argv[1];
    seedFileName = sys.argv[2];
    iterationCount = int(sys.argv[3]);

    graph = networkx.DiGraph();
    
    ################

    inFile = open(edgeFileName, "r");
    inFile.readline();
    inFile.readline();

    for line in inFile:
        info = line.strip().split();
        node1 = int(info[0]);
        node2 = int(info[1]);
        probability = float(info[2]);

        graph.add_edge(node1, node2);
        graph.edge[node1][node2][0] = probability;   # probability from node 1 to node 2

    inFile.close();
    
    ################
    
    seedSet = set();
    inFile = open(seedFileName, "r");
    seedWords = inFile.readline().strip().split();

    for seedWord in seedWords:
        seed = int(seedWord);
        seedSet.add(seed);

    inFile.close();
    
    ################

    print("{0:d} nodes".format(graph.number_of_nodes()));
    print("{0:d} edges".format(graph.number_of_edges()));
    print();
    activeNodeCounts = [];
    
    for i in range(iterationCount):
        ic = IndependentCascadeModel(graph);
        activeNodeCount = ic.run(seedSet);
        
        print("Iteration", i + 1, "\tNumber of activated nodes:", activeNodeCount);
        activeNodeCounts.append(activeNodeCount);

    print();
    mean = statistics.mean(activeNodeCounts);
    stddev = statistics.stdev(activeNodeCounts);
    print("Mean:", mean, "\tStddev:", stddev);

if __name__ == "__main__":
    main();
