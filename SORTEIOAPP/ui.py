# ui.py (VERSÃO FINAL COM LÓGICA DE PAPÉIS)

import tkinter
import customtkinter
import random
import re
import datetime
from tkinter import messagebox, simpledialog

# Importa as funções do nosso novo arquivo de banco de dados
import database

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

APP_ICON = "icone_sorteio.ico"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Sorteio v3.1")
        self.geometry("800x850")
        
        # A variável de estado agora guarda o papel do usuário (ex: 'admin', 'locutor')
        self.usuario_logado_role = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        try:
            self.iconbitmap(APP_ICON)
        except tkinter.TclError:
            try:
                photo = tkinter.PhotoImage(file=APP_ICON.replace(".ico", ".png"))
                self.iconphoto(False, photo)
            except Exception as e:
                print(f"Não foi possível carregar o ícone: {e}")
        
        self.is_formatting_cpf = False
        self.is_formatting_telefone = False

        self.cpf_var = customtkinter.StringVar()
        self.cpf_var.trace_add('write', self.formatar_cpf)
        
        self.telefone_var = customtkinter.StringVar()
        self.telefone_var.trace_add('write', self.formatar_telefone)

        self.tabview = customtkinter.CTkTabview(self, width=780)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.tabview.add("Cadastro")
        self.tabview.add("Login") # Renomeado de "Admin" para "Login"
        
        self.popular_aba_cadastro()
        self.mostrar_tela_login()

    def popular_aba_cadastro(self):
        aba_cadastro = self.tabview.tab("Cadastro")
        aba_cadastro.grid_columnconfigure(0, weight=1)
        
        label_cadastro = customtkinter.CTkLabel(aba_cadastro, text="Cadastro de Participantes", font=("Arial", 20))
        label_cadastro.pack(pady=20)

        form_frame = customtkinter.CTkFrame(aba_cadastro)
        form_frame.pack(pady=10, padx=20) 
        form_frame.grid_columnconfigure(1, weight=1)

        label_nome = customtkinter.CTkLabel(form_frame, text="Nome Completo:")
        label_nome.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_nome = customtkinter.CTkEntry(form_frame, width=250)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        label_cpf = customtkinter.CTkLabel(form_frame, text="CPF:")
        label_cpf.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_cpf = customtkinter.CTkEntry(form_frame, textvariable=self.cpf_var, width=250)
        self.entry_cpf.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        label_telefone = customtkinter.CTkLabel(form_frame, text="Telefone + DDD:")
        label_telefone.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_telefone = customtkinter.CTkEntry(form_frame, textvariable=self.telefone_var, width=250)
        self.entry_telefone.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        self.btn_cadastrar = customtkinter.CTkButton(aba_cadastro, text="Cadastrar", command=self.cadastrar_participante)
        self.btn_cadastrar.pack(pady=20)
        
    def formatar_cpf(self, *args):
        if self.is_formatting_cpf: return
        self.is_formatting_cpf = True
        texto_atual = self.cpf_var.get()
        numeros = re.sub(r'\D', '', texto_atual)[:11]
        formatado = numeros
        if len(numeros) > 9: formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
        elif len(numeros) > 6: formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
        elif len(numeros) > 3: formatado = f"{numeros[:3]}.{numeros[3:]}"
        self.cpf_var.set(formatado)
        self.entry_cpf.icursor(len(formatado))
        self.is_formatting_cpf = False

    def formatar_telefone(self, *args):
        if self.is_formatting_telefone: return
        self.is_formatting_telefone = True
        texto_atual = self.telefone_var.get()
        numeros = re.sub(r'\D', '', texto_atual)[:11]
        formatado = numeros
        if len(numeros) == 11: formatado = f"({numeros[:2]}) {numeros[2]} {numeros[3:7]}-{numeros[7:]}"
        elif len(numeros) >= 10: formatado = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
        elif len(numeros) > 2: formatado = f"({numeros[:2]}) {numeros[2:]}"
        self.telefone_var.set(formatado)
        self.entry_telefone.icursor(len(formatado))
        self.is_formatting_telefone = False

    def cadastrar_participante(self):
        nome = self.entry_nome.get().strip()
        cpf_numeros = re.sub(r'\D', '', self.cpf_var.get())
        telefone_numeros = re.sub(r'\D', '', self.telefone_var.get())

        if not nome or not cpf_numeros or not telefone_numeros:
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios!")
            return
        
        if len(cpf_numeros) != 11:
            messagebox.showerror("Erro de Validação", "CPF inválido! Deve conter 11 dígitos.")
            return

        if len(telefone_numeros) not in (10, 11):
            messagebox.showerror("Erro de Validação", "Telefone inválido! Deve conter 10 ou 11 dígitos.")
            return

        if database.adicionar_participante(nome, cpf_numeros, telefone_numeros):
            messagebox.showinfo("Sucesso", f"{nome} foi cadastrado com sucesso!")
            self.entry_nome.delete(0, 'end')
            self.cpf_var.set("")
            self.telefone_var.set("")
            if self.usuario_logado_role: # Se houver algum usuário logado
                self.carregar_participantes_admin()
        else:
            messagebox.showerror("Erro de Cadastro", "O CPF informado já está cadastrado ou ocorreu um erro.")

    def mostrar_tela_login(self):
        try:
            self.tabview.add("Login")
        except:
            self.tabview.set("Login")
        
        aba_login = self.tabview.tab("Login")
        aba_login.grid_columnconfigure(0, weight=1)
        for widget in aba_login.winfo_children(): widget.destroy()
        
        label_login = customtkinter.CTkLabel(aba_login, text="Acesso Restrito", font=("Arial", 20))
        label_login.pack(pady=40, padx=10)
        btn_login_usuario = customtkinter.CTkButton(aba_login, text="Login", command=self.login_usuario)
        btn_login_usuario.pack(pady=20, padx=10)

    def criar_abas_logado(self):
        self.tabview.delete("Login")
        aba_logada = self.tabview.add("Área Logada")
                    
        admin_tabview = customtkinter.CTkTabview(aba_logada, width=750)
        admin_tabview.pack(expand=True, fill="both", padx=5, pady=5)
        
        aba_sorteio = admin_tabview.add("Sorteio")
        aba_relatorios = admin_tabview.add("Relatórios")
        
        self.popular_aba_sorteio(aba_sorteio)
        self.popular_aba_relatorios(aba_relatorios)

    def popular_aba_sorteio(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        btn_logout_admin = customtkinter.CTkButton(aba, text="Logout", command=self.logout_usuario)
        btn_logout_admin.pack(pady=10, padx=10)
        label_sorteio = customtkinter.CTkLabel(aba, text="Gerenciamento e Sorteio", font=("Arial", 20))
        label_sorteio.pack(pady=10, padx=10)
        
        frame_gerenciamento = customtkinter.CTkFrame(aba)
        frame_gerenciamento.pack(pady=10, padx=10, fill="x")
        
        self.lista_participantes = tkinter.Listbox(frame_gerenciamento, width=70, height=8, selectmode=tkinter.SINGLE)
        
        # --- AQUI ESTÁ A LÓGICA DE PERMISSÃO ---
        # Se o usuário for 'admin', cria a grade com 2 colunas e os dois botões
        if self.usuario_logado_role == 'admin':
            frame_gerenciamento.grid_columnconfigure((0,1), weight=1)
            self.lista_participantes.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
            
            btn_atualizar_lista = customtkinter.CTkButton(frame_gerenciamento, text="Atualizar Lista", command=self.carregar_participantes_admin)
            btn_atualizar_lista.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

            btn_excluir_participante = customtkinter.CTkButton(frame_gerenciamento, text="Excluir Selecionado", command=self.excluir_participante, fg_color="red")
            btn_excluir_participante.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Se for 'locutor' (ou qualquer outro papel), cria a grade com 1 coluna e apenas o botão de atualizar
        else:
            frame_gerenciamento.grid_columnconfigure(0, weight=1)
            self.lista_participantes.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            btn_atualizar_lista = customtkinter.CTkButton(frame_gerenciamento, text="Atualizar Lista", command=self.carregar_participantes_admin)
            btn_atualizar_lista.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # O resto da interface do sorteio é igual para ambos
        btn_sortear = customtkinter.CTkButton(aba, text="REALIZAR SORTEIO", command=self.realizar_sorteio, fg_color="green")
        btn_sortear.pack(pady=10, padx=10)
        self.label_vencedor = customtkinter.CTkLabel(aba, text="O vencedor aparecerá aqui...", font=("Arial", 16))
        self.label_vencedor.pack(pady=5, padx=10)
        label_historico = customtkinter.CTkLabel(aba, text="Histórico Recente de Sorteios", font=("Arial", 16))
        label_historico.pack(pady=5, padx=10)
        self.lista_historico = tkinter.Listbox(aba, width=70, height=4)
        self.lista_historico.pack(pady=5, padx=10, fill="x")

        self.carregar_participantes_admin()
        self.carregar_historico_sorteios()

    def popular_aba_relatorios(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        frame_relatorio = customtkinter.CTkFrame(aba)
        frame_relatorio.pack(pady=20, padx=10, fill="x")
        frame_relatorio.grid_columnconfigure((0, 1), weight=2); frame_relatorio.grid_columnconfigure(2, weight=1)
        label_relatorio = customtkinter.CTkLabel(frame_relatorio, text="Consultar Ganhadores por Mês/Ano:", font=("Arial", 20))
        label_relatorio.grid(row=0, column=0, columnspan=3, padx=5, pady=10)
        current_year = datetime.datetime.now().year
        anos = [str(y) for y in range(current_year, current_year - 5, -1)]
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.mapa_meses = {nome: f"{i+1:02d}" for i, nome in enumerate(meses)}
        self.combo_mes = customtkinter.CTkOptionMenu(frame_relatorio, values=meses)
        self.combo_mes.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.combo_mes.set(meses[datetime.datetime.now().month - 1])
        self.combo_ano = customtkinter.CTkOptionMenu(frame_relatorio, values=anos)
        self.combo_ano.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        btn_buscar_ganhadores = customtkinter.CTkButton(frame_relatorio, text="Buscar", command=self.carregar_ganhadores_do_mes, fg_color="#C00000")
        btn_buscar_ganhadores.grid(row=1, column=2, padx=5, pady=5)
        self.lista_ganhadores_mes = tkinter.Listbox(frame_relatorio, width=70, height=15)
        self.lista_ganhadores_mes.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
    def login_usuario(self):
        usuario = simpledialog.askstring("Login", "Usuário:")
        if not usuario: return
        senha = simpledialog.askstring("Login", "Senha:", show='*')
        if not senha: return
        
        role = database.validar_usuario(usuario, senha)
        
        if role:
            self.usuario_logado_role = role
            self.criar_abas_logado()
            self.tabview.set("Área Logada")
            messagebox.showinfo("Login", f"Login como '{role.capitalize()}' realizado com sucesso!")
        else:
            messagebox.showerror("Login", "Usuário ou senha incorretos!")

    def logout_usuario(self):
        self.usuario_logado_role = None
        self.tabview.delete("Área Logada")
        self.mostrar_tela_login()
        self.tabview.set("Cadastro")
        messagebox.showinfo("Logout", "Usuário deslogado.")

    def carregar_participantes_admin(self):
        if not self.usuario_logado_role: return
        self.lista_participantes.delete(0, 'end')
        participantes = database.buscar_todos_participantes()
        for p in participantes:
            texto = f"ID: {p[0]} | Nome: {p[1]} | CPF: {p[2]} | Tel: {p[3]} | Sorteado: {p[4]}x"
            self.lista_participantes.insert('end', texto)

    def excluir_participante(self):
        if self.usuario_logado_role != 'admin':
            messagebox.showerror("Acesso Negado", "Você não tem permissão para excluir participantes.")
            return
            
        selected_index = self.lista_participantes.curselection()
        if not selected_index:
            messagebox.showwarning("Exclusão", "Selecione um participante para excluir.")
            return
        selected_item = self.lista_participantes.get(selected_index[0])
        id_participante = int(selected_item.split(" | ")[0].split(": ")[1])
        nome_participante = selected_item.split(" | ")[1].split(": ")[1]
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir '{nome_participante}'?"):
            if database.excluir_participante(id_participante):
                messagebox.showinfo("Sucesso", f"'{nome_participante}' excluído!")
                self.carregar_participantes_admin()
            else:
                messagebox.showerror("Erro", "Ocorreu um erro ao excluir o participante.")

    def realizar_sorteio(self):
        if not self.usuario_logado_role: return
        elegiveis = database.buscar_participantes_elegiveis()
        if not elegiveis:
            messagebox.showwarning("Aviso", "Não há participantes elegíveis para o sorteio!")
            return
        vencedor = random.choice(elegiveis)
        id_vencedor, nome_vencedor = vencedor[0], vencedor[1]
        
        if database.registrar_vencedor(id_vencedor, nome_vencedor):
            self.label_vencedor.configure(text=f"🎉 VENCEDOR: {nome_vencedor} 🎉")
            messagebox.showinfo("Parabéns!", f"O vencedor é: {nome_vencedor}!")
            self.carregar_participantes_admin()
            self.carregar_historico_sorteios()
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao registrar o vencedor no banco de dados.")

    def carregar_historico_sorteios(self):
        if not self.usuario_logado_role: return
        self.lista_historico.delete(0, 'end')
        historico = database.buscar_historico_recente()
        for item in historico:
            texto = f"Vencedor: {item[0]} | Data: {item[1]}"
            self.lista_historico.insert('end', texto)

    def carregar_ganhadores_do_mes(self):
        if not self.usuario_logado_role: return
        self.lista_ganhadores_mes.delete(0, 'end')
        mes_nome = self.combo_mes.get()
        ano_selecionado = self.combo_ano.get()
        mes_numero = self.mapa_meses[mes_nome]
        
        info_ganhadores = database.buscar_ganhadores_por_mes(ano_selecionado, mes_numero)
        
        if not info_ganhadores:
            self.lista_ganhadores_mes.insert('end', f"Nenhum ganhador encontrado para {mes_nome} de {ano_selecionado}.")
            return

        for p in info_ganhadores:
            texto = f"ID: {p[0]} | Nome: {p[1]} | CPF: {p[2]} | Tel: {p[3]}"
            self.lista_ganhadores_mes.insert('end', texto)