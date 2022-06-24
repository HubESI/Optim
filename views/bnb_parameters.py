from tkinter import ttk, BooleanVar
from .config import BASE_PADDING


class BnBParameters(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.heuristic_init = BooleanVar(self, True)
        self.heuristic_init_chkbtn = ttk.Checkbutton(
            self,
            text="Initialiser la meilleure solution avec\nune heuristique",
            variable=self.heuristic_init,
            onvalue=True,
            offvalue=False,
        )
        self.heuristic_init_chkbtn.pack(padx=BASE_PADDING, pady=BASE_PADDING)

    def get_kwargs(self):
        return {"heuristic_init": self.heuristic_init.get()}

    def disable(self):
        self.heuristic_init_chkbtn.config(state="disabled")

    def enable(self):
        self.heuristic_init_chkbtn.config(state="normal")