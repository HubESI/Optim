from tkinter import Toplevel, messagebox, ttk

from opt_techniques.branch_and_bound import BranchAndBound
from opt_techniques.coloring import Coloring

from .bnb_parameters import BnBParameters
from .config import BASE_PADDING, BOLD_FONT
from .generic_technique_view import GenericTechniqueView


class TechniqueChoice(ttk.Frame):
    button_width = 50

    def __init__(self, master):
        super().__init__(master)
        exact_techniques_label = ttk.Label(
            self, text="Méthodes exactes", font=BOLD_FONT
        )
        exact_techniques_label.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        self.bnb_window = self.TechniqueWindow(
            self, "Branch and Bound", BranchAndBound, BnBParameters
        )
        bnb = ttk.Button(
            self,
            text="Branch and Bound",
            width=self.button_width,
            command=self.bnb_window.open,
        )
        bnb.pack(pady=BASE_PADDING, padx=BASE_PADDING)
        dp = ttk.Button(self, text="Programmation dynamique", width=self.button_width)
        dp.pack(pady=BASE_PADDING, padx=BASE_PADDING)
        separator1 = ttk.Separator(self, orient="horizontal")
        separator1.pack(padx=BASE_PADDING, pady=3 * BASE_PADDING, fill="x")
        heuristics_label = ttk.Label(self, text="Heuristiques", font=BOLD_FONT)
        heuristics_label.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        bnb_heuristics = ttk.Button(
            self,
            text="Heuristiques basées sur Branch and Bound",
            width=self.button_width,
        )
        bnb_heuristics.pack(pady=BASE_PADDING, padx=BASE_PADDING)
        self.welsh_powell_window = self.TechniqueWindow(
            self, "Welsh and Powell", Coloring
        )
        welsh_powell = ttk.Button(
            self,
            text="Welsh and Powell",
            width=self.button_width,
            command=self.welsh_powell_window.open,
        )
        welsh_powell.pack(pady=BASE_PADDING, padx=BASE_PADDING)
        separator2 = ttk.Separator(self, orient="horizontal")
        separator2.pack(padx=BASE_PADDING, pady=3 * BASE_PADDING, fill="x")
        metaheuristics_label = ttk.Label(self, text="Métaheuristiques", font=BOLD_FONT)
        metaheuristics_label.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        rs = ttk.Button(self, text="Recuit simulé", width=self.button_width)
        rs.pack(pady=BASE_PADDING, padx=BASE_PADDING)
        ag = ttk.Button(self, text="Algorithme génétique", width=self.button_width)
        ag.pack(pady=BASE_PADDING, padx=BASE_PADDING)
        separator3 = ttk.Separator(self, orient="horizontal")
        separator3.pack(padx=BASE_PADDING, pady=3 * BASE_PADDING, fill="x")
        new_metaheuristics_label = ttk.Label(
            self, text="Nouvelle métaheuristique", font=BOLD_FONT
        )
        new_metaheuristics_label.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        woa = ttk.Button(
            self, text="The Whale Optimization Algorithm", width=self.button_width
        )
        woa.pack(padx=BASE_PADDING, pady=BASE_PADDING)

    class TechniqueWindow:
        def __init__(self, outer, name, coloring_class, parameters_class=None):
            self.outer = outer
            self.name = name
            self.coloring_class = coloring_class
            self.parameters_class = parameters_class

        def open(self):
            self.outer.open_generic_technique(
                self.name, self.coloring_class, self.parameters_class
            )

    def open_generic_technique(self, name, coloring_class, parameters_class):
        def on_closing():
            if messagebox.askokcancel("Confirmer", "Quitter ?", parent=window):
                window.destroy()

        window = Toplevel(self)
        window.protocol("WM_DELETE_WINDOW", on_closing)
        window.resizable(False, False)
        window.title(name)
        GenericTechniqueView(window, name, coloring_class, parameters_class).pack(
            padx=BASE_PADDING, pady=BASE_PADDING
        )
