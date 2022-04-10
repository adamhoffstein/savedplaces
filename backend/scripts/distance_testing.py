from typing import List, Tuple
from osmnx import graph_from_bbox
import taxicab as tc
import warnings
import osmnx as ox

ox.config(log_console=True)


warnings.filterwarnings('ignore', module='osmnx')


def tuple_min_max(coords: List[Tuple[float, float]], index: int):
    return min(coords[index]), max(coords[index])


start = (7.907, 98.378)
end = (7.903, 98.377)

xmin, xmax = tuple_min_max([start, end], index=1)
ymin, ymax = tuple_min_max([start, end], index=0)

print(xmin, xmax)
print(ymin, ymax)

G = graph_from_bbox(ymax, ymin, xmin, xmax, network_type='drive', simplify=True)

print("GRAPH")
print(G)
print("CALCULATING ROUTE")
route = tc.distance.shortest_path(G, start, end)

print(route)

tc.plot.plot_graph_route(G, route)