from tkinter import ttk

from .config import base_padding, bold_font


class TechniqueChoice(ttk.Frame):
    button_width = 50

    def __init__(self, master):
        super().__init__(master)
        exact_techniques_label = ttk.Label(
            self, text="Méthodes exactes", font=bold_font
        )
        exact_techniques_label.pack(padx=base_padding, pady=base_padding)
        bnb = ttk.Button(self, text="Branch and Bound", width=self.button_width)
        bnb.pack(pady=base_padding, padx=base_padding)
        dp = ttk.Button(self, text="Programmation dynamique", width=self.button_width)
        dp.pack(pady=base_padding, padx=base_padding)
        separator1 = ttk.Separator(self, orient="horizontal")
        separator1.pack(padx=base_padding, pady=3 * base_padding, fill="x")
        heuristics_label = ttk.Label(self, text="Heuristiques", font=bold_font)
        heuristics_label.pack(padx=base_padding, pady=base_padding)
        bnb_h1 = ttk.Button(self, text="Heuristique B&B 1", width=self.button_width)
        bnb_h1.pack(pady=base_padding, padx=base_padding)
        bnb_h2 = ttk.Button(self, text="Heuristique B&B 2", width=self.button_width)
        bnb_h2.pack(pady=base_padding, padx=base_padding)
        welsh_powell = ttk.Button(self, text="Welsh Powell", width=self.button_width)
        welsh_powell.pack(pady=base_padding, padx=base_padding)
        separator2 = ttk.Separator(self, orient="horizontal")
        separator2.pack(padx=base_padding, pady=3 * base_padding, fill="x")
        metaheuristics_label = ttk.Label(self, text="Métaheuristiques", font=bold_font)
        metaheuristics_label.pack(padx=base_padding, pady=base_padding)
        rs = ttk.Button(self, text="Recuit simulé", width=self.button_width)
        rs.pack(pady=base_padding, padx=base_padding)
        ag = ttk.Button(self, text="Algorithme génétique", width=self.button_width)
        ag.pack(pady=base_padding, padx=base_padding)
        separator3 = ttk.Separator(self, orient="horizontal")
        separator3.pack(padx=base_padding, pady=3 * base_padding, fill="x")
        new_metaheuristics_label = ttk.Label(
            self, text="Nouvelle métaheuristique", font=bold_font
        )
        new_metaheuristics_label.pack(padx=base_padding, pady=base_padding)
        woa = ttk.Button(
            self,
            text="The Whale Optimization Algorithm",
            width=self.choice_button_width,
        )
        woa.pack(pady=base_padding, padx=base_padding)
