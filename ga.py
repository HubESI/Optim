import random
import sys

from coloring import Coloring, Graph, timer
from ga_concepts.individual import Individual, SolutionFound
from ga_concepts.population import Population


class NoSolutionFound(Exception):
    def __init__(self, ga, gen, *args):
        super().__init__(args)
        self.ga = ga
        self.gen = gen


class GA(Coloring):
    def __init__(
        self,
        g,
        confilct_penalty=10,
        population_size=100,
        crossover_rate=0.8,
        mutation_rate=0.1,
        max_iter=100,
    ):
        super().__init__(g)
        self.confilct_penalty = confilct_penalty
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_iter = max_iter

    def crossover_probe(self):
        return random.random() < self.crossover_rate

    def mutation_probe(self):
        return random.random() < self.mutation_rate

    @timer
    def solve(self):
        gen_count = 0
        gen = Population.create_rand(self)
        while gen_count < self.max_iter:
            gen.rank_individuals()
            new_gen = Population(self)
            while len(new_gen) < len(gen):
                operators1 = True
                if operators1:
                    p1, p2 = gen.parents_selection1()
                else:
                    p1, p2 = gen.parents_selection2()
                if self.crossover_probe():
                    o = Individual.crossover(p1, p2)
                else:
                    o = sorted([p1, p2])[-1]
                if self.mutation_probe():
                    if operators1:
                        o.mutation1()
                    else:
                        o.mutation2()
                new_gen.insert(o)
            gen = new_gen
            gen_count += 1
        gen.rank_individuals()
        best = gen.elite[0]
        self.solution = len(set(best.genes)), best.genes
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
    k = None
    exec_count = 0
    while True:
        exec_count += 1
        gen_info, t = col.solve()
        gen_count, gen = gen_info
        if k is None or col.solution[0] < k:
            k = col.solution[0]
            col.to_file(
                output_file,
                graph_info=f"Coloring the graph defined in '{input_file}'",
                method_time_info=f"Genetic Algorithm in {t:0.6f} seconds and after {gen_count} generation",
                method_hyperparameters=f"population_size={col.population_size}, crossover_rate={col.crossover_rate}, mutation_rate={col.mutation_rate}",
                repeat=f"best result after {exec_count} execution",
            )
