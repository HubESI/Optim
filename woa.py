import math
import random
import sys
from turtle import position

import numpy as np

from coloring import Coloring, Graph, timer


CONFLICT_PENALTY = 10


class WOA(Coloring):
    def __init__(self, g: Graph, nb_search_agents: int = 50, max_iter: int = 100):
        super().__init__(g)
        self.dim = self.g.order
        self.nb_search_agents = nb_search_agents
        self.conflict_penalty = CONFLICT_PENALTY
        self.max_iter = max_iter
        self.leader_pos = None
        self.leader_score = None
        self.positions = None
        self.convergence_curve = None

    def objf(self, position) -> None:
        nb_conflicts = 0
        used_colors = set()
        for vi in range(self.dim):
            used_colors.add(position[vi])
            for adji in range(vi + 1, self.dim):
                if position[vi] == position[adji] and self.adj_mat[vi][adji]:
                    nb_conflicts += 1
        nb_colors = len(used_colors)
        fitness = self.conflict_penalty * nb_conflicts + nb_colors
        # Update the leader
        if fitness < self.leader_score:
            self.leader_score = fitness
            # Update alpha
            self.leader_pos = position.copy()
            self.solution = (nb_colors, self.leader_pos)
            if nb_conflicts > 0:
                print("solution avec conflit")

    @timer
    def solve(self):
        # initialize position vector and score for the leader
        self.leader_pos = np.zeros(self.dim)
        self.leader_score = float("inf")

        # Initialize the positions of search agents
        self.positions = np.zeros((self.nb_search_agents, self.dim), dtype=int)
        for i in range(self.nb_search_agents):
            self.positions[i, :] = np.random.randint((1, self.dim + 1, self.dim))

        # Initialize convergence
        self.convergence_curve = np.zeros(self.max_iter)

        t = 0  # Loop counter

        # Main loop
        while t < self.max_iter:
            for i in range(0, self.nb_search_agents):

                # Return back the search agents that go beyond the boundaries of the search space
                self.positions[i, :] = np.clip(self.positions[i, :], 1, self.dim)

                # Calculate objective function for each search agent and update the leader
                self.objf(self.positions[i, :])

            # a decreases linearly from 2 to 0 in Eq. (2.3)
            a = 2 - t * ((2) / self.max_iter)

            # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
            a2 = -1 + t * ((-1) / self.max_iter)

            # Update the Position of search agents
            for i in range(0, self.nb_search_agents):
                r1 = random.random()  # r1 is a random number in [0,1]
                r2 = random.random()  # r2 is a random number in [0,1]

                A = 2 * a * r1 - a  # Eq. (2.3) in the paper
                C = 2 * r2  # Eq. (2.4) in the paper

                b = 1
                #  parameters in Eq. (2.5)
                l = (a2 - 1) * random.random() + 1  #  parameters in Eq. (2.5)

                p = random.random()  # p in Eq. (2.6)

                for j in range(0, self.dim):

                    if p < 0.5:
                        if abs(A) >= 1:
                            rand_leader_index = math.floor(
                                self.nb_search_agents * random.random()
                            )
                            X_rand = self.positions[rand_leader_index, :]
                            D_X_rand = abs(C * X_rand[j] - self.positions[i, j])
                            self.positions[i, j] = X_rand[j] - A * D_X_rand

                        elif abs(A) < 1:
                            D_leader = abs(
                                C * self.leader_pos[j] - self.positions[i, j]
                            )
                            self.positions[i, j] = self.leader_pos[j] - A * D_leader

                    elif p >= 0.5:

                        distance2Leader = abs(self.leader_pos[j] - self.positions[i, j])
                        # Eq. (2.5)
                        self.positions[i, j] = (
                            distance2Leader
                            * math.exp(b * l)
                            * math.cos(l * 2 * math.pi)
                            + self.leader_pos[j]
                        )

            self.convergence_curve[t] = self.leader_score
            print(
                [
                    "At iteration "
                    + str(t)
                    + " the best fitness is "
                    + str(self.leader_score)
                ]
            )
            t = t + 1

        return self.solution


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input_file> [<output_file>]")
    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = f"{input_file}.woa.sol"
    g = Graph.from_file(input_file)
    col = WOA(g)
    info, t = col.solve()
    gen_count, last_gen = info
    col.to_file(
        output_file,
        graph_info=f"Coloring the graph defined in '{input_file}'",
        time_info=f"WOA in {t:0.6f} seconds after {col.max_iter} iteration",
        hyperparameters=f"nb_search_agents={col.nb_search_agents}",
    )
