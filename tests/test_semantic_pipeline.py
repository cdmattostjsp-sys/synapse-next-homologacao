import pytest
from pathlib import Path
from docx import Document
import re

@pytest.fixture
def exemplo_docx():
    path = Path("tests/data/insumos_ficticios/ETP_exemplo.docx")
    return Document(path)

def extrair_conceitos(doc):
    """Simula extração semântica de conceitos principais."""
    texto = " ".join([p.text for p in doc.paragraphs])
    conceitos = re.findall(r"[A-Z][a-z]{3,}", texto)
    return set(conceitos)

def test_extracao_semantica_ficticia(exemplo_docx):
    """Valida se o modelo fictício extrai conceitos simulados."""
    conceitos = extrair_conceitos(exemplo_docx)
    assert len(conceitos) > 0, "Nenhum conceito foi extraído do documento fictício."
    assert "SAAB" not in conceitos, "Conceito institucional real não deve aparecer em teste sintético."
