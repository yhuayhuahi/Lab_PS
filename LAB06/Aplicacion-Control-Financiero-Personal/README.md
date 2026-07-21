# Aplicación de Control Financiero Personal

Una aplicación de escritorio profesional en Python utilizando PySide6 para la gestión de ingresos y gastos personales.

## Tecnologías Utilizadas

- Python 3.12+
- PySide6 (GUI)
- Matplotlib (Gráficos)
- ReportLab (Exportación PDF)
- pytest, pytest-cov, pytest-qt (Pruebas Unitarias)

## Instalación

1. Clona el repositorio o extrae el código.
2. Se recomienda crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para iniciar la aplicación, ejecuta:

```bash
python main.py
```

## Pruebas

Para ejecutar las pruebas con el reporte de cobertura al 100%:

```bash
pytest --cov=app --cov-report=term-missing
```
