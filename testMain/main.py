# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#f9 prints value from in the script into the consel
import json
import networkx as nx
import numpy as np
from random import randint

def createGraph(fileName):
    dataFile = open(fileName)
    friendNet = nx.DiGraph()
    currUser = []

    for line in dataFile:
        data = json.loads(line)
        currUser = data['user_id']
        friendNet.add_node(currUser)
        friendsList = data['friends_followers']

# filters out self references then adds edges between users
        for word in friendsList:
            user = word['user_id']
            if user != currUser:
                friendNet.add_edge(currUser, user)
    dataFile.close()
    return friendNet

# Purpose: To take the graph as input and generate random ratings for each of the movies and also create a matrix which shows the relationships between each of the users (if they're friends or not)
#####needs rewire of movies instead of friends
def randomMatrix(friendGraph):
	# Friend matrix
	userList = friendGraph.nodes()
	friendMat = []
	for user in userList:
		friendList = friendGraph.neighbors(user)
		friendship = []
		friendship.append([user])
		for user in userList:
			if user in friendList:
				friendship.append([user, 1])
			else:
				friendship.append([user, 0])

		friendMat.append(friendship)

	# Movie matrix
	movieMat = []
	# This is a set of all the movies we're working with
	# Will contain the IDs of the movies
	movies = []
	fileDict = convertToDict("TUPVariedFriendList.json")
	# Get all the movies
	for user in userList:
		userDict = fileDict[user]
		for movie in userDict["movies"]:
			if movie["movie_id"] not in movies:
				movies.append(movie["movie_id"])
    

	# Now we can actually start generating ratings
	for user in userList:
		movieRating = []
		movieRating.append([user])
		ratings = []
		for movie in movies:
			rating = randint(0, 10)
			ratings.append([movie, rating])
		movieRating.append(ratings)
		movieMat.append(movieRating)
	return [friendMat, movieMat]
    

# Purpose: converts a given JSON file to a Dictionary
def convertToDict(fileName):
	fileName = open(fileName, "r")
	jsonDict = {}
	for line in fileName:
		data = json.loads(line)
		jsonDict[data["user_id"]] = data
	return jsonDict

# Purpose: Get the list of movie ratings from each of the friends
def movieRatingsList(friendGraph):
	userList = friendGraph.nodes()
	file = "TUPVariedFriendList.json"
	fileDict = convertToDict(file)
	matrix = []
	# Using the friendGraph
	for user in userList:
		singleUser = []
		currUser = [user]
		singleUser.append(currUser)
		friends = friendGraph.neighbors(user)
		for friend in friends:
			singleUser.append([friend])
			movies = fileDict[friend]["movies"]
			ratings = []
			for movie in movies:
				rating = movie["movie_rating"]
				ratings.append(rating)
			singleUser.append(ratings)
		matrix.append(singleUser)
	return matrix

## Purpose: to take the graph of users and create a matrix that reps
## friendships amoung nodes
def userFriendMat(friendGraph):
    userList = friendGraph.nodes()
    userListNum = len(userList)
    A = np.zeros((userListNum, userListNum))

    for x in range(userListNum):
        i = 0
        friendList = friendGraph.neighbors(x+1)
        friListLen = len(friendList)
        for y in range(userListNum):
            if i<friListLen:
                if x == y:
                    A[x][y] = 0.0
                else:
                    if y == friendList[i]-1:
                        A[x][y] = 1.0
                        i = i+1
                    else:
                        A[x][y] = 0.0
    return A
def listRetrieval(userMovieList, friendMovieMat):
    #will be changed to max number of users and max number of movies
    #hard coding bad... bad.
    newMatrix = np.zeros((6,5))
    for i in range(len(friendMovieMat)):
        k = 0
        for j in range(len(friendMovieMat[0])):
            modin = j%5
            if modin == 0 and j != 0:
                k = k+1
                #will change to 0 l8
                newMatrix[k][modin] = randint(1, 10)
            else:                
                newMatrix[k][modin] = randint(1, 10)
        
        userMovieList = ufRecommendation(userMovieList, i, newMatrix)
    return userMovieList
    
def ufRecommendation(userMovieList, i, friendMovieMat):
    numCol = len(userMovieList[i])
    for movieIndex in range(numCol):
        if userMovieList[i][movieIndex] == 0.0:
            # finding the movies a user hasn't seen before"
            userMovieList[i][movieIndex] = avgFriendMovieRatings(movieIndex, friendMovieMat)
    return userMovieList
## purpose: this function takes the averages of all the values in a row of the
## matrix, sums them then stores them in the location of the current users index

##currently this is using the friend matrix what we need are the movies associated
##with this matrix to be able to calculate averages
def avgFriendMovieRatings(movieIndex, friendMovieMat):
    col = movieIndex
    temp = 0.0
    numRow = len(friendMovieMat)
    for x in range(numRow):
        temp = temp+friendMovieMat[x][col-1]
    avgMovieVal = float("{0:.4f}".format(temp/(numRow)))
    return avgMovieVal

##### we need to figure out how we want to store values so we can build the averages
##### function, how will we denote friends for each user? how will we be able to tell
def printMat (userMoveList):
    for i in range(len(userMovieList)):
        print "current user: ", i
        temp = []
        for j in range(len(userMovieList[0])):
            temp.append(userMovieList[i][j])
        print temp
            

if __name__ == "__main__":
    userMovieList = [[0.0,2,7,10,5,0.0],[2,0.0,7,0.0,10,5]]
    userMovieMatrix = [[1,2,3,4,5,5,4,3,2,1,7,6,5,4,3],[9,5,7,2,2,3,9,3,3,1,10,1,2,8,4]]
    friendGraph = createGraph("TUPVariedFriendList.json")
    friend = randomMatrix(friendGraph)
    friendMovieMat = movieRatingsList(friendGraph)
    print
    print "Original User Movie Ratings:"
    printMat(userMovieList)
    userMovieList = listRetrieval(userMovieList, userMovieMatrix)
    print
    print "Recommended User Movie Ratings:"
    printMat (userMovieList)
##THINGS TO DO##
######   need to create an update user function  ######