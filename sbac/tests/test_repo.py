"""
test_repo.py — Pruebas de integración para repo.py (CP-001 a CP-005)
Cubre los comandos: cmd_init, cmd_add, cmd_status
"""

import os
import pytest
from repo import cmd_init, cmd_add, cmd_status
from storage import read_index, repo_exists


@pytest.fixture
def repo_dir(tmp_path, monkeypatch):
    """Cambia el cwd a un directorio temporal limpio para cada prueba."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_cmd_init_crea_sbac(repo_dir, capsys):
    """CP-001: init crea la carpeta .sbac/ en el directorio de trabajo."""
    cmd_init()

    assert os.path.isdir(".sbac"), "La carpeta .sbac/ debe existir tras init"

    captured = capsys.readouterr()
    assert "inicializado correctamente" in captured.out

def test_cmd_init_duplicado_lanza_systemexit(repo_dir, capsys):
    """CP-002: la segunda llamada a init lanza SystemExit sin eliminar .sbac/."""
    cmd_init()  

    with pytest.raises(SystemExit):
        cmd_init()  


def test_cmd_init_duplicado_muestra_error(repo_dir, capsys):
    """CP-002: la segunda llamada a init imprime un mensaje con prefijo 'Error:'."""
    cmd_init()
    capsys.readouterr()  

    with pytest.raises(SystemExit):
        cmd_init()

    captured = capsys.readouterr()
    assert captured.out.startswith("Error:")


def test_cmd_init_duplicado_preserva_sbac(repo_dir, capsys):
    """CP-002: .sbac/ sigue existiendo y es válido tras el intento de init duplicado."""
    cmd_init()

    with pytest.raises(SystemExit):
        cmd_init()

    assert repo_exists(), ".sbac/ debe seguir existiendo y ser válido tras init duplicado"


def test_cmd_add_archivo_valido_confirma_en_salida(repo_dir, capsys):
    """CP-003: add con archivo existente imprime confirmación de seguimiento."""
    cmd_init()
    (repo_dir / "archivo_prueba.txt").write_text("Línea 1\nLínea 2\n")

    cmd_add("archivo_prueba.txt")

    captured = capsys.readouterr()
    assert "agregado al seguimiento" in captured.out


def test_cmd_add_archivo_valido_registra_en_index(repo_dir, capsys):
    """CP-003: add con archivo existente registra el archivo en el index de staging."""
    cmd_init()
    (repo_dir / "archivo_prueba.txt").write_text("Línea 1\nLínea 2\n")

    cmd_add("archivo_prueba.txt")

    assert "archivo_prueba.txt" in read_index()["staged"]

def test_cmd_add_archivo_inexistente_lanza_systemexit(repo_dir, capsys):
    """CP-004: add con archivo inexistente lanza SystemExit."""
    cmd_init()

    with pytest.raises(SystemExit):
        cmd_add("fantasma.txt")


def test_cmd_add_archivo_inexistente_muestra_error(repo_dir, capsys):
    """CP-004: add con archivo inexistente imprime un mensaje con prefijo 'Error:'."""
    cmd_init()
    capsys.readouterr() 

    with pytest.raises(SystemExit):
        cmd_add("fantasma.txt")

    captured = capsys.readouterr()
    assert captured.out.startswith("Error:")


def test_cmd_add_archivo_inexistente_no_modifica_staging(repo_dir, capsys):
    """CP-004: add fallido no agrega ninguna entrada al área de staging."""
    cmd_init()

    with pytest.raises(SystemExit):
        cmd_add("fantasma.txt")

    assert "fantasma.txt" not in read_index()["staged"]


def test_cmd_status_con_staged_muestra_seccion(repo_dir, capsys):
    """CP-005: status con archivos staged muestra la sección 'preparados para commit'."""
    cmd_init()
    (repo_dir / "archivo_prueba.txt").write_text("Contenido de prueba\n")
    cmd_add("archivo_prueba.txt")
    capsys.readouterr() 

    cmd_status()

    captured = capsys.readouterr()
    assert "preparados para commit" in captured.out


def test_cmd_status_con_staged_lista_nombre_archivo(repo_dir, capsys):
    """CP-005: status lista el nombre del archivo staged en la salida."""
    cmd_init()
    (repo_dir / "archivo_prueba.txt").write_text("Contenido de prueba\n")
    cmd_add("archivo_prueba.txt")
    capsys.readouterr()

    cmd_status()

    captured = capsys.readouterr()
    assert "archivo_prueba.txt" in captured.out


def test_cmd_status_sin_staged_muestra_mensaje_vacio(repo_dir, capsys):
    """CP-005b: status sin archivos staged muestra el mensaje informativo correspondiente."""
    cmd_init()
    capsys.readouterr()

    cmd_status()

    captured = capsys.readouterr()
    assert "No hay archivos en el área de preparación" in captured.out