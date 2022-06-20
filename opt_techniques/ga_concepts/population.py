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
        self.total_nb_conflicts = 0
        self.total_nb_colors = 0
        self.total_fitness = 0

    @property
    def valid_solutions(self):
        solutions = []
        for ind in self.elite:
            if ind.nb_conflicts > 0:
                break
            solutions.append(ind)
        return solutions

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
        if len(self) == self.individuals.maxlen and len(self):
            discarded_ind = self.individuals.popleft()
            self.total_nb_conflicts -= discarded_ind.nb_conflicts
            self.total_nb_colors -= discarded_ind.nb_colors
            self.total_fitness -= discarded_ind.fitness
        self.individuals.append(individual)
        self.total_nb_conflicts += individual.nb_conflicts
        self.total_nb_colors += individual.nb_colors
        self.total_fitness += individual.fitness

    def insert_many(self, cl: Iterable[Individual]) -> None:
        for ind in cl:
            self.insert(ind)

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
