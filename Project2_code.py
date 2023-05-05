import pickle
import numpy as np

# n is number of variables
# p is number of lead to conditions
# q is number of false must exist conditions
# t is lead to condition variables
# m is false must exist condition variables


def compute(n, p, q, t, m):
    # all variables set to false(0)
    truthTable = []
    for i in range(n):
        truthTable.append(0)
    satisfied = False
    while satisfied == False:
        satisfied = True
        for i in range(p):
            change = True
            for j in range(len(t[i])-1):
                variable = t[i][j]
                if truthTable[variable] == 0:
                    change = False
                    break
            if change:
                if truthTable[t[i][len(t[i])-1]] == 0:
                    satisfied = False
                    truthTable[t[i][len(t[i])-1]] = 1
        for i in range(q):
            contradict = True
            for j in range(len(m[i])):
                variable = m[i][j]
                if (truthTable[variable] == 0):
                    contradict = False
            if contradict:
                return []
    return truthTable


def main():
    x_list = []
    # change name and route according to input file
    file = open('test_set_large_instances', 'rb')
    dictionary = pickle.load(file)
    for i in range(len(dictionary["n_list"])):
        currList = compute(dictionary["n_list"][i], dictionary["P_list"]
                           [i], dictionary["Q_list"][i], dictionary["T_list"][i], dictionary["M_list"][i])
        x_list.append(currList)
    # change name according to output file
    dataFile = open('large_solutions', 'wb')
    pickle.dump(x_list, dataFile)
    dataFile.close()


if __name__ == "__main__":
    main()

# You can copy this code to Google Colab and run there
