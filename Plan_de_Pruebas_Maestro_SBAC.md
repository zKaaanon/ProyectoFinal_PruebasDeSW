# Plan de Pruebas Maestro (MP)

## Sistema Básico de Administración de Configuración (SBAC)

---

## 1. Información General

| Campo | Valor |
|-------|-------|
| **Proyecto** | Sistema Básico de Administración de Configuración (SBAC) |
| **Versión del Software bajo prueba** | 1.0 |
| **Fecha de Creación** | 29 de mayo de 2026 |
| **Responsable / Autor** | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar |
| **Objetivo** | Definir la estrategia global de pruebas para la aplicación SBAC, validando la integridad del control de versiones de archivos de código en Python y asegurando que los niveles de calidad requeridos se cumplan antes del despliegue final. |
| **Alcance General** | Este plan abarca todo el ciclo de verificación del SBAC v1.0, desde la validación de comandos individuales (unitarios/funcionales) hasta la integración de persistencia de datos y flujo completo de trabajo. |
| **Referencias** | Descripción General del Proyecto SBAC (Profesor Rey Rutiaga), Estándar IEEE 829-2008, Documentación de Diseño del SBAC. |

---

## 2. Elementos a Probar (Items under Test)

Se probarán los siguientes módulos lógicos y sus interfaces de línea de comandos (CLI):

| Módulo | Descripción | Comandos Asociados |
|--------|-------------|-------------------|
| **Módulo de Gestión de Repositorio** | Inicialización del espacio de trabajo y seguimiento de archivos. | `sbac init`, `sbac add <archivo>`, `sbac status` |
| **Módulo de Control de Versiones** | Creación de instantáneas inmutables, navegación histórica y restauración de estado. | `sbac commit "mensaje"`, `sbac history`, `sbac checkout <versión>` |
| **Módulo de Líneas Base** | Marcado de configuraciones estables y consulta de etiquetas. | `sbac baseline "nombre"`, `sbac list-baselines` |
| **Módulo de Comparación** | Cálculo y visualización de diferencias textuales entre versiones. | `sbac diff <v1> <v2>` |

**Elementos explícitamente fuera de alcance:**
- Concurrencia de múltiples usuarios sobre el mismo repositorio.
- Ramificación (branching) y fusión (merging) de versiones.
- Interfaz gráfica de usuario (GUI); solo se prueba la CLI.

---

## 3. Características que se Probarán (Features to be Tested)

### 3.1 Funcionalidades Positivas (Happy Path)
| ID de Rastreo | Característica | Criterio de Éxito |
|---------------|----------------|-------------------|
| F-001 | Inicialización de un repositorio local limpio mediante `sbac init`. | Creación de la carpeta oculta `.sbac` sin errores y mensaje de confirmación al usuario. |
| F-002 | Adición de archivos existentes al área de preparación mediante `sbac add`. | El archivo queda registrado para la siguiente versión y se refleja en `sbac status`. |
| F-003 | Despliegue del estado actual del repositorio mediante `sbac status`. | Lista clara de archivos rastreados, modificados o no rastreados. |
| F-004 | Creación de una nueva versión con metadatos mediante `sbac commit`. | Generación de un ID único de versión, registro de marca temporal y mensaje asociado. |
| F-005 | Consulta del historial de versiones mediante `sbac history`. | Listado cronológico con IDs, mensajes y fechas de todas las confirmaciones. |
| F-006 | Restauración del directorio de trabajo a una versión específica mediante `sbac checkout`. | Los archivos del directorio de trabajo vuelven al estado exacto de la versión solicitada. |
| F-007 | Marcado de una versión como línea base mediante `sbac baseline`. | La etiqueta queda asociada persistentemente a la versión indicada. |
| F-008 | Listado de líneas base disponibles mediante `sbac list-baselines`. | Visualización de todas las etiquetas de línea base creadas y sus versiones asociadas. |
| F-009 | Comparación de diferencias textuales entre dos versiones mediante `sbac diff`. | Salida legible en consola utilizando la biblioteca `difflib` con símbolos `+` y `-`. |

### 3.2 Características Negativas / Manejo de Excepciones (Error Handling)
| ID de Rastreo | Característica | Criterio de Éxito |
|---------------|----------------|-------------------|
| F-010 | Prevención de inicialización duplicada (`sbac init` sobre repo existente). | Mensaje de error claro; integridad de datos previos preservada. |
| F-011 | Rechazo de adición de archivos inexistentes (`sbac add fantasma.txt`). | Mensaje de error indicando que el archivo no se encuentra en el directorio. |
| F-012 | Rechazo de commit sin mensaje o con mensaje vacío. | Mensaje de error advirtiendo la obligatoriedad del mensaje descriptivo. |
| F-013 | Manejo de `checkout` hacia una versión inexistente. | Mensaje de error indicando ID de versión no encontrado. |
| F-014 | Manejo de `diff` entre IDs de versión inexistentes. | Mensaje de error indicando que uno o ambos IDs no existen en el historial. |

---

## 4. Enfoque de Pruebas (Test Approach / Strategy)

### 4.1 Tipos de Pruebas
| Tipo | Descripción | Aplicación en SBAC |
|------|-------------|-------------------|
| **Pruebas Funcionales** | Verificación de comportamiento conforme a requisitos. | Aplicadas a todos los comandos CLI (F-001 a F-014). |
| **Pruebas de Integración** | Verificación de interacción entre módulos y persistencia. | Flujo completo: `init` → `add` → `commit` → `history` → `diff`; validación de escritura en disco/MySQL. |
| **Pruebas de Regresión** | Re-ejecución de pruebas tras correcciones. | Re-ejecución automatizada del suite completo tras cada bugfix en la CLI. |
| **Pruebas de Caja Negra** | Pruebas basadas en entradas/salidas sin conocimiento del código fuente. | Principal técnica para la validación de la CLI desde la perspectiva del usuario final. |

### 4.2 Técnicas de Diseño de Pruebas
- **Análisis de Requisitos:** Cada comando del SBAC se descompone en precondición, entrada, acción y resultado esperado.
- **Partición de Equivalencia:** Se agrupan entradas válidas (archivos existentes, mensajes no vacíos) e inválidas (archivos inexistentes, mensajes vacíos) para reducir redundancia.
- **Análisis de Valor Límite:** Se prueban los extremos de las restricciones (e.g., mensaje de commit vacío ` "" `, versión inexistente `v999`).

### 4.3 Estrategia de Ejecución
1. **Pruebas Unitarias Automatizadas:** Desarrollo de scripts con `pytest` para validar la lógica interna de cada módulo (gestión de archivos, hashing de versiones, parseo de diff).
2. **Pruebas Manuales de CLI:** Ejecución secuencial de comandos en terminal siguiendo los Procedimientos de Prueba (ver documento separado IEEE 829), imitando el flujo de trabajo real de un usuario.
3. **Orden de Ejecución:** Secuencial por dependencia lógica; no se puede probar `commit` sin antes probar `init` y `add`.

### 4.4 Herramientas y Entorno
| Categoría | Herramienta / Entorno |
|-----------|----------------------|
| Lenguaje de Desarrollo | Python 3.x |
| Librería de Diff | `difflib` (biblioteca estándar Python) |
| Framework de Pruebas Unitarias | `pytest` |
| Terminal de Pruebas | CMD / PowerShell (Windows) o Bash (Linux/macOS) |
| Gestión de Defectos | Plantillas IEEE 829 (Registro e Informe de Incidentes) |
| Almacenamiento de Pruebas | Archivos de texto `.txt` con contenido controlado |

---

## 5. Criterios de Aprobación / Rechazo (Entry & Exit Criteria)

### 5.1 Criterios de Entrada (Para comenzar la ejecución de pruebas)
- [ ] El código fuente de los 4 módulos del SBAC está completo y libre de errores de sintaxis en Python.
- [ ] La estructura de almacenamiento (archivos simples o MySQL) está implementada y documentada.
- [ ] La CLI responde a los 9 comandos mínimos sin lanzar excepciones no controladas.
- [ ] El entorno de pruebas está configurado: Python 3.x instalado, terminal accesible y directorios de prueba limpios.

### 5.2 Criterios de Éxito (Aprobación del nivel de pruebas)
- **Cobertura Funcional:** El 100% de las funcionalidades mínimas requeridas (F-001 a F-009) deben ejecutarse sin errores críticos.
- **Robustez:** El 100% de los escenarios de manejo de errores (F-010 a F-014) deben atrapar excepciones y mostrar mensajes claros al usuario en la terminal, sin romper la ejecución del script Python.
- **Integridad de Datos:** No se debe presentar pérdida de metadatos, corrupción de archivos de versión o sobreescritura no intencional de líneas base durante la ejecución de los casos de prueba.

### 5.3 Criterios de Rechazo (Suspensión o conclusión negativa)
- Presencia de **defectos de gravedad Crítica** que bloqueen comandos esenciales (imposibilidad de inicializar, commit fallido que pierda datos, checkout que corrompa archivos).
- Presencia de **defectos de gravedad Alta** en más del 20% de los comandos mínimos.
- Fallo en la persistencia de datos (e.g., `history` no recupera versiones previamente guardadas).

---

## 6. Calendario y Dependencias

| Fase | Actividades | Fechas Estimadas | Dependencias |
|------|-------------|------------------|--------------|
| **Planificación** | Redacción del Plan Maestro, Plan de Nivel, Especificación de Diseño y Casos de Prueba. | 29 - 30 de mayo 2026 | Aprobación de la descripción general del proyecto SBAC por el profesor. |
| **Preparación** | Configuración del entorno Python, diseño de datos de prueba, creación de scripts `pytest` base. | 30 - 31 de mayo 2026 | Finalización de la estructura de almacenamiento elegida (archivos simples / MySQL). |
| **Ejecución** | Pruebas unitarias automatizadas y pruebas manuales de CLI funcionales e integración. | 31 mayo - 02 junio 2026 | Disponibilidad de las funciones base de Python codificadas y estable. |
| **Evaluación** | Levantamiento de incidentes, pruebas de regresión post-corrección y redacción del Informe de Resumen. | 02 - 03 junio 2026 | Conclusión de los ciclos planificados de ejecución de pruebas. |
| **Cierre** | Compleción de la documentación IEEE 829, manual de usuario y preparación de la presentación final. | 03 junio 2026 | Aprobación interna de los informes de pruebas y cierre de incidentes críticos. |

---

## 7. Entregables de Pruebas (Test Deliverables)

Según el estándar IEEE 829 y los requisitos del proyecto, se entregarán los siguientes documentos y artefactos:

1. **Plan de Pruebas Maestro** (este documento).
2. **Plan de Pruebas de Nivel** (Funcionalidad e Integración CLI).
3. **Especificación de Diseño de Pruebas** (técnicas, condiciones previas, identificación de casos CP-001 a CP-014).
4. **Casos de Prueba** (detalle de precondiciones, pasos, datos de entrada y resultados esperados).
5. **Procedimientos de Prueba** (guía paso a paso para la ejecución manual en terminal, incluyendo limpieza de entorno).
6. **Registros de Incidentes** (por cada defecto encontrado durante la ejecución).
7. **Informes de Incidentes** (reportes formales de defectos críticos y altos).
8. **Informe de Resumen de Pruebas** (evaluación final, cobertura alcanzada y recomendaciones de liberación).
9. **Código fuente** del sistema SBAC y scripts de pruebas automatizadas (`pytest`).
10. **Manual de usuario básico** de la CLI.

---

## 8. Recursos Necesarios

### 8.1 Personal
| Rol | Cantidad | Responsabilidad |
|-----|----------|-----------------|
| Ingeniero de Pruebas / Desarrollador | 2 | Diseño de pruebas, ejecución manual y automatizada, documentación IEEE 829. |

### 8.2 Hardware y Software
| Recurso | Especificación |
|---------|---------------|
| Equipo de cómputo | Computadora personal con acceso a terminal de comandos. |
| Sistema Operativo | Windows 10/11 (CMD/PowerShell) o Linux (Bash). |
| Entorno de Ejecución | Python 3.8 o superior instalado y configurado en PATH. |
| Editor / IDE | Visual Studio Code, PyCharm o similar para verificación rápida de código. |

### 8.3 Datos de Prueba
- Directorios de trabajo limpios para pruebas de `init`.
- Archivos de texto simulados (`archivo_prueba.txt`, `archivo1.txt`, `archivo2.txt`) con contenido controlado para validar `add`, `commit` y `diff`.
- Archivos inexistentes (`fantasma.txt`) para pruebas de manejo de errores.

---

## 9. Riesgos, Supuestos y Mitigaciones

| ID | Riesgo / Supuesto | Probabilidad | Impacto | Mitigación |
|----|-------------------|--------------|---------|------------|
| R-001 | Compresión del tiempo disponible debido a la proximidad de la fecha límite de entrega. | Alta | Alto | Priorizar la cobertura de pruebas estrictamente sobre las 4 funcionalidades mínimas y 9 comandos requeridos por la rúbrica antes de funcionalidades opcionales. |
| R-002 | Inestabilidad o corrupción en el almacenamiento local de versiones al ejecutar comandos de escritura concurrentes o repetidos. | Media | Medio | Diseñar procedimientos de prueba que incluyan verificación del estado del repositorio (`status`, `history`) antes y después de cada comando de escritura (`add`, `commit`, `checkout`). |
| R-003 | Falsos positivos derivados de probar comandos sobre un directorio que ya contiene metadatos de pruebas anteriores. | Media | Medio | Incluir en las condiciones previas de cada Procedimiento de Prueba el borrado manual de la carpeta `.sbac` y archivos temporales antes de iniciar un nuevo ciclo de validación. |
| R-004 | Dependencia secuencial de casos de prueba dificulta la automatización aislada. | Alta | Medio | Documentar explícitamente las dependencias entre casos (e.g., CP-006 depende de CP-001 y CP-003) y crear fixtures de `pytest` que preparen el estado requerido. |
| R-005 | Diferencias en comportamiento de la CLI entre terminales Windows (CMD/PowerShell) y Linux (Bash). | Baja | Medio | Ejecutar las pruebas manuales en ambos entornos si es posible, o al menos documentar el entorno de referencia utilizado. |

---

## 10. Trazabilidad de Requisitos a Casos de Prueba

La siguiente matriz garantiza que cada funcionalidad mínima del SBAC se rastrea hasta al menos un caso de prueba positivo y, cuando aplica, un caso negativo. Los IDs de Casos de Prueba (CP-XXX) son consistentes en todos los documentos IEEE 829 derivados.

| Requisito del Proyecto | Funcionalidad (F-ID) | Caso de Prueba Positivo | Caso de Prueba Negativo / Límite |
|------------------------|----------------------|-------------------------|----------------------------------|
| Inicializar repositorio | F-001 | CP-001 | CP-002 |
| Añadir archivos al seguimiento | F-002 | CP-003 | CP-004 |
| Mostrar estado del repositorio | F-003 | CP-005 | — |
| Crear nueva versión (commit) | F-004 | CP-006 | CP-007 |
| Listar historial de versiones | F-005 | CP-008 | — |
| Regresar a versión anterior | F-006 | CP-009 | CP-010 |
| Marcar versión como línea base | F-007 | CP-011 | — |
| Listar líneas base | F-008 | CP-012 | — |
| Comparar diferencias | F-009 | CP-013 | CP-014 |

---

## 11. Glosario

| Término | Definición |
|---------|------------|
| **SBAC** | Sistema Básico de Administración de Configuración. |
| **CLI** | Interfaz de Línea de Comandos (Command Line Interface). |
| **Commit** | Confirmación o instantánea inmutable del estado de los archivos rastreados en un momento dado. |
| **Línea Base (Baseline)** | Versión oficialmente aprobada de un elemento de configuración, que sirve como punto de referencia para desarrollos futuros. |
| **Diff** | Salida que muestra las diferencias textuales entre dos versiones de un archivo. |
| **Caja Negra** | Técnica de prueba que evalúa funcionalidad sin conocer la estructura interna del código. |
| **Happy Path** | Escenario de prueba donde todas las condiciones son ideales y el usuario sigue el flujo esperado. |

---

## 12. Historial de Cambios

| Versión | Fecha | Autor | Descripción del Cambio |
|---------|-------|-------|------------------------|
| 1.0 | 29/05/2026 | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar | Creación inicial del Plan de Pruebas Maestro con cobertura completa de los 9 comandos mínimos del SBAC y alineación IEEE 829. |

---

