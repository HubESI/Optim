class Graph:
    def __init__(self, adj_mat):
        self.adj_mat = adj_mat
    
    @classmethod
    def from_file(cls, file_path):
        with open(file_path) as f:
            line = f.readline()
            while line[0] != "p":
                line = f.readline()
            n = int(line.split()[2])
            adj_mat = [[False]*n]*n
            for line in f:
                if line[0] == "e":
                    w, v = map(int, line.split()[1:])
                    adj_mat[w-1][v-1] = adj_mat[v-1][w-1] = True
        return cls(adj_mat)
