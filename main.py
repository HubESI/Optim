from tkinter import Tk, font

from views.config import base_padding
from views.technique_choice import TechniqueChoice
from views.adjacency_matrix import AdjacencyMatrix

root = Tk()
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="DejaVu Sans", size=11)
root.resizable(False, False)
root.title("OPTIM")
# choose_technique = TechniqueChoice(root)
# choose_technique.pack(padx=2 * base_padding, pady=2 * base_padding)
adj = AdjacencyMatrix(root, 5)
adj.grid(row=0, column=0, padx=5, pady=5)
root.mainloop()
