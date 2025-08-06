# Análisis y Limpieza de Datos de Rentabilidad

Este proyecto contiene un análisis exploratorio y un pipeline de limpieza de datos para un conjunto de datos de rentabilidad de productos. El objetivo es transformar datos crudos con problemas de calidad en un conjunto de datos limpio, validado y listo para el análisis o para ser cargado en un data warehouse.

Este proyecto utiliza `pre-commit` para garantizar la calidad y el estilo del código, y `pip-tools` para un manejo de dependencias robusto y reproducible.

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera para mantener una clara separación de responsabilidades:

```
rentabilidad_proyecto/
├── .gitignore
├── .pre-commit-config.yaml # Configuración para los hooks de pre-commit
├── data/
│   └── rentabilidad_productos.csv # Archivo de datos de entrada (debe ser añadido manualmente)
├── notebooks/
│   └── analisis_y_limpieza.ipynb  # Notebook para exploración y orquestación
├── src/
│   └── data_cleaner.py          # Módulo Python con la lógica de limpieza
├── requirements.in              # Dependencias de la aplicación
├── dev-requirements.in          # Dependencias de desarrollo (testing, linting, etc.)
├── requirements.txt             # Generado por pip-compile (fija las versiones)
└── README.md
```

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
Luego, navegue a `notebooks/analisis_y_limpieza.ipynb` y ejecute las celdas.

El notebook:
1.  Cargará los datos desde `data/rentabilidad_productos.csv`.
2.  Aplicará el pipeline de limpieza definido en `src/data_cleaner.py`.
3.  Guardará el resultado limpio en `data/rentabilidad_productos_limpio.parquet`.
