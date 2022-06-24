from tkinter import Tk, font, messagebox

from views.config import APP_NAME, BASE_PADDING
from views.technique_choice import TechniqueChoice


def on_closing():
    if messagebox.askokcancel("Confirmer", "Quitter ?"):
        root.destroy()


root = Tk()
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="DejaVu Sans", size=11)
root.resizable(False, False)
root.title(APP_NAME)
root.protocol("WM_DELETE_WINDOW", on_closing)
technique_choice = TechniqueChoice(root)
technique_choice.pack(padx=2 * BASE_PADDING, pady=2 * BASE_PADDING)
# conf_adj = ConfigurableAdjacencyMatrix(root, 15)
# conf_adj.pack(padx=BASE_PADDING, pady=BASE_PADDING)
# instance_choice = InstanceChoice(root)
# instance_choice.pack(padx=BASE_PADDING, pady=BASE_PADDING)
# technique_view = GenericTechniqueView(root)
# technique_view.pack(padx=BASE_PADDING, pady=BASE_PADDING)
root.mainloop()
