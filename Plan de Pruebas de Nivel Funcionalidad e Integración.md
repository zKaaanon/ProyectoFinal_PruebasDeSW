# Plan de Pruebas de Nivel: Funcionalidad e Integración (CLI del SBAC)

**1. Información General**

- **Nivel de prueba:** Pruebas funcionales y de integración para la Interfaz de Línea de Comandos (CLI).
- **Responsable:** Cristian Ignacio Reyna Méndez y José Eleazar López Montufar.
- **Objetivo:** Validar que los comandos del sistema permitan a los usuarios autenticar cambios, interactuar con el repositorio local y que el sistema maneje correctamente tanto las entradas válidas como las excepciones .

**2. Alcance Específico**

- Se probará el comportamiento de la terminal interactuando con los módulos lógicos en Python.
- Se validará la integración del código con el sistema de persistencia de datos (verificando la creación física de carpetas ocultas o registros en MySQL).
- Comandos a probar: `init`, `add`, `status`, `commit`, `history`, `checkout`, `baseline`, `list-baselines`, `diff` .

**3. Estrategia de Nivel**

- **Técnica:** Pruebas manuales de caja negra ejecutadas directamente en la consola del sistema operativo.
- **Enfoque:** Ejecución secuencial imitando el flujo de trabajo real de un usuario (inicializar -> añadir -> confirmar -> comparar) . Se forzarán errores deliberados introduciendo comandos con sintaxis incorrecta o archivos inexistentes .

**4. Criterios de Entrada y Salida**

- **Criterios de Entrada:** El código fuente del comando específico a probar debe estar finalizado, sin errores de sintaxis en Python, y el entorno local de pruebas debe estar limpio (sin repositorios previos que generen falsos positivos).
- **Criterios de Salida:** El comando debe superar tanto el caso de prueba funcional ("Happy Path") como su respectivo caso límite o de error, registrando los resultados obtenidos.

**5. Casos de Prueba** 

| **ID** | **Descripción** | **Tipo de Prueba** | **Estado** |
| --- | --- | --- | --- |
| **CP-001** | Inicializar un nuevo repositorio (`sbac init`) en directorio limpio. | Funcional (Positiva) | Pendiente |
| **CP-002** | Inicializar un repositorio duplicado. | Valor Límite (Negativa) | Pendiente |
| **CP-003** | Añadir archivo válido al seguimiento (`sbac add`). | Funcional (Positiva) | Pendiente |
| **CP-004** | Añadir archivo inexistente al seguimiento. | Equivalencia (Negativa) | Pendiente |
| **CP-005** | Crear versión con mensaje (`sbac commit`). | Funcional (Positiva) | Pendiente |
| **CP-006** | Crear versión con mensaje vacío. | Valor Límite (Negativa) | Pendiente |
| **CP-007** | Comparar dos versiones válidas (`sbac diff`). | Integración (Positiva) | Pendiente |

**6. Recursos del Nivel**

- **Personal:** 2 Probador .
- **Herramientas de Software:** Python 3.x, terminal del sistema operativo (CMD/PowerShell o Bash), y un editor de texto/IDE para la verificación rápida de diferencias .
- **Datos de Prueba:** Tres archivos `.txt` de prueba (`archivo1.txt`, `archivo2.txt` vacío, y un archivo no rastreado).

**7. Cronograma Detallado**

- **29 de Mayo:** Configuración del entorno limpio. Diseño detallado y documentación de los 7 casos de prueba (CP-001 a CP-007) estableciendo datos de entrada y resultados esperados .
- **30 de Mayo:** Ejecución interactiva de los comandos en la terminal. Verificación física de la persistencia de datos tras usar `commit` y `add` .
- **31 de Mayo:** Levantamiento y registro de incidentes en caso de fallos (Informes de Incidente) y redacción del Informe de Resumen de Pruebas .

**8. Riesgos y Mitigaciones**

- **Riesgo:** Falsos positivos derivados de probar comandos sobre un directorio que ya contiene metadatos de pruebas anteriores .
- **Mitigación:** Incluir en las condiciones previas de cada Procedimiento de Prueba el borrado manual de la carpeta del repositorio local antes de iniciar un nuevo ciclo de validación.