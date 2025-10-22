# ==========================================================
# 🔧 SynapseNext – Insumos Institucionais (Fase 2: parsing + integração DFD)
# SAAB 5.0 – TJSP
# ==========================================================

import sys
import re
from io import BytesIO
from pathlib import Path
import streamlit as st

# ==========================================================
# ⚙️ Config da página (deve ser o 1º comando Streamlit)
# ==========================================================
st.set_page_config(
    page_title="SynapseNext – Insumos Institucionais",
    layout="wide",
    page_icon="🔧",
)

# ==========================================================
# 🔧 Paths
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# ==========================================================
# 📦 Estilo institucional
# ==========================================================
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

aplicar_estilo_global()

# ==========================================================
# 📚 Imports para parsing (opcionais)
# ==========================================================
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document as DocxDocument
except Exception:
    DocxDocument = None

# ==========================================================
# 🧠 Funções utilitárias – Parsing e Extração de Campos
# ==========================================================
def _extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extrai texto de PDF (melhor esforço)."""
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(BytesIO(file_bytes))
        texts = []
        for page in reader.pages:
            try:
                t = page.extract_text() or ""
            except Exception:
                t = ""
            texts.append(t)
        return "\n".join(texts)
    except Exception:
        return ""

def _extract_text_from_docx(file_bytes: bytes) -> str:
    """Extrai texto de DOCX."""
    if DocxDocument is None:
        return ""
    try:
        doc = DocxDocument(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return ""

def _extract_text_generic(uploaded_file) -> str:
    """Extrai texto legível de PDF, DOCX ou TXT."""
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()  # bytes

    if name.endswith(".pdf"):
        txt = _extract_text_from_pdf(raw)
        if not txt:
            # fallback brando: evita caracteres quebrados
            try:
                return raw.decode("utf-8", errors="ignore")
            except Exception:
                return ""
        return txt

    if name.endswith(".docx"):
        txt = _extract_text_from_docx(raw)
        if not txt:
            try:
                return raw.decode("utf-8", errors="ignore")
            except Exception:
                return ""
        return txt

    # .txt (ou outros)
    try:
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def _capture_after(label_variants, text):
    """Localiza valor após rótulos (ex.: 'Unidade solicitante:', 'Unidade:')."""
    for lab in label_variants:
        # pega até o fim da linha
        pattern = rf"{lab}\s*[:\-–]\s*(.+)"
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            return _norm(m.group(1).split("\n")[0])
    return ""

def _extract_fields_for_dfd(text: str) -> dict:
    """
    Heurística simples para preencher campos do DFD a partir do texto do insumo.
    Ajustamos para termos comuns em documentos institucionais.
    """
    t = text or ""
    # rótulos possíveis (inclui variações comuns)
    unidade = _capture_after(
        ["unidade solicitante", "unidade", "setor demandante", "órgão solicitante"], t
    )
    responsavel = _capture_after(
        ["responsável", "responsavel", "ponto focal", "contato"], t
    )
    objeto = _capture_after(
        ["objeto", "objeto da contratação", "escopo"], t
    )
    justificativa = _capture_after(
        ["justificativa", "motivação", "motivacao", "fundamentação", "fundamentacao"], t
    )
    quantidade = _capture_after(
        ["quantidade", "quantitativo", "itens previstos"], t
    )
    urgencia = _capture_after(
        ["urgência", "urgencia", "prioridade"], t
    )
    riscos = _capture_after(
        ["riscos", "riscos identificados", "riscos/mitigações"], t
    )
    alinhamento = _capture_after(
        ["alinhamento estratégico", "alinhamento", "estratégia institucional"], t
    )

    # Fallbacks leves: se "objeto" e "justificativa" vierem vazios, usar sumário
    if not objeto:
        objeto = _norm(t[:400])
    if not justificativa and len(t) > 800:
        justificativa = _norm(t[400:900])

    return {
        "unidade": unidade,
        "responsavel": responsavel,
        "objeto": objeto,
        "justificativa": justificativa,
        "quantidade": quantidade,
        "urgencia": urgencia,
        "riscos": riscos,
        "alinhamento": alinhamento,
    }

# ==========================================================
# 🏛️ Cabeçalho
# ==========================================================
exibir_cabecalho_padrao(
    "Insumos Institucionais",
    "Upload com leitura automática e integração para pré-preenchimento do DFD"
)
st.divider()

# ==========================================================
# 1) Seleção do artefato
# ==========================================================
st.subheader("1️⃣ Selecione o artefato de destino")

artefato = st.selectbox(
    "Artefato relacionado ao insumo:",
    ["DFD", "ETP", "TR", "Edital", "Contrato"],
    help="Selecione o artefato para o qual o documento servirá de insumo."
)

# ==========================================================
# 2) Upload + Parsing + Registro de sessão
# ==========================================================
st.subheader("2️⃣ Enviar Documento e Extrair Conteúdo")

uploaded_file = st.file_uploader(
    "Selecione o arquivo (PDF, DOCX ou TXT)",
    type=["pdf", "docx", "txt"]
)

descricao = st.text_input("Descrição breve do arquivo:")
usuario = st.text_input("Nome do remetente:", value="Anônimo")

col_a, col_b = st.columns([1,1])

with col_a:
    parse_now = st.button("🧠 Enviar, Ler e Registrar", type="primary", use_container_width=True)

with col_b:
    st.caption("O conteúdo será lido e os campos do DFD serão inferidos automaticamente (melhor esforço).")

if uploaded_file and parse_now:
    # 1) extrai texto
    texto = _extract_text_generic(uploaded_file)
    # 2) extrai campos do DFD (mesmo que o artefato não seja DFD, mantemos pronto)
    campos_dfd = _extract_fields_for_dfd(texto)

    # 3) armazena sessão
    st.session_state["insumo_atual"] = {
        "nome_arquivo": uploaded_file.name,
        "conteudo": texto or "",
        "artefato": artefato,
        "descricao": _norm(descricao),
        "usuario": _norm(usuario),
        "campos_dfd": campos_dfd,  # <- chave nova com campos inferidos
    }

    st.success(f"✅ Insumo '{uploaded_file.name}' registrado e processado.")
    with st.expander("🔎 Campos inferidos para DFD", expanded=True):
        st.json(campos_dfd)

st.divider()

# ==========================================================
# 3) Visualização do insumo ativo
# ==========================================================
if "insumo_atual" in st.session_state:
    ins = st.session_state["insumo_atual"]
    st.markdown(f"**🗂️ Último insumo ativo:** `{ins['nome_arquivo']}` – artefato `{ins['artefato']}`")
    with st.expander("Prévia do conteúdo bruto (legível)", expanded=False):
        st.text(ins["conteudo"][:3000] or "—")
else:
    st.info("Nenhum insumo ativo nesta sessão. Faça upload acima para iniciar.")
