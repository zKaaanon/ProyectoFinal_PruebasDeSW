# SBAC — Master Prompt de Construcción

---

## PARTE 1 — Contexto global del proyecto (incluir SIEMPRE)

```
Estoy construyendo el SBAC (Sistema Básico de Administración de Configuración),
una aplicación de línea de comandos (CLI) en Python 3.8+.

El SBAC es un sistema de control de versiones simplificado, similar a Git pero
mucho más básico. Permite a un usuario rastrear cambios en archivos de texto
dentro de un directorio de trabajo.

STACK TÉCNICO:
- Lenguaje: Python 3.8+
- Almacenamiento: archivos JSON dentro de una carpeta oculta llamada .sbac/
- Librería de diferencias: difflib (biblioteca estándar de Python)
- CLI: argparse (biblioteca estándar de Python)
- Pruebas: pytest

ESTRUCTURA DE ARCHIVOS DEL PROYECTO:
sbac/
├── sbac.py           ← punto de entrada CLI, maneja argparse y despacha comandos
├── storage.py        ← ÚNICO módulo que lee/escribe .sbac/ (ya implementado)
├── repo.py           ← comandos: init, add, status
├── versions.py       ← comandos: commit, history, checkout
├── baselines.py      ← comandos: baseline, list-baselines
├── diff.py           ← comando: diff (usa difflib)
└── tests/
    ├── test_repo.py
    ├── test_versions.py
    ├── test_baselines.py
    └── test_diff.py

ESTRUCTURA DE .sbac/ (carpeta oculta que crea el sistema):
.sbac/
├── config.json        → {"initialized": true, "version": "1.0", "created_at": "..."}
├── index.json         → {"staged": ["archivo.txt", ...]}
├── history.json       → lista de commits (ver formato abajo)
├── baselines.json     → {"Release1.0": "v1", "Sprint2": "v2"}
└── objects/
    └── v1/
        └── archivo_prueba.txt   ← copia física del archivo en esa versión

FORMATO DE UN COMMIT EN history.json:
{
  "id": "v1",
  "message": "Primera versión",
  "timestamp": "2026-05-30T10:30:00",
  "files": {
    "archivo_prueba.txt": "contenido completo del archivo en texto plano"
  }
}

LOS 9 COMANDOS DE LA CLI:
  sbac init                   → inicializa el repositorio (crea .sbac/)
  sbac add <archivo>          → agrega archivo al área de staging
  sbac status                 → muestra archivos en staging y no rastreados
  sbac commit "mensaje"       → crea una nueva versión con los archivos staged
  sbac history                → lista todos los commits con ID, mensaje y fecha
  sbac checkout <versión>     → restaura el directorio al estado de una versión (ej: v1)
  sbac baseline "nombre"      → etiqueta la última versión con un nombre estable
  sbac list-baselines         → lista todas las líneas base creadas
  sbac diff <v1> <v2>         → muestra diferencias textuales entre dos versiones

STORAGE.PY YA ESTÁ IMPLEMENTADO y expone estas funciones:
  init_repo()                          → crea .sbac/ completo
  repo_exists() → bool                 → verifica si .sbac/ existe
  assert_repo_exists()                 → aborta con mensaje si no hay repo
  stage_file(filename)                 → agrega archivo al index.json
  create_commit(message) → dict        → crea commit y limpia staging
  read_history() → list                → devuelve lista de commits
  get_commit(version_id) → dict        → busca commit por ID, lanza StorageError si no existe
  restore_version(version_id)          → restaura archivos al estado de esa versión
  create_baseline(tag) → dict          → etiqueta la última versión
  read_baselines() → dict              → devuelve mapa tag→version_id
  get_file_content_at(v, filename) → str → contenido de un archivo en una versión
  clear_staging()                      → vacía index.json
  read_index() → dict                  → devuelve {"staged": [...]}
  StorageError                         → excepción que lanzan todas las funciones anteriores

REGLA CRÍTICA DE MANEJO DE ERRORES:
Todos los módulos deben capturar StorageError y mostrar su mensaje con print().
Nunca dejar que un traceback de Python llegue al usuario final.
Ejemplo:
  from storage import StorageError
  try:
      storage.create_commit(mensaje)
  except StorageError as e:
      print(f"Error: {e}")
      raise SystemExit(1)

REGLAS DE ESTILO:
- Mensajes de éxito en español, claros y concisos
- Mensajes de error siempre con el prefijo "Error: "
- IDs de versión son v1, v2, v3... (correlativo simple)
- Un módulo = un archivo Python. No mezclar lógica entre módulos.
- Cada función hace UNA sola cosa.
```

---

## PARTE 2 — Prompts por módulo

### PROMPT A: repo.py (init, add, status)

```
Usando el contexto del proyecto SBAC, implementa el archivo repo.py.

Este módulo maneja los comandos de gestión de repositorio: init, add y status.
Importa únicamente desde storage.py — no escribe JSON directamente.

COMANDO: sbac init
  Comportamiento positivo (CP-001):
    - Llama a storage.init_repo()
    - Muestra: "Repositorio inicializado correctamente en .sbac/"
  Comportamiento negativo (CP-002):
    - Si lanza StorageError (ya existe), muestra el mensaje de error
    - NO sobreescribe ni elimina datos existentes

COMANDO: sbac add <archivo>
  Comportamiento positivo (CP-003):
    - Llama a storage.stage_file(filename)
    - Muestra: "Archivo 'archivo.txt' agregado al seguimiento."
  Comportamiento negativo (CP-004):
    - Si el archivo no existe en disco, StorageError lo detecta
    - Muestra: "Error: El archivo 'fantasma.txt' no existe en el directorio actual."

COMANDO: sbac status
  Comportamiento positivo (CP-005):
    - Lee storage.read_index()
    - Muestra dos secciones:
        Archivos preparados para commit:
          - archivo_prueba.txt
        Archivos no rastreados: (lista archivos del directorio que no están staged)
    - Si no hay archivos staged, muestra: "No hay archivos en el área de preparación."

Estructura esperada del archivo:
  from storage import (init_repo, stage_file, read_index,
                       assert_repo_exists, StorageError)
  import os

  def cmd_init(): ...
  def cmd_add(filename): ...
  def cmd_status(): ...

No incluyas el bloque if __name__ == "__main__", eso va en sbac.py.
Incluye docstrings breves en cada función.
```

---

### PROMPT B: versions.py (commit, history, checkout)

```
Usando el contexto del proyecto SBAC (ver arriba), implementa el archivo versions.py.

Este módulo maneja los comandos de control de versiones: commit, history y checkout.

COMANDO: sbac commit "mensaje"
  Comportamiento positivo (CP-006):
    - Llama a storage.create_commit(message)
    - Muestra: "Commit realizado: v1 — Primera versión  [2026-05-30 10:30]"
    - (Adaptar al ID y timestamp reales devueltos por create_commit)
  Comportamiento negativo (CP-007):
    - Mensaje vacío ("") o sin argumento → StorageError lo detecta
    - Muestra: "Error: El mensaje de confirmación es obligatorio y no puede estar vacío."
    - No crea versión, no limpia staging

COMANDO: sbac history
  Comportamiento positivo (CP-008):
    - Lee storage.read_history()
    - Muestra la lista en orden descendente (más reciente primero)
    - Formato por entrada:
        [v2] Segunda versión                  2026-05-30 11:00
        [v1] Primera versión                  2026-05-30 10:30
    - Si no hay commits: "No hay versiones registradas aún."

COMANDO: sbac checkout <versión>
  Comportamiento positivo (CP-009):
    - Llama a storage.restore_version(version_id)
    - Muestra: "Directorio restaurado a la versión v1."
    - El historial NO se modifica (checkout no borra commits)
  Comportamiento negativo (CP-010):
    - Si la versión no existe → StorageError
    - Muestra: "Error: La versión 'v999' no existe en el historial."
    - Los archivos del directorio NO se modifican

Estructura esperada:
  from storage import (create_commit, read_history, restore_version,
                       assert_repo_exists, StorageError)

  def cmd_commit(message): ...
  def cmd_history(): ...
  def cmd_checkout(version_id): ...
```

---

### PROMPT C: baselines.py (baseline, list-baselines)

```
Usando el contexto del proyecto SBAC (ver arriba), implementa el archivo baselines.py.

Este módulo maneja los comandos de líneas base: baseline y list-baselines.

COMANDO: sbac baseline "nombre"
  Comportamiento positivo (CP-011):
    - Llama a storage.create_baseline(tag)
    - Etiqueta la ÚLTIMA versión del historial con el nombre dado
    - Muestra: "Línea base 'Release1.0' creada → apunta a v1"
  Casos de error:
    - Sin commits previos → StorageError: mostrar mensaje
    - Tag ya existente → StorageError: mostrar mensaje
    - Nombre vacío → StorageError: mostrar mensaje

COMANDO: sbac list-baselines
  Comportamiento positivo (CP-012):
    - Lee storage.read_baselines()
    - Muestra:
        Líneas base registradas:
          Release1.0   →  v1
          Sprint2      →  v2
    - Si no hay líneas base: "No hay líneas base registradas."

Estructura esperada:
  from storage import (create_baseline, read_baselines,
                       assert_repo_exists, StorageError)

  def cmd_baseline(tag): ...
  def cmd_list_baselines(): ...
```

---

### PROMPT D: diff.py (diff)

```
Usando el contexto del proyecto SBAC (ver arriba), implementa el archivo diff.py.

Este módulo implementa el comando diff usando la biblioteca difflib de Python.

COMANDO: sbac diff <v1> <v2>
  Comportamiento positivo (CP-013):
    - Obtiene el contenido de TODOS los archivos que aparecen en v1 o v2
    - Para cada archivo, compara su contenido entre versiones con difflib
    - Usa difflib.unified_diff con lineterm="" para formato limpio
    - Muestra:
        --- v1/archivo_prueba.txt
        +++ v2/archivo_prueba.txt
        @@ -1,3 +1,4 @@
         Línea 1
        -Línea 2
        +Línea 2 MODIFICADA
         Línea 3
        +Línea 4 nueva
    - Si los archivos son idénticos: "Sin diferencias entre v1 y v2."
  Comportamiento negativo (CP-014):
    - Si v1 o v2 no existen en el historial → StorageError
    - Muestra: "Error: Una o ambas versiones especificadas no existen en el historial."
    - No intenta calcular nada

LÓGICA DE COMPARACIÓN:
  1. Obtener commit_v1 = storage.get_commit(v1)
  2. Obtener commit_v2 = storage.get_commit(v2)
  3. Unión de archivos: set(commit_v1["files"]) | set(commit_v2["files"])
  4. Para cada archivo en la unión:
     - contenido_v1 = commit_v1["files"].get(archivo, "")
     - contenido_v2 = commit_v2["files"].get(archivo, "")
     - Si son iguales, saltar
     - Si difieren, mostrar diff con difflib.unified_diff

Estructura esperada:
  import difflib
  from storage import get_commit, assert_repo_exists, StorageError

  def cmd_diff(v1, v2): ...
  def _show_file_diff(filename, content_v1, content_v2, id_v1, id_v2): ...
```

---

### PROMPT E: sbac.py (punto de entrada CLI)

```
Usando el contexto del proyecto SBAC (ver arriba), implementa el archivo sbac.py.

Este es el punto de entrada de la CLI. Usa argparse para despachar los 9 comandos
a las funciones de los módulos correspondientes.

ESTRUCTURA DE SUBCOMANDOS:
  parser = argparse.ArgumentParser(prog="sbac", description="Sistema Básico de AC")
  subparsers = parser.add_subparsers(dest="command")

  Registrar un subparser por cada comando:
    init        → sin argumentos
    add         → argumento posicional: archivo (str)
    status      → sin argumentos
    commit      → argumento posicional: mensaje (str)
    history     → sin argumentos
    checkout    → argumento posicional: version (str)
    baseline    → argumento posicional: nombre (str)
    list-baselines → sin argumentos (dest="list_baselines")
    diff        → dos argumentos posicionales: v1 (str), v2 (str)

DESPACHO:
  Según args.command, llamar a la función correspondiente del módulo:
    "init"           → repo.cmd_init()
    "add"            → repo.cmd_add(args.archivo)
    "status"         → repo.cmd_status()
    "commit"         → versions.cmd_commit(args.mensaje)
    "history"        → versions.cmd_history()
    "checkout"       → versions.cmd_checkout(args.version)
    "baseline"       → baselines.cmd_baseline(args.nombre)
    "list-baselines" → baselines.cmd_list_baselines()
    "diff"           → diff.cmd_diff(args.v1, args.v2)
    None             → parser.print_help()

IMPORTS:
  import argparse
  import repo, versions, baselines, diff

Incluir bloque:
  if __name__ == "__main__":
      main()
```

---

### PROMPT F: tests/ (pytest)

```
Usando el contexto del proyecto SBAC, implementa las pruebas unitarias
con pytest para el archivo repo.py.

Las pruebas corresponden a los casos de prueba del estándar IEEE 829 ya definidos.
Cada función de prueba valida UN caso de prueba específico.

CASOS A CUBRIR en test_repo.py:
  CP-001: test_init_crea_sbac_dir()
    - Ejecutar cmd_init() en directorio temporal
    - Assert: existe .sbac/config.json, index.json, history.json, baselines.json
  CP-002: test_init_duplicado_lanza_error()
    - Ejecutar cmd_init() dos veces
    - Assert: segunda llamada imprime mensaje de error (capturar stdout)
    - Assert: .sbac/ no fue sobreescrito (config.json tiene mismo contenido)
  CP-003: test_add_archivo_existente()
    - Crear archivo temporal, ejecutar cmd_add(nombre)
    - Assert: archivo aparece en storage.read_index()["staged"]
  CP-004: test_add_archivo_inexistente()
    - Ejecutar cmd_add("fantasma.txt") sin que exista el archivo
    - Assert: imprime "Error: El archivo 'fantasma.txt' no existe..."
    - Assert: staging sigue vacío
  CP-005: test_status_muestra_staged()
    - Init + add + status
    - Assert: la salida contiene el nombre del archivo

FIXTURE RECOMENDADO (usar en todos los archivos de test):
  import pytest, os, tempfile
  from storage import init_repo

  @pytest.fixture
  def repo_limpio(tmp_path, monkeypatch):
      monkeypatch.chdir(tmp_path)   # cambia el CWD al directorio temporal
      init_repo()                   # inicializa repo limpio
      yield tmp_path                # provee la ruta al test

  @pytest.fixture
  def directorio_vacio(tmp_path, monkeypatch):
      monkeypatch.chdir(tmp_path)
      yield tmp_path

PATRÓN DE CAPTURA DE OUTPUT:
  def test_ejemplo(repo_limpio, capsys):
      cmd_que_imprime_algo()
      captured = capsys.readouterr()
      assert "texto esperado" in captured.out

Implementa los tests con nombres descriptivos, un assert por concepto, y
sin dependencias entre tests (cada uno parte de un fixture limpio).
```

---

## PARTE 3 — Prompt de depuración (cuando algo no funciona)

```
Estoy trabajando en el SBAC (Sistema Básico de Administración de Configuración),
una CLI en Python. [PEGA EL CONTEXTO GLOBAL DE LA PARTE 1 AQUÍ]

Tengo el siguiente problema en el módulo [NOMBRE]:

COMANDO QUE FALLA:
  sbac [comando] [argumentos]

ERROR QUE APARECE EN TERMINAL:
  [pega el output exacto]

CÓDIGO ACTUAL DEL ARCHIVO:
  [pega el código del archivo]

CONTENIDO DE .sbac/ EN ESTE MOMENTO:
  config.json:    [pega contenido]
  index.json:     [pega contenido]
  history.json:   [pega contenido]

CASO DE PRUEBA IEEE 829 QUE DEBE PASAR:
  CP-[número]: [descripción breve]
  Resultado esperado: [qué debería mostrar]
  Resultado real:     [qué muestra actualmente]

Por favor:
1. Identifica la causa raíz del problema
2. Muestra el código corregido
3. Explica brevemente qué estaba mal
```

---

## PARTE 4 — Prompt de documentación (Procedimientos de Prueba IEEE 829)

```
Necesito generar el documento "Procedimientos de Prueba" bajo el estándar IEEE 829
para el SBAC (Sistema Básico de Administración de Configuración).

CONTEXTO DEL PROYECTO: [pega la Parte 1]

Este documento es una guía paso a paso para ejecutar manualmente los 14 casos
de prueba (CP-001 a CP-014) en la terminal. Difiere de los Casos de Prueba en
que incluye:
  - Limpieza de entorno antes de cada bloque
  - Terminal de referencia utilizada (PowerShell / Bash)
  - Pasos numerados exactos con comandos copiables
  - Dónde anotar el ID de versión generado (para usar en CP-009 y CP-013)
  - Verificación física de .sbac/ después de comandos de escritura

ESTRUCTURA DE CADA PROCEDIMIENTO:
  PT-[número] (vinculado a CP-[número])
    - Propósito
    - Terminal y sistema operativo
    - Condición previa (estado del sistema antes de ejecutar)
    - Pasos numerados con comandos exactos
    - Verificación esperada
    - Observaciones a registrar

Genera los procedimientos PT-001 a PT-014, agrupados en los mismos 4 bloques
del Plan de Pruebas de Nivel: Repositorio, Versiones, Líneas Base, Comparación.
Incluye al inicio una sección de "Preparación del entorno" que indica cómo
limpiar .sbac/ antes de cada ciclo.
```

---

## REFERENCIA RÁPIDA — Qué prompt usar para qué tarea

| Tarea | Prompt a usar |
|-------|--------------|
| Construir repo.py desde cero | Parte 1 + Prompt A |
| Construir versions.py | Parte 1 + Prompt B |
| Construir baselines.py | Parte 1 + Prompt C |
| Construir diff.py | Parte 1 + Prompt D |
| Construir sbac.py (CLI) | Parte 1 + Prompt E |
| Escribir pruebas pytest | Parte 1 + Prompt F (especificar módulo) |
| Depurar un error | Parte 1 + Parte 3 (rellenar datos) |
| Generar Procedimientos de Prueba | Parte 1 + Parte 4 |
| Generar Informe de Resumen | Parte 1 + pedirlo directamente |
| Generar Manual de Usuario | Parte 1 + pedirlo directamente |

---

*Generado el 29/05/2026 · Proyecto SBAC v1.0 · Cristian Ignacio Reyna Méndez y José Eleazar López Montufar*