import tkinter as tk
from tkinter import font
from pyswip import Prolog

# Inicializar o Prolog
prolog = Prolog()

# Carregar o código Prolog no Python
prolog.consult("filmes.pl")  

# Lista de filmes assistidos com seus gêneros
filmes_assistidos = []

# Função para obter recomendações (Top 3 filmes)
def recomendar_filmes():
    gostos = gostos_entry.get().split(',')
    gostos = [gosto.strip().lower().replace(" ", "_") for gosto in gostos] 

    filmes_recomendados.delete(1.0, tk.END)  # Limpar a lista de filmes recomendados

    # Consultar Prolog para os filmes recomendados (Top 3)
    query = "top_3_filmes([{}], Top3)".format(",".join(gostos))  
    result = list(prolog.query(query))

    if not result:  # Se o resultado estiver vazio
        filmes_recomendados.insert(tk.END, "Nenhum filme encontrado.\n")
    else:
        count = 0
        filmes_recomendados.insert(tk.END, "Top 3 filmes para você:\n\n")
        # O resultado agora será uma lista com 3 filmes e notas
        for item in result:
            filme_lista = item["Top3"]  
            for filme_info in filme_lista:
                filme = filme_info[0]  
                nota = filme_info[1]  
                filmes_recomendados.insert(tk.END, f"{filme.replace('_', ' ').title()} - Nota: {nota}\n")
                count += 1

# Função para marcar filme como assistido com gênero
def marcar_assistido():
    filme_assistido = filme_entry.get().strip().lower().replace(" ", "_")  # Garantir que o filme está no formato correto
    genero = gostos_entry.get().strip().lower().replace(" ", "_")  # Usar a mesma entrada de gênero dos gostos
    prolog.assertz(f"assistido({filme_assistido})")
    filmes_assistidos.append((filme_assistido, genero))  # Armazenar o filme com o gênero
    status_label.config(text=f"Filme '{filme_assistido.replace('_', ' ').title()}' do gênero '{genero.replace('_', ' ').title()}' marcado como assistido.")

# Função para exibir filmes assistidos de acordo com o gênero
def exibir_filmes_assistidos():
    filmes_recomendados.delete(1.0, tk.END)  # Limpar a área de recomendação
    genero = gostos_entry.get().strip().lower().replace(" ", "_")  # Usar a mesma entrada para o gênero

    filmes_assistidos_filtrados = [filme for filme, gen in filmes_assistidos if gen == genero]

    if filmes_assistidos_filtrados:  # Se houver filmes assistidos do gênero
        filmes_recomendados.insert(tk.END, f"Filmes Assistidos ({genero.replace('_', ' ').title()}):\n\n")
        for filme in filmes_assistidos_filtrados:
            filmes_recomendados.insert(tk.END, f"{filme.replace('_', ' ').title()}\n")
    else:
        filmes_recomendados.insert(tk.END, f"Nenhum filme assistido encontrado para o gênero '{genero.replace('_', ' ').title()}'.\n")

# Função para exibir filmes recomendados
def exibir_filmes_recomendados():
    filmes_recomendados.delete(1.0, tk.END)  # Limpar a área de recomendação
    recomendar_filmes()  # Exibir os filmes recomendados

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Recomendação de Filmes")
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

# Botão "Recomendar Filmes"
btn_recomendar = tk.Button(root, text="Recomendar Filmes", font=font_entrada, bg=btn_color, fg=text_color, bd=0, relief="flat", padx=10, pady=5)
btn_recomendar.bind("<Enter>", lambda e: on_button_hover(e, btn_recomendar, btn_color_hover))
btn_recomendar.bind("<Leave>", lambda e: on_button_leave(e, btn_recomendar, btn_color))
btn_recomendar.config(command=exibir_filmes_recomendados)
btn_recomendar.pack(pady=20)

# Botão "Filmes Assistidos"
btn_assistidos = tk.Button(root, text="Filmes Assistidos", font=font_entrada, bg=highlight_color, fg=text_color, bd=0, relief="flat", padx=10, pady=5)
btn_assistidos.bind("<Enter>", lambda e: on_button_hover(e, btn_assistidos, "#e68917"))
btn_assistidos.bind("<Leave>", lambda e: on_button_leave(e, btn_assistidos, highlight_color))
btn_assistidos.config(command=exibir_filmes_assistidos)
btn_assistidos.pack(pady=10)

# Área de recomendação
filmes_recomendados = tk.Text(root, height=10, width=50, font=font_entrada, bd=2, relief="solid", wrap="word", fg=text_color_2, bg=input_bg_color, insertbackground="white", highlightthickness=2, highlightbackground=highlight_color)
filmes_recomendados.pack(pady=(10, 20))

# Entrada para marcar filme como assistido
tk.Label(root, text="Marcar filme como assistido:", font=font_titulo, bg=bg_color, fg=text_color).pack(pady=10)
filme_entry = tk.Entry(root, width=50, font=font_entrada, bd=0, relief="flat", fg=bg_color, bg=input_bg_color, insertbackground="white", highlightthickness=2, highlightbackground=highlight_color)
filme_entry.pack(pady=5)

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
