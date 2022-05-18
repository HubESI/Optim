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
        population_size=50,
        crossover_rate=1,
        mutation_rate=0.7,
        max_iter=20000,
    ):
        super().__init__(g)
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
        try:
            gen = Population.create_rand(self)
            while gen_count < self.max_iter:
                gen.rank_individuals()
                new_gen = Population(self)
                while len(new_gen) < len(gen):
                    operators1 = gen.elite[0].fitness < 0.25
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
            raise NoSolutionFound(self, gen)
        except SolutionFound as e:
            self.solution = len(set(e.solution.genes)), e.solution.genes
            return gen_count


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
        try:
            gen_count, t = col.solve()
            if k is None or col.solution[0] < k:
                k = col.solution[0]
                col.to_file(
                    output_file,
                    graph_info=f"Coloring the graph defined in '{input_file}'",
                    method_time_info=f"Genetic Algorithm in {t:0.6f} seconds and after {gen_count} generation",
                    method_hyperparameters=f"population_size={col.population_size}, crossover_rate={col.crossover_rate}, mutation_rate={col.mutation_rate}, max_iter={col.max_iter}",
                    repeat=f"best result after {exec_count} execution",
                )
        except NoSolutionFound as e:
            print(f"No solution was found after {e.ga.max_iter} iterations")
            print(e.gen)
            print()
        exec_count += 1
