from tkinter import Tk, font

from views.config import base_padding
from views.technique_choice import TechniqueChoice

root = Tk()
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="DejaVu Sans", size=11)
root.resizable(False, False)
root.title("OPTIM")
choose_technique = TechniqueChoice(root)
choose_technique.pack(padx=2 * base_padding, pady=2 * base_padding)
# conf_adj = ConfigurableAdjacencyMatrix(root, 15)
# conf_adj.pack(padx=base_padding, pady=base_padding)
# instance_choice = InstanceChoice(root)
# instance_choice.pack(padx=base_padding, pady=base_padding)
# technique_view = GenericTechniqueView(root)
# technique_view.pack(padx=base_padding, pady=base_padding)
root.mainloop()
