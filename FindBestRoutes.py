import csv
import networkx as nx

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
        # For simplicity, we'll use a constant weight of 1 for each edge
        G.add_edge(source['IATA'], target['IATA'], weight=1)

# Find airports with 2 or more routes
airports_with_multiple_routes = []

for source_airport in G.nodes:
    for target_airport in G.nodes:
        if source_airport != target_airport:
            # Find all shortest paths between source and target airports
            shortest_paths = list(nx.all_shortest_paths(G, source=source_airport, target=target_airport, weight='weight'))
            # If there are 2 or more paths, consider it as having 2 or more routes
            if len(shortest_paths) >= 2:
                airports_with_multiple_routes.append((source_airport, target_airport))

# Print airports with 2 or more routes between them
for source_airport, target_airport in airports_with_multiple_routes:
    print(f"Airports with 2 or more routes between them: {source_airport} and {target_airport}")
