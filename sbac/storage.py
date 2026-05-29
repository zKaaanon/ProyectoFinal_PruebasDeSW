"""
storage.py — Módulo de persistencia para el SBAC
Gestiona la lectura y escritura de todos los archivos JSON dentro de .sbac/
"""

import json
import os
import shutil
from datetime import datetime

SBAC_DIR     = ".sbac"
CONFIG_FILE  = os.path.join(SBAC_DIR, "config.json")
INDEX_FILE   = os.path.join(SBAC_DIR, "index.json")
HISTORY_FILE = os.path.join(SBAC_DIR, "history.json")
BASELINES_FILE = os.path.join(SBAC_DIR, "baselines.json")
OBJECTS_DIR  = os.path.join(SBAC_DIR, "objects")   # copias físicas de archivos por versión


def _read_json(path: str) -> dict | list:
    """Lee un archivo JSON y devuelve su contenido. Lanza StorageError si falla."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise StorageError(f"Archivo no encontrado: {path}")
    except json.JSONDecodeError as e:
        raise StorageError(f"JSON corrupto en {path}: {e}")


def _write_json(path: str, data: dict | list) -> None:
    """Escribe data en path como JSON con sangría legible."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class StorageError(Exception):
    """Excepción interna del módulo de almacenamiento."""
    pass


def repo_exists() -> bool:
    """Devuelve True si .sbac/ existe y tiene config.json válido."""
    return os.path.isdir(SBAC_DIR) and os.path.isfile(CONFIG_FILE)


def assert_repo_exists() -> None:
    """
    Lanza SystemExit con mensaje amigable si no hay repositorio.
    Llamar al inicio de cualquier comando que requiera init previo.
    """
    if not repo_exists():
        print("Error: no hay repositorio inicializado en este directorio.")
        print("       Ejecuta primero: sbac init")
        raise SystemExit(1)

def init_repo() -> None:
    """
    Crea la estructura completa de .sbac/ para un repositorio nuevo.
    Lanza StorageError si ya existe un repositorio.
    """
    if repo_exists():
        raise StorageError("El repositorio ya está inicializado en este directorio.")

    os.makedirs(OBJECTS_DIR, exist_ok=True)

    _write_json(CONFIG_FILE, {
        "initialized": True,
        "version": "1.0",
        "created_at": datetime.now().isoformat()
    })
    _write_json(INDEX_FILE,    {"staged": []})
    _write_json(HISTORY_FILE,  [])
    _write_json(BASELINES_FILE, {})


def read_config() -> dict:
    return _read_json(CONFIG_FILE)

def read_index() -> dict:
    """Devuelve el índice de staging: {"staged": ["archivo1.txt", ...]}"""
    return _read_json(INDEX_FILE)


def write_index(index: dict) -> None:
    _write_json(INDEX_FILE, index)


def stage_file(filename: str) -> None:
    """
    Agrega filename al área de staging si no está ya.
    Lanza StorageError si el archivo no existe en el directorio de trabajo.
    """
    if not os.path.isfile(filename):
        raise StorageError(f"El archivo '{filename}' no existe en el directorio actual.")

    index = read_index()
    if filename not in index["staged"]:
        index["staged"].append(filename)
        write_index(index)


def clear_staging() -> None:
    """Vacía el área de staging tras un commit exitoso."""
    write_index({"staged": []})

def read_history() -> list:
    """
    Devuelve la lista de commits en orden cronológico ascendente.
    Cada commit tiene: id, message, timestamp, files (dict nombre→contenido).
    """
    return _read_json(HISTORY_FILE)


def write_history(history: list) -> None:
    _write_json(HISTORY_FILE, history)


def next_version_id(history: list) -> str:
    """Genera el siguiente ID correlativo: v1, v2, v3…"""
    return f"v{len(history) + 1}"


def create_commit(message: str) -> dict:
    """
    Crea una nueva entrada en el historial con los archivos en staging.
    - Guarda una copia física de cada archivo en .sbac/objects/
    - Limpia el área de staging
    Lanza StorageError si el mensaje está vacío o si no hay archivos staged.
    """
    message = message.strip()
    if not message:
        raise StorageError("El mensaje de confirmación es obligatorio y no puede estar vacío.")

    index = read_index()
    if not index["staged"]:
        raise StorageError("No hay archivos en el área de preparación. Ejecuta sbac add <archivo> primero.")

    history = read_history()
    version_id = next_version_id(history)

    snapshot = {}
    for filename in index["staged"]:
        if not os.path.isfile(filename):
            raise StorageError(f"El archivo '{filename}' ya no existe en el directorio.")
        object_path = _object_path(version_id, filename)
        os.makedirs(os.path.dirname(object_path), exist_ok=True)
        shutil.copy2(filename, object_path)
        with open(filename, "r", encoding="utf-8") as f:
            snapshot[filename] = f.read()

    commit = {
        "id":        version_id,
        "message":   message,
        "timestamp": datetime.now().isoformat(),
        "files":     snapshot        
    }
    history.append(commit)
    write_history(history)
    clear_staging()
    return commit


def get_commit(version_id: str) -> dict:
    """
    Devuelve el commit con el ID dado.
    Lanza StorageError si no existe.
    """
    for commit in read_history():
        if commit["id"] == version_id:
            return commit
    raise StorageError(f"La versión '{version_id}' no existe en el historial.")


def restore_version(version_id: str) -> None:
    """
    Restaura el directorio de trabajo al estado del commit indicado.
    Sobreescribe los archivos rastreados con el contenido del snapshot.
    Lanza StorageError si la versión no existe.
    """
    commit = get_commit(version_id)   
    for filename, content in commit["files"].items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)


def read_baselines() -> dict:
    """Devuelve el mapa de líneas base: {"Release1.0": "v1", "Sprint2": "v2"}"""
    return _read_json(BASELINES_FILE)


def write_baselines(baselines: dict) -> None:
    _write_json(BASELINES_FILE, baselines)


def create_baseline(tag: str) -> dict:
    """
    Etiqueta la última versión del historial con el tag dado.
    Lanza StorageError si no hay commits o si el tag ya existe.
    """
    tag = tag.strip()
    if not tag:
        raise StorageError("El nombre de la línea base no puede estar vacío.")

    history = read_history()
    if not history:
        raise StorageError("No hay versiones confirmadas. Ejecuta sbac commit primero.")

    baselines = read_baselines()
    if tag in baselines:
        raise StorageError(f"La línea base '{tag}' ya existe y apunta a {baselines[tag]}.")

    latest_id = history[-1]["id"]
    baselines[tag] = latest_id
    write_baselines(baselines)
    return {"tag": tag, "version_id": latest_id}


def _object_path(version_id: str, filename: str) -> str:
    """
    Ruta interna donde se guarda la copia de un archivo para una versión.
    Ejemplo: .sbac/objects/v1/archivo_prueba.txt
    Los subdirectorios del nombre de archivo se aplanan con '__' para evitar
    colisiones en rutas relativas complejas.
    """
    safe_name = filename.replace(os.sep, "__")
    return os.path.join(OBJECTS_DIR, version_id, safe_name)


def get_file_content_at(version_id: str, filename: str) -> str:
    """
    Devuelve el contenido de un archivo en una versión específica.
    Primero busca en el snapshot JSON (rápido); si no está, cae al archivo físico.
    """
    commit = get_commit(version_id)
    if filename in commit["files"]:
        return commit["files"][filename]

    # Fallback: leer desde la copia física en objects/
    object_path = _object_path(version_id, filename)
    if os.path.isfile(object_path):
        with open(object_path, "r", encoding="utf-8") as f:
            return f.read()

    raise StorageError(f"El archivo '{filename}' no está registrado en la versión '{version_id}'.")