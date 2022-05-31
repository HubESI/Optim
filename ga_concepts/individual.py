from functools import total_ordering
from random import getrandbits, randint
from typing import Tuple


@total_ordering
class Individual:
    def __init__(self, ga):
        self.ga = ga
        self.genes = [None] * ga.g.order
        self.nb_conflicts = None
        self.nb_colors = None
        self.fitness = None

    @staticmethod
    def create_rand(ga) -> "Individual":
        individ = Individual(ga)
        for gi in range(ga.g.order):
            individ.genes[gi] = randint(1, ga.bound)
        individ.calc_fitness()
        return individ

    def calc_fitness(self) -> None:
        self.nb_conflicts = 0
        used_colors = set()
        for vi in range(self.ga.g.order):
            used_colors.add(self.genes[vi])
            for adji in range(self.ga.g.order):
                if self.genes[vi] == self.genes[adji] and self.ga.adj_mat[vi][adji]:
                    self.nb_conflicts += 1
        self.nb_colors = len(used_colors)
        self.fitness = 1 / (
            self.ga.confilct_penalty * self.nb_conflicts + self.nb_colors
        )
        if self.nb_conflicts == 0 and self.nb_colors < self.ga.solution[0]:
            self.ga.solution = self.nb_colors, self.genes

    @staticmethod
    def one_point_crossover(
        p1: "Individual", p2: "Individual"
    ) -> Tuple["Individual", "Individual"]:
        assert p1.ga == p2.ga
        ga = p1.ga
        o1, o2 = Individual(ga), Individual(ga)
        cp = randint(0, ga.g.order - 1)
        o1.genes = p1.genes[: cp + 1] + p2.genes[cp + 1 :]
        o2.genes = p2.genes[: cp + 1] + p1.genes[cp + 1 :]
        o1.calc_fitness()
        o2.calc_fitness()
        return o1, o2

    @staticmethod
    def uniform_crossover(
        p1: "Individual", p2: "Individual"
    ) -> Tuple["Individual", "Individual"]:
        assert p1.ga == p2.ga
        ga = p1.ga
        o1, o2 = Individual(ga), Individual(ga)
        for i in range(ga.g.order):
            if getrandbits(1):
                o1.genes[i] = p1.genes[i]
                o2.genes[i] = p2.genes[i]
            else:
                o1.genes[i] = p2.genes[i]
                o2.genes[i] = p1.genes[i]
        o1.calc_fitness()
        o2.calc_fitness()
        return o1, o2

    def mutate(self) -> None:
        self.genes[randint(0, self.ga.g.order - 1)] = randint(1, self.ga.bound)
        self.calc_fitness()

    def __eq__(self, __o: object) -> bool:
        return self.fitness == __o.fitness

    def __lt__(self, __o: object) -> bool:
        return self.fitness < __o.fitness

    def __str__(self) -> str:
        return f"{self.genes} fitness: {self.fitness}"
