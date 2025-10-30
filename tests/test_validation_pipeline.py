import pytest
from pathlib import Path
from docx import Document

@pytest.fixture
def tr_doc():
    return Document(Path("tests/data/insumos_ficticios/TR_exemplo.docx"))

def simular_validacao(doc):
    """Mock do validador de coerência textual."""
    texto = " ".join([p.text for p in doc.paragraphs])
    erros = []
    if "contratação" not in texto.lower():
        erros.append("Falta termo obrigatório 'contratação'.")
    if len(texto) < 100:
        erros.append("Texto muito curto para validação institucional.")
    return erros

def test_validacao_coerencia(tr_doc):
    """Executa uma validação simulada de coerência textual."""
    erros = simular_validacao(tr_doc)
    assert isinstance(erros, list)
    assert all(isinstance(e, str) for e in erros)
