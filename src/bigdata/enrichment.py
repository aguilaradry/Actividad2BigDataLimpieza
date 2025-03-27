import pandas as pd
import os
from datetime import datetime
from zoneinfo import ZoneInfo

class DataEnrichment:
    def __init__(self):
        self.cleaned_csv_path = "src/bigdata/static/csv/cleaned_data.csv"
        self.additional_csv_path = "src/bigdata/static/csv/additional_info.csv"
        self.enriched_csv_path = "src/bigdata/static/csv/enriched_data.csv"
        self.audit_path = "src/bigdata/static/auditoria/enriched_report.txt"

        os.makedirs(os.path.dirname(self.enriched_csv_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)

    def cargar_datasets(self):
        print("Cargando datasets...")
        cleaned_df = pd.read_csv(self.cleaned_csv_path)
        additional_df = pd.read_csv(self.additional_csv_path)
        return cleaned_df, additional_df

    def enriquecer_datos(self, cleaned_df, additional_df):
        print("Enriqueciendo datos...")
        enriched_df = pd.merge(cleaned_df, additional_df, on="id", how="left")
        return enriched_df

    def guardar_datos(self, enriched_df):
        print("Guardando dataset enriquecido...")
        enriched_df.to_csv(self.enriched_csv_path, index=False)

    def generar_auditoria(self, cleaned_df, additional_df, enriched_df):
        print("Generando auditoría de enriquecimiento...")
        zona_horaria = ZoneInfo("America/Bogota")
        fecha_hora = datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')

        registros_enriquecidos = enriched_df['plataforma'].notnull().sum()
        registros_no_encontrados = enriched_df['plataforma'].isnull().sum()

        with open(self.audit_path, "w", encoding="utf-8") as f:
            f.write(f" Auditoría de Enriquecimiento - {fecha_hora}\n")
            f.write("=" * 70 + "\n")
            f.write(f"Total registros base: {len(cleaned_df)}\n")
            f.write(f"Total registros adicionales: {len(additional_df)}\n")
            f.write(f"Total registros enriquecidos: {len(enriched_df)}\n")
            f.write(f"Registros con información adicional: {registros_enriquecidos}\n")
            f.write(f"Registros sin información adicional: {registros_no_encontrados}\n")
            f.write("\nTransformaciones aplicadas:\n")
            f.write("- Unión de datasets por columna 'id'\n")
            f.write("- Integración de columnas: plataforma, calificación, tamaño (GB)\n")

    def ejecutar_proceso(self):
        cleaned_df, additional_df = self.cargar_datasets()
        enriched_df = self.enriquecer_datos(cleaned_df, additional_df)
        self.guardar_datos(enriched_df)
        self.generar_auditoria(cleaned_df, additional_df, enriched_df)
        print("Proceso de enriquecimiento completado con éxito.")

if __name__ == "__main__":
    enricher = DataEnrichment()
    enricher.ejecutar_proceso()