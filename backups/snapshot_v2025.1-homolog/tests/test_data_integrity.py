import os
import pytest

@pytest.mark.parametrize("path", [
    "tests/data/insumos_ficticios/DFD_exemplo.docx",
    "tests/data/insumos_ficticios/ETP_exemplo.docx",
    "tests/data/insumos_ficticios/TR_exemplo.docx",
    "tests/data/insumos_ficticios/edital_exemplo.pdf"
])
def test_fictitious_inputs_exist(path):
    """Garante que os arquivos de insumo fictício existem e estão acessíveis."""
    assert os.path.exists(path), f"O arquivo {path} não foi encontrado."

def test_cache_and_utils_exist():
    """Verifica a estrutura essencial do projeto."""
    required_dirs = ["utils", "streamlit_app/pages", "tests/data"]
    for d in required_dirs:
        assert os.path.isdir(d), f"O diretório {d} está ausente."
