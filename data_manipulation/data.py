import numpy as np
import matplotlib.pyplot as plt

# Enter file name in file
file = "title.basics.tsv"

inp = open("title.basics.tsv", "r")
cnt = 0
ratings = []
for line in inp.readlines():
	if cnt == 0:
		cnt += 1
	# Sets how many ratings to go through
	elif cnt > 0 and cnt <= 100:
		ratings.append(line.split("\t"))
		print line.split("\t")
		ratings.append(float(line.split("\t")[1]))
		cnt += 1
inp.close()
