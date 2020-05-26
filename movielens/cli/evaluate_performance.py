import sys
import statistics

FOLD_COUNT = 8
MAE_scores = []
setting = sys.argv[1]

for i in range(FOLD_COUNT):
    handle = open("inferred-predicates-"+setting+"/RATING_fold_"+str(i)+".txt", "r")
    lines = handle.readlines()
    ratings = dict({})

    for line in lines:
        tokens = line.split("\t")
        ratings[(tokens[0], tokens[1])] = float(tokens[2])

    truth_handle = open("../data/fold"+str(i)+"/rating_truth.txt", "r")
    truth_lines = truth_handle.readlines()
    linecount = len(truth_lines)

    error_sum = 0
    for line in truth_lines:
        tokens = line.split("\t")
        error_sum += abs(ratings[(tokens[0], tokens[1])] - float(tokens[2]))

    MAE_scores += [float(error_sum / linecount)]

print(MAE_scores)
print(statistics.mean(MAE_scores))
print(statistics.stdev(MAE_scores))
