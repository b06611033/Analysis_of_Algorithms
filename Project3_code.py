import pickle
import numpy as np
import copy
import collections

# You can copy the whole code to Google Colab and run there


def label(tree, k):

    labels = []
    for i in range(len(tree)):
        labels.append(-1)

    infoArray, distanceList = preprocess(tree, k)
    bfsLabel(tree, k, labels, infoArray, distanceList)

    for i in range(len(labels)):
        if labels[i] == -1:
            labels[i] = 0

    return labels, computeRatio(tree, k, labels)


def bfsLabel(tree, k, labels, infoArray, distanceList):
    visited = []
    for i in range(len(tree)):
        visited.append(False)

    q = collections.deque()

    q.append(0)
    visited[0] = True

    while q:
        curNode = q.popleft()
        for i in tree[curNode]:
            if visited[i] == False:
                q.append(i)
                visited[i] = True

        dependentNodes = []
        for j in range(len(tree)):
            d = distanceList[curNode][j]
            if d <= infoArray[curNode][1]:
                dependentNodes.append(j)

        if infoArray[curNode][0]:
            for i in dependentNodes:
                if labels[i] == -1:
                    labelChoice = infoArray[curNode][0]
                    label = 0
                    freqMap = {}
                    for choice in labelChoice:
                        freqMap[choice] = 0
                    for j in range(len(tree)):
                        d = distanceList[i][j]
                        if d <= infoArray[j][1]:
                            for choice in labelChoice:
                                if choice in infoArray[j][0]:
                                    freqMap[choice] += 1
                    maxFreq = 0
                    for key in freqMap:
                        if freqMap[key] > maxFreq:
                            maxFreq = freqMap[key]
                            label = key
                    for j in range(len(tree)):
                        d = distanceList[i][j]
                        if d <= infoArray[j][1]:
                            if label in infoArray[j][0]:
                                infoArray[j][0].remove(label)
                    labels[i] = label
                if not infoArray[curNode][0]:
                    break


def preprocess(tree, k):
    infoArray = []
    distanceList = []
    for i in range(len(tree)):
        labelChoice = [j for j in range(k)]
        m, currList = bfsPreprocess(tree, k, i)
        infoArray.append([labelChoice, m])
        distanceList.append(currList)
    return infoArray, distanceList


def bfsPreprocess(tree, k, node):
    visited = []
    for i in range(len(tree)):
        visited.append(False)

    queue = collections.deque()
    distanceq = collections.deque()

    queue.append(node)
    distanceq.append(0)
    visited[node] = True
    count = 1
    m = 0
    dList = []
    for i in range(len(tree)):
        dList.append(0)

    while queue:

        currNode = queue.popleft()
        d = distanceq.popleft()
        dList[currNode] = d

        for i in tree[currNode]:
            if visited[i] == False:
                distanceq.append(d+1)
                queue.append(i)
                visited[i] = True
                count = count + 1
                if count == k:
                    m = d+1

    return m, dList


def computeRatio(tree, k, labels):
    ratio = 1
    for i in range(len(tree)):
        ratio = max(bfsRatio(tree, k, labels, i), ratio)
    return ratio


def bfsRatio(tree, k, labels, node):

    visited = []
    for i in range(len(tree)):
        visited.append(False)

    queue = collections.deque()
    distance = collections.deque()

    queue.append(node)
    distance.append(0)
    labelSet = {labels[node]}
    visited[node] = True
    count = 1
    r = 0
    m = 0

    while queue:

        s = queue.popleft()
        d = distance.popleft()

        for i in tree[s]:
            if visited[i] == False:
                distance.append(d+1)
                queue.append(i)
                visited[i] = True

                count = count + 1
                if count == k:
                    m = d+1

                labelSet.add(labels[i])
                if (len(labelSet) == k):
                    r = d + 1
                    return r/m
    return r/m


def main():
    x_list = []
    # change name and route according to input file
    file1 = open('Test_Set_Large_AdjLists_of_Trees', 'rb')
    file2 = open('Test_Set_Large_of_k_values', 'rb')
    trees = pickle.load(file1)
    kValues = pickle.load(file2)
    maxRatio = 0
    for i in range(len(trees)):
        currList, ratio = label(trees[i], kValues[i])
        maxRatio = max(maxRatio, ratio)
        x_list.append(currList)
        print('the ratio for instance ', i, 'is: ', ratio)
    print("max ratio is: ", maxRatio)
    # change name according to output file
    dataFile = open('large_solutions', 'wb')
    pickle.dump(x_list, dataFile)
    dataFile.close()


if __name__ == "__main__":
    main()
