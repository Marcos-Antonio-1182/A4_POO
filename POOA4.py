from tkinter import *


class Sys(Tk):
    def __init__(self):
        super().__init__()

        # title, icon, size
        self.title("SISTEMA_POO_QUENTINHAS")
        self.iconbitmap('A4_POO/logo.ico')
        self.geometry("720x480")

        # widgets
        self.my_label = Label(self, text="CARDÁPIO", font=("Times New Roman", 20))
        self.my_label.pack(pady=(20, 0))

        # cost adder
        self.cost_label = Label(self, text="Custo: R$ 0.00", font=("Times New Roman", 20))
        self.cost_label.pack(pady=(20, 0))

        # Contador de quentinhas
        self.quantidades = {
            "quent1": 0,
            "quent2": 0,
            "quent3": 0
        }


class WidgQuent(Frame):
    def __init__(self, parent, label_text, button_text, button_name, remove_button_name):
        super().__init__(master=parent)

        # setup grid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1, uniform='z')

        # widgets
        Label(self, text=label_text, font=('Times New Roman', 16)).grid(row=0, column=0, sticky="nsew")
        Button(self, text=button_text, command=lambda: self.add(button_name)).grid(row=0, column=1, sticky="w", padx=10, ipady=10)
        Button(self, text=remove_button_name, command=lambda: self.remove(button_name)).grid(row=0, column=2, sticky="w", padx=10, ipady=10)

        # Label para mostrar quantidade
        self.count_label = Label(self, text="x 0", font=('Times New Roman', 12))
        self.count_label.grid(row=0, column=3, sticky="nsew")

        self.pack(pady=10)

    def add(self, name):
        prices = {
            "quent1": 18.00,
            "quent2": 20.00,
            "quent3": 22.00,
        }
        # Atualizar o custo total
        if not hasattr(self.master, 'total_cost'):
            self.master.total_cost = 0
        self.master.total_cost += prices[name]
        self.master.cost_label.config(text=f"Custo: R$ {self.master.total_cost:.2f}")

        # Atualizar a quantidade
        self.master.quantidades[name] += 1
        self.count_label.config(text=f"x {self.master.quantidades[name]}")

    def remove(self, name):
        prices = {
            "quent1": 18.00,
            "quent2": 20.00,
            "quent3": 22.00,
        }
        # Atualizar o custo total
        if not hasattr(self.master, 'total_cost'):
            self.master.total_cost = 0
        self.master.total_cost = max(0, self.master.total_cost - prices[name])
        self.master.cost_label.config(text=f"Custo: R$ {self.master.total_cost:.2f}")

        # Atualizar a quantidade
        if self.master.quantidades[name] > 0:
            self.master.quantidades[name] -= 1
        self.count_label.config(text=f"x {self.master.quantidades[name]}")


# Inicialização do sistema
sys = Sys()
WidgQuent(sys, "R$18 Quentinha de Frango", "Adicionar", "quent1", "Remover").pack()
WidgQuent(sys, "R$20 Quentinha de Carne", "Adicionar", "quent2", "Remover").pack()
WidgQuent(sys, "R$22 Quentinha de Peixe", "Adicionar", "quent3", "Remover").pack()

sys.mainloop()
