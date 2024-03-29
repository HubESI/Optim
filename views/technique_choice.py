from tkinter import Toplevel, messagebox, ttk

from opt_techniques.branch_and_bound import BranchAndBound
from opt_techniques.coloring import Coloring
from opt_techniques.ga import GA
from opt_techniques.heuristic import Heuristic
from opt_techniques.vdwoa import VDWOA

from .bnb_heuristics_parameters import BnBHeuristicsParameters
from .bnb_parameters import BnBParameters
from .config import BASE_PADDING, BOLD_FONT
from .ga_parameters import GAParameters
from .ga_solution import GASolution
from .generic_technique_view import GenericTechniqueView
from .solution_frame import SolutionFrame
from .vdwa_parameters import VDWOAParameters
from .vdwoa_solution import VDWOASolution


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
        self.bnb_heuristics_window = self.TechniqueWindow(
            self, "Heuristiques BnB", Heuristic, BnBHeuristicsParameters
        )
        bnb_heuristics = ttk.Button(
            self,
            text="Heuristiques basées sur Branch and Bound",
            width=self.button_width,
            command=self.bnb_heuristics_window.open,
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
        ga_window = self.TechniqueWindow(
            self, "Algorithme Génétique", GA, GAParameters, solution_class=GASolution
        )
        ga = ttk.Button(
            self,
            text="Algorithme génétique",
            width=self.button_width,
            command=ga_window.open,
        )
        ga.pack(pady=BASE_PADDING, padx=BASE_PADDING)
        separator3 = ttk.Separator(self, orient="horizontal")
        separator3.pack(padx=BASE_PADDING, pady=3 * BASE_PADDING, fill="x")
        new_metaheuristics_label = ttk.Label(
            self, text="Nouvelle métaheuristique", font=BOLD_FONT
        )
        new_metaheuristics_label.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        ga_window = self.TechniqueWindow(
            self, "VDWOA", VDWOA, VDWOAParameters, solution_class=VDWOASolution
        )
        woa = ttk.Button(
            self, text="VDWOA", width=self.button_width, command=ga_window.open
        )
        woa.pack(padx=BASE_PADDING, pady=BASE_PADDING)

    class TechniqueWindow:
        def __init__(
            self,
            outer,
            name,
            coloring_class,
            parameters_class=None,
            attrs_needed=["solution"],
            solution_class=SolutionFrame,
        ):
            self.outer = outer
            self.name = name
            self.coloring_class = coloring_class
            self.parameters_class = parameters_class
            self.attrs_needed = attrs_needed
            self.solution_class = solution_class

        def open(self):
            self.outer.open_generic_technique(
                self.name,
                self.coloring_class,
                self.parameters_class,
                self.attrs_needed,
                self.solution_class,
            )

    def open_generic_technique(
        self, name, coloring_class, parameters_class, attrs_needed, solution_class
    ):
        def on_closing():
            if messagebox.askokcancel("Confirmer", "Quitter ?", parent=window):
                window.destroy()

        window = Toplevel(self)
        window.protocol("WM_DELETE_WINDOW", on_closing)
        window.resizable(False, False)
        window.title(name)
        GenericTechniqueView(
            window, name, coloring_class, parameters_class, attrs_needed, solution_class
        ).pack(padx=BASE_PADDING, pady=BASE_PADDING)
