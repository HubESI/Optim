from tkinter import CENTER, END, ttk


class GAParameters(ttk.Frame):
    size_error_message = "Veuillez entrer une taille valide"
    rate_error_message = "Veuillez entrer une probabilité"

    class LabeledEntry(ttk.Frame):
        entry_width = 5
        label_width = 22

        def __init__(
            self,
            master,
            label,
            default_value="",
            transformer=lambda v: v,
            validator=lambda v: True,
            on_valid=lambda: None,
            on_unvalid=lambda: None,
        ):
            super().__init__(master)
            self.label = ttk.Label(self, width=self.label_width, text=label)
            self.transformer = transformer
            self.label.grid(row=0, column=0)

            def validator_wrapper(v):
                if validator(v):
                    on_valid()
                    return True
                on_unvalid()
                return False

            vcmd = (self.register(validator_wrapper), "%P")
            self.input = ttk.Entry(self, justify=CENTER, width=self.entry_width)
            self.input.insert(0, default_value)
            self.input.config(
                validate="key",
                validatecommand=vcmd,
            )
            self.input.grid(row=0, column=1)

        def get(self):
            return self.transformer(self.input.get())

        def disable(self):
            self.input.config(state="disabled")

        def enable(self):
            self.input.config(state="normal")

    def __init__(self, master):
        super().__init__(master)
        self.parameters_names = [
            "population_size",
            "rand_proportion",
            "crossover_rate",
            "mutation_rate",
            "max_generations",
        ]
        on_valid_size = lambda: self.clear_error()
        on_unvalid_size = lambda: self.show_error(
            "Veuillez entrer un nombre entier non nul"
        )
        on_valid_rate = lambda: self.clear_error()
        on_unvalid_rate = lambda: self.show_error("Veuillez entrer une probabilité")
        self.population_size = self.LabeledEntry(
            self,
            "Taille de la population",
            "40",
            self.size_transformer,
            self.is_size,
            on_valid_size,
            on_unvalid_size,
        )
        self.population_size.pack()
        self.rand_proportion = self.LabeledEntry(
            self,
            "Proportion aléatoire",
            "0.85",
            self.rate_transformer,
            self.is_rate,
            on_valid_rate,
            on_unvalid_rate,
        )
        self.rand_proportion.pack()
        self.crossover_rate = self.LabeledEntry(
            self,
            "Probabilité de croisement",
            "0.9",
            self.rate_transformer,
            self.is_rate,
            on_valid_rate,
            on_unvalid_rate,
        )
        self.crossover_rate.pack()
        self.mutation_rate = self.LabeledEntry(
            self,
            "Probabilité de mutation",
            "0.01",
            self.rate_transformer,
            self.is_rate,
            on_valid_rate,
            on_unvalid_rate,
        )
        self.mutation_rate.pack()
        self.max_generations = self.LabeledEntry(
            self,
            "Max générations",
            "60",
            self.size_transformer,
            self.is_size,
            on_valid_size,
            on_unvalid_size,
        )
        self.max_generations.pack()
        self.info_label = ttk.Label(self)
        self.info_label.pack()

    def show_error(self, message):
        self.info_label.config(foreground="red")
        self.info_label.config(text=message)

    def clear_error(self):
        self.info_label.config(text="")

    def get_kwargs(self):
        return {
            parameter: getattr(self, parameter).get()
            for parameter in self.parameters_names
        }

    def parameters_names_aliases(self):
        return {
            "population_size": "t_pop",
            "rand_proportion": "prop_aléa",
            "crossover_rate": "p_croisement",
            "mutation_rate": "p_mutation",
            "max_generations": "max_gen",
        }

    def parameters_values_aliases(self):
        return None

    def disable(self):
        for parameter in self.parameters_names:
            getattr(self, parameter).disable()

    def enable(self):
        for parameter in self.parameters_names:
            getattr(self, parameter).enable()

    @staticmethod
    def rate_transformer(v):
        return float(v) if v else 0

    @staticmethod
    def size_transformer(v):
        return int(v) if v else 0

    @staticmethod
    def is_rate(v):
        if v == "":
            return True
        try:
            rate = float(v)
            assert rate >= 0 and rate <= 1
        except (ValueError, AssertionError):
            return False
        return True

    @staticmethod
    def is_size(v):
        if v == "":
            return True
        try:
            assert int(v) > 0
        except (ValueError, AssertionError):
            return False
        return True
