#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa para convertir archivos JSON a CSV utilizando Pandas y DataFrames
Autor: Gastón D'Avola
Fecha: 2024

DECISIÓN DE LIBRERÍAS:
- pandas: Librería principal para manipulación de datos estructurados
  * Ventajas: Manejo eficiente de DataFrames, conversión nativa JSON/CSV
  * Alternativas consideradas: csv (nativo), numpy (menos funcionalidades)
  * Justificación: Pandas ofrece métodos directos read_json() y to_csv()

- json: Librería estándar de Python para manejo de JSON
  * Ventajas: Lectura segura con manejo de errores, control de encoding
  * Alternativas: pandas.read_json() directamente
  * Justificación: Mayor control sobre el proceso de lectura y validación

- os: Librería estándar para operaciones del sistema operativo
  * Ventajas: Manejo de rutas multiplataforma, verificación de archivos
  * Alternativas: pathlib (más moderno)
  * Justificación: Compatibilidad y funcionalidades específicas necesarias

- pathlib: Librería moderna para manejo de rutas
  * Ventajas: Sintaxis más limpia, orientada a objetos
  * Uso: Solo para generar nombres de archivos automáticamente
  * Justificación: Complementa os.path con funcionalidades adicionales
"""

import pandas as pd  # Manipulación de datos estructurados y conversión JSON/CSV
import os           # Operaciones del sistema operativo y manejo de rutas
import json         # Lectura y validación de archivos JSON
from pathlib import Path  # Generación automática de nombres de archivos


def json_to_csv(json_file_path, csv_file_path=None, encoding='utf-8'):
    """
    Convierte un archivo JSON a formato CSV usando Pandas DataFrame
    
    LÓGICA DEL ALGORITMO:
    1. Validación de entrada: Verificar existencia del archivo JSON
    2. Lectura segura: Usar context manager para manejo automático de archivos
    3. Detección de formato: Identificar si el JSON es objeto o array
    4. Conversión a DataFrame: Aplicar método apropiado según el formato
    5. Generación de CSV: Exportar con configuración óptima
    6. Validación de salida: Confirmar creación exitosa del archivo
    
    Args:
        json_file_path (str): Ruta del archivo JSON de entrada
        csv_file_path (str, optional): Ruta del archivo CSV de salida. 
                                      Si no se especifica, se genera automáticamente
        encoding (str): Codificación del archivo (default: 'utf-8')
    
    Returns:
        bool: True si la conversión fue exitosa, False en caso contrario
    """
    
    try:
        # PASO 1: VALIDACIÓN DE ENTRADA
        # Verificar existencia del archivo antes de procesarlo
        # Esto evita errores costosos y proporciona feedback claro al usuario
        if not os.path.exists(json_file_path):
            print(f"❌ Error: El archivo JSON no existe en la ruta: {json_file_path}")
            return False
        
        print(f"📖 Leyendo archivo JSON desde: {json_file_path}")
        
        # PASO 2: LECTURA SEGURA DEL JSON
        # Usar context manager ('with') para garantizar cierre automático del archivo
        # Especificar encoding explícitamente para evitar problemas con caracteres especiales
        with open(json_file_path, 'r', encoding=encoding) as file:
            data = json.load(file)  # json.load() es más eficiente que json.loads() para archivos
        
        # PASO 3: DETECCIÓN DE FORMATO Y CONVERSIÓN A DATAFRAME
        # El JSON puede tener dos formatos principales:
        # - Objeto/Diccionario: {clave1: {datos}, clave2: {datos}}
        # - Array/Lista: [{datos1}, {datos2}, {datos3}]
        if isinstance(data, dict):
            # Para objetos JSON: usar orient='index' para que las claves se conviertan en índice
            # Esto es ideal para datos como {pokemon1: {stats}, pokemon2: {stats}}
            df = pd.DataFrame.from_dict(data, orient='index')
        elif isinstance(data, list):
            # Para arrays JSON: conversión directa, cada elemento se convierte en una fila
            # Esto es ideal para datos como [{pokemon1}, {pokemon2}, {pokemon3}]
            df = pd.DataFrame(data)
        else:
            # Manejar casos edge: JSON con tipos no soportados (números, strings, etc.)
            print("❌ Error: El formato del JSON no es compatible")
            return False
        
        # PASO 4: GENERACIÓN AUTOMÁTICA DE NOMBRE DE ARCHIVO
        # Si no se especifica nombre de salida, generar uno automáticamente
        # Usar Path.stem para obtener nombre sin extensión del archivo original
        if csv_file_path is None:
            json_name = Path(json_file_path).stem  # Extrae nombre sin .json
            csv_file_path = f"{json_name}_converted.csv"  # Agrega sufijo descriptivo
        
        # PASO 5: INFORMACIÓN DIAGNÓSTICA DEL DATAFRAME
        # Mostrar estadísticas básicas para validar la conversión
        # Esto ayuda al usuario a verificar que los datos se procesaron correctamente
        print(f"✅ Datos cargados exitosamente:")
        print(f"   📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
        print(f"   📋 Columnas: {list(df.columns)}")
        
        # Mostrar muestra representativa de los datos
        # df.head() muestra las primeras 5 filas por defecto
        # to_string() asegura formato legible en consola
        print("\n🔍 Primeras 5 filas del DataFrame:")
        print(df.head().to_string())
        
        # PASO 6: EXPORTACIÓN A CSV
        # Configuración de parámetros:
        # - index=True: Incluir índice del DataFrame (útil para datos con claves)
        # - encoding='utf-8': Asegurar compatibilidad con caracteres especiales
        print(f"\n💾 Guardando archivo CSV en: {csv_file_path}")
        df.to_csv(csv_file_path, index=True, encoding=encoding)
        
        # PASO 7: VALIDACIÓN DE SALIDA
        # Verificar que el archivo se creó exitosamente y mostrar información
        if os.path.exists(csv_file_path):
            file_size = os.path.getsize(csv_file_path)
            print(f"✅ ¡Conversión completada exitosamente!")
            print(f"   📁 Archivo creado: {csv_file_path}")
            print(f"   📏 Tamaño: {file_size:,} bytes")
            return True
        else:
            print("❌ Error: No se pudo crear el archivo CSV")
            return False
            
    except json.JSONDecodeError as e:
        # MANEJO DE ERRORES ESPECÍFICOS: JSON malformado
        # json.JSONDecodeError se activa cuando el archivo no es JSON válido
        # Esto puede ocurrir por: sintaxis incorrecta, caracteres especiales, etc.
        print(f"❌ Error al decodificar JSON: {e}")
        return False
    except Exception as e:
        # MANEJO DE ERRORES GENÉRICOS: Captura cualquier otro error inesperado
        # Esto incluye: errores de permisos, espacio en disco, problemas de memoria, etc.
        print(f"❌ Error inesperado: {e}")
        return False


def main():
    """
    Función principal del programa
    
    ARQUITECTURA DEL PROGRAMA:
    1. Configuración: Definir rutas y nombres de archivos
    2. Validación de entorno: Verificar/crear estructura de carpetas
    3. Ejecución: Llamar función de conversión con parámetros específicos
    4. Reporte: Mostrar resultado final del proceso
    
    DISEÑO DE RUTAS:
    - Usar rutas relativas al script para portabilidad
    - Separar datos en carpeta 'dataset' para organización
    - Generar rutas absolutas para evitar problemas de directorio de trabajo
    """
    print("🚀 Convertidor de JSON a CSV usando Pandas")
    print("=" * 50)
    
    # CONFIGURACIÓN DE RUTAS Y ARCHIVOS
    # Definir nombres de archivos y carpetas de manera centralizada
    # Esto facilita el mantenimiento y modificación del programa
    datasets_folder = 'dataset'                    # Carpeta para almacenar datasets
    json_input_filename = 'pokemonDB_dataset.json'  # Archivo JSON de entrada
    csv_output_filename = 'pokemonDB_converted.csv' # Archivo CSV de salida
    
    # CONSTRUCCIÓN DE RUTAS ABSOLUTAS
    # os.path.abspath(__file__) obtiene la ruta absoluta del script actual
    # os.path.dirname() obtiene el directorio padre del script
    # Esto garantiza que las rutas funcionen independientemente del directorio de trabajo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, datasets_folder, json_input_filename)
    csv_file_path = os.path.join(current_dir, datasets_folder, csv_output_filename)
    
    # VALIDACIÓN Y CREACIÓN DE ESTRUCTURA DE CARPETAS
    # Verificar si la carpeta dataset existe, si no, crearla automáticamente
    # Esto mejora la experiencia del usuario evitando errores por carpetas faltantes
    dataset_path = os.path.join(current_dir, datasets_folder)
    if not os.path.exists(dataset_path):
        print(f"❌ Error: La carpeta '{datasets_folder}' no existe")
        print(f"   Creando carpeta '{datasets_folder}'...")
        # exist_ok=True evita errores si la carpeta ya existe (condición de carrera)
        os.makedirs(dataset_path, exist_ok=True)
        print(f"✅ Carpeta '{datasets_folder}' creada")
    
    # EJECUCIÓN DE LA CONVERSIÓN
    # Llamar a la función principal con las rutas configuradas
    # El valor de retorno indica éxito o fallo del proceso
    success = json_to_csv(json_file_path, csv_file_path)
    
    # REPORTE FINAL DEL PROCESO
    # Mostrar resultado claro al usuario con información relevante
    if success:
        print("\n🎉 ¡Proceso completado exitosamente!")
        print(f"   📄 Archivo JSON: {json_input_filename}")
        print(f"   📊 Archivo CSV: {csv_output_filename}")
    else:
        print("\n💥 El proceso falló. Revisa los errores anteriores.")


# PUNTO DE ENTRADA DEL PROGRAMA
# Esta condición asegura que main() solo se ejecute cuando el script se ejecuta directamente
# No se ejecutará si el archivo se importa como módulo en otro script
if __name__ == "__main__":
    main()


"""
RESUMEN DE DECISIONES DE DISEÑO:

1. ARQUITECTURA MODULAR:
   - Separación de responsabilidades: json_to_csv() para lógica, main() para configuración
   - Funciones reutilizables que pueden ser importadas en otros proyectos
   - Punto de entrada claro con if __name__ == "__main__"

2. MANEJO DE ERRORES ROBUSTO:
   - Validación previa de archivos antes de procesamiento
   - Manejo específico de errores JSON vs errores genéricos
   - Retorno de valores booleanos para indicar éxito/fallo
   - Mensajes de error informativos con emojis para mejor UX

3. FLEXIBILIDAD DE FORMATOS:
   - Soporte para JSON como objeto (diccionario) y array (lista)
   - Detección automática del tipo de datos
   - Generación automática de nombres de archivo de salida

4. CONFIGURACIÓN CENTRALIZADA:
   - Variables de configuración al inicio de main()
   - Rutas absolutas para portabilidad
   - Creación automática de estructura de carpetas

5. EXPERIENCIA DE USUARIO:
   - Mensajes informativos durante el proceso
   - Estadísticas del DataFrame (dimensiones, columnas)
   - Vista previa de los datos procesados
   - Confirmación de archivos creados con tamaño

6. OPTIMIZACIONES DE RENDIMIENTO:
   - Context manager para manejo automático de archivos
   - Lectura eficiente con json.load() vs json.loads()
   - Configuración óptima de pandas para CSV (index=True, encoding)

7. COMPATIBILIDAD:
   - Encoding UTF-8 para caracteres especiales
   - Rutas multiplataforma con os.path.join()
   - Manejo de diferentes tipos de JSON
"""
