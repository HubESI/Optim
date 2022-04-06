from functools import total_ordering
from queue import PriorityQueue

from coloring import Coloring, timer


class Heuristic(Coloring):
    def __init__(self, g, node_cost_calculator):
        super().__init__(g)
        self.cost_calculator = node_cost_calculator

    def create_node(self, current_vertex, state, cost):
        return self.Node(self, current_vertex, state, cost)

    @total_ordering
    class Node:
        def __init__(self, outer, current_vertex, state, cost):
            self.outer = outer
            self.current_vertex = current_vertex
            self.state = state
            self.cost = cost

        @classmethod
        def child_node(cls, node, color):
            current_vertex = (
                node.current_vertex + 1
                if node.current_vertex < node.outer.order
                else None
            )
            state = node.state.copy()
            state[node.current_vertex - 1] = color
            cost = node.outer.cost_calculator(node, color)
            return cls(node.outer, current_vertex, state, cost)

        def __eq__(self, other):
            return self.cost == other.cost

        def __lt__(self, other):
            return self.cost < other.cost

    @timer
    def solve(self):
        def available_colors(current_vertex, state):
            colors = set(range(1, self.order + 1))
            for vi in range(self.order):
                if state[vi] and self.adj_mat[current_vertex - 1][vi]:
                    colors.discard(state[vi])
            return colors

        active_nodes = PriorityQueue()
        active_nodes.put(self.create_node(1, [None] * self.order, 0))
        while active_nodes:
            node = active_nodes.get()
            if node.current_vertex is None:
                self.solution = (len(set(node.state)), node.state)
                break
            colors = available_colors(node.current_vertex, node.state)
            for color in colors:
                active_nodes.put(self.Node.child_node(node, color))

    @staticmethod
    def min_color_cost(node, color):
        return color / node.current_vertex
