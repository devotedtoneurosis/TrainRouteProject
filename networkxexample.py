import networkx as nx

#iterate through a trip string and map the weight of the total trip
def get_weight_of_trip(graph,trip):
    weight = 0
    counter = 0
    while counter < len(trip)-1:
        eD = graph.get_edge_data(trip[counter],trip[counter+1])
        if eD:
            weight += int(eD[0]['weight'])
            counter+=1
        else:
            return 'NO SUCH ROUTE'
    return weight
    
def get_steps_of_trip(graph,trip):
    weight = 0
    counter = 0
    while counter < len(trip)-1:
        eD = graph.get_edge_data(trip[counter],trip[counter+1])
        if eD:
            weight += int(eD[0]['weight'])
            counter+=1
        else:
            return None
    return weight
    
def chart_trip_weight(graph,steps):
    weight = 0
    counter = 0
    while counter < len(steps)-1:
        trip = steps[counter]+steps[counter+1]
        weight += get_weight_of_trip(graph,trip)
        counter+=1
    return weight
    
def chart_trip_with_stop_cap(graph,start,end,stops,depthLimit):
    trips = []
    if start==end:
        trips = chart_trip_allow_loops(graph,start,end,depthLimit,"")
    else:
        trips = nx.all_simple_edge_paths(graph, start, end)
        
    counter = 0
    for trip in trips:
        if len(trip) <= stops:
            counter+=1
    return counter
    
def chart_trip_with_stop_amt(graph,start,end,stops,depthLimit):
    trips = []
    if start==end:
        trips = chart_trip_allow_loops(graph,start,end,depthLimit,"")
    else:
        trips = nx.all_simple_edge_paths(graph, start, end)
        
    counter = 0
    for trip in trips:
        if len(trip)%stops:
            counter+=1
    return counter
    
def chart_trip_with_weight_cap(graph,start,end,weightCap,depthLimit):
    trips = []
    if start==end:
        trips = chart_trip_allow_loops(graph,start,end,depthLimit,start)
    else:
        tripOptions = list(nx.all_simple_edge_paths(graph, start, end))
        for trip in tripOptions:
            tripDescription = [start]
            for t in trip:
                tripDescription.append(t[1])
            trips.append(tripDescription)
    
    validTrips = []
    for trip in trips:
        wt = chart_trip_weight(graph,trip)
        if wt and wt < weightCap:
            validTrips.append(trip)
    return validTrips
    
def chart_shortest_trip(graph,start,end,depthLimit):
    trips = []
    if start==end:
        trips = chart_trip_allow_loops(graph,start,end,depthLimit,"")
    else:
        tripOptions = list(nx.all_simple_edge_paths(graph, start, end))
        for trip in tripOptions:
            tripDescription = [start]
            for t in trip:
                tripDescription.append(t[1])
            trips.append(tripDescription)
    
    shortest_trip = None
    for trip in trips:
        wt = chart_trip_weight(graph,trip)
        if wt and shortest_trip == None or wt < shortest_trip[0]:
            shortest_trip = [wt,trip]
    return shortest_trip
    
def chart_trip_allow_loops(graph,start,end,depthLimit,startPath):
    paths = []
    if depthLimit > 0:
        edges = graph.edges(data=True)
        for e in edges:
            if e[0] == start:
                if e[1] == end:
                    paths.append(startPath+e[1])

                subPaths = chart_trip_allow_loops(graph,e[1],end,depthLimit-1,startPath+e[1])
                for subPath in subPaths:
                    paths.append(subPath)
    return paths

def main():   
    graph = nx.MultiDiGraph()
    mapDefinition = "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7"

    #build map from mapDefinition string
    mapElements = mapDefinition.split(", ")
    for el in mapElements:
        graph.add_weighted_edges_from([(el[0], el[1], int(el[2]))])

    print('Output #1:'+str(get_weight_of_trip(graph,'ABC')))
    print('Output #2:'+str(get_weight_of_trip(graph,'AD')))
    print('Output #3:'+str(get_weight_of_trip(graph,'ADC')))
    print('Output #4:'+str(get_weight_of_trip(graph,'AEBCD')))
    print('Output #5:'+str(get_weight_of_trip(graph,'AED')))
    
    print('Output #6:'+str(chart_trip_with_stop_cap(graph,'C','C',3,5)))
    print('Output #7:'+str(chart_trip_with_stop_amt(graph,'A','C',4,5)))

    print('Output #8:'+str(get_weight_of_trip(graph,nx.shortest_path(graph, 'A', 'C', weight='weight', method='dijkstra'))))
    print('Output #9:'+str(chart_shortest_trip(graph,'A','C',5)[0]))
    print('Output #10:'+str(len(chart_trip_with_weight_cap(graph,'C','C',30,10))))


if __name__ == "__main__":
    main()