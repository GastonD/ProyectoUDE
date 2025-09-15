#main.py
# Proyecto 4
# Integrantes: Camila Guerra - Gastón D'Avola

import pandas as pd
import json
import os

# --- Definición de Rutas ---
# Establecemos una variable con el nombre de la carpeta donde se encuentran los datasets
# con el fin de crear una ruta
datasets_folder = 'dataset'

# Nombre de los archivos de entrada (JSON) y salida (CSV)
json_input_filename = 'pokemonDB_dataset.json'
csv_output_filename = 'Datos_en_CSV.csv'

# Construir las rutas completas para los archivos
# Usamos os.path.join() para crear las rutas para ir a buscar el archivo JSON y 
# para guardar el archivo CSV
json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), datasets_folder, json_input_filename)
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), datasets_folder, csv_output_filename)

# --- Lógica de lectura y escritura de archivos ---
# Dentro del bloque try iniciamos la apertura del archivo JSON y la lectura
# Con este bloque buscamos capturar errores mediante excepciones
# Capturamos el más común que es que el archivo a abrir no exista
# Y luego una excepción genérica para el resto de los errores posibles
try:

    # Inicialización del programa
    print("=" * 100)
    print("Convertidor de JSON a CSV usando Pandas")
    print("=" * 100)
    print("\n")
    # Leer el archivo JSON y cargarlo en un DataFrame de pandas de acuerdo a la consigna
    # Mostramos la ruta del archivo JSON que se está leyendo
    print(f"Leyendo el archivo JSON desde: {json_file_path}")
    print("\n")
    #Abro el archivo JSON y utilizo el método para abrirlo:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Con algunos de los datasets que nos descargamos tuvimos problemas para que los datos
    # queden en el formato correcto al pasarlo a CSV
    # Encontramos esta solución que depende el tipo de JSON que recibe 
    # Genera el dataFrame con métodos distintos
    if isinstance(data, dict):
        df = pd.DataFrame.from_dict(data, orient='index')
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        print("Error: El formato del JSON no es compatible")
        raise json.JSONDecodeError

    # Si el archivo es leido correctamente mostramos las primeras 5 filas utilizando print(df.head())
    # Como método de validación interno
    print("=" * 100)
    print("\nDatos leídos del JSON exitosamente. Mostrando las primeras 5 filas:")
    print(df.head())
    print("=" * 100)
    print("\n")
    
    # Escribimos el DataFrame en un CSV
    # Utilizamos la misma función del DataFrame to_csv() para generar el CSV
    # En la ruta que generamos anteriormente
    print("=" * 100)
    print(f"\nGuardando los datos en formato CSV en: {csv_file_path}")
    df.to_csv(csv_file_path, index=True, encoding='utf-8')
    print("=" * 100)
    print("\n")
    # Finalmente hacemos una confirmación para el usuario si el CSV se generó exitosamente.
    print("\n¡Proceso completado! El archivo CSV ha sido creado exitosamente.")

except FileNotFoundError:
    # Manejo de error de el archivo no encontrado
    print(f"Error: No se encontró el archivo en la ruta especificada: {json_file_path}")
    print(f"Por favor, asegúrate de que la carpeta '{datasets_folder}' exista y contenga el archivo {json_input_filename}.")
except json.JSONDecodeError:
    print(f"Error: El formato del JSON no es compatible")
except Exception as e:
    # Manejo de errores genéricos
    print(f"Ocurrió un error inesperado: {e}")