# Prototipo de Limpieza de Datos para Pipeline ELT

Este repositorio contiene el trabajo de **análisis exploratorio y prototipado** para la lógica de limpieza de datos de rentabilidad de productos. El código y los notebooks aquí presentes sirven como la **prueba de concepto (PoC)** para la etapa de Transformación (T) de un pipeline de datos ELT de producción.

El diseño completo de la arquitectura de producción, las decisiones técnicas y las consideraciones operativas se encuentran detalladas en `docs/arquitectura_pipeline.md`.

## Propósito del Repositorio

El objetivo principal de este proyecto no es ser una aplicación final, sino servir como:

1.  **Fase de Exploración:** Identificar y documentar problemas de calidad en una muestra de datos crudos.
2.  **Fase de Prototipado:** Desarrollar y validar la lógica de limpieza en un entorno controlado (Jupyter Notebook y Python modular).
3.  **Fuente de Verdad para la Implementación:** El código en `src/data_cleaner.py` y las conclusiones del notebook son el blueprint que informará la creación de los modelos de transformación (`dbt`) en el pipeline de producción.

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera para mantener una clara separación de responsabilidades:

```
analisis_rentabilidad/
├── .gitignore
├── .pre-commit-config.yaml # Configuración para los hooks de pre-commit
├── data/
│   └── rentabilidad_productos.csv
├── docs/
│   ├── arquitectura_pipeline.md   # Documento de diseño del pipeline de producción
│   └── queries_optimizadas.sql    # Ejemplos de queries SQL para análisis
├── notebooks/
│   └── analisis_y_limpieza.ipynb  # Notebook con el análisis y la validación del prototipo
├── src/
│   └── data_cleaner.py          # Módulo Python con la lógica de limpieza prototipada
├── requirements.in              # Dependencias de la aplicación
├── dev-requirements.in          # Dependencias de desarrollo
├── requirements.txt             # Generado por pip-compile
└── README.md
```
-   **`docs/`**: Contiene la visión estratégica y el diseño de la solución final. **Es el documento más importante para entender el contexto general.**
-   **`src/` y `notebooks/`**: Contienen la implementación práctica del prototipo que valida la lógica a aplicar en la arquitectura descrita en `docs/`.

## Cómo Ejecutar el Prototipo

Las siguientes instrucciones permiten replicar el entorno de análisis para validar o extender la lógica de limpieza.

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
