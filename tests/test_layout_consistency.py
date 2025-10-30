import importlib
import pytest

def test_ui_style_module_exists():
    """Verifica se o módulo ui_style existe e é importável."""
    try:
        importlib.import_module("utils.ui_style")
    except ModuleNotFoundError:
        pytest.fail("O módulo utils.ui_style não foi encontrado!")

def test_ui_style_contains_core_functions():
    """Valida se as funções principais de estilo estão disponíveis."""
    ui_style = importlib.import_module("utils.ui_style")
    expected_attrs = ["aplicar_tema", "cor_primaria", "fonte_base"]
    for attr in expected_attrs:
        assert hasattr(ui_style, attr), f"A função ou atributo '{attr}' está ausente em ui_style."
