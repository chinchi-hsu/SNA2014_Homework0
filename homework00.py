import sys;
import math;
import networkx;

class DegreeDistribution:
    def __init__(self, graph):
        self.graph = graph.to_undirected();

    def estimatePowerLawSlope(self, xMin):
        sumLog = 0.0;
        count = 0;
        
        for node in self.graph.nodes():
            degree = self.graph.degree(node);
            if degree >= xMin:
                sumLog += math.log(float(degree) / xMin);
                count += 1;

        slope = 1 + count / sumLog;
        return slope;

    def getDistribution(self):
        distribution = {};
        
        for node in self.graph.nodes():
            degree = self.graph.degree(node);
            if degree not in distribution:
                distribution[degree] = 0;
            distribution[degree] += 1;

        nodeCount = float(self.graph.number_of_nodes());

        for degree in distribution.keys():
            distribution[degree] /= nodeCount;

        return distribution;

class AveragePathLength:
    def __init__(self, graph):
        self.graph = graph;

    def reduceGraphToLargestComponent(self):
        subgraphs = None;
        if isinstance(self.graph, networkx.DiGraph):
            print("Directed");
            subgraphs = networkx.weakly_connected_component_subgraphs(self.graph);
        else:
            print("Undirected");
            subgraphs = networkx.connected_component_subgraphs(self.graph);

        maxNodeCount = None;
        largestComponent = None;
        for subgraph in subgraphs:
            nodeCount = subgraph.number_of_nodes();
            if maxNodeCount == None or maxNodeCount < nodeCount:
                maxNodeCount = nodeCount;
                largestComponent = subgraph;

        print("Subgraph");
        print("\t{0:d} nodes".format(largestComponent.number_of_nodes()));
        print("\t{0:d} edges".format(largestComponent.number_of_edges()));
        self.graph = largestComponent;

    def compute(self):
        
        lengthDict = networkx.shortest_path_length(self.graph);
        lengthCount = 0;
        lengthMean = 0.0;

        nodeCount = self.graph.number_of_nodes();
        lengthCountUpperBound = None;
        if isinstance(self.graph, networkx.DiGraph):
            print("Directed");
            lengthCountUpperBound = nodeCount * (nodeCount - 1);
        else:
            print("Undirected");
            lengthCountUpperBound = nodeCount * (nodeCount - 1) / 2;
        
        for (source, targetDict) in lengthDict.items():
            for (target, length) in targetDict.items():
                if isinstance(self.graph, networkx.DiGraph):
                    if target != source:
                        lengthMean += length;
                        lengthCount += 1;
                else:
                    if target > source:
                        lengthMean += length;
                        lengthCount += 1;

        lengthMean /= lengthCount;
        lengthRatio = float(lengthCount) / lengthCountUpperBound;
        return (lengthMean, lengthRatio);

class ClosenessCentrality(AveragePathLength):
    def __init__(self, graph):
        self.graph = graph;
        self.centralityDict = {};

    def compute(self):
        self.centralityDict = networkx.closeness_centrality(self.graph);
        return self.centralityDict;

    def generateHistogram(self, binCount):
        maxValue = None;
        minValue = None;
        
        for value in self.centralityDict.values():
            if maxValue == None or maxValue < value:
                maxValue = value;
            if minValue == None or minValue > value:
                minValue = value;

        binWidth = float(maxValue - minValue) / binCount;
        distribution = [0 for i in range(binCount)];
        sumValues = 0.0;

        for value in self.centralityDict.values():
            binIndex = int((value - minValue) / binWidth);
            if binIndex >= binCount:
                binIndex = binCount - 1;

            distribution[binIndex] += 1;
            sumValues += value;

        histogram = [];

        for (binIndex, count) in distribution.items():
            histogram.append((minValue + binIndex * binWidth, minValue + (binIndex + 1) * binWidth, float(count) / sumValues));

        return histogram;

class BetweennessCentrality(ClosenessCentrality):
    def __init__(self, graph):
        super().__init__(graph);

    def compute(self):
        self.centralityDict = networkx.betweenness_centrality(self.graph, normalized = False);
        return self.centralityDict;

def main():
    graphFileName = sys.argv[1];

    inFile = open(graphFileName, "r");
    graphComment = inFile.readline().strip();
    graph = networkx.DiGraph() if graphComment == "Directed" else networkx.Graph();

    for line in inFile:
        info = line.strip().split();
        node1 = int(info[0]);
        node2 = int(info[1]);

        graph.add_edge(node1, node2);

    print("{0:d} nodes".format(graph.number_of_nodes()));
    print("{0:d} edges".format(graph.number_of_edges()));
    print();

    ###############################
    """
    degDist = DegreeDistribution(graph);
    
    for xMin in range(1, 101):
        slope = degDist.estimatePowerLawSlope(xMin);
        print("xMin = {0:d}\tAlpha = {1:.6f}".format(xMin, slope));
        print();
    """
    """
    distribution = degDist.getDistribution();
    print("degree,fraction");
    for (degree, fraction) in sorted(distribution.items()):
        print("{0:d},{1:.6f}".format(degree, fraction));
    """
    ###############################
    """
    avgPathLen = AveragePathLength(graph);
    avgPathLen.reduceGraphToLargestComponent();
    
    (lengthMean, lengthRatio) = avgPathLen.compute();
    print("Average path length: {0:.6f}".format(lengthMean));
    print("Ratio of paths: {0:.6f}".format(lengthRatio));
    print();
    """
    ###############################
    
    closeCen = ClosenessCentrality(graph);
    closeCen.reduceGraphToLargestComponent();
    closenessDict = closeCen.compute();

    printedNodeCount = 0;
    print("node,score");
    for (node, score) in sorted(closenessDict.items(), key = lambda item: item[1], reverse = True):
        if printedNodeCount >= 10:
            break;
        printedNodeCount += 1;
        print("{0:d},{1:.6f}".format(node, score));
    
    ############################### 
    """
    betweenCen = BetweennessCentrality(graph);
    betweenCen.reduceGraphToLargestComponent();
    betweennessDict = betweenCen.compute();

    print("node,score");
    for (node, score) in sorted(betweennessDict.items(), key = lambda item: item[1], reverse = True):
        print("{0:d},{1:.6f}".format(node, score));
    """
if __name__ == "__main__":
    main();
