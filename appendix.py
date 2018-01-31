
def report(FinalClusters, kmeansInfo, S, c):
	appendix = open('report.txt', 'w')
	appendix.write("Appendix\n")
	appendix.write("----------\n")
	appendix.write("Results of algorithms:\n")
	appendix.write(" - Clusters number found by BSAS: %s\n" % FinalClusters)
	appendix.write(" 	- Initialization parameters: S=%s, c=%s\n" % (S, c))
	appendix.write("\n - Clusters with vectors as assigned by K-means algorithm: \n")
	for i in range(1,FinalClusters+1):
		appendix.write("\nCLUSTER: %s" % i)
		#print "\nCLUSTER: %s\n" % i
		appendix.write("\n%s\n" % kmeansInfo[0][i][1:])
		#print kmeansInfo[i][1:]
	appendix.write("\n\n\n - Clusters with vectors as assigned by H.C. algorithm: \n")
	for i in range(1,FinalClusters+1):
		appendix.write("\nCLUSTER: %s" % i)
		#print "\nCLUSTER: %s\n" % i
		appendix.write("\n%s\n" % kmeansInfo[1][i][1:])
		#print kmeansInfo[i][1:]

	appendix.close()




