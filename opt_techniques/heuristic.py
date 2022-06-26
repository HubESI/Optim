import sys
from functools import total_ordering
from queue import PriorityQueue
from typing import Callable, List, Set

from .coloring import Coloring, Graph, timer


class Heuristic(Coloring):
    def __init__(
        self, g: Graph, node_cost_calculator: Callable[["Heuristic.Node", int], float]
    ) -> None:
        super().__init__(g)
        self.cost_calculator = node_cost_calculator

    def create_node(
        self, vertex: int, state: List[int], newest_color: int, cost: float
    ) -> "Heuristic.Node":
        return self.Node(self, vertex, state, newest_color, cost)

    @total_ordering
    class Node:
        def __init__(
            self,
            outer: "Heuristic",
            vertex: int,
            state: List[int],
            newest_color: int,
            cost: float,
        ) -> None:
            self.outer = outer
            self.vertex = vertex
            self.state = state
            self.newest_color = newest_color
            self.cost = cost

        @classmethod
        def child_node(cls, parent: "Heuristic.Node", color: int) -> "Heuristic.Node":
            vertex = parent.vertex + 1 if parent.vertex < parent.outer.g.order else None
            state = parent.state.copy()
            state[parent.vertex - 1] = color
            newest_color = max(parent.newest_color, color)
            cost = parent.outer.cost_calculator(parent, color)
            return cls(parent.outer, vertex, state, newest_color, cost)

        def __eq__(self, other: "Heuristic.Node") -> bool:
            return self.cost == other.cost

        def __lt__(self, other: "Heuristic.Node") -> bool:
            return self.cost < other.cost

    @timer
    def solve(self) -> None:
        def possible_used_colors(current_vertex: int, state: List[int]) -> Set[int]:
            used_colors = set(state)
            used_colors.remove(None)
            for vi in range(self.g.order):
                if state[vi] and self.adj_mat[current_vertex - 1][vi]:
                    used_colors.discard(state[vi])
            return used_colors

        active_nodes = PriorityQueue()
        active_nodes.put(self.create_node(1, [None] * self.g.order, 0, 0))
        while active_nodes:
            node = active_nodes.get()
            if node.vertex is None:
                self.solution = (len(set(node.state)), node.state)
                break
            possible_colors = possible_used_colors(node.vertex, node.state)
            possible_colors.add(node.newest_color + 1)
            for color in possible_colors:
                active_nodes.put(self.Node.child_node(node, color))


def min_color_cost(node: "Heuristic.Node", color: int) -> float:
    return color / node.vertex


def min_nb_colors_cost(node: "Heuristic.Node", color: int) -> float:
    used_colors = set(node.state)
    used_colors.remove(None)
    used_colors.add(color)
    return len(used_colors) / node.vertex


if __name__ == "__main__":
    try:
        cost_function_selector = int(sys.argv[1])
        input_file = sys.argv[2]
        cost_functions = [
            {
                "func": Heuristic.min_color_cost,
                "name": "Minimal color",
                "output_file": "min_color",
            },
            {
                "func": Heuristic.min_nb_colors_cost,
                "name": "Minimal number of colors",
                "output_file": "min_nb_colors",
            },
        ]
        cost_function = cost_functions[cost_function_selector % len(cost_functions)]
    except (IndexError, ValueError):
        raise SystemExit(
            f"Usage: {sys.argv[0]} <cost_function_selector:int> <input_file> [<output_file>]"
        )
    try:
        output_file = sys.argv[3]
    except IndexError:
        output_file = f"{input_file}.{cost_function['output_file']}_heuristic.sol"
    g = Graph.from_file(input_file)

    col = Heuristic(g, cost_function["func"])
    t = col.solve()[1]
    col.to_file(
        output_file,
        graph_info=f"Coloring the graph defined in '{input_file}'",
        method_time_info=f"{cost_function['name']} heuristic in {t:0.6f} seconds",
    )
