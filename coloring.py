import time
from abc import abstractmethod
from typing import Any, Callable, List, Tuple

from graph import Graph


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
        self.solution = None, [None] * len(g.adj_mat)

    @property
    def adj_mat(self) -> List[List[bool]]:
        return self.g.adj_mat

    @property
    def order(self) -> int:
        return self.g.order

    @abstractmethod
    def solve() -> None:
        pass

    def to_file(self, file_path: str, *args, **kwargs) -> None:
        with open(file_path, "w") as f:
            for c in args:
                f.write(f"c {c}\n")
            for _, c in kwargs.items():
                f.write(f"c {c}\n")
            f.write(f"s col {self.solution[0]}\n")
            for vi in range(len(self.solution[1])):
                f.write(f"l {vi+1} {self.solution[1][vi]}\n")
