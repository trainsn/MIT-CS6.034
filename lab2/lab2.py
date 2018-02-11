# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
import math

def quickSort(graph,goal,alist,sortType=0):
   quickSortHelper(graph,goal,alist,0,len(alist)-1,sortType)

def quickSortHelper(graph,goal,alist,first,last,sortType):
   if first<last:

       splitpoint = partition(graph,goal,alist,first,last)

       quickSortHelper(graph,goal,alist,first,splitpoint-1,sortType)
       quickSortHelper(graph,goal,alist,splitpoint+1,last,sortType)

def partition(graph,goal,alist,first,last):
   pivotvalue = graph.get_heuristic(alist[first][-1],goal) #- len(alist[first])

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and \
               graph.get_heuristic(alist[leftmark][-1],goal)  <= pivotvalue:
           leftmark = leftmark + 1

       while graph.get_heuristic(alist[rightmark][-1],goal) >= pivotvalue and \
               rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp


   return rightmark


def quickSort_bnb(graph,goal,alist,sortType=0):
   quickSortHelper_bnb(graph,goal,alist,0,len(alist)-1,sortType)

def quickSortHelper_bnb(graph,goal,alist,first,last,sortType):
   if first<last:

       splitpoint = partition_bnb(graph,goal,alist,first,last)

       quickSortHelper_bnb(graph,goal,alist,first,splitpoint-1,sortType)
       quickSortHelper_bnb(graph,goal,alist,splitpoint+1,last,sortType)

def partition_bnb(graph,goal,alist,first,last):
   pivotvalue = graph.get_heuristic(alist[first][-1],goal) + path_length(graph,alist[first])

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and \
               graph.get_heuristic(alist[leftmark][-1],goal) + path_length(graph,alist[leftmark]) <= pivotvalue:
           leftmark = leftmark + 1

       while graph.get_heuristic(alist[rightmark][-1],goal) + path_length(graph,alist[rightmark]) >= pivotvalue and \
               rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp


   return rightmark

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    pathList = [(start,)]
    
    if start == goal:
        return [start]
    while len(pathList)>0:
        #print pathList
        #print [ graph.get_heuristic(path[-1],goal) for path in pathList ]
        newPaths = []
        while (len(pathList)>0):
            pathToExtend = pathList[0]
            #print pathToExtend 
            pathList.remove(pathToExtend)
            nodeToExtend = pathToExtend[-1]
            #print nodeToExtend
            newNodes = graph.get_connected_nodes(nodeToExtend)
            newNodes = [node for node in newNodes if node not in pathToExtend]    
            if goal in newNodes:
                return list(pathToExtend+(goal,))
            newPaths += [pathToExtend + (node,) for node in newNodes]
            #print newPaths
        pathList.extend(newPaths)        
    return []
    #raise NotImplementedError

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    pathList = [(start,)]
    
    if start == goal:
        return [start]
    while (len(pathList)>0):
        pathToExtend = pathList[0]
        #print pathToExtend 
        pathList.remove(pathToExtend)
        nodeToExtend = pathToExtend[-1]
        #print nodeToExtend
        newNodes = graph.get_connected_nodes(nodeToExtend)
        newNodes = [node for node in newNodes if node not in pathToExtend]    
        if goal in newNodes:
            return list(pathToExtend+(goal,))
        newPaths = [pathToExtend + (node,) for node in newNodes]
        #print newPaths
        newPaths.extend(pathList)   
        pathList = newPaths
    return []
    #raise NotImplementedError


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    pathList = [(start,)]
    
    if start == goal:
        return [start]
    while (len(pathList)>0):
        pathToExtend = pathList[0]
        #print pathToExtend 
        pathList.remove(pathToExtend)
        nodeToExtend = pathToExtend[-1]
        #print nodeToExtend
        newNodes = graph.get_connected_nodes(nodeToExtend)
        newNodes = [node for node in newNodes if node not in pathToExtend]    
        if goal in newNodes:
            return list(pathToExtend+(goal,))
        newPaths = [pathToExtend + (node,) for node in newNodes]
        #print newPaths
        dist = []
        for path in newPaths:
            dist.append(graph.get_heuristic(path[-1], goal))
        #print dist    
        
        for i in range(0,len(newPaths)):
            for j in range(i+1, len(newPaths)):
                if (dist[i] > dist[j]):
                    temp = newPaths[i]
                    newPaths[i] = newPaths[j]
                    newPaths[j] = temp
                    distemp = dist[i]
                    dist[i] = dist[j]
                    dist[j] = distemp
                           
        newPaths.extend(pathList)   
        pathList = newPaths
    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    pathList = [(start,)]
    
    if start == goal:
        return [start]
    while len(pathList)>0:
        #print pathList
        #print [ graph.get_heuristic(path[-1],goal) for path in pathList ]
        newPaths = []
        while (len(pathList)>0):
            pathToExtend = pathList[0]
            #print pathToExtend 
            pathList.remove(pathToExtend)
            nodeToExtend = pathToExtend[-1]
            #print nodeToExtend
            newNodes = graph.get_connected_nodes(nodeToExtend)
            newNodes = [node for node in newNodes if node not in pathToExtend]    
            if goal in newNodes:
                return list(pathToExtend+(goal,))
            newPaths += [pathToExtend + (node,) for node in newNodes]
            
            #print newPaths
            dist = []
            for path in newPaths:
                dist.append(graph.get_heuristic(path[-1], goal))
            #print dist    
            
            for i in range(0,len(newPaths)):
                for j in range(i+1, len(newPaths)):
                    if (dist[i] > dist[j]):
                        temp = newPaths[i]
                        newPaths[i] = newPaths[j]
                        newPaths[j] = temp
                        distemp = dist[i]
                        dist[i] = dist[j]
                        dist[j] = distemp
        pathList.extend(newPaths[:beam_width])        
    return []
    #raise NotImplementedError

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    for i in range(0,len(node_names)-1): 
        length += graph.get_edge(node_names[i], node_names[i+1]).length
    return length
    #raise NotImplementedError


def branch_and_bound(graph, start, goal):
    pathList = [(start,)]
    minDist = 1000
    
    if start == goal:
        return [start]
    while (len(pathList)>0):
        #find the one with lowest distance so far
        dist = []
        for i in range(0,len(pathList)):
            path = pathList[i]
            dist.append(path_length(graph,path))
            
        distemp = 10000;
        for i in range(0,len(pathList)):
            if (dist[i]<distemp):
                distemp = dist[i]
                pathToExtend = pathList[i]              
        pathList.remove(pathToExtend)
        nodeToExtend = pathToExtend[-1]
        #print nodeToExtend
        newNodes = graph.get_connected_nodes(nodeToExtend)
        newNodes = [node for node in newNodes if (node not in pathToExtend)]    
        if goal in newNodes:
            node_names = list(pathToExtend+(goal,))
            if path_length(graph,node_names) < minDist:
                minDist = path_length(graph,node_names)
                ans = node_names
        newPaths = [pathToExtend + (node,) for node in newNodes if path_length(graph,pathToExtend+(node,))<minDist]
        #print newPaths
        newPaths.extend(pathList)   
        pathList = newPaths
    if minDist == 1000:
        return []
    else:
        return ans
    #raise NotImplementedError

def a_star(graph, start, goal):
    pathList = [(start,)];
    if start == goal:
        return [start]
    
    while len(pathList) > 0:
        #print pathList
        #print [ graph.get_heuristic(path[-1],goal) + path_length(graph,path) for path in pathList ]
        dist = []
        for i in range(0,len(pathList)):
            path = pathList[i]
            dist.append(graph.get_heuristic(path[-1],goal) + path_length(graph,path))
            
        distemp = 10000;
        for i in range(0,len(pathList)):
            if (dist[i]<distemp):
                distemp = dist[i]
                pathToExtend = pathList[i]              
        pathList.remove(pathToExtend)
        nodeToExtend = pathToExtend[-1]
        newNodes = graph.get_connected_nodes(nodeToExtend)
        newNodes = [ node for node in newNodes if node not in pathToExtend]

        if goal in newNodes:
            return pathToExtend + (goal,)

        newPaths = [ pathToExtend + (node,) for node in newNodes ]
        newPaths.extend(pathList)
        pathList = newPaths                                   
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node1 in graph.nodes:
        if path_length(graph,branch_and_bound(graph, node1, goal)) < graph.get_heuristic(node1, goal):
            return False
    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        if abs(graph.get_heuristic(edge.node1,goal) - graph.get_heuristic(edge.node2,goal)) > edge.length:
              return False
    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = 'do not count'
WHAT_I_FOUND_INTERESTING = 'a star'
WHAT_I_FOUND_BORING = 'none'
