import os
import json
import requests
import sqlite3
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

class Ingestion:
    def __init__(self):
        self.api_url = "https://api.sampleapis.com/switch/games"
        self.db_path = "src/bigdata/static/db/ingestion.db"
        self.xlsx_path = "src/bigdata/static/xlsx/ingestion.xlsx"
        self.audit_path = "src/bigdata/static/auditoria/ingestion.txt"

        # Crear las carpetas necesarias si no existen
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.xlsx_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)

    def obtener_datos(self):
        print("Obteniendo datos de la API...")
        response = requests.get(self.api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            juegos_procesados = []
            for game in data[:200]:  # Limitamos a 100 juegos
                juegos_procesados.append({
                    "id": game.get("id", "N/A"),
                    "nombre": str(game.get("name", "Desconocido")),  
                    "genero": ", ".join(game.get("genre", ["Desconocido"])) if isinstance(game.get("genre"), list) else str(game.get("genre", "Desconocido")),
                    "desarrolladores": ", ".join(game.get("developers", ["Desconocido"])) if isinstance(game.get("developers"), list) else "Desconocido",
                    "publicadores": ", ".join(game.get("publishers", ["Desconocido"])) if isinstance(game.get("publishers"), list) else "Desconocido",
                    "fecha_lanzamiento": game.get("releaseDates", {}).get("NorthAmerica", "Desconocido")  # Solo fecha de Norteamérica

                })
            
            return juegos_procesados
        
        else:
            print("Error al obtener datos de la API")
            return []

    def guardar_en_db(self, datos):
        print("Guardando datos en SQLite...")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)  # Asegurar que la carpeta de la BD existe
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Eliminar la tabla si existe
        cursor.execute("DROP TABLE IF EXISTS videojuegos")

        # Crear la tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videojuegos (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                genero TEXT,
                desarrolladores TEXT,
                publicadores TEXT,
                fecha_lanzamiento TEXT
            )
        """)

        # Insertar datos con conversión segura
        cursor.executemany("""
            INSERT OR REPLACE INTO videojuegos (id, nombre, genero, desarrolladores, publicadores, fecha_lanzamiento)
            VALUES (:id, :nombre, :genero, :desarrolladores, :publicadores, :fecha_lanzamiento)
        """, [{k: v if v is not None else "Desconocido" for k, v in game.items()} for game in datos])

        conn.commit()
        conn.close()

    def generar_xlsx(self, datos):
        print("Generando archivo Excel...")
        os.makedirs(os.path.dirname(self.xlsx_path), exist_ok=True)  # Asegurar que la carpeta de XLSX existe
        df = pd.DataFrame(datos)
        df.to_excel(self.xlsx_path, index=False, engine="openpyxl")

    def generar_auditoria(self, datos):
        print("Generando archivo de auditoría...")
        os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)  # Asegurar que la carpeta de auditoría existe
        conn = sqlite3.connect(self.db_path)
        db_df = pd.read_sql_query("SELECT * FROM videojuegos", conn)
        conn.close()

        zona_horaria = ZoneInfo("America/Bogota")  # Cambia según tu zona
        fecha_hora = datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')
        with open(self.audit_path, "w", encoding="utf-8") as f:
            f.write(f" Auditoría de Ingesta - {fecha_hora}\n")
            f.write("=" * 46 + "\n")
            f.write(f"Registros obtenidos de la API: {len(datos)}\n")
            f.write(f"Registros en la base de datos: {len(db_df)}\n")
            if len(datos) == len(db_df):
                f.write("Los registros coinciden correctamente.\n")
            else:
                f.write("Advertencia: Discrepancia en los registros.\n")

    def ejecutar_ingesta(self):
        datos = self.obtener_datos()
        if datos:
            self.guardar_en_db(datos)
            self.generar_xlsx(datos)
            self.generar_auditoria(datos)
            print("Ingesta completada con éxito.")
        else:
            print("No se pudo completar la ingesta.")

if __name__ == "__main__":
    ingestion = Ingestion()
    ingestion.ejecutar_ingesta()
