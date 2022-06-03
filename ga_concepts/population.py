from collections import deque
from random import choice
from typing import Iterable, Tuple

from .individual import Individual


class Population:
    def __init__(self, ga) -> None:
        self.ga = ga
        self.individuals = deque(maxlen=ga.population_size)

    @classmethod
    def create_rand(cls, ga) -> "Population":
        rand_pop = cls(ga)
        for _ in range(ga.population_size):
            rand_pop.insert(Individual.create_rand(ga))
        return rand_pop

    @classmethod
    def create_hybrid(cls, ga) -> "Population":
        hybrid_pop = cls(ga)
        rand_size = int(ga.rand_proportion * ga.population_size)
        for _ in range(rand_size):
            hybrid_pop.insert(Individual.create_rand(ga))
        elite_ind = Individual.create(ga, ga.solution[1])
        ind = elite_ind
        for _ in range(ga.population_size - rand_size):
            hybrid_pop.insert(ind)
            ind = ind.clone()
            ind.mutate()
        return hybrid_pop

    @staticmethod
    def tournament(ind1: Individual, ind2: Individual) -> Individual:
        if ind1 >= ind2:
            return ind1
        return ind2

    def __len__(self) -> int:
        return len(self.individuals)

    def insert(self, individual: Individual) -> None:
        self.individuals.append(individual)

    def insert_many(self, cl: Iterable[Individual]) -> None:
        for ind in cl:
            self.insert(ind)

    def tournament_selection(self) -> Tuple[Individual, Individual]:
        p1 = self.tournament(choice(self.individuals), choice(self.individuals))
        p2 = self.tournament(choice(self.individuals), choice(self.individuals))
        return p1, p2

    def __str__(self) -> str:
        return "\n".join(
            [f"total_fitness: {self.total_fitness}"]
            + [str(individ) for individ in self.elite]
        )
