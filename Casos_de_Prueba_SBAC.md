# Casos de Prueba

## Sistema Básico de Administración de Configuración (SBAC)

---

## 1. Información General del Nivel de Pruebas

| Campo | Valor |
|-------|-------|
| **Proyecto** | Sistema Básico de Administración de Configuración (SBAC) |
| **Versión del Software** | 1.0 |
| **Responsables** | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar |
| **Fecha de Creación** | 29 de mayo de 2026 |
| **Elementos bajo prueba** | Módulos de Gestión de Repositorio, Control de Versiones, Líneas Base y Comparación ejecutados a través de la Interfaz de Línea de Comandos (CLI) en Python |
| **Documentos de Referencia** | Plan de Pruebas Maestro SBAC v1.0, Plan de Pruebas de Nivel: Funcionalidad e Integración CLI, Especificación de Diseño de Pruebas SBAC v1.0 |

---

## 2. Especificación Detallada de los Casos de Prueba

Los siguientes casos de prueba siguen el estándar IEEE 829. Cada caso incluye: ID único, condiciones previas, datos de entrada, pasos de ejecución detallados, resultados esperados, y campos para completar durante la ejecución (resultados reales, estado, comentarios).

---

### MÓDULO: Gestión de Repositorio

---

### CP-001: Inicialización exitosa del repositorio

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-001 |
| **Título/Descripción** | Verificar la creación correcta de un repositorio SBAC en un directorio vacío |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. Entorno de Python configurado y accesible desde la terminal. <br> 2. Terminal abierta en un directorio vacío (e.g., `C:\\test_repo` o `~/test_repo`). <br> 3. No existe una carpeta `.sbac` en el directorio actual. |
| **Datos de entrada** | Comando: `sbac init` |
| **Pasos de ejecución** | 1. Abrir la terminal del sistema operativo. <br> 2. Navegar al directorio de pruebas vacío: `cd test_repo`. <br> 3. Verificar que el directorio está vacío: `ls` (Linux/macOS) o `dir` (Windows). <br> 4. Ejecutar el comando: `sbac init`. <br> 5. Observar el mensaje de salida en consola. <br> 6. Verificar la existencia de la carpeta `.sbac` con: `ls -a` o `dir /a`. <br> 7. Inspeccionar el contenido de `.sbac/` para confirmar estructura de metadatos. |
| **Resultados esperados** | 1. La consola muestra: "Repositorio inicializado correctamente." <br> 2. Se crea la carpeta oculta `.sbac` en el directorio actual. <br> 3. La carpeta `.sbac` contiene archivos de configuración base (e.g., `config`, `index`, `objects/`). <br> 4. No se generan errores ni excepciones de Python. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Validar con explorador de archivos o comando `ls -a` / `dir /a` que `.sbac` es efectivamente una carpeta oculta. Verificar que los permisos de la carpeta permiten lectura/escritura. |

---

### CP-002: Inicialización en un repositorio existente (Valor Límite)

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-002 |
| **Título/Descripción** | Verificar que el sistema impide la inicialización duplicada y preserva los datos existentes |
| **Técnica** | Pruebas de Valor Límite + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. El directorio ya contiene una carpeta `.sbac` creada previamente por la ejecución exitosa de CP-001. <br> 2. La carpeta `.sbac` contiene metadatos válidos del repositorio. |
| **Datos de entrada** | Comando: `sbac init` |
| **Pasos de ejecución** | 1. Abrir la terminal en el directorio donde ya se ejecutó CP-001. <br> 2. Verificar que `.sbac` existe: `ls -a` o `dir /a`. <br> 3. Anotar el contenido actual de `.sbac/` (lista de archivos). <br> 4. Ejecutar el comando: `sbac init`. <br> 5. Observar el mensaje de salida en consola. <br> 6. Verificar nuevamente el contenido de `.sbac/`. <br> 7. Comparar el contenido antes y después de la ejecución. |
| **Resultados esperados** | 1. La consola muestra un mensaje de error claro: "Error: El repositorio ya está inicializado en este directorio." <br> 2. La carpeta `.sbac` preexistente **no es eliminada ni sobrescrita**. <br> 3. Los archivos de metadatos previos permanecen intactos (misma lista, mismos tamaños). <br> 4. No se generan excepciones no controladas. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Verificar que los datos previos permanezcan intactos comparando hashes o timestamps de los archivos en `.sbac/` antes y después. Si el sistema sobrescribe la configuración, reportar como defecto crítico. |

---

### CP-003: Añadir archivo válido al seguimiento

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-003 |
| **Título/Descripción** | Verificar que un archivo existente puede registrarse en el área de preparación (staging) |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001 ejecutado exitosamente en este directorio). <br> 2. El archivo `archivo_prueba.txt` existe en el directorio de trabajo con contenido de texto plano. |
| **Datos de entrada** | Comando: `sbac add archivo_prueba.txt` |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio inicializado. <br> 2. Verificar que `archivo_prueba.txt` existe: `ls archivo_prueba.txt` o `dir archivo_prueba.txt`. <br> 3. Ejecutar el comando: `sbac add archivo_prueba.txt`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar el estado del repositorio con: `sbac status`. <br> 6. Inspeccionar el archivo de índice en `.sbac/` para confirmar el registro del archivo. |
| **Resultados esperados** | 1. La consola muestra: "Archivo 'archivo_prueba.txt' agregado al seguimiento." <br> 2. El archivo queda registrado en el área de preparación. <br> 3. `sbac status` muestra `archivo_prueba.txt` en estado "preparado" o "staged". <br> 4. No se generan errores de ejecución. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Comprobar con `sbac status` que existe comunicación correcta entre los comandos `add` y `status`. Verificar que el archivo de índice en `.sbac/` refleje la ruta y el hash/contenido del archivo agregado. |

---

### CP-004: Añadir archivo inexistente al seguimiento (Equivalencia)

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-004 |
| **Título/Descripción** | Verificar que el sistema rechaza la adición de un archivo que no existe en el directorio |
| **Técnica** | Partición de Equivalencia (clase inválida) + Caja Negra |
| **Prioridad** | Media |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001 ejecutado). <br> 2. El archivo `fantasma.txt` **no existe** en el directorio de trabajo. |
| **Datos de entrada** | Comando: `sbac add fantasma.txt` |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio inicializado. <br> 2. Verificar que `fantasma.txt` no existe: `ls fantasma.txt` (debe indicar que no se encuentra). <br> 3. Ejecutar el comando: `sbac add fantasma.txt`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar que el área de preparación no se modificó: `sbac status`. <br> 6. Verificar que no se generó excepción de Python (no hay traceback en consola). |
| **Resultados esperados** | 1. La consola muestra un mensaje de error claro: "Error: El archivo 'fantasma.txt' no existe en el directorio actual." <br> 2. El área de preparación no se modifica (ningún archivo nuevo aparece en `status`). <br> 3. No se genera excepción no controlada (crash del script). <br> 4. El script termina con código de salida diferente de cero (opcional, según diseño). |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Validar que la consola retorna de forma limpia, sin dejar el terminal en un estado de error o sin mostrar un traceback interno de Python. Verificar que el archivo de índice en `.sbac/` no contenga referencias a `fantasma.txt`. |

---

### CP-005: Consultar estado actual del repositorio

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-005 |
| **Título/Descripción** | Verificar que el comando `status` refleja correctamente los archivos en el área de preparación |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. El archivo `archivo_prueba.txt` ha sido agregado al área de preparación (CP-003). |
| **Datos de entrada** | Comando: `sbac status` |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Ejecutar el comando: `sbac status`. <br> 3. Observar la salida en consola. <br> 4. Verificar que el formato de salida es legible y estructurado. <br> 5. Comparar la salida con el estado real del directorio (archivos existentes vs. rastreados). |
| **Resultados esperados** | 1. La consola muestra una lista estructurada del estado del repositorio. <br> 2. `archivo_prueba.txt` aparece en la sección de archivos "preparados" o "staged". <br> 3. No se listan archivos inexistentes como rastreados. <br> 4. El formato es consistente y legible para el usuario. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Corroborar la comunicación entre `add` y `status`. Si se agregan más archivos después, verificar que `status` los refleje incrementalmente. Validar que archivos no rastreados aparezcan en una sección separada (e.g., "Archivos no rastreados"). |

---

### MÓDULO: Control de Versiones

---

### CP-006: Crear versión con cambios (Commit exitoso)

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-006 |
| **Título/Descripción** | Verificar la creación de una instantánea inmutable del estado actual con metadatos asociados |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. Al menos un archivo agregado al área de preparación (CP-003). <br> 3. El archivo `archivo_prueba.txt` está en estado "preparado" según `sbac status`. |
| **Datos de entrada** | Comando: `sbac commit "Primera versión"` |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Verificar el estado previo: `sbac status` (confirmar archivo preparado). <br> 3. Ejecutar el comando: `sbac commit "Primera versión"`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar el historial: `sbac history`. <br> 6. Inspeccionar la carpeta `.sbac/` para confirmar la creación de la nueva versión. <br> 7. Verificar que el área de preparación se limpió: `sbac status`. |
| **Resultados esperados** | 1. La consola muestra: "Commit realizado: [ID] - Primera versión" (donde [ID] es un identificador único generado). <br> 2. Se genera un registro inmutable de la versión en el historial. <br> 3. `sbac history` muestra la nueva entrada con ID, mensaje y marca temporal. <br> 4. El área de preparación se limpia (ningún archivo en estado "staged"). <br> 5. Los metadatos se almacenan físicamente en `.sbac/`. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Verificar registro en base de datos o archivos dentro de `.sbac/`. Anotar el ID generado para usarlo en pruebas posteriores (CP-009, CP-013). Validar que la marca temporal sea razonable (fecha/hora actual). |

---

### CP-007: Crear versión sin mensaje asociado (Valor Límite)

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-007 |
| **Título/Descripción** | Verificar que el sistema impide la creación de un commit sin mensaje descriptivo |
| **Técnica** | Pruebas de Valor Límite (cadena vacía) + Caja Negra |
| **Prioridad** | Media |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. Archivos en el área de preparación (CP-003 ejecutado). <br> 3. El archivo `archivo_prueba.txt` está en estado "preparado". |
| **Datos de entrada** | Comando: `sbac commit ""` o `sbac commit` (sin argumento de mensaje) |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Verificar que hay archivos preparados: `sbac status`. <br> 3. Ejecutar el comando con mensaje vacío: `sbac commit ""`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar que no se creó una nueva versión: `sbac history`. <br> 6. Verificar que los archivos permanecen en el área de preparación: `sbac status`. <br> 7. *(Opcional)* Probar también: `sbac commit` (sin comillas ni argumento). |
| **Resultados esperados** | 1. La consola muestra: "Error: El mensaje de confirmación es obligatorio y no puede estar vacío." <br> 2. **No se genera una nueva versión** en el historial. <br> 3. Los archivos permanecen en el área de preparación (estado "staged"). <br> 4. No se genera excepción no controlada. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Validar restricciones en la entrada de texto. Verificar si el sistema distingue entre `sbac commit ""` (cadena vacía explícita) y `sbac commit` (falta de argumento). Ambos escenarios deben ser rechazados. |

---

### CP-008: Consultar historial de versiones (History)

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-008 |
| **Título/Descripción** | Verificar la recuperación y despliegue del historial completo de confirmaciones |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. Al menos un commit exitoso registrado (CP-006 ejecutado). <br> 3. Idealmente, múltiples commits con mensajes distintos para validar el listado. |
| **Datos de entrada** | Comando: `sbac history` |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Ejecutar el comando: `sbac history`. <br> 3. Observar la salida en consola. <br> 4. Verificar que cada entrada del historial incluye: ID de versión, mensaje del commit, fecha/hora. <br> 5. Verificar el orden cronológico de las entradas. <br> 6. Comparar el número de entradas mostradas con el número de commits realizados. |
| **Resultados esperados** | 1. Se despliega en consola la lista secuencial de versiones confirmadas. <br> 2. Cada entrada muestra: ID único, mensaje descriptivo, marca de tiempo. <br> 3. El orden es consistente (descendente: más reciente primero, o ascendente, según diseño). <br> 4. No se omiten commits previamente realizados. <br> 5. El formato es legible y estructurado. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Verificar recuperación de metadatos. Si se realizaron 3 commits, `history` debe mostrar exactamente 3 entradas. Validar que las marcas de tiempo sean cronológicamente coherentes. Anotar los IDs de versión para uso en CP-009 y CP-013. |

---

### CP-009: Regresar a una versión válida (Checkout exitoso)

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-009 |
| **Título/Descripción** | Verificar que el directorio de trabajo se restaura al estado exacto de una versión histórica válida |
| **Técnica** | Análisis de Requisitos + Pruebas de Integración + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. Repositorio con al menos dos commits distintos (CP-006 ejecutado múltiples veces). <br> 2. Entre commits, el contenido de `archivo_prueba.txt` fue modificado para crear diferencias. <br> 3. Se conoce el ID de la primera versión (anotado de CP-008, e.g., `v1`). |
| **Datos de entrada** | Comando: `sbac checkout v1` (reemplazar `v1` por el ID real de la primera versión) |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Verificar el contenido actual de `archivo_prueba.txt` (debe reflejar la última versión). <br> 3. Ejecutar el comando: `sbac checkout [ID_primera_version]`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar el contenido de `archivo_prueba.txt` nuevamente (debe reflejar la primera versión). <br> 6. Verificar que `sbac history` sigue mostrando todas las versiones (el checkout no elimina historial). <br> 7. Verificar que no se perdieron archivos no rastreados (si aplica). |
| **Resultados esperados** | 1. La consola muestra: "Directorio restaurado a la versión [ID]." <br> 2. El contenido de `archivo_prueba.txt` vuelve al estado exacto de la primera versión. <br> 3. `sbac history` continúa mostrando todas las versiones sin eliminación. <br> 4. No se generan errores ni excepciones. <br> 5. Los archivos no rastreados (si existen) no se ven afectados. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Este caso es crítico para la integridad del sistema. Verificar físicamente el contenido del archivo con `cat archivo_prueba.txt` o `type archivo_prueba.txt` antes y después del checkout. Si el contenido no cambia o cambia incorrectamente, reportar como defecto crítico. |

---

### CP-010: Regresar a una versión inexistente

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-010 |
| **Título/Descripción** | Verificar el manejo de error cuando se solicita checkout de un ID de versión que no existe |
| **Técnica** | Partición de Equivalencia (ID inválido) + Caja Negra |
| **Prioridad** | Media |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. Al menos un commit registrado (CP-006). <br> 3. Se conoce el estado actual del directorio de trabajo. |
| **Datos de entrada** | Comando: `sbac checkout v999` (donde `v999` es un ID que no existe en el historial) |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Verificar el contenido actual de los archivos (anotar para comparación). <br> 3. Ejecutar el comando: `sbac checkout v999`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar que el contenido de los archivos **no cambió** respecto al estado anterior. <br> 6. Verificar que no se generó excepción de Python. |
| **Resultados esperados** | 1. La consola muestra: "Error: La versión 'v999' no existe en el historial." <br> 2. El directorio de trabajo **no es modificado** en absoluto. <br> 3. Ningún archivo cambia de contenido. <br> 4. No se genera excepción no controlada. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Verificar que el sistema no entre en un estado inconsistente tras el error. Si el directorio de trabajo queda modificado o corrupto, reportar como defecto de gravedad Alta. Validar también con IDs malformados (e.g., `checkout abc` si el sistema espera numérico). |

---

### MÓDULO: Líneas Base

---

### CP-011: Marcar una versión como línea base

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-011 |
| **Título/Descripción** | Verificar que una versión específica puede etiquetarse como línea base estable |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Prioridad** | Media |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. Al menos un commit registrado (CP-006). <br> 3. Se conoce el ID de la última versión (anotado de CP-008). |
| **Datos de entrada** | Comando: `sbac baseline "Release1.0"` |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Verificar el historial: `sbac history` (anotar el ID de la última versión). <br> 3. Ejecutar el comando: `sbac baseline "Release1.0"`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar la creación de la línea base: `sbac list-baselines`. <br> 6. Inspeccionar los metadatos en `.sbac/` para confirmar la etiqueta. |
| **Resultados esperados** | 1. La consola muestra: "Línea base 'Release1.0' creada correctamente." <br> 2. La etiqueta "Release1.0" queda asociada a la última versión confirmada. <br> 3. `sbac list-baselines` muestra la nueva línea base. <br> 4. Los metadatos se almacenan en `.sbac/` sin corromper el historial de commits. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Comprobar con `sbac list-baselines` que la etiqueta se persistió correctamente. Verificar que la línea base no se pierda al ejecutar comandos posteriores (`add`, `commit`). Si el sistema permite múltiples líneas base con el mismo nombre, documentar como observación. |

---

### CP-012: Listar líneas base disponibles

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-012 |
| **Título/Descripción** | Verificar la consulta de todas las líneas base registradas en el repositorio |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Prioridad** | Media |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. Al menos una línea base creada (CP-011 ejecutado, e.g., "Release1.0"). <br> 3. Opcional: múltiples líneas base para validar el listado completo. |
| **Datos de entrada** | Comando: `sbac list-baselines` |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Ejecutar el comando: `sbac list-baselines`. <br> 3. Observar la salida en consola. <br> 4. Verificar que cada línea base muestra: nombre de etiqueta y versión asociada. <br> 5. Comparar el número de líneas base mostradas con las creadas previamente. |
| **Resultados esperados** | 1. Se despliega en consola el listado de líneas base. <br> 2. Cada entrada muestra: nombre de etiqueta y versión asociada (e.g., "Release1.0 -> v1"). <br> 3. Todas las líneas base creadas aparecen en el listado. <br> 4. El formato es legible y estructurado. <br> 5. Si no existen líneas base, mensaje informativo: "No hay líneas base registradas." |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Si se crearon múltiples líneas base (e.g., "Release1.0" y "Sprint2"), verificar que ambas aparecen. Validar que la versión asociada sea correcta según el commit que estaba activo al momento de crear la línea base. |

---

### MÓDULO: Comparación

---

### CP-013: Comparar dos versiones existentes (Diff)

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-013 |
| **Título/Descripción** | Verificar que el sistema calcula y muestra diferencias textuales entre dos versiones válidas usando `difflib` |
| **Técnica** | Análisis de Requisitos + Pruebas de Integración + Caja Negra |
| **Prioridad** | Alta |
| **Condiciones previas** | 1. Repositorio con al menos dos commits donde `archivo_prueba.txt` tenga contenido diferente (CP-006 ejecutado múltiples veces con modificaciones intermedias). <br> 2. Se conocen los IDs de ambas versiones (anotados de CP-008, e.g., `v1` y `v2`). |
| **Datos de entrada** | Comando: `sbac diff v1 v2` (reemplazar `v1` y `v2` por los IDs reales) |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Verificar el historial: `sbac history` (anotar los IDs de las versiones a comparar). <br> 3. Recordar o anotar el contenido de `archivo_prueba.txt` en ambas versiones. <br> 4. Ejecutar el comando: `sbac diff [ID_v1] [ID_v2]`. <br> 5. Observar la salida en consola. <br> 6. Verificar que las diferencias mostradas corresponden exactamente a los cambios realizados. <br> 7. Verificar el formato de salida (símbolos `+` y `-`). |
| **Resultados esperados** | 1. Se muestran las diferencias textuales entre ambas versiones. <br> 2. El formato utiliza símbolos `+` para líneas añadidas y `-` para líneas eliminadas (formato `difflib`). <br> 3. Las diferencias corresponden exactamente a los cambios realizados entre las versiones. <br> 4. La salida es legible en la CLI. <br> 5. No se generan errores de ejecución. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Validar legibilidad en la CLI. Si la salida es muy extensa, verificar que no se trunca. Confirmar que `difflib` de Python es la biblioteca utilizada (según requisito del proyecto). Si las diferencias mostradas no corresponden a los cambios reales, reportar como defecto de integración. |

---

### CP-014: Comparar versiones con ID inexistente

| Campo | Descripción |
|-------|-------------|
| **ID del Caso de Prueba** | CP-014 |
| **Título/Descripción** | Verificar el manejo de error cuando al menos uno de los IDs en el comando diff no existe |
| **Técnica** | Partición de Equivalencia (ID inválido) + Caja Negra |
| **Prioridad** | Media |
| **Condiciones previas** | 1. Repositorio inicializado (CP-001). <br> 2. Al menos un commit registrado (CP-006). <br> 3. Se conoce un ID válido (e.g., `v1`) y se usará un ID inexistente (e.g., `v999`). |
| **Datos de entrada** | Comando: `sbac diff v1 v999` (donde `v999` no existe en el historial) |
| **Pasos de ejecución** | 1. Abrir la terminal en el repositorio. <br> 2. Verificar el historial: `sbac history` (confirmar que `v999` no existe). <br> 3. Ejecutar el comando: `sbac diff [ID_válido] v999`. <br> 4. Observar el mensaje de salida en consola. <br> 5. Verificar que no se intentó calcular diferencias con datos inexistentes. <br> 6. Verificar que no se generó excepción de Python. |
| **Resultados esperados** | 1. La consola muestra: "Error: Una o ambas versiones especificadas no existen en el historial." <br> 2. No se intenta calcular ni mostrar diferencias. <br> 3. No se genera excepción no controlada. <br> 4. El script termina limpiamente. |
| **Resultados reales** | *(Por completar durante la ejecución)* |
| **Estado** | *(Por completar durante la ejecución: Pasó / Falló / Bloqueado)* |
| **Comentarios** | Validar también el escenario donde ambos IDs son inexistentes (`sbac diff v999 v998`). Verificar que el mensaje de error sea específico y no genérico, para facilitar la depuración al usuario. |

---

## 3. Resumen de Casos de Prueba

| Módulo | ID | Descripción | Tipo | Prioridad | Estado |
|--------|-----|-------------|------|-----------|--------|
| **Gestión de Repositorio** | CP-001 | Inicialización exitosa del repositorio | Positiva | Alta | Pendiente |
| | CP-002 | Inicialización en repositorio existente | Negativa (Límite) | Alta | Pendiente |
| | CP-003 | Añadir archivo válido al seguimiento | Positiva | Alta | Pendiente |
| | CP-004 | Añadir archivo inexistente al seguimiento | Negativa (Equivalencia) | Media | Pendiente |
| | CP-005 | Consultar estado actual del repositorio | Positiva | Alta | Pendiente |
| **Control de Versiones** | CP-006 | Crear versión con cambios (Commit) | Positiva | Alta | Pendiente |
| | CP-007 | Crear versión sin mensaje | Negativa (Límite) | Media | Pendiente |
| | CP-008 | Consultar historial de versiones | Positiva | Alta | Pendiente |
| | CP-009 | Regresar a una versión válida (Checkout) | Positiva/Integración | Alta | Pendiente |
| | CP-010 | Regresar a una versión inexistente | Negativa | Media | Pendiente |
| **Líneas Base** | CP-011 | Marcar versión como línea base | Positiva | Media | Pendiente |
| | CP-012 | Listar líneas base disponibles | Positiva | Media | Pendiente |
| **Comparación** | CP-013 | Comparar dos versiones existentes (Diff) | Positiva/Integración | Alta | Pendiente |
| | CP-014 | Comparar versiones con ID inexistente | Negativa | Media | Pendiente |

---

## 4. Matriz de Dependencias entre Casos

| Caso | Dependencia Directa | Justificación |
|------|---------------------|---------------|
| CP-001 | Ninguna | Caso raíz; no requiere estado previo. |
| CP-002 | CP-001 | Requiere que `.sbac` ya exista. |
| CP-003 | CP-001 | Requiere repositorio inicializado. |
| CP-004 | CP-001 | Requiere repositorio inicializado. |
| CP-005 | CP-001, CP-003 | Requiere repositorio inicializado y archivo agregado. |
| CP-006 | CP-001, CP-003 | Requiere repositorio inicializado y archivo en staging. |
| CP-007 | CP-001, CP-003 | Requiere repositorio inicializado y archivo en staging. |
| CP-008 | CP-001, CP-006 | Requiere repositorio inicializado y al menos un commit. |
| CP-009 | CP-001, CP-003, CP-006 (×2) | Requiere múltiples commits para poder regresar. |
| CP-010 | CP-001, CP-006 | Requiere repositorio inicializado y al menos un commit. |
| CP-011 | CP-001, CP-006 | Requiere repositorio inicializado y al menos un commit. |
| CP-012 | CP-001, CP-011 | Requiere repositorio inicializado y línea base creada. |
| CP-013 | CP-001, CP-003, CP-006 (×2) | Requiere múltiples commits con cambios en archivos. |
| CP-014 | CP-001, CP-006 | Requiere repositorio inicializado y al menos un commit. |

---

## 5. Datos de Prueba Requeridos

| ID de Dato | Descripción | Uso en Casos |
|------------|-------------|--------------|
| **DIR-001** | Directorio vacío `test_repo/` | CP-001, CP-002 |
| **FILE-001** | `archivo_prueba.txt` con contenido inicial (e.g., "Línea 1\nLínea 2") | CP-003, CP-005, CP-006, CP-009, CP-013 |
| **FILE-002** | `archivo_prueba.txt` modificado (e.g., "Línea 1\nLínea 2 modificada\nLínea 3") | CP-006 (segundo commit), CP-009, CP-013 |
| **FILE-003** | `archivo1.txt` (archivo adicional para pruebas de múltiples archivos) | CP-003 (opcional) |
| **FILE-004** | `fantasma.txt` (archivo inexistente, no creado en disco) | CP-004 |
| **MSG-001** | `"Primera versión"` | CP-006 |
| **MSG-002** | `"Segunda versión"` | CP-006 (segundo commit) |
| **MSG-003** | `""` (cadena vacía) | CP-007 |
| **TAG-001** | `"Release1.0"` | CP-011 |
| **TAG-002** | `"Sprint2"` | CP-011 (opcional, para CP-012) |
| **ID-INV-001** | `v999` (ID de versión inexistente) | CP-010, CP-014 |

---

## 6. Historial de Cambios

| Versión | Fecha | Autor | Descripción del Cambio |
|---------|-------|-------|------------------------|
| 1.0 | 29/05/2026 | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar | Creación inicial. 14 casos de prueba detallados (CP-001 a CP-014) con estructura IEEE 829 completa: precondiciones, pasos, resultados esperados, campos para resultados reales y estado. Alineación completa con Plan Maestro, Plan de Nivel y Especificación de Diseño. Corrección de IDs desfasados respecto a versiones previas. |

---