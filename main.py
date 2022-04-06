import sys

from graph import Graph
from heuristic import Heuristic

try:
    input_file = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <input_file> [<output_file>]")
try:
    output_file = sys.argv[2]
except IndexError:
    output_file = f"{input_file}.min_color_heuristic.sol"
g = Graph.from_file(input_file)
col = Heuristic(g, Heuristic.min_color_cost)
t = col.solve()[1]
col.to_file(
    output_file,
    graph_info=f"Coloring the graph defined in '{input_file}'",
    method_time_info=f"Minimal color heuristic in {t:0.6f} seconds",
)
