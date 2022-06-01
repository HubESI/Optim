from collections import deque
from random import choice, choices
from typing import Iterable, List, Tuple

from .individual import Individual


class Population:
    def __init__(self, ga) -> None:
        self.ga = ga
        self.individuals = deque(maxlen=ga.population_size)
        self.weights = None
        self.elite = None
        self.total_fitness = 0

    @classmethod
    def create_rand(cls, ga) -> "Population":
        rand_pop = cls(ga)
        for _ in range(ga.population_size):
            rand_pop.insert(Individual.create_rand(ga))
        return rand_pop

    @staticmethod
    def tournament(ind1: Individual, ind2: Individual) -> Individual:
        if ind1 >= ind2:
            return ind1
        return ind2

    def __len__(self) -> int:
        return len(self.individuals)

    def insert(self, individual: Individual) -> None:
        if len(self) == self.individuals.maxlen and len(self):
            self.total_fitness -= self.individuals.popleft().fitness
        self.individuals.append(individual)
        self.total_fitness += individual.fitness

    def insert_many(self, cl: Iterable[Individual]) -> None:
        for ind in cl:
            self.insert(ind)

    def insert_solution(self):
        self.insert(Individual.create(self.ga, self.ga.solution[1]))

    def setup_weights(self) -> None:
        self.weights = [ind.fitness / self.total_fitness for ind in self.individuals]

    def rank_individuals(self) -> None:
        self.elite = sorted(self.individuals, reverse=True)

    def tournament_selection(self) -> Tuple[Individual, Individual]:
        p1 = self.tournament(choice(self.individuals), choice(self.individuals))
        p2 = self.tournament(choice(self.individuals), choice(self.individuals))
        return p1, p2

    def roulette_selection(self) -> Tuple[Individual, Individual]:
        p1, p2 = choices(self.individuals, weights=self.weights, k=2)
        return p1, p2

    def elitism_selection(self, proportion: float) -> List[Individual]:
        return self.elite[: int(proportion * len(self.individuals))]

    def __str__(self) -> str:
        if self.elite is None:
            self.rank_individuals()
        return "\n".join(
            [f"total_fitness: {self.total_fitness}"]
            + [str(individ) for individ in self.elite]
        )
