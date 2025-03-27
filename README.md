## proyecto_integrador_edwin_sanchez_nikol_tamayo_adriana_aguilar

## Actividad 1: Proyecto de Ingesta de Datos desde una API a SQLite

### Descripción del Proyecto  

Este proyecto automatiza la extracción, almacenamiento y validación de datos desde la API [Sample APIs - Nintendo Switch Games](https://api.sampleapis.com/switch/games) hacia una base de datos SQLite, generando además archivos de auditoría y evidencia en Excel. Todo el desarrollo se realizó en **GitHub Codespaces**.

La automatización se realiza mediante **GitHub Actions**, garantizando que los datos se actualicen sin intervención manual.  


### Metodología de Desarrollo  

#### **Extracción de Datos desde el API**  
- Se seleccionó la API de videojuegos de Nintendo Switch.
- Se creó un script en Python para consumir la API usando `requests`.  
- Se procesaron los datos extraídos asegurando su correcta estructura. 

#### **Almacenamiento en Base de Datos SQLite**  
- Se creó una base de datos en `src/bigdata/static/db/ingestion.db`.
- Se diseñó un esquema con una tabla `videojuegos` para almacenar los datos.
- Se insertaron los datos extraídos de la API en la base de datos.

#### **Generación de Evidencias**  
- **Archivo Excel**: Se usa `pandas` para exportar los datos a `ingestion.xlsx`.  
- **Archivo de Auditoría**: Se compara la cantidad de registros obtenidos de la API y los almacenados en la base de datos. 

#### **Automatización con GitHub Actions**  
- Se configuró un **workflow** que ejecuta la extracción, almacenamiento y generación de evidencias automáticamente.  
- Se verifica que la base de datos y los archivos generados sean correctos.  


### 📂 Estructura del Proyecto  

[proyecto_integrador_edwin_sanchez_nikol_tamayo_adriana_aguilar]
├── setup.py
├── README.md
├── .github
│   └── workflows
│       └── test_actividad1.yml
└── src
    ├── static
    │   ├── auditoria
    │   │   └── ingestion.txt
    │   ├── db
    │   │   └── ingestion.db
    │   └── xlsx
    │       └── ingestion.xlsx
    └── ingestion.py

### **Automatización con GitHub Actions**
El proyecto usa GitHub Actions para ejecutar la ingesta de datos automáticamente.
Srchivo: .github/workflows/test_actividad1.yml
- Se crea un entorno virtual (python -m venv venv)
- Se activa el entorno virtual (./venv/Scripts/activate )
- Se actualiza pip (pip install --upgrade pip)
- Instalación de dependencias (pip install -e .)
- Ejecución del script (python src/bigdata/ingestion.py)
- Commit y push de los cambios

### **Tecnologías Utilizadas**
- Python (Requests, SQLite3, Pandas, OpenPyXL)
- GitHub Codespaces (para desarrollo en la nube)
- GitHub Actions (para la automatización del proceso)
- SQLite (como base de datos para almacenamiento)

Este proyecto permite la extracción y almacenamiento de datos de videojuegos de Nintendo Switch de manera estructurada y automatizada. Gracias a Codespaces, todo el desarrollo se realizó en la nube sin necesidad de configuraciones locales. Además, la integración con GitHub Actions garantiza la ejecución automática y reproducible del proceso.

## Actividad 2: Preprocesamiento y Limpieza de Datos en Plataforma de Big Data en la Nube

### Descripción
En esta actividad, se llevó a cabo un análisis exploratorio de datos (EDA) utilizando Pandas y SQLite, con el objetivo de identificar problemas de calidad en los datos. Posteriormente, se aplicaron técnicas de limpieza para corregir estos problemas y almacenr los datos limpios en un archivo de formato CSV.

### Objetivos

- Cargar los datos desde una base SQLite.
- Realizar un análisis exploratorio para identificar:
    - Registros duplicados
    - Valores nulos
    - Inconsistencias en tipos de datos
- Introducir errores en los datos para simular problemas de calidad.
- Aplicar técnicas de limpieza de datos para corregir los problemas detectados.
- Generar un informe de auditoría con los cambios realizados.
- Configurar un workflow en GitHub Actions para integrar el script de preprocesamiento y limpieza 

### Análisis Exploratorio
Se identificaron los siguientes problemas en los datos:
- Duplicados → Se introdujeron 10 registros duplicados y se eliminaron en la limpieza.
- Valores nulos → Se detectaron valores nulos en la columna "desarrolladores", que fueron reemplazados por "Desconocido".
- Errores en nombres → Se limpiaron nombres eliminando caracteres especiales como #.
- Formato de fechas → Se convirtieron a formato YYYY-MM-DD.
- Conversión de fechas (valores vacíos se reemplazan con la fecha actual)

### Técnicas de Limpieza Aplicadas
- Eliminación de duplicados
- Imputación de valores nulos
- Normalización de nombres y géneros
- Corrección de formato en las fechas
- Transformaciones en los tipos de datos

### Reportes Generados
- exploratory_analysis.txt → Análisis de los datos antes de la limpieza
- cleaning_report.txt → Transformaciones aplicadas en la limpieza
- cleaned_data.csv → Datos limpios listos para su uso

### 📂 Estructura del proyecto después de la actividad 2
.github/workflows/
│── test_proyecto.yml               # Archivo de configuración para CI/CD
src/bigdata/
│── static/
│   ├── auditoria/                   # Carpeta de reportes de auditoría
│   │   ├── cleaning_report.txt      # Registro de la limpieza de datos
│   │   ├── exploratory_analysis.txt # Análisis exploratorio previo a la limpieza
│   │   ├── ingestion.txt            # Registro de la ingesta de datos
│   ├── csv/                         # Datos en formato CSV
│   │   ├── cleaned_data.csv         # Datos después de la limpieza
│   │   ├── dirty_data.csv           # Datos con errores introducidos para pruebas
│   ├── db/                          # Base de datos SQLite
│   │   ├── ingestion.db             # Archivo de la base de datos
│   ├── xlsx/                        # Datos en formato Excel
│   │   ├── ingestion.xlsx           # Archivo Excel con los datos crudos
│── cleaning.py                      # Script para la limpieza de datos
│── ingestion.py                     # Script para la ingestión de datos
│── .gitignore                       # Archivos ignorados por Git
│── README.md                        # Documentación del proyecto
│── setup.py                         # Configuración del entorno y dependencias


## Actividad 3: Enriquecimiento de Datos en Plataforma de Big Data en la Nube

### Descripción
En esta actividad, su objetivo principal es implementar la etapa de enriquecimiento de datos a partir del dataset limpio generado en la Actividad 2.
El proceso consiste en integrar información adicional proveniente de diferentes fuentes para complementar el conjunto de datos base y así mejorar su calidad y valor analítico.

### Objetivos

- Cargar el conjunto de datos limpio generado previamente.
- Integrar información adicional desde archivos en diversos formatos (CSV, JSON, XLSX, TXT, XML, HTML), 
  se escogió el formato CSV
- Generar un archivo enriquecido y un reporte de auditoría que documenten el proceso.
- Automatizar el proceso utilizando GitHub Actions.

### Descripción del Proceso
El script enrichment.py realiza las siguientes tareas:
- Carga de Datasets:
    - Lee el archivo cleaned_data.csv generado en la Actividad 2.
    - Lee el archivo adicional additional_data.csv con información complementaria.
- Enriquecimiento:
    - Combina ambos datasets utilizando la columna id como clave.
    - Agrega las columnas: plataforma, calificacion, tamano_gb.
- Guardado de Resultados:
    - Guarda el dataset enriquecido en: src/csv/enriched_data.csv.
- Generación de Auditoría:
    - Crea un reporte enriched_report.txt que contiene: cantidad de registros coincidentes, registros que no encontraron información adicional y transformaciones aplicadas.

### Automatización
Se incluye un Workflow de GitHub Actions ubicado en .github/workflows/test_proyecto.yml que:
- Ejecute el script de enriquecimiento automáticamente cuando se sube código al repositorio.
- Genere como artefactos los archivos: enriched_data.csv y enriched_report.txt

### 📂 Estructura del proyecto después de la actividad 3

[proyecto_integrador_edwin_sanchez_nikol_tamayo_adriana_aguilar]
├── .github
│   └── workflows
│       └── test_proyecto.yml              # Workflow para la ingesta, limpieza y enriquecimiento
├── src
│   └── bigdata
│       ├── static
│       │   ├── auditoria
│       │   │   ├── cleaning_report.txt    # Reporte de limpieza
│       │   │   ├── exploratory_analysis.txt
│       │   │   ├── ingestion.txt
│       │   │   └── enrichment_report.txt  # Reporte de auditoría del enriquecimiento
│       │   ├── csv
│       │   │   ├── cleaned_data.csv       # Datos limpios
│       │   │   ├── dirty_data.csv         # Datos originales
│       │   │   ├── additional_info.csv    # Datos adicionales para enriquecer
│       │   │   └── enriched_data.csv      # Dataset enriquecido
│       │   ├── db
│       │   │   └── ingestion.db
│       │   └── xlsx
│       │       └── ingestion.xlsx
│       ├── cleaning.py                    # Script de limpieza de datos
│       ├── enrichment.py                  # Script de enriquecimiento de datos
│       └── ingestion.py                   # Script de ingesta de datos
├── .gitignore
├── README.md
└── setup.py