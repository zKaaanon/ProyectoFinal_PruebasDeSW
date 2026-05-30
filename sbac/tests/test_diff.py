"""
test_diff.py — Pruebas de integración para diff.py (CP-013, CP-014)
Cubre el comando: cmd_diff
"""

import pytest
from diff import cmd_diff
from storage import init_repo, stage_file, create_commit

@pytest.fixture
def repo_con_dos_versiones(tmp_path, monkeypatch):
    """
    Prepara un repositorio con dos commits donde archivo_prueba.txt
    tiene contenido diferente entre v1 y v2.
    Devuelve tmp_path para acceso al directorio si se necesita.
    """
    monkeypatch.chdir(tmp_path)
    init_repo()

    archivo = tmp_path / "archivo_prueba.txt"

    # v1: contenido inicial
    archivo.write_text("Línea 1\nLínea 2\nLínea 3\n", encoding="utf-8")
    stage_file("archivo_prueba.txt")
    create_commit("Primera versión")

    # v2: contenido modificado
    archivo.write_text("Línea 1\nLínea 2 MODIFICADA\nLínea 3\nLínea 4 nueva\n", encoding="utf-8")
    stage_file("archivo_prueba.txt")
    create_commit("Segunda versión")

    return tmp_path


@pytest.fixture
def repo_con_versiones_identicas(tmp_path, monkeypatch):
    """
    Prepara un repositorio con dos commits donde archivo_prueba.txt
    tiene el mismo contenido en ambas versiones.
    """
    monkeypatch.chdir(tmp_path)
    init_repo()

    archivo = tmp_path / "archivo_prueba.txt"
    archivo.write_text("Línea 1\nLínea 2\n", encoding="utf-8")

    stage_file("archivo_prueba.txt")
    create_commit("Primera versión")

    stage_file("archivo_prueba.txt")
    create_commit("Segunda versión — sin cambios")

    return tmp_path


@pytest.fixture
def repo_con_un_commit(tmp_path, monkeypatch):
    """Prepara un repositorio con un único commit válido (v1)."""
    monkeypatch.chdir(tmp_path)
    init_repo()

    archivo = tmp_path / "archivo_prueba.txt"
    archivo.write_text("Contenido base\n", encoding="utf-8")
    stage_file("archivo_prueba.txt")
    create_commit("Primera versión")

    return tmp_path

def test_diff_muestra_lineas_eliminadas(repo_con_dos_versiones, capsys):
    """CP-013: el diff marca con '-' las líneas que desaparecieron en v2."""
    cmd_diff("v1", "v2")

    captured = capsys.readouterr()
    assert "-Línea 2\n" in captured.out or "-Línea 2" in captured.out


def test_diff_muestra_lineas_agregadas(repo_con_dos_versiones, capsys):
    """CP-013: el diff marca con '+' las líneas nuevas que aparecen en v2."""
    cmd_diff("v1", "v2")

    captured = capsys.readouterr()
    assert "+Línea 2 MODIFICADA" in captured.out


def test_diff_muestra_encabezado_fromfile(repo_con_dos_versiones, capsys):
    """CP-013: el encabezado '---' referencia el archivo en v1."""
    cmd_diff("v1", "v2")

    captured = capsys.readouterr()
    assert "--- v1/archivo_prueba.txt" in captured.out


def test_diff_muestra_encabezado_tofile(repo_con_dos_versiones, capsys):
    """CP-013: el encabezado '+++' referencia el archivo en v2."""
    cmd_diff("v1", "v2")

    captured = capsys.readouterr()
    assert "+++ v2/archivo_prueba.txt" in captured.out


def test_diff_muestra_marcador_hunk(repo_con_dos_versiones, capsys):
    """CP-013: la salida incluye el marcador de hunk '@@' de unified_diff."""
    cmd_diff("v1", "v2")

    captured = capsys.readouterr()
    assert "@@" in captured.out


def test_diff_versiones_identicas_sin_diferencias(repo_con_versiones_identicas, capsys):
    """CP-013: cuando ambas versiones son idénticas, informa que no hay diferencias."""
    cmd_diff("v1", "v2")

    captured = capsys.readouterr()
    assert "Sin diferencias" in captured.out


def test_diff_segundo_id_inexistente_muestra_error(repo_con_un_commit, capsys):
    """CP-014: si el segundo ID no existe, imprime mensaje de error."""
    with pytest.raises(SystemExit):
        cmd_diff("v1", "v999")

    captured = capsys.readouterr()
    assert "Error:" in captured.out


def test_diff_segundo_id_inexistente_lanza_systemexit(repo_con_un_commit, capsys):
    """CP-014: si el segundo ID no existe, lanza SystemExit."""
    with pytest.raises(SystemExit):
        cmd_diff("v1", "v999")


def test_diff_primer_id_inexistente_muestra_error(repo_con_un_commit, capsys):
    """CP-014: si el primer ID no existe, imprime mensaje de error."""
    with pytest.raises(SystemExit):
        cmd_diff("v999", "v1")

    captured = capsys.readouterr()
    assert "Error:" in captured.out


def test_diff_ambos_ids_inexistentes_muestra_error(repo_con_un_commit, capsys):
    """CP-014: si ambos IDs no existen, imprime mensaje de error sin crashear."""
    with pytest.raises(SystemExit):
        cmd_diff("v998", "v999")

    captured = capsys.readouterr()
    assert "Error:" in captured.out


def test_diff_id_inexistente_no_calcula_diferencias(repo_con_un_commit, capsys):
    """CP-014: con ID inválido no se imprime ningún marcador de diff ('@@', '---', '+++')."""
    with pytest.raises(SystemExit):
        cmd_diff("v1", "v999")

    captured = capsys.readouterr()
    assert "@@" not in captured.out
    assert "---" not in captured.out