import json
from tkinter import *
from tkinter import messagebox
import time


class Sys(Tk):
    def __init__(self):
        super().__init__()

        # Configurações da janela principal
        self.title("SISTEMA_POO_QUENTINHAS")
        self.iconbitmap('A4_POO/logo.ico')
        self.geometry("720x480")
        self.center_window(720, 480)

        # Inicializando o custo total
        self.total_cost = 0
        self.payment_type = None
        self.change_value = 0

        # Inicializando a lista de quentinhas
        self.quantidades = {
            "quent1": 0,
            "quent2": 0,
            "quent3": 0
        }

        # Carrega os dados dos usuários
        self.users = self.load_users()
        self.current_user = None

        # Bloquear a interface até o login
        self.withdraw()  # Esconde a janela principal
        self.show_login_popup()

        # Botão de finalização do pedido
        self.finalize_button = Button(self, text="Finalizar Pedido", font=("Times New Roman", 18), command=self.finalize_order)
        self.finalize_button.pack(pady=20)

        # Label de custo
        self.cost_label = Label(self, text=f"Custo: R$ {self.total_cost:.2f}", font=("Times New Roman", 20))
        self.cost_label.pack(pady=(20, 0))

        # Widgets do cardápio
        self.cardapio_frame = Frame(self)
        self.cardapio_frame.pack(pady=10)

        WidgQuent(self.cardapio_frame, "R$18 Quentinha de Frango", "Adicionar", "quent1", "Remover", self).pack()
        WidgQuent(self.cardapio_frame, "R$20 Quentinha de Carne", "Adicionar", "quent2", "Remover", self).pack()
        WidgQuent(self.cardapio_frame, "R$22 Quentinha de Peixe", "Adicionar", "quent3", "Remover", self).pack()

    def center_window(self, width, height):
        """Centraliza uma janela na tela."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_login_popup(self):
        """Exibe o popup de login."""
        login_popup = LoginPopup(self)
        login_popup.grab_set()  # Bloqueia interação com outras janelas

    def load_users(self):
        """Carrega os usuários de um arquivo JSON."""
        try:
            with open("users.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self):
        """Salva os usuários em um arquivo JSON."""
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def finalize_order(self):
        """Inicia o processo de status do pedido após escolher o pagamento."""
        delivery_popup = DeliveryPopup(self)
        delivery_popup.grab_set()

    def start_order_status(self):
        """Redireciona para a tela de status do pedido e inicia a contagem de status."""
        status_screen = StatusScreen(self)
        status_screen.grab_set()

    def reset_order(self):
        """Reseta os dados do pedido (limpa custo e quantidades)."""
        self.total_cost = 0
        self.payment_type = None
        self.change_value = 0
        self.quantidades = {
            "quent1": 0,
            "quent2": 0,
            "quent3": 0
        }
        self.cost_label.config(text=f"Custo: R$ {self.total_cost:.2f}")
        for widget in self.cardapio_frame.winfo_children():
            if isinstance(widget, WidgQuent):
                widget.update_quantity()

    def start_payment(self, delivery_type):
        """Redireciona para a tela de escolha de pagamento."""
        if delivery_type == "Entrega":
            self.total_cost += 5  # Adiciona o custo de entrega
        self.cost_label.config(text=f"Custo: R$ {self.total_cost:.2f}")

        payment_popup = PaymentPopup(self)
        payment_popup.grab_set()


class LoginPopup(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Login")
        self.geometry("300x200")
        self.center_window(300, 200)

        self.master = master

        Label(self, text="Usuário:").pack(pady=5)
        self.username_entry = Entry(self)
        self.username_entry.pack()

        Label(self, text="Senha:").pack(pady=5)
        self.password_entry = Entry(self, show="*")
        self.password_entry.pack()

        Button(self, text="Login", command=self.try_login).pack(pady=10)
        Button(self, text="Cadastrar", command=self.go_to_register).pack()

    def center_window(self, width, height):
        """Centraliza o popup na tela."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def try_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.master.users and self.master.users[username] == password:
            self.master.current_user = username
            self.destroy()  # Fecha o popup
            self.master.deiconify()  # Mostra a janela principal
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos!")

    def go_to_register(self):
        self.destroy()
        RegisterPopup(self.master)


class RegisterPopup(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro")
        self.geometry("300x250")
        self.center_window(300, 250)

        self.master = master

        Label(self, text="Novo Usuário:").pack(pady=5)
        self.username_entry = Entry(self)
        self.username_entry.pack()

        Label(self, text="Nova Senha:").pack(pady=5)
        self.password_entry = Entry(self, show="*")
        self.password_entry.pack()

        Label(self, text="Confirme a Senha:").pack(pady=5)
        self.confirm_entry = Entry(self, show="*")
        self.confirm_entry.pack()

        Button(self, text="Cadastrar", command=self.register_user).pack(pady=10)
        Button(self, text="Cancelar", command=self.cancel_register).pack()

    def center_window(self, width, height):
        """Centraliza o popup na tela."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()

        if username in self.master.users:
            messagebox.showerror("Erro de Cadastro", "Usuário já existe!")
        elif password != confirm_password:
            messagebox.showerror("Erro de Cadastro", "As senhas não conferem!")
        elif not username or not password:
            messagebox.showerror("Erro de Cadastro", "Campos não podem estar vazios!")
        else:
            self.master.users[username] = password
            self.master.save_users()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.destroy()
            self.master.show_login_popup()

    def cancel_register(self):
        self.destroy()
        self.master.show_login_popup()


class DeliveryPopup(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Escolher Tipo de Entrega")
        self.geometry("300x150")
        self.center_window(300, 150)

        self.master = master

        Label(self, text="Escolha o tipo de entrega:").pack(pady=10)
        Button(self, text="Retirar no local", command=lambda: [self.master.start_payment("Retirada"), self.destroy()]).pack(pady=5)
        Button(self, text="Entrega (R$ 5,00)", command=lambda: [self.master.start_payment("Entrega"), self.destroy()]).pack(pady=5)

    def center_window(self, width, height):
        """Centraliza o popup na tela."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


class PaymentPopup(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Escolha de Pagamento")
        self.geometry("400x300")
        self.center_window(400, 400)

        self.master = master

        # Display the total cost
        self.cost_label = Label(self, text=f"Custo: R$ {self.master.total_cost:.2f}", font=("Times New Roman", 20))
        self.cost_label.pack(pady=(20, 0))  # Add padding to the label

        Label(self, text="Escolha o tipo de pagamento:").pack(pady=10)

        self.payment_type_var = StringVar()

        Radiobutton(self, text="Cartão", variable=self.payment_type_var, value="Cartão").pack(pady=5)
        Radiobutton(self, text="Dinheiro", variable=self.payment_type_var, value="Dinheiro").pack(pady=5)

        self.confirm_button = Button(self, text="Confirmar", command=self.confirm_payment)
        self.confirm_button.pack(pady=10)

    def center_window(self, width, height):
        """Centraliza o popup na tela."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def confirm_payment(self):
        """Confirma o tipo de pagamento e, se for dinheiro, pergunta pelo troco."""
        self.master.payment_type = self.payment_type_var.get()
        if self.master.payment_type == "Dinheiro":
            self.ask_for_change()
        else:
            self.master.start_order_status()  

    def center_window(self, width, height):
        """Centraliza o popup na tela."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def confirm_payment(self):
        """Confirma o tipo de pagamento e, se for dinheiro, pergunta pelo troco."""
        self.master.payment_type = self.payment_type_var.get()
        if self.master.payment_type == "Dinheiro":
            self.ask_for_change()
        else:
            self.master.start_order_status()  # Redireciona para o status do pedido

    def ask_for_change(self):
        """Solicita o valor para o troco."""
        self.change_label = Label(self, text="Qual o valor em dinheiro?")
        self.change_label.pack(pady=10)

        self.change_entry = Entry(self)
        self.change_entry.pack()

        self.confirm_change_button = Button(self, text="Confirmar", command=self.calculate_change)
        self.confirm_change_button.pack(pady=10)

    def calculate_change(self):
        """Calcula o troco e redireciona para a tela de status."""
        try:
            money_given = float(self.change_entry.get())
            if money_given < self.master.total_cost:
                messagebox.showerror("Erro", "Valor insuficiente!")
                return
            self.master.change_value = money_given - self.master.total_cost
            messagebox.showinfo("Troco", f"Troco: R$ {self.master.change_value:.2f}")
            self.master.start_order_status()  # Redireciona para o status do pedido
            self.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor válido.")


class StatusScreen(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Status do Pedido")
        self.geometry("300x200")
        self.center_window(300, 200)

        self.master = master

        self.status_label = Label(self, text="Registrado", font=("Times New Roman", 18))
        self.status_label.pack(pady=20)

        self.counter = 0
        self.update_status()

    def update_status(self):
        """Atualiza o status do pedido a cada 2 segundos."""
        status_list = ["Registrado", "Em Preparo", "Pronto para Entrega", "Entregue", ""]
        self.status_label.config(text=status_list[self.counter])
        self.counter += 1
        if self.counter < len(status_list):
            self.after(2000, self.update_status)  # Chama a função a cada 2 segundos
        else:
            self.master.reset_order()
            self.destroy()

    def center_window(self, width, height):
        """Centraliza o popup na tela."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


class WidgQuent(Frame):
    def __init__(self, parent, text, add_button_text, name, remove_button_text, master):
        super().__init__(parent)

        self.master = master
        self.name = name

        self.text = text
        self.add_button_text = add_button_text
        self.remove_button_text = remove_button_text

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        Label(self, text=self.text, font=("Times New Roman", 14)).grid(row=0, column=1)
        Button(self, text=self.add_button_text, font=('Times New Roman', 14), command=self.add_quentinha).grid(row=0, column=2)
        Button(self, text=self.remove_button_text, font=('Times New Roman', 14), command=self.remove_quentinha).grid(row=0, column=3)
    
        self.count_label = Label(self, text="x 0", font=('Times New Roman', 12))
        self.count_label.grid(row=0, column=4, sticky="nsew")

    def add_quentinha(self):
        """Adiciona uma quentinha ao pedido"""
        self.master.quantidades[self.name] += 1
        self.master.total_cost += 18 if self.name == "quent1" else 20 if self.name == "quent2" else 22
        self.master.cost_label.config(text=f"Custo: R$ {self.master.total_cost:.2f}")
        self.count_label.config(text=f"x {self.master.quantidades[self.name]}")

    def remove_quentinha(self):
        """Remove uma quentinha do pedido"""
        if self.master.quantidades[self.name] > 0:
            self.master.quantidades[self.name] -= 1
            self.master.total_cost -= 18 if self.name == "quent1" else 20 if self.name == "quent2" else 22
            self.master.cost_label.config(text=f"Custo: R$ {self.master.total_cost:.2f}")
        self.count_label.config(text=f"x {self.master.quantidades[self.name]}")

    def update_quantity(self):
        """Atualiza a quantidade exibida para a quentinha"""
        self.count_label.config(text=f"x {self.master.quantidades[self.name]}")




# Inicialização do sistema
sys = Sys()
sys.mainloop()
