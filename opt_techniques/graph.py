from typing import List


class Graph:
    def __init__(self, adj_mat: List[List[bool]], name=None, e=None) -> None:
        self.adj_mat = adj_mat
        self.name = name
        self.v = len(adj_mat)
        if e is None:
            self.e = 0
            for i in range(self.v):
                for j in range(i + 1, self.v):
                    if adj_mat[i][j]:
                        self.e += 1
        else:
            self.e = e

    @property
    def order(self) -> int:
        return len(self.adj_mat)

    @classmethod
    def from_file(cls, file_path: str) -> "Graph":
        with open(file_path) as f:
            instance_name = file_path.split("/")[-1]
            line = f.readline()
            while line[0] != "p":
                line = f.readline()
            v = int(line.split()[2])
            e = int(line.split()[3])
            adj_mat = [[False] * v for _ in range(v)]
            for line in f:
                if line[0] == "e":
                    x, y = map(int, line.split()[1:])
                    adj_mat[x - 1][y - 1] = adj_mat[y - 1][x - 1] = True
        return cls(adj_mat, instance_name, e)

    def to_file(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            if self.name:
                f.write(f"c {self.name}\n")
            f.write(f"p edge {self.v} {self.e}\n")
            edges_lines = []
            for i in range(self.v):
                for j in range(i + 1, self.v):
                    if self.adj_mat[i][j]:
                        edges_lines.append(f"e {i+1} {j+1}\n")
            f.writelines(edges_lines)
