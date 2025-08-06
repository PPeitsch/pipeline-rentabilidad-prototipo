# Análisis y Limpieza de Datos de Rentabilidad

Este proyecto contiene un análisis exploratorio y un pipeline de limpieza de datos para un conjunto de datos de rentabilidad de productos. El objetivo es transformar datos crudos con problemas de calidad en un conjunto de datos limpio, validado y listo para el análisis o para ser cargado en un data warehouse.

Este proyecto utiliza `pre-commit` para garantizar la calidad y el estilo del código, y `pip-tools` para un manejo de dependencias robusto y reproducible.

## Lógica de Limpieza Aplicada

El pipeline de limpieza implementado en `src/data_cleaner.py` realiza las siguientes transformaciones clave:

-   **Normalización de Nombres de Columnas:** Convierte los nombres a un formato estándar de Python (minúsculas, con guiones bajos, sin caracteres especiales).
-   **Conversión de Tipos de Datos:** Asegura que las columnas numéricas (como `precio_venta`) y de fecha estén en su formato correcto (`float`, `datetime`).
-   **Registros Duplicados:** Elimina SKUs duplicados, conservando el registro con la fecha de actualización más reciente.
-   **Manejo de Valores Nulos:** Imputa valores faltantes en columnas categóricas y elimina filas donde datos críticos (como precios o fechas) son nulos.
-   **Limpieza de Texto:** Elimina espacios en blanco innecesarios en todas las columnas de texto.

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera para mantener una clara separación de responsabilidades:

```
analisis_rentabilidad/
├── .gitignore
├── .pre-commit-config.yaml # Configuración para los hooks de pre-commit
├── data/
│   └── rentabilidad_productos.csv # Archivo de datos de entrada
├── notebooks/
│   └── analisis_y_limpieza.ipynb  # Notebook para exploración y orquestación
├── src/
│   └── data_cleaner.py          # Módulo Python con la lógica de limpieza
├── requirements.in              # Dependencias de la aplicación
├── dev-requirements.in          # Dependencias de desarrollo
├── requirements.txt             # Generado por pip-compile
└── README.md
```
-   **`src/`**: Contiene el código fuente modular y reutilizable, principalmente el pipeline de limpieza.
-   **`notebooks/`**: Contiene los Jupyter Notebooks utilizados para el análisis exploratorio, la visualización y la narración del proceso.
-   **`data/`**: Destinado a contener los datos de entrada crudos y los datos de salida procesados.

## Resultado (Output)

Al ejecutar el notebook `analisis_y_limpieza.ipynb`, se genera el siguiente archivo:

-   **`data/rentabilidad_productos_limpio.parquet`**: Un archivo en formato Parquet que contiene los datos limpios y validados, listo para ser consumido por herramientas de BI o cargado en un data warehouse.

## Setup y Ejecución

### 1. Prerrequisitos
- Python 3.8+
- Git

### 2. Clonar el Repositorio
```bash
git clone git@github.com:PPeitsch/analisis_rentabilidad.git
cd analisis_rentabilidad
```

### 3. Colocar el Archivo de Datos
Asegúrese de colocar el archivo de datos `rentabilidad_productos.csv` dentro del directorio `data/`.

### 4. Configurar el Entorno Virtual y Dependencias
Se recomienda encarecidamente usar un entorno virtual.

```bash
# Crear y activar el entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar pip-tools para manejar dependencias
pip install pip-tools

# Compilar e instalar dependencias de desarrollo y de aplicación
pip-compile dev-requirements.in -o dev-requirements.txt
pip-compile requirements.in -o requirements.txt
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

### 5. Configurar `pre-commit`
Para asegurar que las comprobaciones de calidad se ejecuten automáticamente antes de cada commit, instale los hooks de Git:

```bash
pre-commit install
```
Ahora, cada vez que ejecute `git commit`, `pre-commit` revisará los archivos modificados.

### 6. Ejecutar el Notebook
Inicie Jupyter Lab desde la raíz del proyecto para que las rutas funcionen correctamente:
```bash
jupyter lab
```
Luego, navegue a `notebooks/analisis_y_limpieza.ipynb` y ejecute todas las celdas.
