import tkinter as tk
from pyswip import Prolog

# Inicializar o Prolog
prolog = Prolog()

# Carregar o código Prolog no Python
prolog.consult("filmes.pl")  # Carrega o arquivo Prolog

# Função para obter recomendações
def recomendar_filmes():
    gostos = gostos_entry.get().split(',')
    gostos = [gosto.strip() for gosto in gostos]

    # Consultar Prolog para recomendação
    query = "recomendar({}, Filme)".format(str(gostos))
    result = list(prolog.query(query))

    filmes_recomendados.delete(1.0, tk.END)  # Limpar a lista de filmes recomendados

    if result:
        for item in result:
            filme = item["Filme"]
            filmes_recomendados.insert(tk.END, filme + '\n')
    else:
        filmes_recomendados.insert(tk.END, "Nenhum filme recomendado.\n")

# Função para marcar filme como assistido
def marcar_assistido():
    filme_assistido = filme_entry.get()
    prolog.assertz(f"assistido({filme_assistido})")
    status_label.config(text=f"Filme '{filme_assistido}' marcado como assistido.")

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Recomendação de Filmes")

# Entradas
tk.Label(root, text="Gêneros de interesse (separados por vírgula):").pack()
gostos_entry = tk.Entry(root, width=50)
gostos_entry.pack()

tk.Button(root, text="Recomendar Filmes", command=recomendar_filmes).pack()

# Área de recomendação
filmes_recomendados = tk.Text(root, height=10, width=50)
filmes_recomendados.pack()

# Entrada para marcar filme como assistido
tk.Label(root, text="Marcar filme como assistido:").pack()
filme_entry = tk.Entry(root, width=50)
filme_entry.pack()

tk.Button(root, text="Marcar como Assistido", command=marcar_assistido).pack()

# Status
status_label = tk.Label(root, text="")
status_label.pack()

# Iniciar a interface gráfica
root.mainloop()
