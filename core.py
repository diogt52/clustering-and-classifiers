#!/usr/bin/env python

'''
A simple python script!
Writen and tested on Python 2.7.10
NOTE: Not compatible with python 3.X.X!
Program def Function() path: main() --> () / ()

'''

'''
About Classifiers:
	Pre-proscess data:  x > 3 [0 or 1]
		.base: 80_000 lines
		.test: 20_000 lines
	Init MLP and LeastSquers

'''

__author__ = "diogt"
__copyright__ = "Copyright (C) Unipi Student P15098"
__license__ = "CC BY-NC-SA"
__version__ = "0.1 -beta-"

'''
Next version:
	version 1.0: generalized to accept any data to process
			   	 going from script to program

'''

# importing libs - START
from math import sqrt
import time
import sys
from random import shuffle
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from tqdm import tqdm
from itertools import groupby
import appendix
#import prep
# importing libs - END

# Create List - START
# preprocess the given data
def CreateList():
	finalList = []
	movRating = []
	userId = []
	movRatCoun = []
	movie_types = []

	# open u.item file
	fMovies = open('u.item')
	# put every line of u.item in list: lines
	lines = fMovies.readlines()


	# find type(s) for every movie
	for i in range(0,1682):
		tempList = []
		# split the information 
		info = lines[i].split("|")
		# get only the movie type
		for i in range(5,24):
			if i == 23:
				# if i == 23 break
				tempList.append(int(info[i]))
				break
			tempList.append(int(info[i]))
		# put tempList in final list. index of elements represent movie_ids
		movie_types.append(tempList)
		
	# close u.item
	fMovies.close()
	
	# Final list that the function will return (with the final result)
	bigList = [[[int(0) for i in range(2)] for j in range(19)] for k in range(943)]
	
	# for information in u.data
	with open("u.data") as data:
		# for every line in u.data
		for line in data:
			user = int(line.split("	")[0])
			rating = int(line.split("	")[2])
			movie = int(line.split("	")[1])
			# set user id - Not needed. Index of list elements is user_id
			# bigList[user -1][0] = user
			# check every movie_type for every entry in u.data
			for po in range(19):
				
				# if movie_type is TRUE (1 not 0)
				if movie_types[movie -1][po] == 1:
					# add rating for current user
					bigList[user - 1][po][0] += rating
					# add count for current movie_type (to find average of every type)
					bigList[user - 1][po][1] += 1
			
		# for every user
		for user in bigList:
			# for every type
			for tt in range(19):
				# if type has rating then:
				if user[tt][1] != 0:
					# find average rating for this type (round with accuracy of 1 decimal)
					user[tt] = round(float(user[tt][0]) / float(user[tt][1]), 1)
				else:
					# else rating is: 0 
					user[tt] = float(0)
		# return the final list
		return bigList

# ==== Create List End ====
# =========================


# euclidian_distance - START
def euclidian_distance(a, b):
	# find euclidian distance of 2 vectors
	dist = sqrt(sum( (a - b)**2 for a, b in zip(a, b)))
	# return distance
	return dist

# ==== euclidian_distance  End ====
# =================================

# cluster_distance - START
# find min distance of vector-cluster
def cluster_distance(vector, cluster):
	distance = []
	# for every vector in cluster
	for cVector in cluster:
		# find distance with function: euc_dist and
		# append the result in list: distance
		distance.append(euclidian_distance(vector, cVector))
	# return min distance vector-vector(in cluster). Book page: 523
	return min(distance)

# ==== cluster_distance  End ====
# ===============================

# MinMaxVector - START
# Fin min/max distance of all vectors
def MinMaxVector(vectorsList):
	# list to hold all the distances. 
	# 1 list is better that an if condition with 2 variables to check
	distance = []
	# tqdm for bar effect
	# for every  vector find distance with every other vector
	for i in tqdm(range(len(vectorsList))):
		# for vector[i] find every distance with other vectors
		for j in range(i+1, len(vectorsList)):
			# calculate distance and append it in list: distance
			distance.append(euclidian_distance(vectorsList[i],vectorsList[j]))
		
	# return min and max distance in a list
	return min(distance), max(distance)


# ==== MinMaxVector  End ====
# ===========================



# BSAS - START
def BSAS(vectors, max_distance, max_clusters):
	# Initialize first cluster with first vector
	clusters = [[vectors[0]]]
	# Set current number of clusters
	cluster_count = 1

	# For every vector except the first one (already in cluster)
	for vector in vectors[1:]:
		# keep every distance between vector - clusters
		distances = []
		# for every cluster
		for cluster in clusters:
			# calculate the distance between the current cluster and vector
			distances.append(cluster_distance(vector, cluster))
		# max_distance == threshold book page: 542
		if min(distances) > max_distance and cluster_count < max_clusters:
			# create new cluster
			clusters.append([vector])
			cluster_count += 1

		else: 
			# add to the cluster with min distance from vector
			clusters[distances.index(min(distances))].append(vector)
	'''
	return number of clusters
	Note:  
		we do not need to return the actual clusters
		because we need to estimate the number of them, 
		not find the vectors in every cluster.
	'''
	return cluster_count
	

# ==== BSAS  End ====
# ===================

# FindClusters - START
# Calculate the best number of clusters (with BSAS) as seen on book page: 545
def FindClusters(vectors, minTheta, maxTheta, S , c):
	tempRes = []
	threshold = minTheta
	
	# Run loop until threshold pass maximum distance between all vectors
	while not threshold > maxTheta:
		res = []
		count = []
		# loop BSAS S times
		for i in range(S): 
			# shuffle vectors
			shuffle(vectors)
			# run BSAS
			cluster = BSAS(vectors, threshold, len(vectors)+1)
			# append res in list: res
			res.append(cluster)	
			
		# pick in random if more than 1 elements is max
		numOfClusters = max(set(res), key=res.count) 
		tempRes.append(numOfClusters)
		
		
		# threshol = threshold + c 
		threshold += c
		
	'''
	Find best cluster number by analizing outpout data
	We will analyze the data by using list comprehension 
	and groupby from itertools 
	'''
	print tempRes
	group = [(k, sum(1 for i in g)) for k,g in groupby(tempRes) if k != 1]
	print group
	'''
	Now on list group we have tuples with every number
	and its constant appearance, except number 1 because
	there is no meaning in picking as number of clusters: 1

	Example of use:
		>>> from itertools import groupby
		>>> tempRes = [1,1,1,3,4,4,4,4,5,6,6,6,6,7,7,8,9,9,1,4,4,4,7,7]
		>>> group = [(k, sum(1 for i in g)) for k,g in groupby(tempRes) if k != 1]
		>>> print group
		[(3, 1), (4, 4), (5, 1), (6, 4), (7, 2), (8, 1), (9, 2), (4, 3), (7, 2)]
		
		Notes:
			1 is ignored
			numbers: 4 and 7 has two tuples because they 
			appear in different places inside the list

	As we see this is a very easy and fast way to analyze the given data 
	with only one library in use (groupby from itertools), without the need
	of threshold values for every cluster.
	'''


	# temporary variables
	temp1 = 0
	temp2 = 0

	'''
	We continue to analyze the data
	Now trying to find the number with the 
	highest frequency of continuous display
	in list: group
	'''
	for item in group:
		if item[1] > temp1:
	 		temp1 = item[1]
	 		temp2 = item[0]
	
	# Check if the highest frequency is in more that 1 elements in the list
	same = []
	tsame = 0
	for item in group:
		if item[1] == temp1:
			same.append(item[0])
			tsame += 1

	# if: TRUE then pick in random and print a message
	if tsame >= 2:
		print "Non succesfull, found with same: "
		print same
		print "\npicking in random"

	# return best number of clusters
	return temp2

# ==== FinalClusters  End ====
# ==========================


# Kmeans - START
def Kmeans(vectors, numofc):
	# Init kmeans with scikit lib and fit vectors
	kmeans = KMeans(n_clusters=numofc, init='random', n_init=15, max_iter=400, precompute_distances=True, copy_x=True, algorithm='full').fit(vectors)
	# prediction for our vectors(list ordered by user_id) in list: pre
	# pre = kmeans.predict(vectors)
	# lebels
	kmeansLabels = kmeans.labels_
	# Cluster Centers
	clusterCenters = kmeans.cluster_centers_
	# Return the predictions
	return kmeansLabels

# ==== Kmeans  End ====
# =====================

# Hierarchical_clustering - START
def Hierarchical_clustering(vectorsList, FinalClusters):
	# init
	hc = AgglomerativeClustering(n_clusters = FinalClusters, affinity = 'euclidean', linkage = 'ward')
	# predict clusters
	y_hc = hc.fit_predict(vectorsList)
	# return results
	return y_hc
# ====== Run H.C. End ======
# ==========================	


# RunKmeansHC - START
# Run Kmeans & HC
def RunKmeansHC(vectorsList, FinalClusters):

	# Ask user
	runKmeans = raw_input("Continue with K-means and H.C.? (y/n): ")
	# keep count and if the user gives 10 times wrong input exit the script
	cnt = 0
	while runKmeans != "n" and runKmeans != "y":
		runKmeans =  raw_input("write [y] for yes and [n] for no: ")
		cnt += 1
		if cnt == 10: # break infinite loop of empty input
			print("\n[x] 10 times wrong answer [break]\n")
			sys.exit()
	# if answer is no then exit
	if runKmeans == "n" :
		sys.exit()
	# else run Kmeans
	else: 
		print "[*] Running K-means and H.C."

	#run K-means
	kmeansLab = Kmeans(list(vectorsList), FinalClusters)
	HcLab = Hierarchical_clustering(list(vectorsList), FinalClusters)
	
	# Process the output data of Kmeans
	# final list of clusters
	clustersOrdK = []
	clustersOrdH = []
	for i in range(0,943):
		clustersOrdK.append([0])
		clustersOrdH.append([0])
		# +1 so cluster number starts from one(1) and not zero(0)
		kmeansLab[i] += 1
		HcLab[i] += 1
	
		
	# create list of clusters
	for i in range(0, 943):
		'''
		For every vector from 1 to 943 
		append it to the corresponding cluster
		for every algorithm
		'''
		clustersOrdK[kmeansLab[i]].append(i+1)
		clustersOrdH[HcLab[i]].append(i+1)


	return clustersOrdK, clustersOrdH 
	
		
# === Run K-meansHC  End ===
# ==========================







'''
 Main Function holds together the above functions
 and gives a User Interface style interaction 
 with the script.

Use: i) Print Information
	 ii) Run the above functions
'''
def main(): 
	print "A simple python script about clustering"
	print "\n[*] Creating List"
	vectorsList = CreateList()
	#print vectorsList[0]
	print "	List is ready.\n"
	print "[!] Continuing on calculation of min/max distance in the vectors."
	minmax = MinMaxVector(list(vectorsList))
	print '	min distance is:  %s ' % minmax[0]
	print '	max distance is:  %s \n' % minmax[1]
	#sys.stdout.write("Lets see\n")
	try: 
		print "Enter parameters for BSAS (number of loops and step\n"
		print "Press [enter] to run with precalculated number of clusters: 5"
		print "S = 15, c(Steps)= 0.4\n"
		S = int(raw_input("Enter number of loops (S) for BSAS: "))
		c = float(raw_input("Enter number of steps (c) for BSAS (up to: %s): " % round(minmax[1])))
		while c >= minmax[1]:
			print "[x] Invalid c."
			c = float(raw_input("Enter number of steps (c) for BSAS (up to: %s): " % round(minmax[1])))
		print "Runing BSAS to find most efficient number of clusters"
		FinalClusters = FindClusters(list(vectorsList), minmax[0], minmax[1], S, c)
	except:
		print "Using precalculated data"
		print "Number of clusters for S=15 and c=0.4: 5"
		S = 15
		c = 0.4
		FinalClusters = 5

	
	print 'Number of clusters: %s' % FinalClusters
	
	kmeansHcInfo = RunKmeansHC(vectorsList, FinalClusters)
	Hierarchical_clustering(vectorsList, FinalClusters)
	appendix.report(FinalClusters, kmeansHcInfo, S, c)
	print "You can see the results in the file: appendix.txt"

	
	#prep.main()



# ==== MAIN END ====
# ==================


# START Program
start_time = time.time()


# Python does not call main() by default
if __name__ == "__main__":
	#try:
	main()
	#except:
	#	print "[x] An unknown error has occurred!"
else:
	print "[x] Do not import me!"

print("--- %s seconds elapsed  ---" % (time.time() - start_time))
