# Especificación de Diseño de Pruebas (TDS)

## Sistema Básico de Administración de Configuración (SBAC)

---

## 1. Información General

| Campo | Valor |
|-------|-------|
| **Proyecto** | Sistema Básico de Administración de Configuración (SBAC) |
| **Versión del Software bajo prueba** | 1.0 |
| **Módulos bajo diseño de pruebas** | Gestión de Repositorio, Control de Versiones, Líneas Base y Comparación |
| **Responsables** | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar |
| **Fecha de Creación** | 29 de mayo de 2026 |
| **Objetivo** | Definir los casos de prueba detallados para validar el correcto funcionamiento de los comandos del sistema SBAC, garantizando la cobertura de los requisitos funcionales y el manejo robusto de excepciones. Este documento establece el diseño lógico de cada prueba antes de su ejecución. |
| **Técnicas de Diseño Aplicadas** | Pruebas de Caja Negra, Análisis de Requisitos, Partición de Equivalencia, Pruebas de Valor Límite y Pruebas de Integración. |
| **Documentos de Referencia** | Plan de Pruebas Maestro SBAC v1.0 (Sección 10: Trazabilidad), Plan de Pruebas de Nivel: Funcionalidad e Integración CLI. |

---

## 2. Condiciones Previas Generales

Las siguientes condiciones deben cumplirse antes de la ejecución de cualquier caso de prueba diseñado en este documento:

1. **Entorno de Ejecución:** El intérprete de Python 3.8+ debe estar instalado y configurado en las variables de entorno del sistema (PATH). La CLI del SBAC debe ser invocable desde la terminal como `sbac`.
2. **Directorio de Pruebas:** Las pruebas deben ejecutarse en directorios locales de pruebas aislados (e.g., `C:\test_repo` o `~/test_repo`), separados físicamente del código fuente del SBAC para evitar contaminación.
3. **Permisos:** El usuario ejecutor debe tener permisos de lectura, escritura y eliminación en el directorio de pruebas.
4. **Datos de Prueba Base:** Los archivos de texto simulados (`archivo_prueba.txt`, `archivo1.txt`, `archivo2.txt`) deben existir con contenido controlado y permisos de lectura/escritura antes de ejecutar casos que dependan de su existencia.
5. **Limpieza Inicial:** Antes de cada ciclo de pruebas secuenciales, el directorio de pruebas no debe contener una carpeta `.sbac` residual ni archivos temporales de ejecuciones previas.

---

## 3. Identificación de Pruebas y Diseño Detallado

Los casos de prueba siguientes han sido diseñados aplicando las técnicas declaradas en la sección 1. Cada ID es único e inmutable en todo el conjunto de documentación IEEE 829 del proyecto SBAC.

### 3.1 Módulo: Gestión de Repositorio

#### CP-001: Inicialización exitosa del repositorio
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-001 |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Descripción** | Verificar que el comando `sbac init` crea correctamente la estructura de configuración en un directorio vacío. |
| **Precondiciones** | Directorio de pruebas limpio y vacío. No existe carpeta `.sbac`. |
| **Datos de Entrada** | Comando: `sbac init` |
| **Resultado Esperado** | 1. Creación de la carpeta oculta `.sbac` con la estructura interna de metadatos. <br> 2. Mensaje en consola indicando éxito (e.g., "Repositorio inicializado correctamente"). |
| **Prioridad** | Alta |
| **Dependencias** | Ninguna. Es el caso raíz del flujo de trabajo. |

#### CP-002: Inicialización en repositorio existente (Valor Límite)
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-002 |
| **Técnica** | Pruebas de Valor Límite + Caja Negra |
| **Descripción** | Verificar que el sistema previene la inicialización duplicada y protege los datos existentes. |
| **Precondiciones** | El directorio ya contiene una carpeta `.sbac` creada previamente por CP-001. |
| **Datos de Entrada** | Comando: `sbac init` |
| **Resultado Esperado** | 1. Mensaje de error claro en consola: "Error: El repositorio ya está inicializado en este directorio." <br> 2. La carpeta `.sbac` preexistente **no es sobrescrita ni eliminada**. <br> 3. Los metadatos previos permanecen intactos. |
| **Prioridad** | Alta |
| **Dependencias** | CP-001 debe haberse ejecutado previamente en este directorio. |

#### CP-003: Añadir archivo válido al seguimiento
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-003 |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Descripción** | Verificar que un archivo existente en el directorio de trabajo puede registrarse en el área de preparación. |
| **Precondiciones** | Repositorio inicializado (CP-001 ejecutado). El archivo `archivo_prueba.txt` existe en el directorio con contenido de texto. |
| **Datos de Entrada** | Comando: `sbac add archivo_prueba.txt` |
| **Resultado Esperado** | 1. El sistema registra el archivo en el área de preparación (staging). <br> 2. Mensaje de confirmación: "Archivo 'archivo_prueba.txt' agregado al seguimiento." <br> 3. No se generan errores de ejecución. |
| **Prioridad** | Alta |
| **Dependencias** | CP-001 |

#### CP-004: Añadir archivo inexistente (Equivalencia)
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-004 |
| **Técnica** | Partición de Equivalencia (clase inválida) + Caja Negra |
| **Descripción** | Verificar que el sistema rechaza la adición de un archivo que no existe en el directorio de trabajo. |
| **Precondiciones** | Repositorio inicializado (CP-001). El archivo `fantasma.txt` **no existe** en el directorio. |
| **Datos de Entrada** | Comando: `sbac add fantasma.txt` |
| **Resultado Esperado** | 1. Mensaje de error legible: "Error: El archivo 'fantasma.txt' no existe en el directorio actual." <br> 2. El área de preparación no se modifica. <br> 3. No se genera excepción no controlada (crash del script). |
| **Prioridad** | Media |
| **Dependencias** | CP-001 |

#### CP-005: Consultar estado actual del repositorio
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-005 |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Descripción** | Verificar que el comando `status` refleja correctamente los archivos en el área de preparación. |
| **Precondiciones** | Repositorio inicializado (CP-001). El archivo `archivo_prueba.txt` ha sido agregado (CP-003). |
| **Datos de Entrada** | Comando: `sbac status` |
| **Resultado Esperado** | 1. La consola muestra una lista que incluye `archivo_prueba.txt` con estado "preparado" o "staged". <br> 2. No se listan archivos no rastreados como modificados. <br> 3. El formato de salida es legible y consistente. |
| **Prioridad** | Alta |
| **Dependencias** | CP-001, CP-003 |

---

### 3.2 Módulo: Control de Versiones

#### CP-006: Crear versión con cambios (Commit exitoso)
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-006 |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Descripción** | Verificar la creación de una instantánea inmutable del estado actual con metadatos asociados. |
| **Precondiciones** | Repositorio inicializado (CP-001). Al menos un archivo agregado al área de preparación (CP-003). |
| **Datos de Entrada** | Comando: `sbac commit "Primera versión"` |
| **Resultado Esperado** | 1. Generación de un ID único de versión (e.g., `v1`, hash corto o UUID). <br> 2. Registro de marca temporal y mensaje asociado en el historial. <br> 3. Mensaje de éxito: "Commit realizado: [ID] - Primera versión". <br> 4. El área de preparación se limpia tras el commit. |
| **Prioridad** | Alta |
| **Dependencias** | CP-001, CP-003 |

#### CP-007: Crear versión sin mensaje asociado (Valor Límite)
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-007 |
| **Técnica** | Pruebas de Valor Límite (cadena vacía) + Caja Negra |
| **Descripción** | Verificar que el sistema impide la creación de un commit sin mensaje descriptivo. |
| **Precondiciones** | Repositorio inicializado (CP-001). Archivos en área de preparación (CP-003). |
| **Datos de Entrada** | Comando: `sbac commit ""` o `sbac commit` (sin argumento) |
| **Resultado Esperado** | 1. Operación rechazada. <br> 2. Mensaje de error: "Error: El mensaje de confirmación es obligatorio y no puede estar vacío." <br> 3. No se genera una nueva versión. <br> 4. Los archivos permanecen en el área de preparación. |
| **Prioridad** | Media |
| **Dependencias** | CP-001, CP-003 |

#### CP-008: Consultar historial de versiones (History)
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-008 |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Descripción** | Verificar la recuperación y despliegue del historial completo de confirmaciones. |
| **Precondiciones** | Repositorio inicializado (CP-001). Al menos un commit exitoso registrado (CP-006). |
| **Datos de Entrada** | Comando: `sbac history` |
| **Resultado Esperado** | 1. Listado cronológico en consola de todas las versiones confirmadas. <br> 2. Cada entrada muestra: ID de versión, mensaje del commit, fecha/hora. <br> 3. El orden es descendente (más reciente primero) o ascendente, pero consistente. <br> 4. No se omiten commits previamente realizados. |
| **Prioridad** | Alta |
| **Dependencias** | CP-001, CP-006 |

#### CP-009: Regresar a una versión válida (Checkout exitoso)
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-009 |
| **Técnica** | Análisis de Requisitos + Pruebas de Integración + Caja Negra |
| **Descripción** | Verificar que el directorio de trabajo se restaura al estado exacto de una versión histórica válida. |
| **Precondiciones** | Repositorio con al menos dos commits distintos (CP-006 ejecutado dos veces con archivos diferentes o modificados). Se conoce el ID de la primera versión (`v1`). |
| **Datos de Entrada** | Comando: `sbac checkout v1` (o ID válido correspondiente) |
| **Resultado Esperado** | 1. Los archivos en el directorio de trabajo vuelven al contenido y estado que tenían en la versión `v1`. <br> 2. Mensaje de éxito: "Directorio restaurado a la versión v1." <br> 3. No se pierden archivos no rastreados (si aplica según diseño del SBAC). <br> 4. El historial (`sbac history`) sigue mostrando todas las versiones; el checkout no elimina commits. |
| **Prioridad** | Alta |
| **Dependencias** | CP-001, CP-003, CP-006 (múltiples veces) |

#### CP-010: Regresar a una versión inexistente
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-010 |
| **Técnica** | Partición de Equivalencia (ID inválido) + Caja Negra |
| **Descripción** | Verificar el manejo de error cuando se solicita checkout de un ID de versión que no existe en el historial. |
| **Precondiciones** | Repositorio inicializado (CP-001) con al menos un commit (CP-006). |
| **Datos de Entrada** | Comando: `sbac checkout v999` (ID inexistente) |
| **Resultado Esperado** | 1. Mensaje de error claro: "Error: La versión 'v999' no existe en el historial." <br> 2. El directorio de trabajo **no es modificado**. <br> 3. No se genera excepción no controlada. |
| **Prioridad** | Media |
| **Dependencias** | CP-001, CP-006 |

---

### 3.3 Módulo: Líneas Base

#### CP-011: Marcar una versión como línea base
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-011 |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Descripción** | Verificar que una versión específica puede etiquetarse como línea base estable. |
| **Precondiciones** | Repositorio con al menos un commit (CP-006). Se conoce el ID de la última versión. |
| **Datos de Entrada** | Comando: `sbac baseline "Release1.0"` |
| **Resultado Esperado** | 1. La etiqueta "Release1.0" queda asociada persistentemente a la última versión confirmada (o a la versión actual según diseño). <br> 2. Mensaje de éxito: "Línea base 'Release1.0' creada correctamente." <br> 3. Los metadatos de la línea base se almacenan en `.sbac/` sin corromper el historial de commits. |
| **Prioridad** | Media |
| **Dependencias** | CP-001, CP-006 |

#### CP-012: Listar líneas base disponibles
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-012 |
| **Técnica** | Análisis de Requisitos + Caja Negra |
| **Descripción** | Verificar la consulta de todas las líneas base registradas en el repositorio. |
| **Precondiciones** | Repositorio con al menos una línea base creada (CP-011). |
| **Datos de Entrada** | Comando: `sbac list-baselines` |
| **Resultado Esperado** | 1. Listado en consola de todas las líneas base creadas. <br> 2. Cada entrada muestra: nombre de la etiqueta y versión asociada (e.g., "Release1.0 -> v1"). <br> 3. Si no existen líneas base, mensaje informativo: "No hay líneas base registradas." |
| **Prioridad** | Media |
| **Dependencias** | CP-001, CP-011 |

---

### 3.4 Módulo: Comparación

#### CP-013: Comparar dos versiones existentes (Diff)
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-013 |
| **Técnica** | Análisis de Requisitos + Pruebas de Integración + Caja Negra |
| **Descripción** | Verificar que el sistema calcula y muestra diferencias textuales entre dos versiones válidas usando `difflib`. |
| **Precondiciones** | Repositorio con al menos dos commits donde un archivo rastreado tenga contenido diferente entre versiones (e.g., `archivo_prueba.txt` modificado entre v1 y v2). |
| **Datos de Entrada** | Comando: `sbac diff v1 v2` |
| **Resultado Esperado** | 1. Salida en consola con formato de diferencias estándar (`+` para líneas añadidas, `-` para líneas eliminadas). <br> 2. Las diferencias corresponden exactamente a los cambios realizados entre ambas versiones. <br> 3. Uso correcto de la biblioteca `difflib` de Python (formato legible). <br> 4. No se muestran diferencias de archivos no modificados. |
| **Prioridad** | Alta |
| **Dependencias** | CP-001, CP-003, CP-006 (múltiples commits con cambios en archivos) |

#### CP-014: Comparar versiones con ID inexistente
| Atributo | Descripción |
|----------|-------------|
| **ID** | CP-014 |
| **Técnica** | Partición de Equivalencia (ID inválido) + Caja Negra |
| **Descripción** | Verificar el manejo de error cuando al menos uno de los IDs en el comando diff no existe. |
| **Precondiciones** | Repositorio inicializado (CP-001) con al menos un commit (CP-006). |
| **Datos de Entrada** | Comando: `sbac diff v1 v999` (donde `v999` no existe) |
| **Resultado Esperado** | 1. Mensaje de error claro: "Error: Una o ambas versiones especificadas no existen en el historial." <br> 2. No se intenta calcular diferencias con datos inexistentes. <br> 3. No se genera excepción no controlada. |
| **Prioridad** | Media |
| **Dependencias** | CP-001, CP-006 |

---

## 4. Trazabilidad de Requisitos a Casos de Prueba

| Requisito del Proyecto SBAC | Funcionalidad (Plan Maestro) | Caso de Prueba | Técnica de Diseño | Tipo |
|-----------------------------|------------------------------|----------------|-------------------|------|
| Inicializar repositorio | F-001 | CP-001 | Análisis de Requisitos | Positiva |
| Prevenir init duplicado | F-010 | CP-002 | Valor Límite | Negativa |
| Añadir archivos al seguimiento | F-002 | CP-003 | Análisis de Requisitos | Positiva |
| Rechazar archivos inexistentes | F-011 | CP-004 | Equivalencia (inválida) | Negativa |
| Mostrar estado del repositorio | F-003 | CP-005 | Análisis de Requisitos | Positiva |
| Crear nueva versión (commit) | F-004 | CP-006 | Análisis de Requisitos | Positiva |
| Rechazar commit sin mensaje | F-012 | CP-007 | Valor Límite (vacío) | Negativa |
| Listar historial de versiones | F-005 | CP-008 | Análisis de Requisitos | Positiva |
| Regresar a versión válida | F-006 | CP-009 | Integración | Positiva |
| Manejar checkout inválido | F-013 | CP-010 | Equivalencia (inválida) | Negativa |
| Marcar versión como línea base | F-007 | CP-011 | Análisis de Requisitos | Positiva |
| Listar líneas base | F-008 | CP-012 | Análisis de Requisitos | Positiva |
| Comparar diferencias | F-009 | CP-013 | Integración | Positiva |
| Manejar diff con ID inexistente | F-014 | CP-014 | Equivalencia (inválida) | Negativa |

---

## 5. Criterios de Éxito del Diseño

El diseño de pruebas se considera exitoso y listo para su ejecución cuando se cumplen las siguientes condiciones:

1. **Cobertura Completa:** Todos los comandos mínimos del SBAC (`init`, `add`, `status`, `commit`, `history`, `checkout`, `baseline`, `list-baselines`, `diff`) tienen al menos un caso de prueba positivo diseñado.
2. **Cobertura de Excepciones:** Todos los comandos que aceptan entradas variables o destructivas (`init`, `add`, `commit`, `checkout`, `diff`) tienen al menos un caso de prueba negativo o de valor límite diseñado.
3. **Consistencia de IDs:** Los identificadores CP-001 a CP-014 son únicos y coinciden exactamente con los documentos Plan de Pruebas Maestro, Plan de Pruebas de Nivel y Casos de Prueba.
4. **Independencia Lógica:** Cada caso de prueba define explícitamente sus precondiciones, datos de entrada y resultados esperados de forma no ambigua.
5. **Trazabilidad Verificable:** Existe una ruta clara y documentada desde cada requisito funcional del SBAC hasta su caso de prueba correspondiente (ver sección 4).

---

## 6. Observaciones y Supuestos de Diseño

1. **Ejecución Secuencial:** Debido a la naturaleza del sistema de control de versiones, la ejecución de la mayoría de los casos de prueba es secuencial. Por ejemplo, CP-006 (`commit`) depende estrictamente del éxito previo de CP-001 (`init`) y CP-003 (`add`). El diseño asume que los Procedimientos de Prueba respetarán este orden o prepararán el estado vía fixtures.
2. **Persistencia de Datos:** Se asume que el SBAC utiliza archivos simples (carpeta `.sbac/`) o MySQL para persistencia. Los resultados esperados de CP-008, CP-009, CP-011 y CP-012 asumen que la lectura de metadatos es consistente tras reinicios del sistema.
3. **Formato de IDs de Versión:** El diseño utiliza IDs genéricos (`v1`, `v2`) en los datos de entrada. Se asume que el SBAC generará IDs únicos (numéricos, hash o UUID) y que los Procedimientos de Prueba adaptarán los comandos `checkout` y `diff` a los IDs reales generados durante la ejecución.
4. **Alcance de `difflib`:** CP-013 asume que la salida de diferencias utilizará la biblioteca estándar `difflib` de Python, produciendo un formato legible en consola. No se exige formato unificado (`unified diff`) a menos que el diseño del SBAC lo especifique.
5. **Línea Base sobre última versión:** CP-011 asume que `sbac baseline` etiqueta la versión más reciente por defecto, a menos que el diseño del SBAC permita especificar un ID de versión objetivo.

---

## 7. Historial de Cambios

| Versión | Fecha | Autor | Descripción del Cambio |
|---------|-------|-------|------------------------|
| 1.0 | 29/05/2026 | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar | Creación inicial. Diseño completo de 14 casos de prueba (CP-001 a CP-014) cubriendo los 9 comandos mínimos del SBAC. Alineación con Plan Maestro y Plan de Nivel. Corrección de IDs desfasados respecto a versiones previas del proyecto. |

---

*Documento elaborado bajo el estándar IEEE 829-2008. Los IDs de casos de prueba (CP-001 a CP-014) son consistentes en todo el conjunto de documentación del proyecto SBAC.*
