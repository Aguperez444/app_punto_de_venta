import ttkbootstrap as ttk
import tkinter
import project_functions

# ----------------------------------------- Funciones ---------------------------------------------
def realizar_busqueda(*args):
    a = project_functions.busqueda(str_buscado)
    if a:
        project_functions.pasar_al_cuadro(a, cuadro)
    else:
        cuadro.delete(*cuadro.get_children())
# -----------------------------------------ventana_principal------------------------------------------------
window = ttk.Window(themename='journal')
window.title('Catalogo-Alpha-0.0.1')
window.geometry('1280x720')

# -----------------------------------------ttk_variables------------------------------------------------
str_buscado = ttk.StringVar()

# -----------------------------------------bootstrap widgets------------------------------------------------
entry = ttk.Entry(master=window, textvariable=str_buscado)

str_buscado.trace_add('write', realizar_busqueda)

style = ttk.Style()
style.configure('Treeview', rowheight=30)


cuadro = ttk.Treeview(master=window, columns=("col1","col2","col3","col4"))
cuadro.column("#0", width=80, anchor="center")
cuadro.column("col1", width=80,  anchor="center")
cuadro.column("col2", width=80, anchor="center")
cuadro.column("col3", width=200, anchor="center")
cuadro.column("col4", width=200, anchor="center")


cuadro.heading("#0", text="Producto")
cuadro.heading("col1", text="Codigo")
cuadro.heading("col2", text="Precio")
cuadro.heading("col3", text="Detalle")
cuadro.heading("col4", text="Codigo de barras")


cuadro.tag_configure('par', foreground= "black", background= "white", font=('Calibri', 18,))
cuadro.tag_configure('impar',foreground= "white", background= "grey", font=('Calibri', 18,))
# -----------------------------------------------packing---------------------------------------------------
entry.pack()
cuadro.pack()


# -----------------------------------------------Main loop---------------------------------------------------
window.mainloop()

