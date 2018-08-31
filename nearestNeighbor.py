#!/usr/bin/python
import math
import argparse
import os
import sys
import time
import profile
import timeit

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the nearest two points on a plan')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ruteforce only or (d)ivide and conquer only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',\
    help='Input dataset of points')

def DACrecursion(points):
    if len(points) <= 3:
        return bruteForceNearestNeighbor(points)
    #end if
    midIndex = int(len(points)/2)
    leftPoints = points[:midIndex]
    rightPoints = points[midIndex:]
    minLeft = DACrecursion(leftPoints) #left
    minRight = DACrecursion(rightPoints) #right
    minDistance = min(minLeft[0], minRight[0])
    point1 = (0,0)
    point2 = (0,0)
    if minDistance == minLeft[0]:
        point1 = minLeft[1]
        point2 = minLeft[2]
    #end if
    else:
        point1 = minRight[1]
        point2 = minRight[2]
    #end else
        
    midStrip = []
    
    for i in range(0,len(points)):
        if (math.fabs(points[i][0]-points[midIndex][0])) < minDistance:
            midStrip.append(points[i])
        #end if
    #end for
    stripTuple = smallestPoints(midStrip,minDistance,point1,point2)
    stripMin = stripTuple[0]
    minimum_distance = min(stripMin, minDistance)
    
    if minDistance == stripMin:
        return (minimum_distance, point1, point2)
        
    return stripTuple
    
#end recursion

def smallestPoints(midStrip, minDistance, dot1, dot2):
    point1 = dot1
    point2 = dot2
    
    minimum_distance = minDistance
    
    midStrip.sort(key = lambda y:y[1])
    j = 1
    for i in range(0,len(midStrip)):
        j = 1 + i
        while j < len(midStrip) and midStrip[j][1] - midStrip[i][1] < minimum_distance:
            currentDistance = math.sqrt(math.pow(midStrip[i][0] - midStrip[j][0],2) + math.pow(midStrip[i][1] - midStrip[j][1],2))
            if currentDistance < minimum_distance:
                point1 = midStrip[i]
                point2 = midStrip[j]
                minimum_distance = currentDistance
            #end if
            j = j + 1
        #end for
    #end for
    return (minimum_distance, point1, point2)
            

#Divide and conquer version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def divideAndConquerNearestNeighbor(points):
    points.sort(key = lambda point:point[0])
    minimum_distance = DACrecursion(points)
    #TODO: Complete this function
    return (minimum_distance[0],minimum_distance[1],minimum_distance[2])
#end def divide_and_conquer(points):


#Brute force version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates 
#   [(x,y),(x,y),...,(x,y)]
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def bruteForceNearestNeighbor(points):
    minimum_distance = 0;
    if len(points) <= 1:
        return (math.inf, points[0][0], points[0][1])
    point1 = points[0]
    point2 = points[1]
    #TODO: Complete this function
    minimum_distance = math.sqrt(math.pow(points[1][0] - points[0][0],2) + math.pow(points[1][1] - points[0][1],2))
    for point in range(0, len(points)):
        for innerPoint in range(point+1, len(points)):
            currentDistance = math.sqrt(math.pow(points[innerPoint][0] - points[point][0],2) + math.pow(points[innerPoint][1] - points[point][1],2))
            if currentDistance < minimum_distance:
                minimum_distance = currentDistance
                point1 = (points[point][0],points[point][1])
                point2 = (points[innerPoint][0],points[innerPoint][1])
            #end if
        #end innerfor
    #end outterfor
    #print("Brute force algorithm is incomplete")
    return (minimum_distance,point1,point2)
#end def brute_force_nearest_neighbor(points):

#Parse the input file
#Input: filename := string of the name of the test case
#Output: points := unsorted array of (x,y) coordinates
#   [(x,y),(x,y),...,(x,y)]
def parseFile(filename):
    points = []
    f = open(filename,'r') 
    lines = f.readlines()
    for line in lines:
        coordinate = line.split(' ')
        points.append((float(coordinate[0]),float(coordinate[1])))
    return points
#end def parse_file(filename):

#Main
#Input: filename  := string of the name of the test case
#       algorithm := flag for the algorithm to run, 'a': all 'b': brute force, 'd': d and c
def main(filename,algorithm):
    points = parseFile(filename)
    result = bruteForceResult = divideAndConquerResult = None
    if algorithm == 'a' or algorithm == 'b':
        start = timeit.default_timer()
        bruteForceResult = bruteForceNearestNeighbor(points)
        #TODO: Insert timing code here
        end = timeit.default_timer()
        print(end - start)
        
    if algorithm == 'a' or algorithm == 'd':
        #TODO: Insert timing code here
        start = timeit.default_timer()
        divideAndConquerResult = divideAndConquerNearestNeighbor(points)
        end = timeit.default_timer()
        print(end - start)
    if algorithm == 'a': # Print whether the results are equal (check)
        if args.verbose:
            print('Brute force result: '+str(bruteForceResult))
            print('Divide and conquer result: '+str(divideAndConquerResult))
            print('Algorithms produce the same result? '+str(bruteForceResult == divideAndConquerResult))
        result = bruteForceResult if bruteForceResult == divideAndConquerResult else ('Error','N/A','N/A')
    else:  
        result = bruteForceResult if bruteForceResult is not None else divideAndConquerResult
    with open(os.path.splitext(filename)[0]+'_distance.txt','w') as f:
        f.write(str(result[1])+'\n')
        f.write(str(result[2])+'\n')
        f.write(str(result[0])+'\n')
#end def main(filename,algorithm):

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
#end if __name__ == '__main__':

