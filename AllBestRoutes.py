import csv
import networkx as nx
from math import radians, sin, cos, sqrt, atan2


# Function to calculate the Haversine distance between two points (latitude, longitude)
def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371.0 * c  # Radius of the Earth in kilometers
    return distance


# Read data from the CSV file
airport_data = []
with open('airports.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        iata, airport, city, state, country, latitude, longitude = row
        airport_data.append({
            'IATA': iata,
            'AIRPORT': airport,
            'CITY': city,
            'STATE': state,
            'COUNTRY': country,
            'LATITUDE': float(latitude),
            'LONGITUDE': float(longitude)
        })

# Create a graph
G = nx.Graph()

# Add airports as nodes to the graph
for airport_info in airport_data:
    G.add_node(airport_info['IATA'], **airport_info)

# Calculate distances between airports and add weighted edges to the graph
for i in range(len(airport_data)):
    for j in range(i + 1, len(airport_data)):
        source = airport_data[i]
        target = airport_data[j]
        distance = haversine_distance(
            source['LATITUDE'], source['LONGITUDE'],
            target['LATITUDE'], target['LONGITUDE']
        )
        G.add_edge(source['IATA'], target['IATA'], weight=distance)

# Find all shortest paths between two airports
start_airport = 'DCA'  # Replace with the IATA code of the starting airport
end_airport = 'BOS'  # Replace with the IATA code of the destination airport

try:
    all_shortest_paths = list(nx.all_shortest_paths(G, source=start_airport, target=end_airport, weight='weight'))

    # Print all shortest paths with distances
    for i, path in enumerate(all_shortest_paths, start=1):
        total_distance = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
        print(f"Path {i}:")
        for i in range(len(path) - 1):
            source_airport = path[i]
            target_airport = path[i + 1]
            edge_distance = G[source_airport][target_airport]['weight']
            print(f"{source_airport} to {target_airport}: {edge_distance:.2f} km")
        print(f"Total Distance for Path {i}: {total_distance:.2f} km\n")

except nx.NetworkXNoPath:
    print(f"No path found between {start_airport} and {end_airport}.")
