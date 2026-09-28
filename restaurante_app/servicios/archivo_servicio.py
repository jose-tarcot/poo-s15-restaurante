import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, carpeta_datos: str | Path) -> None:
        self.carpeta_datos = Path(carpeta_datos)

    def leer_json(self, nombre_archivo: str) -> list:
        # Lee un archivo JSON de la carpeta de datos y devuelve su contenido como lista.
        ruta = self.carpeta_datos / nombre_archivo

        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            print(f"No se encontro {nombre_archivo}. Se continua con una lista vacia.")
            return []
        except json.JSONDecodeError:
            print(f"El archivo {nombre_archivo} tiene un formato JSON invalido.")
            return []
        except PermissionError:
            print(f"No hay permisos suficientes para leer {nombre_archivo}.")
            return []

        if not isinstance(datos, list):
            print(f"El contenido de {nombre_archivo} debe ser una lista.")
            return []

        return datos

    def escribir_json(self, nombre_archivo: str, datos: list) -> bool:
        # Guarda la informacion en disco; se conserva para la evolucion del proyecto.
        ruta = self.carpeta_datos / nombre_archivo

        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with ruta.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"No hay permisos suficientes para escribir {nombre_archivo}.")
            return False
