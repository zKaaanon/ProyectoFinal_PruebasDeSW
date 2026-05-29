# Plan de Pruebas Maestro: Sistema Básico de Administración de Configuración (SBAC)

**1. Información General**

- **Proyecto:** Sistema Básico de Administración de Configuración (SBAC) .
- **Versión del Software:** 1.0.
- **Fecha de Creación:** 29 de mayo de 2026.
- **Responsable / Autor:** Cristian Ignacio Reyna Méndez y José Eleazar López Montufar.
- **Objetivo:** Definir la estrategia global de pruebas para la aplicación SBAC, validando la integridad del control de versiones de archivos de código en Python y asegurando que los niveles de calidad requeridos se cumplan antes del despliegue final.

**2. Elementos a Probar**

- **Módulo de Gestión de Repositorio:** Componentes lógicos encargados de la inicialización y el seguimiento de archivos.
- **Módulo de Control de Versiones:** Componentes lógicos encargados del historial y la navegación entre estados del código.
- **Módulo de Líneas Base:** Componentes encargados del marcado y aseguramiento de configuraciones estables.
- **Módulo de Comparación:** Componentes encargados del cálculo de diferencias de texto.

**3. Características que se Probarán**

- Inicialización correcta de un repositorio local mediante el comando `sbac init`.
- Adición y registro de archivos al sistema de seguimiento con `sbac add <archivo>`.
- Despliegue del estado actual del repositorio con `sbac status`.
- Creación de nuevas versiones con metadatos asociados mediante `sbac commit "mensaje"`.
- Despliegue del historial completo de confirmaciones con `sbac history`.
- Capacidad de regresar el directorio de trabajo a una versión específica con `sbac checkout <versión>`.
- Marcado y listado de líneas base utilizando `sbac baseline "nombre"` y `sbac list-baselines` .
- Visualización precisa de cambios y diferencias textuales empleando `sbac diff <v1> <v2>`.

**4. Enfoque de Pruebas (Estrategia General)**

- **Tipos de Pruebas:** Se realizarán pruebas unitarias para validar de forma aislada cada componente de la CLI, pruebas de integración para verificar la correcta persistencia de metadatos en el almacenamiento (archivos simples o MySQL), y pruebas de regresión básicas al introducir ajustes en la interfaz de usuario o comandos .
- **Técnicas de Diseño:** Aplicación de pruebas de caja negra, análisis de particiones de equivalencia para manejar datos inválidos, y pruebas de valor límite para verificar restricciones en las entradas de comandos (como mensajes de confirmación vacíos) .
- **Herramientas y Entorno:** Ejecución en consola sobre el entorno configurado de Python, utilizando la biblioteca estándar `difflib` para la lógica de comparación de archivos.

**5. Criterios de Aprobación / Rechazo**

- **Criterios de Éxito:** Ejecución correcta de las funcionalidades mínimas del sistema de administración de configuración (35% de la funcionalidad del sistema).
- **Criterios de Aceptación:** Robustez ante fallos; el sistema debe atrapar excepciones e imprimir mensajes de error claros al usuario en la terminal en lugar de romper la ejecución del script en Python.
- **Criterios de Rechazo:** Presencia de cualquier defecto de gravedad alta o crítica que bloquee comandos esenciales (como fallos al guardar archivos o pérdida de metadatos) en la versión de entrega .

**6. Calendario y Dependencias**

| **Fase** | **Actividades** | **Dependencias** |
| --- | --- | --- |
| **Planificación** | Redacción del Plan Maestro de Pruebas y definición de criterios de éxito. | Aprobación de la descripción general del proyecto SBAC . |
| **Preparación** | Configuración del entorno de desarrollo y diseño de casos de prueba iniciales (positivos y negativos). | Finalización de la estructura de almacenamiento elegida (Archivos simples / MySQL). |
| **Ejecución** | Realización de pruebas unitarias modulares y de integración sobre la CLI. | Disponibilidad de las funciones base de Python codificadas. |
| **Informe** | Compleción de la documentación técnica bajo el estándar IEEE 829 y evaluación de resultados. | Conclusión de los ciclos planificados de ejecución de pruebas. |

**7. Entregables**

- Código fuente final del sistema de administración de configuración (SBAC).
- Código de los scripts de prueba automatizados desarrollados.
- Documentación IEEE 829 completa: Plan de Pruebas Maestro, Especificaciones de Diseño, Casos de Prueba, Procedimientos, Informes de Incidentes e Informe de Resumen de Pruebas .
- Manual de usuario básico de la CLI.

**8. Recursos Necesarios**

- **Personal:** 2 Ingeniero de Pruebas / Desarrollador .
- **Hardware y Software:** Equipo de cómputo personal con entorno de ejecución Python instalado y terminal de comandos accesible.
- **Datos de Prueba:** Archivos de código fuente simulados con diferentes extensiones y contenidos para verificar el seguimiento y control de versiones.

**9. Riesgos y Mitigaciones**

| **Riesgo** | **Impacto** | **Mitigación** |
| --- | --- | --- |
| Compresión del tiempo disponible debido a la proximidad de la fecha límite de entrega. | Alto | Priorizar la cobertura de pruebas estrictamente sobre las 4 funcionalidades mínimas requeridas por la rúbrica . |
| Inestabilidad o corrupción en el almacenamiento local de versiones al ejecutar comandos concurrentes. | Medio | Diseñar procedimientos de prueba específicos que verifiquen el estado del repositorio antes y después de cada comando de escritura (`add`, `commit`) . |