import osmnx as ox
import numpy as np

place = '3, 41 Soi Samkong 1, Ratsada, Amphoe Meuang, Phuket 83000, Thailand'

G = ox.graph_from_place(place, network_type="drive")

orig = list(G)[0]
print(orig)