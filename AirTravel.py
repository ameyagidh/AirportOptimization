import csv
import heapq
import math

def read_airports_data(filename):
    airports = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airport_code = row['IATA']
            latitude = float(row['LATITUDE'])
            longitude = float(row['LONGITUDE'])
            airports[airport_code] = (latitude, longitude)
    return airports

def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def adjacency_list(data, routes_file):
    graph = {}
    with open(routes_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            start, end, distance = row[0], row[1], float(row[2])
            if start not in graph:
                graph[start] = {}
            graph[start][end] = distance
    return graph

def dijkstra(graph, start, end):
    pq, distances, previous_nodes = [], {node: float('inf') for node in graph}, {node: None for node in graph}
    distances[start] = 0
    heapq.heappush(pq, (0, start))
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            path = []
            while current_node:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            return path[::-1]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    return None

def find_best_route(airports_data, routes_file, start_airport, end_airport):
    if start_airport not in airports_data or end_airport not in airports_data:
        print("Invalid airport code.")
        return

    graph = adjacency_list(airports_data, routes_file)
    possible_stops = [airport for airport in airports_data if airport != start_airport and airport != end_airport]
    routes = []
    for stop in possible_stops:
        path1 = dijkstra(graph, start_airport, stop)
        path2 = dijkstra(graph, stop, end_airport)
        if path1 and path2:
            routes.append(path1[:-1] + path2)

    best_route = min(routes, key=lambda route: sum(graph[route[i]][route[i + 1]] for i in range(len(route) - 1)), default=None)

    if best_route:
        print("Optimal flight path:", ' -> '.join(best_route))
    else:
        print("No available route.")

def main():
    airports_data = read_airports_data('airports.csv')
    start_airport = input("Enter the starting airport code: ")
    end_airport = input("Enter the destination airport code: ")

    find_best_route(airports_data, 'routes.csv', start_airport, end_airport)

if __name__ == "__main__":
    main()
