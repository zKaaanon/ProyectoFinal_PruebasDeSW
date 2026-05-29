# Especificación de Diseño de Pruebas

**1. Información General**

- **Proyecto:** Sistema Básico de Administración de Configuración (SBAC) .
- **Módulos:** Gestión de Repositorio, Control de Versiones, Líneas Base y Comparación .
- **Responsables:** Cristian Ignacio Reyna Méndez y José Eleazar López Montufar.
- **Objetivo:** Definir los casos de prueba detallados para validar el correcto funcionamiento de los comandos del sistema SBAC, garantizando la cobertura de los requisitos funcionales y el manejo de excepciones .
- **Técnicas de Diseño Aplicadas:** Pruebas de Caja Negra, Análisis de Requisitos, Pruebas de Valor Límite y Pruebas de Equivalencia .

**2. Condiciones Previas**

- El entorno de ejecución de Python debe estar configurado y la CLI del SBAC debe estar accesible en el sistema.
- Las pruebas deben ejecutarse en un directorio local de pruebas aislado y vacío (para los casos de inicialización) .
- Los archivos de texto simulados para pruebas (`archivo_prueba.txt`) deben tener permisos de lectura y escritura.

**3. Identificación de Pruebas**

| **ID** | **Descripción** | **Datos de Entrada** | **Resultado Esperado** |
| --- | --- | --- | --- |
| **CP-001** | Inicialización exitosa del repositorio | Comando: `sbac init` en un directorio vacío | Creación de la estructura de configuración oculta y mensaje de éxito. |
| **CP-002** | Inicialización en repositorio existente | Comando: `sbac init` en un directorio ya inicializado | Mensaje de error indicando que el repositorio ya existe; no se sobrescriben datos. |
| **CP-003** | Añadir archivo válido al seguimiento | Comando: `sbac add archivo_prueba.txt` (archivo existente) | El archivo se registra correctamente para la próxima versión. |
| **CP-004** | Añadir archivo inexistente | Comando: `sbac add fantasma.txt` | Mensaje de error indicando que el archivo especificado no se encuentra en el directorio. |
| **CP-005** | Consultar estado del repositorio | Comando: `sbac status` | Muestra la lista de archivos rastreados y sus estados actuales de modificación. |
| **CP-006** | Crear versión con cambios | Comando: `sbac commit "Primera versión"` tras un `add` | Se genera un registro inmutable de la versión en el historial con su respectivo mensaje. |
| **CP-007** | Crear versión sin mensaje | Comando: `sbac commit ""` o `sbac commit` | Mensaje de error advirtiendo que el mensaje de confirmación es obligatorio. |
| **CP-008** | Consultar historial de versiones | Comando: `sbac history` | Se despliega en consola la lista secuencial de versiones confirmadas y sus detalles. |
| **CP-009** | Marcar línea base | Comando: `sbac baseline "Release1.0"` | Se asigna la etiqueta "Release1.0" a la versión actual. |
| **CP-010** | Comparar dos versiones existentes | Comando: `sbac diff v1 v2` (IDs válidos) | Se muestran las diferencias textuales entre ambas versiones utilizando la biblioteca `difflib` . |

**4. Criterios de Éxito**

- Cada prueba debe completarse sin errores de ejecución a nivel de intérprete (crash del script) y cumplir estrictamente con los resultados esperados detallados.
- Las pruebas de validación de entradas (CP-002, CP-004, CP-007) deben demostrar un correcto manejo de errores mediante mensajes legibles para el usuario.

**5. Observaciones**

- Debido a la naturaleza del sistema de control de versiones, la ejecución de la mayoría de los casos de prueba es secuencial; pruebas como `sbac commit` (CP-006) dependen estrictamente del éxito previo de `sbac init` (CP-001) y `sbac add` (CP-003) .