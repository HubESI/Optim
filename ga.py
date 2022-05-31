import random
import sys

from coloring import Coloring, Graph, timer
from ga_concepts.individual import Individual
from ga_concepts.population import Population


class GA(Coloring):
    def __init__(
        self,
        g: Graph,
        bound: int = None,
        confilct_penalty: int = 10,
        population_size: int = 100,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.1,
        max_generations: int = 100,
    ):
        super().__init__(g)
        self.greedy_coloring()
        self.bound = bound or self.solution[0]
        self.confilct_penalty = confilct_penalty
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

    def crossover_probe(self):
        return random.random() < self.crossover_rate

    def mutation_probe(self):
        return random.random() < self.mutation_rate

    @timer
    def solve(self):
        gen_count = 0
        gen = Population.create_rand(self)
        while gen_count < self.max_generations:
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
    gen_info, t = col.solve()
    gen_count, gen = gen_info
    col.to_file(
        output_file,
        graph_info=f"Coloring the graph defined in '{input_file}'",
        time_info=f"Genetic Algorithm in {t:0.6f} seconds and after {gen_count} generations",
        operators="tournament_selection, uniform_crossover",
        hyperparameters1=f"confilct_penalty={col.confilct_penalty}, population_size={col.population_size}",
        hyperparameters2=f"crossover_rate={col.crossover_rate}, mutation_rate={col.mutation_rate}",
    )
