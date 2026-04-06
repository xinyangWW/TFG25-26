## TFG25-26

A continuación se describen los 6 scripts generales para evaluar los modelos de lenguaje usando testing metamórfico.
## 1. `merge_results.py`

Script encargado de **fusionar los resultados generados por los distintos integrantes del equipo** en un único archivo final por modelo.

Para cada modelo (`chatgpt`, `gemma`, `deepseek`), el script:
- Busca todos los archivos `resultados_<modelo>_*.csv`, donde * es el nombre de cierto integrante
- Combina sus contenidos en un único CSV:
  - `resultados_finales_<modelo>.csv`
- Calcula estadísticas agregadas:
  - Número total de casos
  - Casos que cumplen la relación metamórfica (MR)
  - Errores técnicos
  - Distribución de resultados por tipo de relación

Esto permite obtener una **visión global del rendimiento del modelo** a partir de ejecuciones distribuidas entre varios miembros del equipo.

## 2. 'mr_utils.py'

Módulo encargado de **normalizar y comparar respuestas de los modelos** para evaluar relaciones metamórficas (MR).

- Convierte respuestas a un formato estándar (números, fracciones, “sin solución”, “R”, etc.)
- Limpia ruido (LaTeX, etiquetas, texto irrelevante)
- Detecta errores técnicos
- Compara respuestas base y transformadas para determinar si se cumple la MR

Permite una **evaluación robusta y consistente** entre respuestas heterogéneas.

## 3. 'print_results.py'

Módulo para **mostrar resultados en consola** de forma clara.

- Imprime modelo, tipo de relación y caso
- Muestra respuestas originales y normalizadas
- Indica si se cumple la MR (✔ / ✘ con colores)
- Incluye tiempo de ejecución

Facilita la **interpretación rápida de resultados**.

## 4. 'results_manager.py'

Módulo para **guardar resultados en CSV** por modelo.

- Genera archivos: `resultados_<modelo>.csv`
- Añade resultados automáticamente
- Normaliza datos antes de guardarlos
- Guarda métricas clave (MR, errores, tiempo)

Permite **recolectar resultados de forma estructurada**.

## 5. 'query_model.py'

Módulo para **interactuar con modelos vía Ollama**.

- Precarga modelos para mejorar rendimiento
- Envía prompts y obtiene respuestas
- Soporta múltiples modelos (`chatgpt`, `gemma`, `deepseek`)
- Maneja errores con reintentos
- Registra ejecución en logs

Permite una **ejecución automatizada y fiable de consultas a modelos**.

## 6. `run_all.py`

Script encargado de **ejecutar automáticamente todos los casos de prueba del proyecto** para un modelo específico.

### Uso:
En la terminal hay que ejecutar los siguientes comandos: 

python run_all.py chatgpt
python run_all.py gemma
python run_all.py deepseek
