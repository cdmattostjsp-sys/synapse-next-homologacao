import io
import re
import fitz  # PyMuPDF
from PyPDF2 import PdfReader


# ============================
# FUNÇÃO PRINCIPAL DE EXTRAÇÃO
# ============================

def extract_text_from_pdf(uploaded_file):
    """
    Extrai o texto completo de um arquivo PDF enviado via Streamlit.
    Usa PyMuPDF (fitz) para extração robusta de PDFs complexos.
    Retorna um dicionário com texto e metadados básicos.
    """
    try:
        pdf_bytes = uploaded_file.read()
        text = ""

        # Tentativa 1 – PyMuPDF (melhor qualidade)
        try:
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text("text")
        except Exception:
            # Tentativa 2 – PyPDF2 (fallback)
            pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in pdf_reader.pages:
                text += page.extract_text() or ""

        # Limpeza básica do texto
        text = clean_text(text)

        # Extração de metadados relevantes
        meta = extract_metadata(text)

        return {
            "success": True,
            "text": text,
            "metadata": meta,
            "page_count": meta.get("page_count", 0)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================
# LIMPEZA DO TEXTO
# ============================

def clean_text(text: str) -> str:
    """Remove múltiplos espaços, quebras e cabeçalhos repetidos."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Página\s*\d+\s*de\s*\d+", "", text)
    text = text.replace("Tribunal de Justiça do Estado de São Paulo", "")
    return text.strip()


# ============================
# EXTRAÇÃO DE METADADOS
# ============================

def extract_metadata(text: str) -> dict:
    """
    Identifica elementos úteis nos documentos administrativos do TJSP.
    Exemplo: número de processo, unidade, data, tipo de artefato, etc.
    """
    meta = {}

    # Número do processo
    proc = re.search(r"\d{7,}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", text)
    if proc:
        meta["process_number"] = proc.group(0)

    # Unidade / Fórum
    unidade = re.search(r"(Fórum|Comarca|Secretaria)\s+[A-ZÁ-Úa-zá-ú\s]+", text)
    if unidade:
        meta["unit_name"] = unidade.group(0)

    # Datas
    datas = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", text)
    if datas:
        meta["dates"] = list(set(datas))

    # Palavras-chave
    keywords = []
    for palavra in ["demanda", "contratação", "justificativa", "objeto", "projeto", "licitação", "urgência"]:
        if palavra in text.lower():
            keywords.append(palavra)
    meta["keywords"] = keywords

    # Contagem de páginas (estimada)
    meta["page_count"] = len(re.findall(r"Formulário|Página", text)) or "N/D"

    return meta


# ============================
# UTILITÁRIO PARA RESUMO
# ============================

def summarize_text(text: str, max_length: int = 1200) -> str:
    """
    Retorna um resumo textual curto do documento, para exibição prévia no Streamlit.
    """
    preview = text[:max_length] + "..." if len(text) > max_length else text
    return preview
