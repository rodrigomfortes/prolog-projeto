import tkinter as tk
from tkinter import font
from pyswip import Prolog

# Inicializar o Prolog
prolog = Prolog()

# Carregar o código Prolog no Python
prolog.consult("recomendacao.pl")

# Função para recomendar conteúdos com base no tipo (Filme, Série, Anime)
def recomendar_conteudos():
    gostos = gostos_entry.get().split(',')
    gostos = [gosto.strip().lower().replace(" ", "_") for gosto in gostos] 
    tipo = tipo_var.get()  # Tipo escolhido: Filme, Série ou Anime

    filmes_recomendados.delete(1.0, tk.END)  # Limpar a lista de conteúdos recomendados

    # Ajustar a consulta dependendo do tipo de conteúdo
    if tipo == "Filme":
        query = "top_3_filmes([{}], Top3)".format(",".join(gostos))  
    elif tipo == "Série":
        query = "top_3_series([{}], Top3)".format(",".join(gostos))
    elif tipo == "Anime":
        query = "top_3_animes([{}], Top3)".format(",".join(gostos))
    
    result = list(prolog.query(query))

    if not result:  # Se o resultado estiver vazio
        filmes_recomendados.insert(tk.END, "Nenhum conteúdo encontrado.\n")
    else:
        count = 0
        filmes_recomendados.insert(tk.END, f"Top 3 {tipo}s recomendados:\n\n")
        # O resultado agora será uma lista com 3 filmes, séries ou animes
        for item in result:
            conteudo_lista = item["Top3"]  
            for conteudo_info in conteudo_lista:
                conteudo = conteudo_info[0]  
                nota = conteudo_info[1]  
                filmes_recomendados.insert(tk.END, f"{conteudo.replace('_', ' ').title()} - Nota: {nota}\n")
                count += 1

# Função para marcar conteúdo como assistido (Filme, Série ou Anime)
def marcar_assistido():
    conteudo_assistido = conteudo_entry.get().strip().lower().replace(" ", "_")  # Garantir que o conteúdo está no formato correto
    tipo = tipo_var.get()  # Tipo escolhido: Filme, Série ou Anime
    
    # Ajustando para usar o Prolog para marcar como assistido
    if tipo == "Filme":
        prolog.assertz(f"assistido(filme, {conteudo_assistido})")
    elif tipo == "Série":
        prolog.assertz(f"assistido(serie, {conteudo_assistido})")
    elif tipo == "Anime":
        prolog.assertz(f"assistido(anime, {conteudo_assistido})")
    
    status_label.config(text=f"'{conteudo_assistido.replace('_', ' ').title()}' do tipo '{tipo}' marcado como assistido.")
    conteudo_entry.delete(0, tk.END)

# Função para exibir conteúdos assistidos de acordo com o tipo
def exibir_conteudos_assistidos():
    filmes_recomendados.delete(1.0, tk.END)  # Limpar a área de recomendação
    tipo = tipo_var.get().strip().lower().replace(" ", "_")  # Usar a mesma entrada para o tipo

    # Consultar os conteúdos assistidos no Prolog usando o predicado correto
    if tipo == "filme":
        consulta = f"assistido(filme, Conteudo)"
    elif tipo == "serie":
        consulta = f"assistido(serie, Conteudo)"
    elif tipo == "anime":
        consulta = f"assistido(anime, Conteudo)"
    
    assistidos = list(prolog.query(consulta))

    if assistidos:  # Se houver conteúdos assistidos do tipo
        filmes_recomendados.insert(tk.END, f"Conteúdos Assistidos ({tipo.replace('_', ' ').title()}):\n\n")
        for item in assistidos:
            conteudo = item["Conteudo"].replace('_', ' ').title()  # Formatando a exibição
            filmes_recomendados.insert(tk.END, f"{conteudo}\n")
    else:
        filmes_recomendados.insert(tk.END, f"Nenhum conteúdo assistido encontrado para o tipo '{tipo.replace('_', ' ').title()}'.\n")


# Função para exibir conteúdos recomendados
def exibir_conteudos_recomendados():
    filmes_recomendados.delete(1.0, tk.END)  # Limpar a área de recomendação
    recomendar_conteudos()  # Exibir os conteúdos recomendados

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Recomendação de Conteúdos")
root.geometry("500x600")  # Definir tamanho fixo da janela

# Definir fontes e estilos
font_titulo = font.Font(family="Helvetica", size=14, weight="bold")
font_entrada = font.Font(family="Helvetica", size=12)
font_status = font.Font(family="Helvetica", size=10)

# Definir as cores do tema
bg_color = "#2e3b4e"
btn_color = "#4CAF50"
btn_color_hover = "#45a049"
highlight_color = "#FF9800"
text_color = "#ffffff"
text_color_2 = "#333333"
input_bg_color = "#f1f1f1"
status_color = "#7CFC00"

root.config(bg=bg_color)

# Funções auxiliares para botões
def on_button_hover(event, button, color):
    button.config(bg=color)

def on_button_leave(event, button, color):
    button.config(bg=color)

# Entradas
tk.Label(root, text="Gêneros de interesse (separados por vírgula):", font=font_titulo, bg=bg_color, fg=text_color).pack(pady=(30, 5))
gostos_entry = tk.Entry(root, width=50, font=font_entrada, bd=0, relief="flat", fg=bg_color, bg=input_bg_color, insertbackground="white", highlightthickness=2, highlightbackground=highlight_color)
gostos_entry.pack(pady=5)

# Criar o filtro de tipo (Filme, Série, Anime)
tipo_var = tk.StringVar()
tipo_var.set("Filme")  # Valor inicial

tipo_menu = tk.OptionMenu(root, tipo_var, "Filme", "Série", "Anime")
tipo_menu.config(font=font_entrada, bg=input_bg_color, fg=bg_color)
tipo_menu.pack(pady=10)

# Botões "Recomendar Conteúdos" e "Conteúdos Assistidos" lado a lado
frame_botoes = tk.Frame(root, bg=bg_color)  # Criar um frame para organizar os botões lado a lado

btn_recomendar = tk.Button(frame_botoes, text="Recomendar Conteúdos", font=font_entrada, bg=btn_color, fg=text_color, bd=0, relief="flat", padx=10, pady=5)
btn_recomendar.bind("<Enter>", lambda e: on_button_hover(e, btn_recomendar, btn_color_hover))
btn_recomendar.bind("<Leave>", lambda e: on_button_leave(e, btn_recomendar, btn_color))
btn_recomendar.config(command=exibir_conteudos_recomendados)

btn_assistidos = tk.Button(frame_botoes, text="Conteúdos Assistidos", font=font_entrada, bg=highlight_color, fg=text_color, bd=0, relief="flat", padx=10, pady=5)
btn_assistidos.bind("<Enter>", lambda e: on_button_hover(e, btn_assistidos, "#e68917"))
btn_assistidos.bind("<Leave>", lambda e: on_button_leave(e, btn_assistidos, highlight_color))
btn_assistidos.config(command=exibir_conteudos_assistidos)

# Empacotar os botões no frame (lado a lado)
btn_recomendar.pack(side="left", padx=5)
btn_assistidos.pack(side="left", padx=5)

frame_botoes.pack(pady=20)  # Empacotar o frame na interface

# Área de recomendação
filmes_recomendados = tk.Text(root, height=10, width=50, font=font_entrada, bd=2, relief="solid", wrap="word", fg=text_color_2, bg=input_bg_color, insertbackground="white", highlightthickness=2, highlightbackground=highlight_color)
filmes_recomendados.pack(pady=(10, 20))

# Entrada para marcar conteúdo como assistido
tk.Label(root, text="Marcar conteúdo como assistido:", font=font_titulo, bg=bg_color, fg=text_color).pack(pady=10)
conteudo_entry = tk.Entry(root, width=50, font=font_entrada, bd=0, relief="flat", fg=bg_color, bg=input_bg_color, insertbackground="white", highlightthickness=2, highlightbackground=highlight_color)
conteudo_entry.pack(pady=5)

# Botão "Marcar como Assistido"
btn_assistido = tk.Button(root, text="Marcar como Assistido", font=font_entrada, bg=highlight_color, fg=text_color, bd=0, relief="flat", padx=10, pady=5)
btn_assistido.bind("<Enter>", lambda e: on_button_hover(e, btn_assistido, "#e68917"))
btn_assistido.bind("<Leave>", lambda e: on_button_leave(e, btn_assistido, highlight_color))
btn_assistido.config(command=marcar_assistido)
btn_assistido.pack(pady=20)

# Status
status_label = tk.Label(root, text="", font=font_status, bg=bg_color, fg=status_color)
status_label.pack(pady=10)

# Iniciar a interface gráfica
root.mainloop()
