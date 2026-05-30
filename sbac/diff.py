"""
diff.py — Módulo de comparación para el SBAC
Implementa el comando: diff <v1> <v2>
Usa difflib.unified_diff para mostrar diferencias textuales entre versiones.
"""

import difflib
from storage import get_commit, assert_repo_exists, StorageError


def cmd_diff(v1: str, v2: str):
    """Muestra las diferencias textuales entre dos versiones del repositorio."""
    assert_repo_exists()

    try:
        commit_v1 = get_commit(v1)
        commit_v2 = get_commit(v2)
    except StorageError:
        print("Error: Una o ambas versiones especificadas no existen en el historial.")
        raise SystemExit(1)

    archivos = set(commit_v1["files"]) | set(commit_v2["files"])

    hay_diferencias = False
    for archivo in sorted(archivos):
        contenido_v1 = commit_v1["files"].get(archivo, "")
        contenido_v2 = commit_v2["files"].get(archivo, "")

        if contenido_v1 != contenido_v2:
            hay_diferencias = True
            _show_file_diff(archivo, contenido_v1, contenido_v2, v1, v2)

    if not hay_diferencias:
        print(f"Sin diferencias entre {v1} y {v2}.")


def _show_file_diff(filename: str, content_v1: str, content_v2: str,
                    id_v1: str, id_v2: str):
    """Imprime el diff unificado de un archivo entre dos versiones."""
    lines_v1 = content_v1.splitlines(keepends=True)
    lines_v2 = content_v2.splitlines(keepends=True)

    diff = difflib.unified_diff(
        lines_v1,
        lines_v2,
        fromfile=f"{id_v1}/{filename}",
        tofile=f"{id_v2}/{filename}",
        lineterm="",
    )

    for line in diff:
        print(line)