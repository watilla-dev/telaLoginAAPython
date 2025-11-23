import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox
#Importando as bibliotecas.

# Classe principal responsavel por todas as chamadas
class BackEnd():
    def conecta_db(self):
        #Conecta ao banco de dados SQLite
        self.conn = sqlite3.connect("Sistema_cadastros.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado")

    def desconecta_db(self):
        #Encerra a conexão
        self.conn.close()
        print("Banco de dados desconectado")

    def cria_tabela(self):
        #Cria a tabela de usuários se ainda não existir
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela Criada com sucesso!")
        self.desconecta_db()

    def cadastrar_usuario(self):
        #Coleta de dados dos campos de entradas
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        try:
            #Verificações de preenchimento e validação
            if (self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de login", message="ERRO!!!\n Por favor preencha todos os campos!")
            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="O nome de usuario deve ser pelo menos 4 caracteres.")
            elif (len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Sistema de login", message="A senha deve ser pelo menos 4 caracteres.")
            elif (self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Sistema de login", message="ERRO\nAs senhas colocadas não estão iguais")
            else:
                #Caso esteja tudo certo, irar adcionar os dados no banco de dados
                self.conecta_db()
                self.cursor.execute("""
                    INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
                    VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
                self.conn.commit()
                messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_cadastro}\nOs seus dados foram cadastrados!")
                self.desconecta_db()
                self.limpa_entry_cadastro()
        except Exception as e:
            #Tratamento de erro genérico
            messagebox.showerror(title="Sistema de login", message=f"Erro no processamento do seu cadastro!\n{e}")
            self.desconecta_db()

    def verifica_login(self):
        #Coleta os dados dos campos de login
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        print(self.username_login, self.senha_login)
        self.limpa_entry_login()

        self.conecta_db()
        #Verifica no banco de dados se o usuário e senha existem
        self.cursor.execute("SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)", (self.username_login, self.senha_login))
        self.verifica_dados = self.cursor.fetchone()

        try:
            #Verificação de login correto e incorreto
            if (self.username_login == "" or self.senha_login == ""):
                messagebox.showwarning(title="Sistema de login", message="Por favor preencha todos os campos")
            elif self.verifica_dados:
                messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_login}\nLogin feito com sucesso!")
                self.desconecta_db()
                self.limpa_entry_login()
            else:
                messagebox.showerror(title="Sistema de Login", message="ERRO!!!\nDados não encontrados em nosso sistema")
                self.desconecta_db()
        except Exception as e:
            messagebox.showerror(title="Sistema de Login", message=f"Erro durante login\n{e}")
            self.desconecta_db()

#Classe principal da interface gráfica
class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.title_label = None
        self.tela_de_login()
        self.cria_tabela()

    def configuracoes_da_janela_inicial(self):
        #Define o tamanho da janela
        self.geometry("700x500")
        self.title("Sistema de login")
        self.resizable(False, False)

    def atualizar_titulo(self):
        #Cria a tela inicial de login
        if self.title_label:
            self.title_label.destroy()
        self.title_label = ctk.CTkLabel(self, text="Faça o seu login ou Cadastre-se\n", font=("Century Gothic bold", 14))
        self.title_label.grid(row=0, column=0, pady=10, padx=10)

    # Configuração de itens na tela posicionamentos e tamanhos
    # Essas configurações se referem ao TKinter
    def tela_de_login(self):
        self.atualizar_titulo()

        self.img = PhotoImage(file="login_image.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=1)

        self.frame_login = ctk.CTkFrame(self, width=350, height=480)
        self.frame_login.place(x=350, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuario..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#003AFA")
        self.username_login_entry.grid(row=1, column=0, pady=5, padx=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Sua senha..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#E01818", show="-")
        self.senha_login_entry.grid(row=2, column=0, pady=5, padx=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique aqui para ver a senha", font=("Century Gothic bold", 12), corner_radius=20, command=self.alternar_senha_login)
        self.ver_senha.grid(row=3, column=0, pady=5, padx=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Fazer login".upper(), font=("Century Gothic bold", 16), corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, pady=5, padx=10)

        self.span = ctk.CTkLabel(self.frame_login, text="Se não tem conta, clique no botão abaixo\n para poder se cadastrar\n no nosso sistema", font=("Century Gothic", 10))
        self.span.grid(row=5, column=0, pady=5, padx=10)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="#138809", hover_color="#111250", text="Fazer cadastro".upper(), font=("Century Gothic bold", 16), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, pady=5, padx=10)

    def tela_de_cadastro(self):
        #Tela de cadastro de novos usuários
        self.frame_login.place_forget()
        self.atualizar_titulo()

        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)

        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuario..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#003AFA")
        self.username_cadastro_entry.grid(row=1, column=0, pady=5, padx=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email de usuario..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#003AFA")
        self.email_cadastro_entry.grid(row=2, column=0, pady=5, padx=10)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Sua senha", font=("Century Gothic bold", 16), corner_radius=15, border_color="#E01818", show="-")
        self.senha_cadastro_entry.grid(row=3, column=0, pady=5, padx=10)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirmar senha", font=("Century Gothic bold", 16), corner_radius=15, border_color="#E01818", show="-")
        self.confirma_senha_entry.grid(row=4, column=0, pady=5, padx=10)
 
        #Caixa para ver/ocultar senha
        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique aqui para ver a senha", font=("Century Gothic bold", 12), corner_radius=20, command=self.alternar_senha_cadastro)
        self.ver_senha.grid(row=5, column=0, pady=5)

        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="#138809", hover_color="#111250", text="Fazer cadastro".upper(), font=("Century Gothic bold", 16), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, pady=5, padx=10)

        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar para a tela de login".upper(), font=("Century Gothic bold", 16), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, pady=5, padx=10)

    #Altera visibilidade da senha e confirmação no cadastro
    def alternar_senha_login(self):
        if self.ver_senha.get() == 1:
            self.senha_login_entry.configure(show="")
        else:
            self.senha_login_entry.configure(show="-")

    def alternar_senha_cadastro(self):
        if self.ver_senha.get() == 1:
            self.senha_cadastro_entry.configure(show="")
            self.confirma_senha_entry.configure(show="")
        else:
            self.senha_cadastro_entry.configure(show="-")
            self.confirma_senha_entry.configure(show="-")
    #Limpa os campos de entrada da tela de cadastro
    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    #Limpa os campos da tela de login
    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)

#Inicia o progama
if __name__ == "__main__":
    app = App()
    app.mainloop()
