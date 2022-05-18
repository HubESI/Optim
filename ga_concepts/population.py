from collections import deque
from random import choice

from .individual import Individual


class Population:
    def __init__(self, ga):
        self.ga = ga
        self.individuals = deque(maxlen=ga.population_size)
        self.elite = None
        self.total_fitness = 0

    @staticmethod
    def create_rand(ga):
        rand_pop = Population(ga)
        for _ in range(ga.population_size):
            rand_pop.insert(Individual.create_rand(ga))
        return rand_pop

    def __len__(self):
        return len(self.individuals)

    def insert(self, individual):
        if len(self) == self.individuals.maxlen and len(self):
            self.total_fitness -= self.individuals.popleft().fitness
        self.individuals.append(individual)
        self.total_fitness += individual.fitness

    def parents_selection1(self):
        p1 = sorted([choice(self.individuals), choice(self.individuals)])[-1]
        p2 = sorted([choice(self.individuals), choice(self.individuals)])[-1]
        return p1, p2

    def parents_selection2(self):
        if self.elite is None:
            self.rank_individuals()
        return self.elite[0], self.elite[0]

    def rank_individuals(self):
        self.elite = sorted(self.individuals, reverse=True)

    def __str__(self):
        if self.elite is None:
            self.rank_individuals()
        return "\n".join(
            [f"total_fitness: {self.total_fitness}"]
            + [str(individ) for individ in self.elite]
        )
