import time

def timer(func):
    def wrapper_timer(*args, **kwargs):
        tic = time.process_time_ns()
        value = func(*args, **kwargs)
        toc = time.process_time_ns()
        return value, toc-tic
    return wrapper_timer

class Coloring:
    def __init__(self, g):
        self.g = g
        self.solution = len(g.adj_mat), [c+1 for c in range(len(g.adj_mat))]

    @timer
    def branch_and_bound(self):
        pass

    def to_file(self, file_path="sol.col", *args):
        with open(file_path, "w") as f:
            for c in args:
                f.write(f"c {c}\n")
            f.write(f"s col {self.solution[0]}\n")
            for v in range(len(self.solution[1])):
                f.write(f"l {v+1} {self.solution[1][v]}\n")
