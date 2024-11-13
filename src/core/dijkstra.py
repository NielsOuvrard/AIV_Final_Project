'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-13 14:36:02
 # @ Description:
 '''

class Node:
    def __init__(self, name: str, dist: float = float('infinity'), path: list[str] = []) -> None:
        self.name = name
        self.dist = dist
        self.path = path
    
    def __eq__(self, other) -> bool:
        return self.dist == other.dist and self.path == other.path
    
    def __str__(self) -> str:
        return f'{self.name} - distance {self.dist} - path {self.path}'
    
    def __repr__(self) -> str:
        return self.__str__()

class Graph:
    def __init__(self, edges: dict[str, dict[str, int]]):
        self.edges = edges
        self.nodes = {node: Node(node) for node in edges.keys()}

    def __str__(self) -> str:
        return str(self.edges)
    
    def __repr__(self) -> str:
        return self.__str__()
    
def dijkstra(graph: Graph, start: str) -> dict[str, Node]:
    distances = graph.nodes
    distances[start].dist = 0
    unvisited = set(graph.nodes.keys())

    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node].dist)

        for neighbor, weight in graph.edges[current_node].items():
            distance = distances[current_node].dist + weight
            if distance < distances[neighbor].dist:
                distances[neighbor].dist = distance
                distances[neighbor].path = distances[current_node].path + ([current_node] if current_node != start else [])

        unvisited.remove(current_node)

    return distances
