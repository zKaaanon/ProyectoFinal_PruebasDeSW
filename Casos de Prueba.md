# Casos de Prueba

## 1. Información General del Nivel de Pruebas

- **Proyecto:** Sistema Básico de Administración de Configuración (SBAC)
- **Versión del Software:** 1.0
- **Responsables:** Cristian Ignacio Reyna Méndez y José Eleazar López Montufar
- **Fecha de Creación:** 29 de mayo de 2026
- **Elementos bajo prueba:** Módulos de Gestión de Repositorio, Control de Versiones, Líneas Base y Comparación ejecutados a través de la Interfaz de Línea de Comandos (CLI) en Python

## 2. Especificación Detallada de los Casos de Prueba

### CP-001: Inicialización exitosa del repositorio

- **Condiciones previas:** Entorno de Python configurado y terminal abierta en un directorio vacío.
- **Datos de entrada:** `sbac init`
- **Pasos de ejecución:**
    1. Abrir la terminal.
    2. Navegar al directorio vacío.
    3. Ejecutar `sbac init`.
- **Resultados esperados:** Creación de la carpeta oculta `.sbac` y mensaje de éxito.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Validar con explorador de archivos o `ls -a`.

### CP-002: Inicialización en un repositorio existente (Valor Límite)

- **Condiciones previas:** Carpeta `.sbac` ya existente.
- **Datos de entrada:** `sbac init`
- **Pasos de ejecución:**
    1. Abrir terminal en el repositorio inicializado.
    2. Ejecutar `sbac init`.
- **Resultados esperados:** Mensaje de error indicando repositorio ya inicializado.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Verificar que los datos previos permanezcan intactos.

### CP-003: Añadir archivo válido al seguimiento

- **Condiciones previas:** Repositorio inicializado y archivo `archivo_prueba.txt` existente.
- **Datos de entrada:** `sbac add archivo_prueba.txt`
- **Pasos de ejecución:**
    1. Abrir terminal en el repositorio.
    2. Ejecutar `sbac add archivo_prueba.txt`.
- **Resultados esperados:** Registro del archivo en el área de preparación.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Comprobar con `sbac status`.

### CP-004: Añadir archivo inexistente al seguimiento (Equivalencia)

- **Condiciones previas:** Repositorio inicializado, archivo `fantasma.txt` no existente.
- **Datos de entrada:** `sbac add fantasma.txt`
- **Pasos de ejecución:**
    1. Abrir terminal en el repositorio.
    2. Ejecutar `sbac add fantasma.txt`.
- **Resultados esperados:** Mensaje de error indicando inexistencia del archivo.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Validar retorno limpio de la consola.

### CP-005: Consultar estado actual del repositorio

- **Condiciones previas:** Repositorio inicializado y archivo agregado (CP-003).
- **Datos de entrada:** `sbac status`
- **Pasos de ejecución:**
    1. Abrir terminal en el repositorio.
    2. Ejecutar `sbac status`.
- **Resultados esperados:** Mostrar `archivo_prueba.txt` en estado preparado.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Corroborar comunicación entre `add` y estado.

### CP-006: Crear versión con cambios (Commit exitoso)

- **Condiciones previas:** Repositorio inicializado y archivo preparado.
- **Datos de entrada:** `sbac commit "Primera versión"`
- **Pasos de ejecución:**
    1. Abrir terminal en el proyecto.
    2. Ejecutar `sbac commit "Primera versión"`.
- **Resultados esperados:** Generación de versión con ID único y metadatos.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Verificar registro en base de datos o archivos.

### CP-007: Crear versión sin mensaje asociado (Valor Límite)

- **Condiciones previas:** Repositorio con archivos preparados.
- **Datos de entrada:** `sbac commit ""` o `sbac commit`
- **Pasos de ejecución:**
    1. Abrir terminal en el repositorio.
    2. Ejecutar `sbac commit ""`.
- **Resultados esperados:** Rechazo de operación con alerta de obligatoriedad del mensaje.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Validar restricciones en entrada de texto.

### CP-008: Consultar historial de versiones (History)

- **Condiciones previas:** Al menos un commit exitoso.
- **Datos de entrada:** `sbac history`
- **Pasos de ejecución:**
    1. Abrir terminal en el proyecto.
    2. Ejecutar `sbac history`.
- **Resultados esperados:** Listado cronológico de versiones con IDs, mensajes y marcas de tiempo.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Verificar recuperación de metadatos.

### CP-009: Marcar una versión como línea base (Baseline)

- **Condiciones previas:** Al menos un commit registrado.
- **Datos de entrada:** `sbac baseline "Release1.0"`
- **Pasos de ejecución:**
    1. Abrir terminal en el repositorio.
    2. Ejecutar `sbac baseline "Release1.0"`.
- **Resultados esperados:** Etiqueta "Release1.0" asociada a la última versión.
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Comprobar con `sbac list-baselines`.

### CP-010: Comparar diferencias entre dos versiones

- **Condiciones previas:** Al menos dos versiones existentes con cambios.
- **Datos de entrada:** `sbac diff v1 v2`
- **Pasos de ejecución:**
    1. Abrir terminal en el repositorio.
    2. Ejecutar `sbac diff v1 v2`.
- **Resultados esperados:** Mostrar diferencias usando `difflib` con símbolos (+/-).
- **Resultados reales:** (Por completar)
- **Estado:** (Por completar)
- **Comentarios:** Validar legibilidad en la CLI.