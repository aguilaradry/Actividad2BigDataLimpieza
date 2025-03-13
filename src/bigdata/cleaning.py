import os
import sqlite3
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

class DataCleaning:
    def __init__(self):
        self.db_path = "src/bigdata/static/db/ingestion.db"
        self.dirty_csv_path = "src/bigdata/static/csv/dirty_data.csv"
        self.cleaned_csv_path = "src/bigdata/static/csv/cleaned_data.csv"
        self.audit_path = "src/bigdata/static/auditoria/cleaning_report.txt"
        self.analysis_path = "src/bigdata/static/auditoria/exploratory_analysis.txt"
        
        # Crear carpetas si no existen
        os.makedirs(os.path.dirname(self.dirty_csv_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.cleaned_csv_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)

    def cargar_datos(self):
        print("Cargando datos desde SQLite...")
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM videojuegos", conn)
        conn.close()
        return df

    def ensuciar_datos(self, df):
        # Introduce errores en los datos para simular problemas de calidad 

        df_dirty = df.copy()

        # Duplicar registros
        num_duplicados = int(len(df_dirty) * 0.1)  # 10% de duplicados
        indices_duplicados = random.sample(df_dirty.index.tolist(), num_duplicados)
        df_duplicados = df_dirty.loc[indices_duplicados].copy()
        df_dirty = pd.concat([df_dirty, df_duplicados], ignore_index=True)

        # Agregar valores nulos en la columna 'desarrolladores'
        num_nulos = int(len(df_dirty) * 0.05)  # 5% con valores nulos
        indices_nulos = random.sample(df_dirty.index.tolist(), num_nulos)
        df_dirty.loc[indices_nulos, "desarrolladores"] = None

        # Guardar los datos sucios en CSV
        df_dirty.to_csv(self.dirty_csv_path, index=False)

        return df_dirty

    def analisis_exploratorio(self, df):
        print("Realizando análisis exploratorio...")

        total_registros = len(df)
        total_nulos = df.isnull().sum()
        total_duplicados = df.duplicated().sum()
        informacion = df.info()
        resumen = df.describe(include="all")

        with open(self.analysis_path, "w", encoding="utf-8") as f:
            f.write("Análisis Exploratorio de Datos Sucios\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total de registros: {total_registros}\n")
            f.write(f"Total de duplicados: {total_duplicados}\n")
            f.write("Valores nulos por columna:\n")
            f.write(f"{total_nulos}\n\n")
            f.write("Información general:\n")
            f.write(f"{informacion}\n\n")
            f.write("Resumen estadístico:\n")
            f.write(f"{resumen}\n")

        print(f"Análisis exploratorio guardado en {self.analysis_path}")

    def limpiar_datos(self, df):
        print("Limpiando datos...")

        df_cleaned = df.copy()

        # Eliminar duplicados
        df_cleaned.drop_duplicates()

        # Reemplazar valores nulos en columna 'desarrolladores' con "Desconocido"
        df_cleaned["desarrolladores"].fillna("Desconocido", inplace=True)

        # Normalizar nombres y géneros
        df_cleaned["nombre"] = df_cleaned["nombre"].apply(lambda x: x.capitalize().strip("#") if isinstance(x, str) else "Desconocido")
        df_cleaned["genero"] = df_cleaned["genero"].apply(lambda x: x.capitalize() if isinstance(x, str) else "Desconocido")

        # Limpiar y convertir la columna de fecha
        valores_invalidos_fecha = ["TBA", "Unreleased", "Coming Soon", "-", "Unknown"]
        df_cleaned["fecha"] = df_cleaned["fecha"].apply(lambda x: None if x in valores_invalidos_fecha else x)

        # Convertir fechas válidas a datetime
        df_cleaned["fecha"] = pd.to_datetime(df_cleaned["fecha"], errors='coerce')
        df_cleaned["fecha"] = pd.to_datetime(df_cleaned["fecha"], errors='coerce')  # errors='coerce' Convierte y deja NaT en valores inválidos
        df_cleaned["fecha"] = df_cleaned["fecha"].dt.strftime("%Y-%m-%d")

        return df_cleaned


    def guardar_datos(self, df):
        print("Guardando datos limpios en CSV...")
        df.to_csv(self.cleaned_csv_path, index=False)

    def generar_auditoria(self, original_df, dirty_df, cleaned_df):
        """ Genera un archivo de auditoría con el impacto de la limpieza """
        print("Generando auditoría de limpieza...")
        zona_horaria = ZoneInfo("America/Bogota")
        fecha_hora = datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')

        with open(self.audit_path, "w", encoding="utf-8") as f:
            f.write(f" Auditoría de Limpieza - {fecha_hora}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total registros originales: {len(original_df)}\n")
            f.write(f"Total registros después de ensuciar: {len(dirty_df)}\n")
            f.write(f"Total registros después de limpieza: {len(cleaned_df)}\n")
            f.write(f"Duplicados agregados: {len(dirty_df) - len(original_df)}\n")
            f.write(f"Duplicados eliminados: {len(dirty_df) - len(cleaned_df)}\n")
            f.write(f"Valores nulos introducidos en 'desarrolladores': {dirty_df['desarrolladores'].isnull().sum()}\n")
            f.write("Transformaciones aplicadas:\n")
            f.write("- Nombres normalizados\n")
            f.write("- Géneros ajustados\n")
            f.write("- Valores nulos de 'desarrolladores' reemplazados\n")

    def ejecutar_proceso(self):
        original_df = self.cargar_datos()
        df_dirty = self.ensuciar_datos(original_df)

        # Ejecutar análisis exploratorio después de ensuciar los datos
        self.analisis_exploratorio(df_dirty)

        df_cleaned = self.limpiar_datos(df_dirty)
        self.guardar_datos(df_cleaned)
        self.generar_auditoria(original_df, df_dirty, df_cleaned)

        print("Limpieza completada con éxito.")

if __name__ == "__main__":
    cleaner = DataCleaning()
    cleaner.ejecutar_proceso()