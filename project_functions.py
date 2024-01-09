import sqlite3
from screeninfo import get_monitors
import ttkbootstrap as ttk
import datetime

# alpha 0.0.8

db_name = 'productos.db'


def obtener_config(config_deseada: str):
    config_file = open('config.txt', 'rt')
    config_lines = config_file.readlines()
    config_file.close()
    if config_deseada.lower() == 'tema':
        return config_lines[0]


def cambiar_tema_config(tema_new):
    config_file = open('config.txt', 'rt')
    config_lines = config_file.readlines()
    config_file.close()

    config_lines[0] = tema_new

    config_file = open('config.txt', 'wt')
    config_file.writelines(config_lines)
    config_file.close()


def cambiar_modo(actual, window, str_modo):
    if actual == 'journal_mod':
        window.style.theme_use('darkly_2')
        actual = 'darkly_2'
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        str_modo.set('Modo claro')

        cambiar_tema_config(actual)

    else:
        window.style.theme_use('journal_mod')
        actual = 'journal_mod'
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        str_modo.set('Modo oscuro')

        cambiar_tema_config(actual)


def calcular_res_ventana():
    monitores = get_monitors()
    ancho = int(monitores[0].width // 1.3)
    alto = int(monitores[0].height // 1.3)
    return f'{ancho}x{alto}', ancho, alto


def volver_al_menu(ventana_secundaria, ventana_principal):
    ventana_secundaria.destroy()
    ventana_principal.state('zoomed')
    ventana_principal.deiconify()



def busqueda(str_var_buscado):
    buscado = str_var_buscado.get()
    if buscado == '':
        return
    global db_name
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Productos WHERE producto LIKE ?"
                   " OR detalle LIKE ? OR codigo LIKE ? OR codigo_de_barras LIKE ?",
                   (f'%{buscado}%', f'%{buscado}%', f'%{buscado}%', f'%{buscado}%'))
    encontrado = cursor.fetchall()

    connection.close()
    return encontrado


def busqueda_por_id(id_buscado):
    if id_buscado == '':
        return
    global db_name
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM Productos WHERE id = {id_buscado}")
    encontrado = cursor.fetchall()

    connection.close()
    return encontrado


def pasar_al_cuadro(matrix, treeview_var):
    # Borrar todas las filas existentes en el Treeview
    treeview_var.delete(*treeview_var.get_children())
    contador = 0
    # Añadir nuevas filas
    for tupla in matrix:
        if contador % 2 == 0:
            treeview_var.insert("", "end", text=tupla[1], values=(tupla[2],
                                tupla[3], tupla[4], tupla[6], tupla[0]), tags=('par',))
        else:
            treeview_var.insert("", "end", text=tupla[1], values=(tupla[2],
                                tupla[3], tupla[4], tupla[6], tupla[0]), tags=('impar',))
        contador += 1
    return


def registrar_venta(id_producto, amount):
    # obtener fecha y hora
    fecha_hora_actual = datetime.datetime.now()
    formato_fecha = "%Y-%m-%d"
    formato_hora = "%H:%M:%S"
    fecha = fecha_hora_actual.strftime(formato_fecha)
    hora = fecha_hora_actual.strftime(formato_hora)

    # conectar a base de datos
    global db_name
    connection_db = sqlite3.connect(db_name)
    cursor = connection_db.cursor()
    try:
        a = int(amount)
        if a <= 0:
            raise ValueError('cero o negativo no es una cantidad valida')
    except ValueError:
        amount = 1
    datos_venta = (int(id_producto), int(amount), fecha, hora)
    cursor.execute(f'''
        INSERT INTO Ventas (product_id, cantidad, fecha, hora)
        VALUES (?,?,?,?)
        ''', datos_venta)
    connection_db.commit()
    connection_db.close()
    return


def actualizar_stock(id_producto, cantidad):
    global db_name
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, id_producto))
    connection.commit()
    connection.close()
    return


def add_to_db(vector):
    try:
        vector[5] = int(vector[5])
    except ValueError:
        print('error tipo invalido')
        return False

    global db_name
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Productos (producto, codigo, precio, detalle, codigo_de_barras, stock)
                   VALUES (?, ?, ?, ?, ?, ?)''', vector)
    connection.commit()
    connection.close()
    return True
