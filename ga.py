from operator import ge
import random
import sys

from coloring import Coloring, Graph, timer
from ga_concepts.individual import Individual
from ga_concepts.population import Population

CONFLICT_PENALTY = 10


class GA(Coloring):
    def __init__(
        self,
        g: Graph,
        population_size: int = 80,
        rand_proportion: float = 0.85,
        crossover_rate: float = 0.9,
        mutation_rate: float = 0.01,
        stagnation_metric: int = 5,
    ):
        super().__init__(g)
        self.greedy_coloring()
        self.bound = self.solution[0]
        self.confilct_penalty = CONFLICT_PENALTY
        self.population_size = population_size
        self.rand_proportion = rand_proportion
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.stagnation_metric = stagnation_metric

    def crossover_probe(self):
        return random.random() < self.crossover_rate

    def mutation_probe(self):
        return random.random() < self.mutation_rate

    @timer
    def solve(self):
        gen_count = 0
        stag_count = self.stagnation_metric
        gen = Population.create_hybrid(self)
        while stag_count:
            new_gen = Population(self)
            while len(new_gen) < len(gen):
                p1, p2 = gen.tournament_selection()
                o1, o2 = (
                    Individual.uniform_crossover(p1, p2)
                    if self.crossover_probe()
                    else (p1, p2)
                )
                if self.mutation_probe():
                    o1.mutate()
                if self.mutation_probe():
                    o2.mutate()
                new_gen.insert(o1)
                new_gen.insert(o2)
            if new_gen.total_fitness <= gen.total_fitness:
                stag_count -= 1
            else:
                stag_count = self.stagnation_metric
            gen = new_gen
            gen_count += 1
        return gen_count, gen


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input_file> [<output_file>]")
    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = f"{input_file}.genetic_algorithm.sol"
    g = Graph.from_file(input_file)
    col = GA(g)
    info, t = col.solve()
    gen_count, last_gen = info
    col.to_file(
        output_file,
        graph_info=f"Coloring the graph defined in '{input_file}'",
        time_info=f"Genetic Algorithm in {t:0.6f} seconds and after {gen_count} generations",
        last_gen=f"Obtained Last generation average fitness={last_gen.total_fitness/col.population_size}",
        hyperparameters=f"population_size={col.population_size}, crossover_rate={col.crossover_rate}, mutation_rate={col.mutation_rate}",
    )