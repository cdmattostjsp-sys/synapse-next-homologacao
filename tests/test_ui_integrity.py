import importlib
import os
import pytest

PAGES_PATH = "streamlit_app/pages"

def list_page_modules():
    """Lista todos os módulos .py das páginas do Streamlit."""
    return [
        f"{PAGES_PATH.replace('/', '.')}.{os.path.splitext(f)[0]}"
        for f in os.listdir(PAGES_PATH)
        if f.endswith(".py") and not f.startswith("__")
    ]

@pytest.mark.parametrize("module_name", list_page_modules())
def test_import_pages(module_name):
    """Verifica se cada página pode ser importada sem erro."""
    try:
        importlib.import_module(module_name)
    except Exception as e:
        pytest.fail(f"Falha ao importar {module_name}: {e}")
