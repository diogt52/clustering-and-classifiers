#!/usr/bin/env python

'''
A simple python script!
Writen and tested on Python 2.7.10
'''


'''
NOTES:

.base: 80_000 lines
.test: 20_000 lines
 
 Missing:
 	i) preprocessing of .test files - READY
	ii) K-fold (for loop) to process lists - READY
	iii) Algorithms (MLPerceptron &  Least Squares) - READY

MLP: http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html
Least Squeres: http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html

K-fold. In this case: 5-fold
 You give the algorithm 5 training sets, along with 5 test sets to "learn" the data and
 make more accurate predictions.

 How it works: http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html

 NOTE: We can not use KFold from scikit because we already have our 5-fold files.
 	   We just need to process them like below


'''

# START
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import sys
import numpy as np
from tqdm import tqdm



__author__ = "diogt"


# list of files directories
trainingFiles = ['5-fold/u1.base','5-fold/u2.base','5-fold/u3.base','5-fold/u4.base','5-fold/u5.base']
testFiles = ['5-fold/u1.test','5-fold/u2.test','5-fold/u3.test','5-fold/u4.test','5-fold/u5.test']



def PreProcess(vec):
	bigList = []
	# same loop for all u[i].base files, i E [1,5], i E |R 
	for i in tqdm(range(5),desc='Data preprocessing..'):
		# open every file
		with open(vec[i]) as data:
			# temp list too build every line
			temp = []
			# for every line in the file
			for line in data:
				# take first line and split it in: list
				list = line.split("	")
				# change str to int & remove last entry (timestamp) [:-1]
				# put line in temp list
				temp.append([int(x) for n, x in enumerate(list[:-1])])

		# put temp list in final list (bigList)
		bigList.append(temp)
	# change ratings to: 0 or 1
	for tt in bigList:
		for vector in tt:
			if vector[2] >= 3:
				vector[2] = 1
			else: 
				vector[2] = 0
	return bigList

def Process2(ProcessedData):
	userMovieId = []
	res = []
	for lists in list(ProcessedData):
		temp = []
		temp2 = []
		for data in list(lists):
			temp.append(data[:-1])
			temp2.append(data[2:3])
		userMovieId.append(temp)
		res.append(temp2)
	return userMovieId, res


def main():
	final = Process2(PreProcess(trainingFiles))
	finalTest = Process2(PreProcess(testFiles))
	
	# Final Lists ===========
	uMTest = finalTest[0]
	res2 = finalTest[1]

	userMovieId = final[0]
	res = final[1]
	# =======================
	
	scaler = StandardScaler()

	accMLP = []
	accLinReg = []
	LinReg = LinearRegression(copy_X=True,fit_intercept=True, normalize=False)
	MLP = MLPClassifier(hidden_layer_sizes=(4,2), activation='logistic', solver='sgd', alpha=1e-5, learning_rate='adaptive', max_iter=1000,shuffle=True)
	
	# Train classifiers with 5fold cross-validation
	for i in tqdm(range(5),desc='Training classifiers'):
	
		for it in res2[i]:
			for tt in it:
				tt = [1]
		#scale data 
		scaler.fit(userMovieId[i])
		userMovieId[i] =  scaler.transform(userMovieId[i])
		uMTest[i] = scaler.transform(uMTest[i]) 

		MLP.fit(userMovieId[i], np.ravel(res[i]))
		accMLP.append(MLP.score(uMTest[i], np.ravel(res2[i])))
		LinReg.fit(userMovieId[i], np.ravel(res[i]))
		accLinReg.append(LinReg.score(uMTest[i], np.ravel(res2[i])))
	print "Average accuracy of Multi-layer Perceptron: ", sum(accMLP)/len(accMLP)*100,"%"
	print "Average accuracy of Least Squeres: ", round(sum(accLinReg)/len(accLinReg)*100,2),"%"
	

	# Input IDs for prediction
	print"\nNow the two classifiers are able to try to predict if a user has seen a spesific movie"
	
	makePred = True

	while makePred:
		check = []
		try:
			uID =  int(raw_input("\nEnter user ID: "))
			mID =  int(raw_input("Enter movie ID: "))
			
			while uID > 943 or uID < 1 or mID > 1682 or mID < 1:
				print "Give valid input!"
				uID =  int(raw_input("\nEnter user ID: "))
				mID =  int(raw_input("Enter movie ID: "))
			
		except:
			print "[x] An unknown error has occurred!"
			print "exiting..."
			sys.exit()
		check.append(uID)
		check.append(mID) 
		passit = []
		passit.append(check)
		passit = scaler.transform(passit)
		mlpPr = round(MLP.predict(passit))
		linPr = round(LinReg.predict(passit))
		print "\nMulti-layer Perceptron:"
		if mlpPr == 1:
			print "	user with id %s has seen the movie with id %s " % (uID, mID)
		else:
			print "	user with id %s has NOT seen the movie with id %s " % (uID, mID)
		
		print "Least Squeres:"
		if linPr == 1:
			print "	user with id %s has seen the movie with id %s " % (uID, mID)
		else:
			print "	user with id %s has not seen the movie with id %s " % (uID, mID)
		
		new = raw_input("\nTry new prediction?(y/n): ")

		while new not in ['y', 'Y', 'yes', 'Yes', 'YES','n','N','no','NO']:
			new = raw_input("Enter yes or no (y/n): ")


		if new in ['y', 'Y', 'yes', 'Yes', 'YES']:
			makePred = True
		else:
			makePred = False


	


print " A simple python script!"
main()






