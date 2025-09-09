

def no_contiene_letras(cadena):
    return not any(caracter.isalpha() for caracter in cadena)

# TODO esto debe ser una responsabilidad del controller de ventas (pedir ventas y devolver total)
def calcular_total_del_dia(matrix):
    try:
        acumulador = 0
        for tupla in matrix:
            acumulador += tupla[5]
        return f'${acumulador}'
    except ValueError:
        return "Error al calcular"



