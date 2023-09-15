import csv
import math
import heapq

def read_airports_data(filename):
    airports = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row['STATE'] == 'CA'):
                airport_code = row['IATA']  # Use 'IATA' 
                latitude = float(row['LATITUDE'])  # Use 'LATITUDE' 
                longitude = float(row['LONGITUDE'])  # Use 'LONGITUDE'
                airports[airport_code] = (latitude, longitude)
    return airports

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Radius of the Earth in miles
    radius_miles = 3959.0
    
    # Calculate the distance in miles
    distance_miles = radius_miles * c
    return distance_miles

def adjacency_list(data, origin, destination):
    graph = {}
    for start in data:
        graph[start] = {}
        #print(start + "----------------------------------")
        for end in data:
            if start != end and (start != origin or end != destination):
                lat1, lon1 = data[start]
                lat2, lon2 = data[end]
                distance = haversine(lat1, lon1, lat2, lon2)
                graph[start][end] = distance
                #print(start + " " + end + " " + str(distance))
    return graph

def dijkstra(graph, start, end):
    # Implement Dijkstra's algorithm here to find the shortest path
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]

    # Keep track of the previous node in the path
    #previous = {node: None for node in graph}

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        # Skip if we already found a shorter path to this node
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                #previous[neighbor] = current_node
                heapq.heappush(heap, (distance, neighbor))

    return distances

def main():
    airports_data = read_airports_data('airports.csv')

    # start_airport = input("Enter the starting airport code: ")
    # end_airport = input("Enter the destination airport code: ")
    # stops_count = int(input("Enter the number of stops (1 or 2): "))

    # Check if the provided airport codes exist in the airports_data dictionary
    #if start_airport not in airports_data or end_airport not in airports_data:
    #    print("Invalid airport code.")
    #    return

    # Step 3: Implement Dijkstra's algorithm build graph
    graph = adjacency_list(airports_data, "BUR", "BFL")
    # print(graph)

    # ... Create a weighted graph representing the connections between airports ...

    distances = dijkstra(graph, "BUR", "BFL")
    # print(distances)

    # Step 5: Find the closest stops based on the number of stops requested
    # closest_stops = find_closest_stops(shortest_path, stops_count, airports_data)
    
    # Check if dij is giving is direct flights
    
    print(distances["BFL"])

    # print(graph["BUR"]["ONT"])
    # ... Print the optimal flight path ...  
if __name__ == "__main__":
    main()