import customtkinter as tk

def receber_dados():
    indice = input_imovel.get()
    data_inicio = input_data_inicio.get()
    data_atual = input_data.get()
    email = input_usuario.get()
    senha = input_senha.get()
    return indice, data_inicio, data_atual, email, senha

def exibir_dialogo_confirmacao():
    def continuar_operacao():
        window_confirmacao.destroy()

        indice, data_inicio, data_atual, email, senha = receber_dados()

        if not indice or not data_inicio or not data_atual or not email or not senha:
            print("Por favor, preencha todos os campos.")
            return

        try:
            indice = int(indice)
        except ValueError:
            print("O índice deve ser um número inteiro.")
            return

        textos = {
            'url': 'https://signin.valuegaia.com.br/?provider=imob',
            'email': email,
            'senha': senha,
            'data_inicio': data_inicio,
            'data_atual': data_atual,
            'indice': indice
        }


    def cancelar_operacao():
        window_confirmacao.destroy()

    window_confirmacao = tk.CTkToplevel()
    window_confirmacao.title('Confirmação')
    window_confirmacao.geometry('300x150')
    window_confirmacao.grab_set()

    label_confirmação = tk.CTkLabel(window_confirmacao, text='Confirme os dados e clique em continuar.', text_color='#4D4D4D', font=fonte_confirmacao)
    label_confirmação.pack(pady=20)

    button_continuar = tk.CTkButton(window_confirmacao, text='Continuar', fg_color='#F82E52', hover_color='#FA1131', command=continuar_operacao)
    button_continuar.pack(padx=10, pady=10, side='right')

    button_cancelar = tk.CTkButton(window_confirmacao, text='Cancelar', fg_color='#F82E52', hover_color='#FA1131', command=cancelar_operacao)
    button_cancelar.pack(padx=10, pady=10, side='left')

tk.set_appearance_mode('light')
window = tk.CTk()
window.geometry('450x550')
window.minsize(450, 550)
window.title('Kenlo Imob - Automação')

fonte_titulo = tk.CTkFont('Roboto', 18, 'bold')
fonte_principal = tk.CTkFont('Roboto', 14, 'bold')
fonte_secundaria = tk.CTkFont('Poppins', 11)
fonte_confirmacao = tk.CTkFont('Poppins', 14)

# Título
label_titulo = tk.CTkLabel(window, text='CADASTRO DE DADOS', font=fonte_titulo, text_color='#F82E52')
label_titulo.pack(pady=(40, 10))

# Imóvel
label_imovel = tk.CTkLabel(window, text='Imóvel', font=fonte_principal, text_color='#4D4D4D')
label_imovel.pack(pady=5)
input_imovel = tk.CTkEntry(window, placeholder_text='Digite o número do imóvel inicial', font=fonte_secundaria, corner_radius=7, width=300)
input_imovel.pack(pady=5)

# Data inicial
label_data_inicio = tk.CTkLabel(window, text='Data inicial', font=fonte_principal, text_color='#4D4D4D')
label_data_inicio.pack(pady=5)
input_data_inicio = tk.CTkEntry(window, placeholder_text='Digite a data inicial', font=fonte_secundaria, corner_radius=7, width=300)
input_data_inicio.pack(pady=5)

# Data atual
label_data = tk.CTkLabel(window, text='Data atual', font=fonte_principal, text_color='#4D4D4D')
label_data.pack(pady=5)
input_data = tk.CTkEntry(window, placeholder_text='Digite a data atual', font=fonte_secundaria, corner_radius=7, width=300)
input_data.pack(pady=5)

# Usuário
label_usuario = tk.CTkLabel(window, text='Usuário', font=fonte_principal, text_color='#4D4D4D')
label_usuario.pack(pady=5)
input_usuario = tk.CTkEntry(window, placeholder_text='Digite seu usuário', font=fonte_secundaria, corner_radius=7, width=300)
input_usuario.pack(pady=5)

# Senha
label_senha = tk.CTkLabel(window, text='Senha', font=fonte_principal, text_color='#4D4D4D')
label_senha.pack(pady=5)
input_senha = tk.CTkEntry(window, placeholder_text='Digite sua senha', font=fonte_secundaria, corner_radius=7, width=300)
input_senha.pack(pady=5)

# Iniciar
button_iniciar = tk.CTkButton(window, text='Iniciar', command=exibir_dialogo_confirmacao, corner_radius=7, height=30, fg_color='#F82E52', hover_color='#FA1131')
button_iniciar.pack(pady=30)

window.mainloop()
