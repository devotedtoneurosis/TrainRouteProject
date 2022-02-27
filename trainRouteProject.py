#!/usr/bin/env python3

DEPTH_LIMIT = 20
nodeDictionary = {}

class Node:
    id = ""
    conn = []
    def __init__(self,identifier, connections):
        self.id = identifier
        self.conn = connections

class Edge:
    id = None
    weight = -1
    def __init__(self,dest, wt):
        self.id = dest
        self.weight = wt
        
#The Route class could be accomplished by creating a new  list of nodes, each with only one conneciton
#which represents a valid path, including weights. However, this will lead to a lower stack function
#eventually having an interpretation of a node that is a true node, as well as "false nodes" that only
#represent paths. For the sake of developer clarity and onboarding, the decision was made to use a 
#specific route object to accomplish this.
class Route:
    end = None
    weight = -1
    childRoute = None
    def __init__(self,dest, wt, child):
        self.end = dest
        self.weight = wt
        self.childRoute = child
        
#recursive function taking origin object, and destination name
def find_path_to(origin,destination,allowStops,depthLim,terminateOnDestination):
    dict = nodeDictionary
    connections = []   
    if depthLim > 0:
        #print('='+origin)
        for edge in dict.get(origin).conn:
            #print('edge:'+ edge.id +' '+ str(edge.weight))
            hitDestination = False
            if edge.id == destination:
                connections.append(Route(edge.id,edge.weight,None))
                hitDestination = True

            if hitDestination == False or terminateOnDestination == False:
                if allowStops:
                    childConnections = find_path_to(edge.id,destination,allowStops,depthLim-1,terminateOnDestination)
                    if childConnections:
                        connections.append(Route(edge.id,edge.weight,childConnections))
    
    if len(connections) > 0:
        return connections
    else:
        return None

#as application complexity or map complexity increases, it likely will become worthwhile
#to merge calculate_path_steps, calculate_path_weight, form_path_description to reduce wasted 
#computational load, but right now they are kept for programmatic clarity
def calculate_path_weight(route):
    weight = 0;
    print(route.end)
    if route.childRoute:
        weight += calculate_path_weight(route.childRoute[0])
    else:
        weight += route.weight
    return weight
    
def calculate_route_lowest_weight(route):
    shortest = route.weight
    newWeight = -1
    if route.childRoute:
        for r in route.childRoute:   
            chainWt = calculate_route_lowest_weight(r)
            if newWeight == -1 or chainWt < newWeight:
                newWeight = chainWt
    if newWeight > -1:
        shortest+=newWeight
    return shortest
            

def calculate_path_steps(route):
    steps = 1
    if route.childRoute:
        for el in route.childRoute:
            steps+=calculate_path_steps(el)
    return steps
    
def form_path_descriptions(route):
    first = route.end;
    pathList = []
    if route.childRoute:
        for el in route.childRoute:
            childList = form_path_descriptions(el)
            if len(childList) > 0:    
                for ch in childList:
                    pathList.append(first+ch)
            else:
                pathList.append(first+el.end)
    return pathList
    
def get_all_subroute_weights(route,name):
    first = route.weight;
    name += route.end
    weightList = []
    if route.childRoute:
        for el in route.childRoute:
            childList = get_all_subroute_weights(el,name)
            if len(childList) > 0:    
                for ch in childList:
                    weightList.append([name+ch[0],first+ch[1]])
            else:
                weightList.append([name,first])
    else:
        weightList.append([name,first])
    return weightList

#potentially multiple equally short paths could exist. I would typically  list all of the shortest
#paths that have an equal length but the specification states to only list one, so I will sort and
#print the first in the list to satisfy this requirement
def find_shortest_path(origin,destination,allowStops):
    paths = []
    #print('FINDING SHORTEST PATH:'+origin.id+' '+destination)
    connections = find_path_to(origin,destination,allowStops,DEPTH_LIMIT,True)
    if connections:
        for route in connections:
            paths.append([ route, calculate_route_lowest_weight(route) ]);
        
        if len(paths) > 0:
            paths.sort(key=lambda tup: tup[1]) 
            return paths[0]
    else:
        return None

    
def calculate_multi_step_distance(steps,allowStops):
    dict = nodeDictionary
    distance = -1
    index = 0
    for step in steps:
        if index < (len(steps)-1):
            p0 = find_shortest_path(dict.get(steps[index]).id,steps[index+1],allowStops)
            if p0:
                if distance < 0:
                    distance = 0;
                distance += p0[1]
            else:
                return -1
        index+=1        
    return distance
    
    
    
#build graph from passed map parameters. Parameter is passed as a string by the user. String sanitization/input error
#handling is out of scope of this specification, however, it would be good to add in a future release. To prevent 
#add-by-value rather than add-by-reference issues, the dictionary is directly referenced whenever possible rather
#than a local variable cache
def build_graph(map):
    
    mapElements = map.split(", ")
    for el in mapElements:
        firstNode = None
        secondNode = None
        
        #Add nodes if they do not already exist
        if el[0] not in nodeDictionary:
            firstNode = Node(el[0],[])
            nodeDictionary[el[0]] = firstNode
            
        if el[1] not in nodeDictionary:
            secondNode = Node(el[1],[]);
            nodeDictionary[el[1]] = secondNode
            
        #specification states that a given route will never appear more than once, for this reason, ensure no duplicate
        #this could be expanded on in the future by simply not performing this check
        connectionExists = False
        for connection in nodeDictionary.get(el[0]).conn:
            if connection.id == el[1]:
                connectionExists = True
        
        #add connection
        if connectionExists == False:
            weight = int(el[2])
            nodeDictionary.get(el[0]).conn.append(Edge(el[1],weight))
            
    
      

def main():    
    
    build_graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    
    #distance of route A-B-C
    steps='ABC'
    dist = calculate_multi_step_distance(steps,False)
    if dist != -1:
        print('Output #1:'+str(dist))
    else:
        print('Output #1:NO SUCH ROUTE')
    
    #distance of route A-D
    steps='AD'
    dist = calculate_multi_step_distance(steps,False)
    if dist != -1:
        print('Output #2:'+str(dist))
    else:
        print('Output #2:NO SUCH ROUTE')
    
    #disance of route A-D-C
    steps='ADC'
    dist = calculate_multi_step_distance(steps,False)
    if dist != -1:
        print('Output #3:'+str(dist))
    else:
        print('Output #3:NO SUCH ROUTE')
    
    #The distance of the route A-E-B-C-D.
    steps='AEBCD'
    dist = calculate_multi_step_distance(steps,False)
    if dist != -1:
        print('Output #4:'+str(dist))
    else:
        print('Output #4:NO SUCH ROUTE')
    
    #The distance of the route A-E-D.
    steps='AED'
    dist = calculate_multi_step_distance(steps,False)
    if dist != -1:
        print('Output #5:'+str(dist))
    else:
        print('Output #5:NO SUCH ROUTE')
    
    #The number of trips starting at C and ending at C with a maximum of 3stops. 
    routes = find_path_to('C','C',True,3,False)
    print('Output #6:'+str(len(routes)))
    
    #The number of trips starting at A and ending at C with exactly 4 stops.
    routes = find_path_to('A','C',True,4,False)
    count = 0
    for r in routes:
        rList = form_path_descriptions(r)
        for el in rList:
            if len(el) == 4:
                count+=1
    print('Output #7:'+str(count))
    
    #The length of the shortest route (in terms of distance to travel) from A to C.
    route = find_shortest_path('A','C',True)
    print('Output #8:'+str(route[1]))
    
    #The length of the shortest route (in terms of distance to travel) from B to B.
    route = find_shortest_path('B','B',True)
    print('Output #9:'+str(route[1]))
    
    #The number of different routes from C to C with a distance of less than 30.
    routes = find_path_to('C','C',True,DEPTH_LIMIT,False)
    count = 0
    for r in routes:
        wList = get_all_subroute_weights(r,'')
        for w in wList:      
            if w[1] < 30:
                count+=1
    print('Output #10:'+str(count))
    
    print("Done.")


if __name__ == "__main__":
    main()