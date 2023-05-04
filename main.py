#Initialize Empty Dictionary
adjList = {"-1": [("NULL1", "NULL2")]}

def buildGraph(adjList, inputFile):
    # Opening file
    file1 = open(inputFile, 'r')
    edges = 0
    vertex = "-1"
    # Using for loop
    print("Using for loop")
    for line in file1:
        vars = line.split()

        if edges <= 0 :
            vertex = vars[0]
            edges = int(vars[1])
            adjList[vertex] = [None]
        else :
            if vars[1] not in adjList:
                adjList[vars[1]] = [None]
            adjList[vertex].append((vars[0], vars[1]))
            edges -= 1
    # Closing files
    file1.close()
buildGraph(adjList, "./testGraph.txt")
print("End")
