import sys;
import math;
import copy;
import networkx;

class LinearThresholdModel:
    def __init__(self, graph):
        self.graph = graph;

    def run(self, seedSet):
        for node in self.graph.nodes():
            self.graph.node[node][1] = 0.0;

        activeNodeCount = 0;
        activeNodeSet = copy.deepcopy(seedSet);
        visitedNodeSet = copy.deepcopy(seedSet);

        while len(visitedNodeSet) > 0:
            nextVisitedNodeSet = set();

            for node in visitedNodeSet:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in activeNodeSet:
                        self.graph.node[neighbor][1] += self.graph.edge[node][neighbor][0];
                        if self.graph.node[neighbor][1] >= self.graph.node[neighbor][0]:
                            activeNodeSet.add(neighbor);
                            nextVisitedNodeSet.add(neighbor);
                            activeNodeCount += 1;

            visitedNodeSet = nextVisitedNodeSet;

        return (activeNodeCount, activeNodeSet - seedSet);

def main():
    nodeFileName = sys.argv[1];
    edgeFileName = sys.argv[2];
    seedFileName = sys.argv[3];

    graph = networkx.DiGraph();
    
    ################

    inFile = open(nodeFileName, "r");
    inFile.readline();

    for line in inFile:
        info = line.strip().split();
        node = int(info[0]);
        threshold = float(info[1]);

        graph.add_node(node);
        graph.node[node][0] = threshold;        # threshold to be active
        graph.node[node][1] = 0.0;              # energy, accumulative weights

    inFile.close();
    
    ################

    inFile = open(edgeFileName, "r");
    inFile.readline();
    inFile.readline();

    for line in inFile:
        info = line.strip().split();
        node1 = int(info[0]);
        node2 = int(info[1]);
        weight = float(info[2]);

        graph.add_edge(node1, node2);
        graph.edge[node1][node2][0] = weight;   # weight from node 1 to node 2

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

    lt = LinearThresholdModel(graph);
    (activeNodeCount, activeNodeSet) = lt.run(seedSet);
    print("Number of activated nodes:", activeNodeCount);
    
    isFirst = True;
    for node in sorted(activeNodeSet):
        if isFirst:
            isFirst = False;
        else:
            print(" ", end = "");
        print(node, end = "");
    print();

if __name__ == "__main__":
    main();
