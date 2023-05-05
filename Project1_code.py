import pickle
import numpy as np


def compute(n, x, y, c):
    # compute single line error
    xSum = np.zeros(n+1)
    ySum = np.zeros(n+1)
    xySum = np.zeros(n+1)
    xsquareSum = np.zeros(n+1)
    ysquareSum = np.zeros(n+1)
    for i in range(1, n+1):
        xSum[i] = xSum[i-1] + x[i-1]
        ySum[i] = ySum[i-1] + y[i-1]
        xySum[i] = xySum[i-1] + x[i-1]*y[i-1]
        xsquareSum[i] = xsquareSum[i-1] + x[i-1]**2
        ysquareSum[i] = ysquareSum[i-1] + y[i-1]**2
    error = np.zeros((n, n))
    for i in range(1, n+1):
        for j in range(1, i+1):
            if j == i or j == i-1:
                error[j-1, i-1] = 0
            else:
                xTotal = xSum[i] - xSum[j-1]
                yTotal = ySum[i] - ySum[j-1]
                xyTotal = xySum[i] - xySum[j-1]
                xsquareTotal = xsquareSum[i] - xsquareSum[j-1]
                ysquareTotal = ysquareSum[i] - ysquareSum[j-1]
                num = i - j + 1
                aTop = num*xyTotal - xTotal*yTotal
                aBottom = num*xsquareTotal - xTotal**2
                a = aTop/aBottom
                b = (yTotal - a*xTotal)/num
                error[j-1, i-1] = a**2*xsquareTotal + 2*a*b*xTotal - \
                    2*a*xyTotal + num*b**2 - 2*b*yTotal + ysquareTotal

    # dynamic programming to compute the optimal solution
    segments = []
    dp = np.zeros(n+1)
    start = [0]
    for i in range(1, n+1):
        start.append(0)
        for j in range(1, i+1):
            currCost = dp[j-1] + error[j-1, i-1] + c
            if currCost < dp[i] or dp[i] == 0:
                dp[i] = currCost
                start[i] = j
    # backtrack to find segments
    point = n
    while point != 0:
        segments.append(point-1)
        point = start[point] - 1
    segments.reverse()
    return dp[n], segments


def main():
    kList = []
    pointList = []
    costList = []
    # change name and route according to input file
    file = open('examples_of_small_instances', 'rb')
    dictionary = pickle.load(file)
    for i in range(len(dictionary["n_list"])):
        totalCost, currList = compute(dictionary["n_list"][i], dictionary["x_list"]
                                      [i], dictionary["y_list"][i], dictionary["C_list"][i])
        kList.append(len(currList))
        pointList.append(currList)
        costList.append(totalCost)
    data = {}
    data['k_list'] = kList
    data['last_points_list'] = pointList
    data['OPT_list'] = costList
    dataFile = open('mySolution', 'wb')  # change name according to output file
    pickle.dump(data, dataFile)
    dataFile.close()


if __name__ == "__main__":
    main()

# You can copy this code to Google Colab and run there
