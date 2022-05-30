from collections import deque
from random import choice, choices

from .individual import Individual


class Population:
    def __init__(self, ga):
        self.ga = ga
        self.individuals = deque(maxlen=ga.population_size)
        self.weights = None
        self.elite = None
        self.total_fitness = 0

    @staticmethod
    def create_rand(ga):
        rand_pop = Population(ga)
        for _ in range(ga.population_size):
            rand_pop.insert(Individual.create_rand(ga))
        return rand_pop

    @staticmethod
    def tournament(ind1, ind2):
        if ind1 >= ind2:
            return ind1
        return ind2

    def __len__(self):
        return len(self.individuals)

    def insert(self, individual):
        if len(self) == self.individuals.maxlen and len(self):
            self.total_fitness -= self.individuals.popleft().fitness
        self.individuals.append(individual)
        self.total_fitness += individual.fitness

    def insert_many(self, cl):
        for ind in cl:
            self.insert(ind)

    def setup_weights(self):
        self.weights = [ind.fitness / self.total_fitness for ind in self.individuals]

    def rank_individuals(self):
        self.elite = sorted(self.individuals, reverse=True)

    def tournament_selection(self):
        p1 = self.tournament(choice(self.individuals), choice(self.individuals))
        p2 = self.tournament(choice(self.individuals), choice(self.individuals))
        return p1, p2

    def roulette_selection(self):
        p1, p2 = choices(self.individuals, weights=self.weights, k=2)
        return p1, p2

    def elitism_selection(self, proportion):
        return self.elite[: int(proportion * len(self.individuals))]

    def __str__(self):
        if self.elite is None:
            self.rank_individuals()
        return "\n".join(
            [f"total_fitness: {self.total_fitness}"]
            + [str(individ) for individ in self.elite]
        )
