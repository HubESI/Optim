from tkinter import BooleanVar, ttk

from .config import BASE_PADDING
from opt_techniques.heuristic import Heuristic


class BnBHeuristicsParameters(ttk.Frame):
    parameters_width = 35

    def __init__(self, master):
        super().__init__(master)
        self.file_instance = None
        self.cost_function_choice = BooleanVar(self, False)
        parameter_label = ttk.Label(self, text="Fonction de coût")
        parameter_label.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        self.min_color_choice = ttk.Radiobutton(
            self,
            text="min_color_cost",
            variable=self.cost_function_choice,
            value=False,
            width=self.parameters_width,
        )
        self.min_color_choice.pack(padx=BASE_PADDING, pady=BASE_PADDING)
        self.min_nb_colors_choice = ttk.Radiobutton(
            self,
            text="min_nb_colors_cost",
            variable=self.cost_function_choice,
            value=True,
            width=self.parameters_width,
        )
        self.min_nb_colors_choice.pack(padx=BASE_PADDING, pady=BASE_PADDING)

    def get_kwargs(self):
        cost_function = (
            Heuristic.min_nb_colors_cost
            if self.cost_function_choice.get()
            else Heuristic.min_color_cost
        )
        return {"node_cost_calculator": cost_function}

    def parameters_names_aliases(self):
        return {"node_cost_calculator": "fonction_coût"}

    def parameters_values_aliases(self):
        cost_function_alias = (
            "min_nb_colors_cost"
            if self.cost_function_choice.get()
            else "min_color_cost"
        )

        return {"node_cost_calculator": cost_function_alias}

    def disable(self):
        self.min_color_choice.config(state="disabled")
        self.min_nb_colors_choice.config(state="disabled")

    def enable(self):
        self.min_color_choice.config(state="normal")
        self.min_nb_colors_choice.config(state="normal")
