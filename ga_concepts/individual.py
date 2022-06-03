from copy import copy
from functools import total_ordering
from random import getrandbits, randint
from typing import List, Tuple


@total_ordering
class Individual:
    def __init__(self, ga) -> None:
        self.ga = ga
        self.genes = [None] * ga.g.order
        self.fitness = None

    @classmethod
    def create_rand(cls, ga) -> "Individual":
        ind = cls(ga)
        for gi in range(ga.g.order):
            ind.genes[gi] = randint(1, ga.bound)
        ind.calc_fitness()
        return ind

    @classmethod
    def create(cls, ga, genes: List[int]) -> "Individual":
        ind = cls(ga)
        ind.genes = genes
        ind.calc_fitness()
        return ind

    def calc_fitness(self) -> None:
        nb_conflicts = 0
        used_colors = set()
        for vi in range(self.ga.g.order):
            used_colors.add(self.genes[vi])
            for adji in range(vi + 1, self.ga.g.order):
                if self.genes[vi] == self.genes[adji] and self.ga.adj_mat[vi][adji]:
                    nb_conflicts += 1
        nb_colors = len(used_colors)
        self.fitness = 1 / (self.ga.confilct_penalty * nb_conflicts + nb_colors)
        if nb_conflicts == 0 and nb_colors < self.ga.solution[0]:
            self.ga.solution = nb_colors, copy(self.genes)

    @classmethod
    def uniform_crossover(
        cls, p1: "Individual", p2: "Individual"
    ) -> Tuple["Individual", "Individual"]:
        assert p1.ga == p2.ga
        ga = p1.ga
        o1, o2 = cls(ga), cls(ga)
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

    def clone(self) -> "Individual":
        clone_ind = Individual(self.ga)
        clone_ind.genes = copy(self.genes)
        clone_ind.fitness = self.fitness
        return clone_ind

    def __eq__(self, __o: object) -> bool:
        return self.fitness == __o.fitness

    def __lt__(self, __o: object) -> bool:
        return self.fitness < __o.fitness

    def __str__(self) -> str:
        return f"{self.genes} fitness: {self.fitness}"
