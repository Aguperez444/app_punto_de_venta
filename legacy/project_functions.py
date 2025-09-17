import sqlite3
from screeninfo import get_monitors
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
import datetime
import re
import os
import sys

# beta 0.1.1


ruta_bdd = '/home/agustin/MEGA/AB No de la Facultad/Proyectos/Proyectos_personales/APP_FARMACIA/productos.Database'
ruta_archivo = '/home/agustin/Documents/catalogo/config.txt'


def set_ruta_bdd():
    global ruta_archivo
    with open(ruta_archivo, 'rt') as config_file:
        lines = config_file.readlines()
        new_ruta_bdd = lines[1].replace('\n', '')
        global ruta_bdd
        ruta_bdd = new_ruta_bdd


def is_first_time_running():
    documentos = os.path.join(os.path.expanduser('~'), 'Documents')
    ruta_carpeta = os.path.join(documentos, 'catalogo')
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    global ruta_archivo
    ruta_archivo = os.path.join(ruta_carpeta, 'config.txt')
    try:
        with open(ruta_archivo, 'rt') as _archivo_config:
            return False
    except FileNotFoundError:
        with open(ruta_archivo, 'wt') as archivo_config:
            contenido_lineas = "journal\n"
            archivo_config.write(contenido_lineas * 2)
            return True


def obtener_config(config_deseada: str):
    global ruta_archivo
    config_file = open(ruta_archivo, 'rt')
    config_lines = config_file.readlines()
    config_file.close()
    tema = config_lines[0].replace('\n', '')
    if config_deseada.lower() == 'tema':
        return tema
    return None


def no_contiene_letras(cadena):
    return not any(caracter.isalpha() for caracter in cadena)


def cambiar_tema_config(tema_new):
    global ruta_archivo
    config_file = open(ruta_archivo, 'rt')
    config_lines = config_file.readlines()
    config_file.close()

    config_lines[0] = f'{tema_new}\n'

    config_file = open(ruta_archivo, 'wt')
    config_file.writelines(config_lines)
    config_file.close()


def cambiar_ruta_bdd(ruta_new):
    global ruta_archivo
    with open(ruta_archivo, 'rt') as config_file:
        config_lines = config_file.readlines()

    config_lines[1] = ruta_new

    with open(ruta_archivo, 'wt') as config_file:
        config_file.writelines(config_lines)


def cambiar_modo(actual, window, str_modo):
    if actual == 'journal':
        window.style.theme_use('darkly')
        actual = 'darkly'
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        menu_button_style = ttk.Style()
        menu_button_style.configure('my.TButton', font='arial 12 bold')
        danger_button_style = ttk.Style()
        danger_button_style.configure('danger.TButton', font='arial 11 bold')
        success_button_style = ttk.Style()
        success_button_style.configure('success.TButton', font='arial 11 bold')
        warning_button_style = ttk.Style()
        warning_button_style.configure('warning.TButton', font='arial 11 bold')
        str_modo.set('Modo claro')

        cambiar_tema_config(actual)

    else:
        window.style.theme_use('journal')
        actual = 'journal'
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        menu_button_style = ttk.Style()
        menu_button_style.configure('my.TButton', font='arial 12 bold')
        danger_button_style = ttk.Style()
        danger_button_style.configure('danger.TButton', font='arial 11 bold')
        success_button_style = ttk.Style()
        success_button_style.configure('success.TButton', font='arial 11 bold')
        danger_button_style = ttk.Style()
        danger_button_style.configure('danger.TButton', font='arial 11 bold')
        str_modo.set('Modo oscuro')

        cambiar_tema_config(actual)


def buscar_base_de_datos():
    def abrir_explorador():
        ruta_var.set(filedialog.askopenfilename())
        etiqueta_ruta.config(text=f'Ruta seleccionada: {ruta_var.get()}')

    def confirmar_ruta():
        if ruta_var.get() != '':
            cambiar_ruta_bdd(ruta_var.get())
            window.destroy()
        else:
            messagebox.showerror('Ruta incompleta', 'Porfavor ingrese una ruta valida')

    window = ttk.Window()
    window.title('Seleccionar ruta de la base de datos')
    window.geometry('500x400')

    ruta_var = ttk.StringVar(value='')

    boton_explorador = ttk.Button(master=window, text='Buscar ruta', command=abrir_explorador)
    boton_explorador.pack(pady=20)

    boton_aceptar = ttk.Button(master=window, text='Confirmar', command=confirmar_ruta)

    etiqueta_ruta = ttk.Label(window, text='Ruta seleccionada: None')
    etiqueta_ruta.pack()
    boton_aceptar.pack()

    window.mainloop()


def encontrar_ruta_icono_old():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # En el caso de PyInstaller
        base_path = sys._MEIPASS
    else:
        # En el caso de ejecutar directamente el script
        base_path = os.path.abspath(".")

    # Construir la ruta al archivo de icono
    icon_path = os.path.join(base_path, "program_icon.ico")
    return icon_path


def encontrar_ruta_icono():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # En el caso de PyInstaller
        base_path = sys._MEIPASS
    else:
        # En el caso de ejecutar directamente el script
        base_path = os.path.abspath(".")

    # Construir la ruta al archivo de icono
    icon_path = os.path.join(base_path, "program_icon.png")
    return icon_path


def calcular_res_ventana():
    monitores = get_monitors()
    ancho = int(monitores[0].width // 1.3)
    alto = int(monitores[0].height // 1.3)
    return f'{ancho}x{alto}', ancho, alto


def volver_al_menu(ventana_secundaria, ventana_principal):
    ventana_secundaria.destroy()
    #ventana_principal.state('zoomed') funciona en windows, no en linux
    ventana_principal.attributes('-zoomed', True)
    ventana_principal.deiconify()


def busqueda(str_var_buscado):
    buscado = str_var_buscado.get()
    if buscado == '':
        return None

    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Productos WHERE producto LIKE ?"
                   " OR detalle LIKE ? OR codigo LIKE ? OR codigo_de_barras LIKE ?",
                   (f'%{buscado}%', f'%{buscado}%', f'%{buscado}%', f'%{buscado}%'))
    encontrado = cursor.fetchall()

    connection.close()
    return encontrado


def busqueda_no_stock(str_var_buscado):
    buscado = str_var_buscado.get()
    if buscado == '':
        return None
    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Productos WHERE (producto LIKE ?"
                   " OR detalle LIKE ? OR codigo LIKE ? OR codigo_de_barras LIKE ?) AND stock < 1",
                   (f'%{buscado}%', f'%{buscado}%', f'%{buscado}%', f'%{buscado}%'))
    encontrado = cursor.fetchall()

    connection.close()
    return encontrado


def busqueda_por_id(id_buscado):
    if id_buscado == '':
        return None
    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM Productos WHERE id = {id_buscado}")
    encontrado = cursor.fetchall()

    connection.close()
    return encontrado


def busqueda_multiples_ids(ids_buscadas):
    if ids_buscadas == '' or ids_buscadas == () or ids_buscadas == []:
        return None
    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    encontrado = ()
    for id_buscado in ids_buscadas:
        cursor.execute(f"SELECT * FROM Productos WHERE id = {id_buscado}")
        encontrado = encontrado + tuple(cursor.fetchall())

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
                                                                  tupla[3], tupla[4], tupla[6], tupla[0]),
                                tags=('par',))
        else:
            treeview_var.insert("", "end", text=tupla[1], values=(tupla[2],
                                                                  tupla[3], tupla[4], tupla[6], tupla[0]),
                                tags=('impar',))
        contador += 1
    return


def registrar_venta(id_producto, amount, product_price):
    # obtener fecha y hora
    fecha_hora_actual = datetime.datetime.now()
    formato_fecha = "%#d/%#m/%Y"
    formato_hora = "%H:%M:%S"
    fecha = fecha_hora_actual.strftime(formato_fecha)
    hora = fecha_hora_actual.strftime(formato_hora)

    # conectar a base de datos
    global ruta_bdd
    with sqlite3.connect(ruta_bdd) as connection_db:
        cursor = connection_db.cursor()
        try:
            a = int(amount)
            if a <= 0:
                raise ValueError('cero o negativo no es una cantidad valida')
        except ValueError:
            amount = 1

        precio = float(product_price.replace('$', ''))
        total_price = round((precio * int(amount)), 2)
        datos_venta = (int(id_producto), int(amount), fecha, hora, total_price)
        cursor.execute(f'''
            INSERT INTO Ventas (product_id, cantidad, fecha, hora, total_price)
            VALUES (?,?,?,?,?)
            ''', datos_venta)
        connection_db.commit()
    return


def actualizar_stock(id_producto, cantidad):
    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()
    cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, id_producto))
    connection.commit()
    connection.close()
    return


def es_valido(precio):
    patron = re.compile(r'^\$?\d+$')
    if patron.match(precio):
        return True
    return False


def es_valido_stock(stock: str):
    if stock.isdigit() and int(stock) > 0:
        return True
    return False


def add_to_db(vector):
    vector[5] = int(vector[5])

    if not es_valido(vector[2]):
        raise SyntaxError

    if '$' not in vector[2]:
        vector[2] = f'${vector[2]}'

    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Productos (producto, codigo, precio, detalle, codigo_de_barras, stock)
                   VALUES (?, ?, ?, ?, ?, ?)''', vector)
    connection.commit()
    connection.close()
    return True


def get_all():
    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM Productos''')
    all_items = cursor.fetchall()

    connection.close()

    return all_items


def get_no_stock():
    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM Productos WHERE stock < 1''')
    all_items = cursor.fetchall()

    connection.close()

    return all_items


def update_all(percent=0):
    percent_multiplier = round((1 + int(percent) / 100.0), 2)
    global ruta_bdd

    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute("SELECT id, precio FROM productos")
    all_items = cursor.fetchall()

    for tupla_item in all_items:
        product_id, current_price_str = tupla_item
        current_price_str = current_price_str.replace(',', '.').replace('$', '')

        current_price = round(float(current_price_str), 2)
        new_price = round((current_price * percent_multiplier), 2)

        cursor.execute("UPDATE productos SET precio = ? WHERE id = ?",
                       (f'${new_price}', product_id))

    connection.commit()
    connection.close()


def update_selected(ids_list, percent=0):
    percent_multiplier = round((1 + int(percent) / 100.0), 2)
    global ruta_bdd

    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    for prod in ids_list:
        cursor.execute("SELECT precio FROM productos WHERE id = ?", (prod,))
        tupla_item = cursor.fetchone()

        current_price_str = tupla_item[0]
        current_price_str = current_price_str.replace(',', '.').replace('$', '')

        current_price = round(float(current_price_str), 2)
        new_price = round((current_price * percent_multiplier), 2)

        cursor.execute("UPDATE productos SET precio = ? WHERE id = ?",
                       (f'${new_price}', prod))

        connection.commit()
    connection.close()


def update_price_to_new(ids_list, new_price):
    global ruta_bdd

    if not es_valido(new_price):
        raise SyntaxError

    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    for prod in ids_list:

        if '$' not in new_price:
            new_price = f'${new_price}'

        cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (f'{new_price}', prod))

        connection.commit()
    connection.close()


def busqueda_venta_fecha(str_fecha_buscada):
    buscado = str_fecha_buscada.get()
    if buscado == '':
        return None
    global ruta_bdd
    connection = sqlite3.connect(ruta_bdd)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Ventas WHERE fecha = ?", (f'{buscado}',))
    encontrado = cursor.fetchall()

    connection.close()
    return encontrado


def obtener_ventas_mes(var_fecha_del_mes):
    str_fecha_mes = str(var_fecha_del_mes.get())
    tupla_fecha = str_fecha_mes.split('/')
    mes = tupla_fecha[1]
    ventas_del_mes = []

    global ruta_bdd
    with sqlite3.connect(ruta_bdd) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Ventas")
        retornado = cursor.fetchall()
    for venta in retornado:
        fecha_tpl = venta[3].split('/')
        if fecha_tpl[1] == mes:
            ventas_del_mes.append(venta)
    return ventas_del_mes


def buscar_nombre_por_id(product_id):
    global ruta_bdd
    with sqlite3.connect(ruta_bdd) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT producto FROM Productos WHERE id = ?", (product_id,))
        found = cursor.fetchone()
    if found:
        return found
    return 'No encontrado'


def pasar_al_cuadro_ventas(matrix, treeview_var):
    treeview_var.delete(*treeview_var.get_children())
    contador = 0
    for tupla in matrix:
        nombre_prod, = buscar_nombre_por_id(tupla[1])

        if contador % 2 == 0:
            treeview_var.insert("", "end", tags=('par',), text=nombre_prod, values=(tupla[2], f'${tupla[5]}',
                                                                                    tupla[3], tupla[4]))
        else:
            treeview_var.insert("", "end", tags=('impar',), text=nombre_prod, values=(tupla[2], f'${tupla[5]}',
                                                                                      tupla[3], tupla[4]))
        contador += 1
    return


def calcular_total_del_dia(matrix):
    try:
        acumulador = 0
        for tupla in matrix:
            acumulador += tupla[5]
        return f'${acumulador}'
    except ValueError:
        return "Error al calcular"


def add_to_stock(ids_list, stock_to_add):
    global ruta_bdd

    if not es_valido_stock(str(stock_to_add)):
        raise SyntaxError

    with sqlite3.connect(ruta_bdd) as connection:
        cursor = connection.cursor()
        for prod in ids_list:

            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?",
                           (int(stock_to_add), prod))

        connection.commit()


def update_info_product_bdd(current_data, new_data):
    global ruta_bdd

    print('current data:', current_data)

    print()

    print('new data:', new_data)

    for i in range(len(new_data)):
        if new_data[i] == '' or new_data[i] == '$':
            new_data[i] = current_data[i+1]

    if not es_valido(new_data[2]):
        raise SyntaxError

    if '$' not in new_data[2]:
        new_data[2] = f'${new_data[2]}'

    with sqlite3.connect(ruta_bdd) as connection:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE productos SET "
            "producto = ?, codigo = ?, precio = ?, detalle = ?, codigo_de_barras = ?, stock = ? "
            "WHERE id = ?",
            (new_data[0], new_data[1], new_data[2],
             new_data[3], new_data[4], new_data[5], current_data[0]))

        connection.commit()
