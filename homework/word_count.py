"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import string
import time
from itertools import groupby

#
# Escriba la funcion que  genere n copias de los archivos de texto en la
# carpeta files/raw en la carpeta files/input. El nombre de los archivos
# generados debe ser el mismo que el de los archivos originales, pero con
# un sufijo que indique el número de copia. Por ejemplo, si el archivo
# original se llama text0.txt, el archivo generado se llamará text0_1.txt,
# text0_2.txt, etc.
#

def copy_raw_files_to_input_folder(n):
    """Funcion copy_files"""

    # Mira si existe la carpeta
    if os.path.exists("files/input"):
        for file in glob.glob("files/input/*"):
            os.remove(file) # Borra archivos del directorio
        os.rmdir("files/input") # Borra la carpeta

    os.makedirs("files/input") # Crea la carpeta input

    # Itera sobre todos los archivos en 'files/raw/'
    for file in glob.glob("files/raw/*"):
        for i in range(1, n + 1):
            with open(file, "r", encoding="utf-8") as f:
                # Crea un nuevo archivo en 'files/input' con sufijo numérico
                with open(
                    f"files/input/{os.path.basename(file).split('.')[0]}_{i}.txt",
                    "w",
                    encoding="utf-8",
                ) as f2:
                    # Copia el contenido del archivo original
                    f2.write(f.read())
                    
#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#
def load_input(input_directory):
    """Funcion load_input"""

    # Creamos una lista vacía donde se almacenarán las líneas de los archivos junto con sus nombres
    sequence = []

    # Usamos glob para obtener todos los archivos dentro del directorio de entrada (input_directory)
    # El patrón '*' indica que queremos todos los archivos sin importar su extensión
    files = glob.glob(f"{input_directory}/*")

    # Abrimos todos los archivos a la vez usando fileinput, que permite iterar sobre varios archivos como si fueran uno solo
    with fileinput.input(files=files) as f:
        # Iteramos línea por línea a través de todos los archivos
        for line in f:
            # Agregamos a la lista 'sequence' una tupla que contiene:
            # - El nombre del archivo actual
            # - La línea de texto actual
            sequence.append((fileinput.filename(), line))
    return sequence

#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence):
    """Line Preprocessing"""
    # Elimina signos de puntuación y convierte a minúsculas cada valor de la secuencia
    sequence = [
        (key, value.translate(str.maketrans("", "", string.punctuation)).lower())
        for key, value in sequence
    ]
    return sequence
  
#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#

def mapper(sequence):
    """Mapper"""
    # Esta línea toma una secuencia de pares (clave, valor), divide cada valor en palabras y 
    # genera una lista de tuplas (palabra, 1) para cada palabra encontrada.
    return [(word, 1) for _, value in sequence for word in value.split()]


# 
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    # Ordena la secuencia por la clave (primer elemento de cada tupla)
    return sorted(sequence, key=lambda x: x[0])


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    """Reducer"""
    result = []
    # Agrupa los elementos consecutivos que comparten la misma clave
    for key, group in groupby(sequence, lambda x: x[0]):
        # Suma todos los valores asociados a la clave
        result.append((key, sum(value for _, value in group)))
    return result


#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#
def create_ouptput_directory(output_directory):
    """Create Output Directory"""

    # Si el directorio de salida existe, elimina todos sus archivos y luego el directorio
    if os.path.exists(output_directory):
        for file in glob.glob(f"{output_directory}/*"):
            os.remove(file)           # Elimina cada archivo dentro del directorio
        os.rmdir(output_directory)    # Elimina el directorio vacío

    # Crea nuevamente el directorio de salida
    os.makedirs(output_directory)

#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """Save Output"""

    # Escribe la secuencia en un archivo llamado 'part-00000', usando tabulador como separador
    with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n") # Escribe una línea en el archivo



#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""
    # Crear un archivo de marcacion para confirmar que corre todo (lo hace la maquina maestro)
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")

#
# Escriba la función job, la cual orquesta las funciones anteriores.
# from pprint import pprint

def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = line_preprocessing(sequence)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_ouptput_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory) 



if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
