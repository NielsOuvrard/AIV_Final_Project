import unittest
import copy
from src.core.dijkstra import Node, Graph, dijkstra

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.graphs = [
            Graph({
                'A': {'B': 3, 'C': 5},
                'B': {'A': 3, 'C': 6, 'D': 1},
                'C': {'A': 5, 'B':6, 'D': 2},
                'D': {'B': 1, 'C': 2}
            }),
            Graph({
                'A': {'B': 5, 'C': 8},
                'B': {'A': 5, 'C': 2, 'D': 2},
                'C': {'A': 8, 'B': 2, 'D': 6},
                'D': {'B': 2, 'C': 6}
            }),
            Graph({
                'A': {'B': 2, 'C': 4},
                'B': {'C': 1, 'D': 4, 'E': 2, 'A': 2},
                'C': {'A': 4, 'B': 1, 'E': 3},
                'D': {'B': 4, 'E': 3, 'F': 2},
                'E': {'B': 2, 'C': 3, 'D': 3, 'F': 2},
                'F': {'D': 2, 'E': 2}
            }),
            Graph({
                'A': {'B': 10, 'C': 2},
                'B': {'A': 10, 'H': 1},
                'C': {'A': 2, 'D': 5},
                'D': {'C': 5, 'E': 3},
                'E': {'D': 3, 'F': 4},
                'F': {'E': 4, 'G': 1},
                'G': {'F': 1, 'H': 2},
                'H': {'B': 1, 'G': 2}
            })
        ]

    def test_dijkstra_graph_1(self):
        graph = self.graphs[0]
        expected_distances = {
            'A': {
                'A': Node('A', 0, []),
                'B': Node('B', 3, []),
                'C': Node('C', 5, []),
                'D': Node('D', 4, ['B'])
            },
            'B': {
                'A': Node('A', 3, []),
                'B': Node('B', 0, []),
                'C': Node('C', 3, ['D']),
                'D': Node('D', 1, [])
            },
            'C': {
                'A': Node('A', 5, []),
                'B': Node('B', 3, ['D']),
                'C': Node('C', 0, []),
                'D': Node('D', 2, []),
            },
            'D': {
                'A': Node('A', 4, ['B']),
                'B': Node('B', 1, []),
                'C': Node('C', 2, []),
                'D': Node('D', 0, []),
            }
        }

        for start in graph.edges.keys():
            distances = dijkstra(copy.deepcopy(graph), start)
            for node in graph.edges.keys():
                self.assertEqual(distances[node].dist, expected_distances[start][node].dist)
                self.assertEqual(distances[node].path, expected_distances[start][node].path)


    def test_dijkstra_graph_2(self):
        graph = self.graphs[1]
        expected_distances = {
            'A': {
                'A': Node('A', 0, []),
                'B': Node('B', 5, []),
                'C': Node('C', 7, ['B']),
                'D': Node('D', 7, ['B'])
            },
            'B' : {
                'A': Node('A', 5, []),
                'B': Node('B', 0, []),
                'C': Node('C', 2, []),
                'D': Node('D', 2, []),
            },
            'C' : {
                'A': Node('A', 7, ['B']),
                'B': Node('B', 2, []),
                'C': Node('C', 0, []),
                'D': Node('D', 4, ['B']),
            },
            'D' : {
                'A': Node('A', 7, ['B']),
                'B': Node('B', 2, []),
                'C': Node('C', 4, ['B']),
                'D': Node('D', 0, []),
            }
        }
        for start in graph.edges.keys():
            distances = dijkstra(copy.deepcopy(graph), start)
            for node in graph.edges.keys():
                self.assertEqual(distances[node].dist, expected_distances[start][node].dist)
                self.assertEqual(distances[node].path, expected_distances[start][node].path)

    def test_dijkstra_graph_3(self):
        graph = self.graphs[2]
        expected_distances = {
            'A': {
                'A': Node('A', 0, []),
                'B': Node('B', 2, []),
                'C': Node('C', 3, ['B']),
                'D': Node('D', 6, ['B']),
                'E': Node('E', 4, ['B']),
                'F': Node('F', 6, ['B', 'E'])
            },
            'B': {
                'A': Node('A', 2, []),
                'B': Node('B', 0, []),
                'C': Node('C', 1, []),
                'D': Node('D', 4, []),
                'E': Node('E', 2, []),
                'F': Node('F', 4, ['E']),
            },
            'C': {
                'A': Node('A', 3, ['B']),
                'B': Node('B', 1, []),
                'C': Node('C', 0, []),
                'D': Node('D', 5, ['B']),
                'E': Node('E', 3, []),
                'F': Node('F', 5, ['E']),
            },
            'D': {
                'A': Node('A', 6, ['B']),
                'B': Node('B', 4, []),
                'C': Node('C', 5, ['B']),
                'D': Node('D', 0, []),
                'E': Node('E', 3, []),
                'F': Node('F', 2, []),
            },
            'E': {
                'A': Node('A', 4, ['B']),
                'B': Node('B', 2, []),
                'C': Node('C', 3, []),
                'D': Node('D', 3, []),
                'E': Node('E', 0, []),
                'F': Node('F', 2, []),
            },
            'F': {
                'A': Node('A', 6, ['E', 'B']),
                'B': Node('B', 4, ['E']),
                'C': Node('C', 5, ['E']),
                'D': Node('D', 2, []),
                'E': Node('E', 2, []),
                'F': Node('F', 0, []),
            }
        }
        for start in graph.edges.keys():
            distances = dijkstra(copy.deepcopy(graph), start)
            for node in graph.edges.keys():
                self.assertEqual(distances[node].dist, expected_distances[start][node].dist)
                self.assertEqual(distances[node].path, expected_distances[start][node].path)

    def test_dijkstra_graph_4(self):
        graph = self.graphs[3]
        expected_distances = {
            'A': {
                'A': Node('A', 0, []),
                'B': Node('B', 10, []),
                'C': Node('C', 2, []),
                'D': Node('D', 7, ['C']),
                'E': Node('E', 10, ['C', 'D']),
                'F': Node('F', 14, ['C', 'D', 'E']),
                'G': Node('G', 13, ['B', 'H']),
                'H': Node('H', 11, ['B']),
            },
            'B': {
                'A': Node('A', 10, []),
                'B': Node('B', 0, []),
                'C': Node('C', 12, ['A']),
                'D': Node('D', 11, ['H', 'G', 'F', 'E']),
                'E': Node('E', 8, ['H', 'G', 'F']),
                'F': Node('F', 4, ['H', 'G']),
                'G': Node('G', 3, ['H']),
                'H': Node('H', 1, []),
            },
            'C': {
                'A': Node('A', 2, []),
                'B': Node('B', 12, ['A']),
                'C': Node('C', 0, []),
                'D': Node('D', 5, []),
                'E': Node('E', 8, ['D']),
                'F': Node('F', 12, ['D', 'E']),
                'G': Node('G', 13, ['D', 'E', 'F']),
                'H': Node('H', 13, ['A', 'B']),
            },
            'D': {
                'A': Node('A', 7, ['C']),
                'B': Node('B', 11, ['E', 'F', 'G', 'H']),
                'C': Node('C', 5, []),
                'D': Node('D', 0, []),
                'E': Node('E', 3, []),
                'F': Node('F', 7, ['E']),
                'G': Node('G', 8, ['E', 'F']),
                'H': Node('H', 10, ['E', 'F', 'G']),
            },
            'E': {
                'A': Node('A', 10, ['D', 'C']),
                'B': Node('B', 8, ['F', 'G', 'H']),
                'C': Node('C', 8, ['D']),
                'D': Node('D', 3, []),
                'E': Node('E', 0, []),
                'F': Node('F', 4, []),
                'G': Node('G', 5, ['F']),
                'H': Node('H', 7, ['F', 'G']),
            },
            'F': {
                'A': Node('A', 14, ['G', 'H', 'B']),
                'B': Node('B', 4, ['G', 'H']),
                'C': Node('C', 12, ['E', 'D']),
                'D': Node('D', 7, ['E']),
                'E': Node('E', 4, []),
                'F': Node('F', 0, []),
                'G': Node('G', 1, []),
                'H': Node('H', 3, ['G']),
            },
            'G': {
                'A': Node('A', 13, ['H', 'B']),
                'B': Node('B', 3, ['H']),
                'C': Node('C', 13, ['F', 'E', 'D']),
                'D': Node('D', 8, ['F', 'E']),
                'E': Node('E', 5, ['F']),
                'F': Node('F', 1, []),
                'G': Node('G', 0, []),
                'H': Node('H', 2, []),
            },
            'H': {
                'A': Node('A', 11, ['B']),
                'B': Node('B', 1, []),
                'C': Node('C', 13, ['B', 'A']),
                'D': Node('D', 10, ['G', 'F', 'E']),
                'E': Node('E', 7, ['G', 'F']),
                'F': Node('F', 3, ['G']),
                'G': Node('G', 2, []),
                'H': Node('H', 0, []),
            }
        }
        for start in graph.edges.keys():
            distances = dijkstra(copy.deepcopy(graph), start)
            for node in graph.edges.keys():
                self.assertEqual(distances[node].dist, expected_distances[start][node].dist)
                self.assertEqual(distances[node].path, expected_distances[start][node].path)

if __name__ == '__main__':
    unittest.main()