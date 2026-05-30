"""
repo.py — Módulo de gestión de repositorio para el SBAC
Maneja los comandos: init, add, status
"""

import os
from storage import (init_repo, stage_file, read_index,
                     assert_repo_exists, StorageError)


def cmd_init():
    """Inicializa un nuevo repositorio SBAC en el directorio actual."""
    try:
        init_repo()
        print("Repositorio inicializado correctamente en .sbac/")
    except StorageError as e:
        print(f"Error: {e}")
        raise SystemExit(1)


def cmd_add(filename: str):
    """Agrega un archivo existente al área de preparación (staging)."""
    assert_repo_exists()
    try:
        stage_file(filename)
        print(f"Archivo '{filename}' agregado al seguimiento.")
    except StorageError as e:
        print(f"Error: {e}")
        raise SystemExit(1)


def cmd_status():
    """Muestra los archivos en staging y los archivos no rastreados del directorio."""
    assert_repo_exists()

    index = read_index()
    staged = index.get("staged", [])

    if staged:
        print("Archivos preparados para commit:")
        for filename in staged:
            print(f"  - {filename}")
    else:
        print("No hay archivos en el área de preparación.")

    untracked = [
        f for f in os.listdir(".")
        if os.path.isfile(f) and f not in staged
    ]

    if untracked:
        print("\nArchivos no rastreados:")
        for filename in untracked:
            print(f"  - {filename}")