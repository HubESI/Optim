from functools import total_ordering
from random import choice, randint


@total_ordering
class Individual:
    def __init__(self, ga):
        self.ga = ga
        self.genes = [None] * ga.g.order
        self.fitness = None

    @staticmethod
    def create_rand(ga):
        individ = Individual(ga)
        for gi in range(ga.g.order):
            individ.genes[gi] = randint(1, ga.g.order)
        individ.calc_fitness()
        return individ

    def calc_fitness(self):
        nb_conflicts = 0
        for vi in range(self.ga.g.order):
            for adji in range(self.ga.g.order):
                if self.genes[vi] == self.genes[adji] and self.ga.adj_mat[vi][adji]:
                    nb_conflicts += 1
        self.fitness = 1 / (
            self.ga.confilct_penalty * nb_conflicts + len(set(self.genes))
        )

    @staticmethod
    def crossover(p1, p2):
        assert p1.ga == p2.ga
        ga = p1.ga
        o = Individual(ga)
        cp = randint(0, ga.g.order - 1)
        o.genes = p1.genes[: cp + 1] + p2.genes[cp + 1 :]
        o.calc_fitness()
        return o

    def mutation1(self):
        all_colors = set(range(1, self.ga.g.order + 1))
        vertices_adj_colors = [None] * self.ga.g.order
        vertices_coloring_conflicts = [False] * self.ga.g.order
        for vi in range(self.ga.g.order):
            vertices_adj_colors[vi] = set()
            for adji in range(self.ga.g.order):
                vertices_adj_colors[vi].add(self.genes[adji])
                if self.genes[vi] == self.genes[adji] and self.ga.adj_mat[vi][adji]:
                    vertices_coloring_conflicts[vi] = True
        for vi in range(self.ga.g.order):
            if vertices_coloring_conflicts[vi]:
                valid_colors = all_colors - vertices_adj_colors[vi]
                self.genes[vi] = choice(tuple(valid_colors))
        self.calc_fitness()

    def mutation2(self):
        all_colors = range(1, self.ga.g.order + 1)
        for vi in range(self.ga.g.order):
            for adji in range(self.ga.g.order):
                if self.genes[vi] == self.genes[adji] and self.ga.adj_mat[vi][adji]:
                    self.genes[vi] = choice(all_colors)
        self.calc_fitness()

    def __eq__(self, __o):
        return self.fitness == __o.fitness

    def __lt__(self, __o):
        return self.fitness < __o.fitness

    def __str__(self):
        return f"{self.genes} fitness: {self.fitness}"
