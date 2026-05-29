# Plan de Pruebas de Nivel: Funcionalidad e Integración (CLI del SBAC)

## 1. Información General

| Campo | Valor |
|-------|-------|
| **Nivel de prueba** | Pruebas funcionales y de integración para la Interfaz de Línea de Comandos (CLI) |
| **Proyecto** | Sistema Básico de Administración de Configuración (SBAC) v1.0 |
| **Fecha de Creación** | 29 de mayo de 2026 |
| **Responsables** | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar |
| **Objetivo** | Validar que los comandos del sistema permitan a los usuarios interactuar con el repositorio local, gestionar versiones de archivos de código y que el sistema maneje correctamente tanto las entradas válidas como las excepciones, garantizando la integridad de la persistencia de datos. |
| **Documento Maestro de Referencia** | Plan de Pruebas Maestro SBAC v1.0 (sección 10: Trazabilidad de Requisitos a Casos de Prueba) |

---

## 2. Alcance Específico

### 2.1 Dentro del Alcance
Este plan de nivel se centra en la validación exhaustiva de los 9 comandos mínimos de la CLI del SBAC, ejecutados secuencialmente para simular un flujo de trabajo real de administración de configuración:

- **Módulo de Gestión de Repositorio:** `sbac init`, `sbac add <archivo>`, `sbac status`
- **Módulo de Control de Versiones:** `sbac commit "mensaje"`, `sbac history`, `sbac checkout <versión>`
- **Módulo de Líneas Base:** `sbac baseline "nombre"`, `sbac list-baselines`
- **Módulo de Comparación:** `sbac diff <v1> <v2>`

Se probarán tanto los **escenarios positivos (Happy Path)** como los **escenarios negativos y de valor límite** para cada comando que lo requiera, conforme a la matriz de trazabilidad del Plan Maestro.

### 2.2 Fuera del Alcance de este Nivel
- Pruebas de rendimiento o estrés (volumen masivo de archivos).
- Pruebas de seguridad (autenticación, permisos de usuario).
- Pruebas de usabilidad de una interfaz gráfica (GUI); este nivel es exclusivo de CLI.
- Pruebas de concurrencia (múltiples instancias simultáneas del SBAC).

---

## 3. Estrategia de Nivel

### 3.1 Técnica Principal
**Pruebas manuales de Caja Negra** ejecutadas directamente en la terminal del sistema operativo, donde el probador interactúa con la CLI sin conocer la implementación interna del código Python.

### 3.2 Técnica Complementaria
**Pruebas unitarias automatizadas** mediante scripts en `pytest` para validar la lógica interna de persistencia (lectura/escritura de la carpeta `.sbac`, integridad de metadatos, generación de IDs de versión y funcionamiento de `difflib`).

### 3.3 Enfoque de Ejecución
- **Secuencial por dependencia:** El flujo de pruebas respeta el orden lógico de un sistema de control de versiones: no se puede probar `commit` sin antes ejecutar `init` y `add`; no se puede probar `diff` sin antes tener al menos dos versiones.
- **Inyección de errores deliberados:** Se introducirán comandos con sintaxis incorrecta, archivos inexistentes, mensajes vacíos e IDs de versión inexistentes para validar la robustez del sistema.
- **Verificación física de persistencia:** Tras comandos de escritura (`init`, `add`, `commit`, `checkout`, `baseline`), se verificará manualmente el estado del directorio `.sbac` y los archivos de metadatos para confirmar la integridad de los datos.

### 3.4 Ambiente de Pruebas
| Componente | Especificación |
|------------|---------------|
| Sistema Operativo | Windows 10/11 (PowerShell) o Linux (Bash) |
| Entorno de Ejecución | Python 3.8+ |
| Terminal | CMD, PowerShell o Bash |
| Directorio de Trabajo | Carpetas locales temporales (`test_repo/`) aisladas del repositorio de desarrollo |
| Datos de Prueba | Archivos `.txt` de contenido controlado (`archivo_prueba.txt`, `archivo1.txt`, `archivo2.txt`) |

---

## 4. Criterios de Entrada y Salida

### 4.1 Criterios de Entrada (Para iniciar este nivel de pruebas)
- [ ] El código fuente de los 4 módulos del SBAC está completo, sin errores de sintaxis en Python y accesible desde la terminal.
- [ ] La CLI responde a los 9 comandos mínimos (`init`, `add`, `status`, `commit`, `history`, `checkout`, `baseline`, `list-baselines`, `diff`) sin lanzar excepciones no controladas al nivel del intérprete.
- [ ] La estructura de almacenamiento (archivos simples en `.sbac/` o MySQL) está implementada y permite la escritura y lectura de metadatos.
- [ ] El entorno local de pruebas está limpio: no existen carpetas `.sbac` residuales ni archivos temporales de ejecuciones previas que puedan generar falsos positivos.
- [ ] Los datos de prueba (archivos `.txt`) están creados con permisos de lectura/escritura en un directorio de pruebas aislado.

### 4.2 Criterios de Salida (Para dar por concluido este nivel)
- [ ] El 100% de los casos de prueba positivos (CP-001, CP-003, CP-005, CP-006, CP-008, CP-009, CP-011, CP-012, CP-013) han sido ejecutados y documentados con estado **Pasó**.
- [ ] El 100% de los casos de prueba negativos y de valor límite (CP-002, CP-004, CP-007, CP-010, CP-014) han sido ejecutados y documentados con estado **Pasó**, demostrando un manejo de errores claro y sin corrupción de datos.
- [ ] Se ha verificado físicamente la persistencia de datos tras cada comando de escritura (existencia de archivos en `.sbac/`, contenido de metadatos).
- [ ] Los incidentes de gravedad **Crítica** o **Alta** encontrados han sido reportados mediante Registros de Incidente y, de ser posible, corregidos y validados con pruebas de regresión.
- [ ] La documentación de resultados de ejecución está completa en los Casos de Prueba (campos "Resultados Reales" y "Estado" llenados).

---

## 5. Casos de Prueba del Nivel

Los siguientes casos de prueba son consistentes con la matriz de trazabilidad del Plan de Pruebas Maestro (sección 10). Cada ID es inmutable en todos los documentos derivados.

### 5.1 Módulo de Gestión de Repositorio

| ID | Descripción | Tipo de Prueba | Estado |
|----|-------------|----------------|--------|
| **CP-001** | Inicializar un nuevo repositorio (`sbac init`) en directorio limpio. | Funcional (Positiva) | Pendiente |
| **CP-002** | Inicializar un repositorio duplicado (`sbac init` sobre `.sbac` existente). | Valor Límite (Negativa) | Pendiente |
| **CP-003** | Añadir archivo válido al seguimiento (`sbac add archivo_prueba.txt`). | Funcional (Positiva) | Pendiente |
| **CP-004** | Añadir archivo inexistente al seguimiento (`sbac add fantasma.txt`). | Equivalencia (Negativa) | Pendiente |
| **CP-005** | Consultar estado actual del repositorio (`sbac status`) con archivos preparados. | Funcional (Positiva) | Pendiente |

### 5.2 Módulo de Control de Versiones

| ID | Descripción | Tipo de Prueba | Estado |
|----|-------------|----------------|--------|
| **CP-006** | Crear versión con mensaje válido (`sbac commit "Primera versión"`). | Funcional (Positiva) | Pendiente |
| **CP-007** | Crear versión con mensaje vacío (`sbac commit ""` o `sbac commit` sin argumento). | Valor Límite (Negativa) | Pendiente |
| **CP-008** | Consultar historial de versiones (`sbac history`) con commits previos. | Funcional (Positiva) | Pendiente |
| **CP-009** | Regresar a una versión válida (`sbac checkout <ID_válido>`). | Funcional / Integración (Positiva) | Pendiente |
| **CP-010** | Regresar a una versión inexistente (`sbac checkout v999`). | Funcional (Negativa) | Pendiente |

### 5.3 Módulo de Líneas Base

| ID | Descripción | Tipo de Prueba | Estado |
|----|-------------|----------------|--------|
| **CP-011** | Marcar una versión como línea base (`sbac baseline "Release1.0"`). | Funcional (Positiva) | Pendiente |
| **CP-012** | Listar líneas base disponibles (`sbac list-baselines`) tras crear al menos una. | Funcional (Positiva) | Pendiente |

### 5.4 Módulo de Comparación

| ID | Descripción | Tipo de Prueba | Estado |
|----|-------------|----------------|--------|
| **CP-013** | Comparar dos versiones válidas con cambios (`sbac diff v1 v2`). | Integración (Positiva) | Pendiente |
| **CP-014** | Comparar versiones donde al menos un ID no existe (`sbac diff v1 v999`). | Funcional (Negativa) | Pendiente |

### 5.5 Resumen de Cobertura por Módulo

| Módulo | Casos Positivos | Casos Negativos | Total |
|--------|-----------------|-----------------|-------|
| Gestión de Repositorio | CP-001, CP-003, CP-005 | CP-002, CP-004 | 5 |
| Control de Versiones | CP-006, CP-008, CP-009 | CP-007, CP-010 | 5 |
| Líneas Base | CP-011, CP-012 | — | 2 |
| Comparación | CP-013 | CP-014 | 2 |
| **Total General** | **9** | **5** | **14** |

---

## 6. Recursos del Nivel

### 6.1 Personal
| Rol | Cantidad | Responsabilidad |
|-----|----------|-----------------|
| Probador / Desarrollador | 2 | Ejecución manual de comandos en terminal, verificación física de archivos, documentación de resultados. |

### 6.2 Herramientas de Software
| Herramienta | Propósito |
|-------------|-----------|
| Python 3.x | Entorno de ejecución del SBAC y framework de pruebas unitarias. |
| Terminal (CMD / PowerShell / Bash) | Ejecución manual de la CLI del SBAC. |
| Editor de texto / IDE (VS Code, PyCharm) | Verificación rápida de archivos de metadatos generados en `.sbac/`. |
| `pytest` (opcional, para capa unitaria) | Automatización de pruebas sobre la lógica interna de persistencia y diff. |

### 6.3 Datos de Prueba
- **Directorio limpio:** `test_repo/` vacío para pruebas de `init`.
- **Archivos existentes:** `archivo_prueba.txt` (con contenido de texto plano), `archivo1.txt`, `archivo2.txt`.
- **Archivos inexistentes:** `fantasma.txt` (no creado en disco, para prueba CP-004).
- **Mensajes de commit:** `"Primera versión"`, `"Segunda versión"`, `""` (vacío, para CP-007).
- **Etiquetas de línea base:** `"Release1.0"`, `"Sprint2"`.

---

## 7. Cronograma Detallado

| Fecha | Actividades | Producto Esperado |
|-------|-------------|-------------------|
| **29 de mayo 2026** | Configuración del entorno limpio. Revisión del Plan Maestro y diseño detallado de los 14 casos de prueba (CP-001 a CP-014) estableciendo datos de entrada y resultados esperados. | Plan de Nivel v1.0 aprobado internamente. Especificación de Diseño de Pruebas actualizada con IDs consistentes. |
| **30 de mayo 2026** | Ejecución interactiva de los comandos en la terminal. Verificación física de la persistencia de datos tras usar `add`, `commit`, `checkout` y `baseline`. Registro de resultados reales en los Casos de Prueba. | Campos "Resultados Reales" y "Estado" completados para CP-001 a CP-014. |
| **31 de mayo 2026** | Levantamiento y registro de incidentes en caso de fallos (Informes de Incidente). Pruebas de regresión sobre defectos corregidos. Redacción del Informe de Resumen de Pruebas de Nivel. | Registros de Incidentes (INC-XXX), Informe de Resumen de Pruebas y recomendaciones de liberación. |

---

## 8. Riesgos y Mitigaciones Específicas del Nivel

| ID | Riesgo | Impacto | Probabilidad | Mitigación |
|----|--------|---------|--------------|------------|
| RN-001 | Falsos positivos derivados de probar comandos sobre un directorio que ya contiene metadatos de pruebas anteriores (`.sbac` residual). | Medio | Alta | **Incluir en las condiciones previas de cada Procedimiento de Prueba el borrado manual de la carpeta `.sbac` y archivos temporales antes de iniciar un nuevo ciclo de validación.** |
| RN-002 | Dependencia secuencial entre casos de prueba dificulta la ejecución aislada (e.g., CP-006 depende de CP-001 y CP-003). | Medio | Alta | Documentar explícitamente las dependencias en el campo "Condiciones Previas" de cada Caso de Prueba. Utilizar fixtures de `pytest` que automaticen la preparación del estado requerido para las pruebas unitarias complementarias. |
| RN-003 | Diferencias en comportamiento de la CLI entre terminales (Windows vs. Linux) o codificación de caracteres. | Medio | Media | Especificar en los Procedimientos de Prueba la terminal de referencia utilizada. Si se detectan discrepancias, documentarlas como observaciones en los casos afectados. |
| RN-004 | Pérdida de tiempo en depuración de errores del propio código del SBAC durante la fase de ejecución de pruebas. | Alto | Media | Reservar la mañana del 30 de mayo exclusivamente para ejecución de pruebas sobre código ya estabilizado. Si el código presenta errores críticos de sintaxis, suspender la ejecución y retomar tras corrección. |
| RN-005 | Corrupción del almacenamiento local al ejecutar `checkout` sobre un directorio de trabajo modificado. | Alto | Media | Verificar el estado del repositorio con `sbac status` antes y después de cada `checkout`. Documentar cualquier archivo no rastreado que pudiera sobrescribirse. |

---

## 9. Relación con Otros Documentos IEEE 829

| Documento IEEE 829 | Relación con este Plan de Nivel |
|--------------------|--------------------------------|
| **Plan de Pruebas Maestro** | Este documento deriva directamente del Plan Maestro. La sección 5 de este nivel respeta la matriz de trazabilidad (CP-001 a CP-014) definida en el Plan Maestro, sección 10. |
| **Especificación de Diseño de Pruebas** | Define las técnicas (caja negra, equivalencia, valor límite) aplicadas a cada CP. Este Plan de Nivel asigna esos CP a fases de ejecución y recursos. |
| **Casos de Prueba** | Documento detallado con precondiciones, pasos, datos de entrada y resultados esperados para cada CP-001 a CP-014. |
| **Procedimientos de Prueba** | Guía paso a paso de cómo ejecutar cada caso en terminal, incluyendo limpieza de entorno y verificación de resultados intermedios. |
| **Registros de Incidentes** | Se generarán durante la ejecución (30-31 mayo) si los resultados reales difieren de los esperados. |
| **Informe de Resumen de Pruebas** | Se redactará al cierre de este nivel (31 mayo) evaluando si se cumplieron los criterios de salida. |

---

## 10. Historial de Cambios

| Versión | Fecha | Autor | Descripción del Cambio |
|---------|-------|-------|------------------------|
| 1.0 | 29/05/2026 | Cristian Ignacio Reyna Méndez y José Eleazar López Montufar | Creación inicial. Alineación completa con Plan Maestro: 14 casos de prueba (CP-001 a CP-014) cubriendo los 9 comandos mínimos del SBAC. Corrección de desfases de IDs respecto a versiones previas. |

---

*Documento elaborado bajo el estándar IEEE 829-2008. IDs de casos de prueba consistentes con el Plan de Pruebas Maestro SBAC v1.0.*
