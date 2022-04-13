from functools import total_ordering
from queue import PriorityQueue
from typing import Callable, List, Set

from coloring import Coloring, Graph, timer


class Heuristic(Coloring):
    def __init__(
        self, g: Graph, node_cost_calculator: Callable[["Heuristic.Node", int], float]
    ) -> None:
        super().__init__(g)
        self.cost_calculator = node_cost_calculator

    def create_node(
        self, current_vertex: int, state: List[int], cost: float
    ) -> "Heuristic.Node":
        return self.Node(self, current_vertex, state, cost)

    @total_ordering
    class Node:
        def __init__(
            self, outer: "Heuristic", current_vertex: int, state: List[int], cost: float
        ) -> None:
            self.outer = outer
            self.current_vertex = current_vertex
            self.state = state
            self.cost = cost

        @classmethod
        def child_node(cls, node: "Heuristic.Node", color: int) -> "Heuristic.Node":
            current_vertex = (
                node.current_vertex + 1
                if node.current_vertex < node.outer.order
                else None
            )
            state = node.state.copy()
            state[node.current_vertex - 1] = color
            cost = node.outer.cost_calculator(node, color)
            return cls(node.outer, current_vertex, state, cost)

        def __eq__(self, other: "Heuristic.Node") -> bool:
            return self.cost == other.cost

        def __lt__(self, other: "Heuristic.Node") -> bool:
            return self.cost < other.cost

    @timer
    def solve(self) -> None:
        def available_colors(current_vertex: int, state: List[int]) -> Set[int]:
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
    def min_color_cost(node: "Heuristic.Node", color: int) -> float:
        return color / node.current_vertex

    @staticmethod
    def min_nb_colors_cost(node: "Heuristic.Node", color: int) -> float:
        used_colors = set(node.state)
        # used_colors.remove(None)
        return len(used_colors) / node.current_vertex
