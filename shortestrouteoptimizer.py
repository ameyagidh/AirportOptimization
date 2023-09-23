import csv
import heapq
import math
from collections import deque
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

Main_best_path = ""
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

def haversine_distance(coord1, coord2):
    # Radius of the Earth in miles
    earth_radius = 3958.8  # miles

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance

def adjacency_list(data, routes_file):
    graph = {}
    with open(routes_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            start, end = row[2], row[4]
            if start not in data or end not in data:
                continue
            distance = haversine_distance(data[start], data[end])
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

        if current_node not in graph:
            continue

        for neighbor, weight in graph[current_node].items():
            if neighbor not in distances:
                continue
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return None

def bellman_ford(graph, start, end):
    distances, previous_nodes = {node: float('inf') for node in graph}, {node: None for node in graph}
    distances[start] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            if node not in distances:
                continue
            for neighbor, weight in graph[node].items():
                if neighbor not in distances:
                    continue
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    previous_nodes[neighbor] = node

    # Check for negative weight cycles
    for node in graph:
        if node not in distances:
            continue
        for neighbor, weight in graph[node].items():
            if neighbor not in distances:
                continue
            if distances[node] + weight < distances[neighbor]:
                print("Negative weight cycle detected.")
                return None

    path = []
    current_node = end
    while current_node:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    return path[::-1]

def dfs(graph, start, end):
    stack = [(start, [start])]
    visited = set()

    while stack:
        (node, path) = stack.pop()
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None

def bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        (node, path) = queue.popleft()
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return None

def find_best_route_with_distance(airports_data, routes_file, start_airport, end_airport):
    if start_airport not in airports_data or end_airport not in airports_data:
        print("Invalid airport code.")
        return None  # Return None if no valid route is found

    graph = adjacency_list(airports_data, routes_file)
    possible_stops = [airport for airport in airports_data if airport != start_airport and airport != end_airport]
    results = {}  # Dictionary to store results from each algorithm

    # Dijkstra's algorithm
    path1 = dijkstra(graph, start_airport, end_airport)
    if path1:
        total_distance1 = sum(graph[path1[i]][path1[i + 1]] for i in range(len(path1) - 1))
        results['Dijkstra'] = (path1, total_distance1)

    # Bellman-Ford algorithm
    path2 = bellman_ford(graph, start_airport, end_airport)
    if path2:
        total_distance2 = sum(graph[path2[i]][path2[i + 1]] for i in range(len(path2) - 1))
        results['Bellman-Ford'] = (path2, total_distance2)

    # DFS algorithm
    path3 = dfs(graph, start_airport, end_airport)
    if path3:
        total_distance3 = sum(graph[path3[i]][path3[i + 1]] for i in range(len(path3) - 1))
        results['DFS'] = (path3, total_distance3)

    # BFS algorithm
    path4 = bfs(graph, start_airport, end_airport)
    if path4:
        total_distance4 = sum(graph[path4[i]][path4[i + 1]] for i in range(len(path4) - 1))
        results['BFS'] = (path4, total_distance4)

    if not results:
        print("No available route.")
        return None  # Return None if no valid route is found

    # Find the algorithm with the shortest total distance
    best_algorithm, (best_path, best_total_distance) = min(results.items(), key=lambda x: x[1][1])

    print(f"Optimal flight path ({best_algorithm}): {' -> '.join(best_path)}")
    print(f"Total distance ({best_algorithm}): {best_total_distance} miles")

    # Print results from all algorithms
    for algorithm, (path, total_distance) in results.items():
        if algorithm != best_algorithm:
            print(f"Optimal flight path ({algorithm}): {' -> '.join(path)}")
            print(f"Total distance ({algorithm}): {total_distance} miles")

    return best_path  # Return the best path

def plot_flight_paths_on_map(airports_data, flight_paths):
    fig = go.Figure()

    for algorithm_name, (best_path, _) in flight_paths.items():
        lats, lons = zip(*[airports_data[airport] for airport in best_path])
        fig.add_trace(go.Scattergeo(lat=lats, lon=lons, name=algorithm_name, mode='lines'))

    fig.update_geos(projection_type="albers usa")
    fig.show()


def main():
    airports_data = read_airports_data('airports.csv')
    start_airport = "BOS"
    end_airport = "LAX"

    # Run Dijkstra's algorithm
    best_path = find_best_route_with_distance(airports_data, 'routes.csv', start_airport, end_airport)

    if best_path:
        lats, lons = zip(*[airports_data[airport] for airport in best_path])
        trace = go.Scattergeo(lat=lats, lon=lons, name="Dijkstra", mode='lines')
        layout = go.Layout(geo=dict(projection_type="albers usa"))
        fig = go.Figure(data=[trace], layout=layout)

        fig.update_geos(projection_type="albers usa")
        fig.update_layout(showlegend=True)

        fig.show()


if __name__ == "__main__":
    main()
