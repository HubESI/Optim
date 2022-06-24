import sys
import time
from abc import abstractmethod
from typing import Any, Callable, List, Tuple

from .graph import Graph


def timer(func: Callable) -> Callable[..., Tuple[Any, float]]:
    def wrapper_timer(*args, **kwargs) -> Tuple[Any, float]:
        tic = time.process_time()
        value = func(*args, **kwargs)
        toc = time.process_time()
        return value, toc - tic

    return wrapper_timer


class Coloring:
    def __init__(self, g: Graph):
        self.g = g
        self.solution = None, [None] * g.order

    @property
    def adj_mat(self) -> List[List[bool]]:
        return self.g.adj_mat

    @abstractmethod
    def solve(self) -> None:
        pass

    @timer
    def greedy_coloring(self) -> None:
        solution = [-1] * self.g.order
        # Assign the first color to first vertex
        solution[0] = 1
        # A temporary array to store the available colors.
        # False value of available[c] would mean that the
        # color c is assigned to one of its adjacent vertices
        available_colors = [True] * self.g.order
        # Assign colors to remaining n-1 vertices
        for u in range(1, self.g.order):
            # Process all adjacent vertices and
            # flag their colors as unavailable
            for i in range(self.g.order):
                if self.adj_mat[u][i] and solution[i] != -1:
                    available_colors[solution[i] - 1] = False
            # Find the first available color
            c = available_colors.index(True) + 1
            # Assign the found color
            solution[u] = c
            # Reset the values back to false
            # for the next iteration
            available_colors = [True] * self.g.order
        self.solution = len(set(solution)), solution

    def to_file(self, file_path: str, *args, **kwargs) -> None:
        with open(file_path, "w") as f:
            for c in args:
                f.write(f"c {c}\n")
            for _, c in kwargs.items():
                f.write(f"c {c}\n")
            f.write(f"s col {self.solution[0]}\n")
            for vi in range(len(self.solution[1])):
                f.write(f"l {vi+1} {self.solution[1][vi]}\n")


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input_file> [<output_file>]")
    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = f"{input_file}.greedy_coloring.sol"
    g = Graph.from_file(input_file)
    col = Coloring(g)
    t = col.greedy_coloring()[1]
    col.to_file(
        output_file,
        graph_info=f"Coloring the graph defined in '{input_file}'",
        method_time_info=f"Greedy coloring (Welsh Powell) in {t:0.6f} seconds",
    )
