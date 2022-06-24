from tkinter import ttk

from .config import BASE_PADDING, BOLD_FONT


class TechniqueChoice(ttk.Frame):
    button_width = 50

    def __init__(self, master):
        super().__init__(master)
        exact_techniques_label = ttk.Label(
            self, text="Méthodes exactes", font=BOLD_FONT
        )
        exact_techniques_label.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        bnb = ttk.Button(self, text="Branch and Bound", width=self.button_width)
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
        welsh_powell = ttk.Button(
            self, text="Welsh and Powell", width=self.button_width
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
            self,
            text="The Whale Optimization Algorithm",
            width=self.button_width,
        )
        woa.pack(padx=BASE_PADDING, pady=BASE_PADDING)
