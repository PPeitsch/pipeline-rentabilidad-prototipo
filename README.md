# Análisis y Limpieza de Datos

Este proyecto contiene un análisis exploratorio y un pipeline de limpieza de datos para un conjunto de datos de rentabilidad de productos. El objetivo es transformar datos crudos con problemas de calidad en un conjunto de datos limpio, validado y listo para el análisis o para ser cargado en un data warehouse.

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera para mantener una clara separación de responsabilidades:

```
rentabilidad_proyecto/
├── .gitignore
├── notebooks/
│   └── analisis_y_limpieza.ipynb
├── src/
│   └── data_cleaner.py
└── README.md
```

-   **`notebooks/`**: Contiene los notebooks de Jupyter. El rol del notebook en este proyecto es para la exploración interactiva, la visualización y para documentar el proceso de análisis.
-   **`src/`**: Contiene el código fuente de Python. La lógica de negocio, como las funciones de limpieza de datos, se encuentra aquí para que sea reutilizable y fácil de probar.

## Cómo Ejecutar

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone git@github.com:PPeitsch/analisis_rentabilidad.git
    cd analisis_rentabilidad
    ```

2.  **Configurar el Entorno:**
    Se recomienda usar un entorno virtual.
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install pandas matplotlib seaborn missingno jupyterlab
    ```

3.  **Ejecutar el Notebook:**
    Abra y ejecute el notebook `notebooks/analisis_y_limpieza.ipynb` en un entorno de Jupyter (como Jupyter Lab o Google Colab).

    -   El notebook cargará los datos, los limpiará usando el módulo `src/data_cleaner.py`, y guardará el resultado limpio en formato Parquet.
