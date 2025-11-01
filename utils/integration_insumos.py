# ==========================================================
# utils/integration_insumos.py
# SynapseNext – SAAB / TJSP
# Versão estável vNext (2025-11)
# Integração institucional entre INSUMOS → DFD / ETP / TR / EDITAL
# ==========================================================

from __future__ import annotations
import os
import io
import re
import json
import datetime as dt
from typing import Dict, Any, Optional

# Streamlit (opcional para testes)
try:
    import streamlit as st  # type: ignore
except Exception:
    st = None

# ==========================================================
# 📦 Dependências opcionais de leitura
# ==========================================================
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    import docx2txt
except Exception:
    docx2txt = None

try:
    import docx
except Exception:
    docx = None

# ==========================================================
# 🔐 OpenAI – criação tardia e opcional
# ==========================================================
def _get_openai_client():
    api_key = None
    if st and getattr(st, "secrets", None):
        api_key = st.secrets.get("OPENAI_API_KEY")
    api_key = api_key or os.getenv("OPENAI_API_KEY")

    try:
        from openai import OpenAI
    except Exception:
        return None, None
    if not api_key:
        return None, None

    try:
        return OpenAI(api_key=api_key), "gpt-4o-mini"
    except Exception:
        return None, None


# ==========================================================
# 📂 Estrutura de diretórios
# ==========================================================
_EXPORTS_DIR = os.path.join("exports", "insumos")
_EXPORTS_JSON_DIR = os.path.join(_EXPORTS_DIR, "json")
os.makedirs(_EXPORTS_DIR, exist_ok=True)
os.makedirs(_EXPORTS_JSON_DIR, exist_ok=True)

# ==========================================================
# 🧾 Utilitários de E/S
# ==========================================================
def salvar_insumo(uploaded_file, artefato: str) -> str:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = f"{ts}__{artefato.upper()}__{uploaded_file.name}"
    path = os.path.join(_EXPORTS_DIR, base_name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def listar_insumos() -> list[str]:
    if not os.path.exists(_EXPORTS_DIR):
        return []
    return sorted(
        [f for f in os.listdir(_EXPORTS_DIR) if os.path.isfile(os.path.join(_EXPORTS_DIR, f))],
        reverse=True
    )


def _dump_json_safely(payload: Dict[str, Any], name_hint: str) -> Optional[str]:
    try:
        safe_name = re.sub(r"[^a-zA-Z0-9_\-]+", "_", name_hint)[:120]
        path = os.path.join(_EXPORTS_JSON_DIR, f"{safe_name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return path
    except Exception:
        return None

# ==========================================================
# 📄 Extração de texto (PDF/DOCX/TXT)
# ==========================================================
def extrair_texto_arquivo(uploaded_file) -> str:
    nome = uploaded_file.name.lower()
    data = uploaded_file.read()
    uploaded_file.seek(0)

    # TXT direto
    if nome.endswith(".txt"):
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return data.decode("latin-1", errors="ignore")

    # PDF
    if nome.endswith(".pdf"):
        if fitz is not None:
            try:
                pdf = fitz.open(stream=data, filetype="pdf")
                return "".join(page.get_text() for page in pdf)
            except Exception:
                pass
        if PdfReader is not None:
            try:
                reader = PdfReader(io.BytesIO(data))
                texto = []
                for page in getattr(reader, "pages", []):
                    texto.append(page.extract_text() or "")
                return "\n".join(texto)
            except Exception:
                pass
        return ""

    # DOCX
    if nome.endswith(".docx"):
        if docx2txt is not None:
            try:
                return docx2txt.process(io.BytesIO(data)) or ""
            except Exception:
                pass
        if docx is not None:
            try:
                document = docx.Document(io.BytesIO(data))
                return "\n".join(p.text for p in document.paragraphs)
            except Exception:
                pass
        return ""

    return ""


# ==========================================================
# 🔍 Heurísticas e normalização para EDITAL
# ==========================================================
_EDITAL_KEYMAP = {
    "unidade_solicitante": ["unidade", "setor", "orgao"],
    "responsavel_tecnico": ["responsavel", "gestor", "fiscal"],
    "objeto": ["objeto", "descricao", "escopo"],
    "modalidade": ["modalidade", "tipo_modalidade"],
    "regime_execucao": ["regime_execucao", "regime"],
    "base_legal": ["base_legal", "fundamentacao_legal"],
    "justificativa_modalidade": ["justificativa", "motivacao"],
    "habilitacao": ["habilitacao", "condicoes_participacao"],
    "criterios_julgamento": ["criterios", "criterio_julgamento"],
    "prazo_execucao": ["prazo_execucao", "prazos"],
    "forma_pagamento": ["forma_pagamento", "pagamento"],
    "penalidades": ["penalidades", "sancoes"],
    "observacoes_finais": ["observacoes", "notas"],
}

def _norm_key(key: str) -> Optional[str]:
    k = key.strip().lower()
    for target, aliases in _EDITAL_KEYMAP.items():
        if k == target or k in aliases:
            return target
    return None

def _normalize_for_edital(raw: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in (raw or {}).items():
        nk = _norm_key(str(k))
        if nk:
            out[nk] = v
    return out


# ==========================================================
# 🧠 IA opcional – extração assistida
# ==========================================================
def _analisar_insumo_ia(texto: str, artefato: str) -> Dict[str, Any]:
    client, model = _get_openai_client()
    if client is None or not model or not texto.strip():
        return {}

    prompt = (
        "Você é um redator técnico do TJSP (SAAB). "
        f"Extraia os campos do artefato '{artefato.upper()}' conforme os modelos institucionais. "
        "Responda apenas em JSON. "
        "Chaves esperadas: ['unidade_solicitante','responsavel_tecnico','objeto',"
        "'modalidade','regime_execucao','base_legal','habilitacao','criterios_julgamento',"
        "'prazo_execucao','forma_pagamento','penalidades','observacoes_finais'].\n\n"
        f"TEXTO:\n{texto[:8000]}"
    )

    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": "Você segue o padrão SAAB/TJSP e a Lei 14.133/2021."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
        )
        content = resp.choices[0].message.content or ""
        m = re.search(r"\{.*\}", content, re.S)
        if m:
            return json.loads(m.group(0))
    except Exception:
        pass
    return {}


# ==========================================================
# 🧩 Propagação entre módulos (DFD, ETP, TR, EDITAL)
# ==========================================================
def _propagar_para_modulo(artefato: str, campos_norm: dict):
    """
    Restaura a propagação automática de campos entre módulos,
    garantindo o pré-preenchimento imediato dos formulários.
    """
    if st is None:
        return

    artefato = artefato.upper()
    mapping = {
        "DFD": "dfd_campos_ai",
        "ETP": "etp_campos_ai",
        "TR": "tr_campos_ai",
        "EDITAL": "edital_campos_ai",
    }
    chave_destino = mapping.get(artefato)
    if chave_destino:
        st.session_state[chave_destino] = campos_norm
        st.session_state["last_insumo"] = {"artefato": artefato, "campos_ai": campos_norm}


# ==========================================================
# 🚀 Função principal
# ==========================================================
def processar_insumo(uploaded_file, artefato: str = "EDITAL") -> Dict[str, Any]:
    artefato = (artefato or "EDITAL").upper()
    texto = extrair_texto_arquivo(uploaded_file)

    heur = {}  # heurísticas mínimas podem ser reintroduzidas depois
    via_ia = _analisar_insumo_ia(texto, artefato)

    merged: Dict[str, Any] = {**heur, **via_ia} if via_ia else heur
    campos_norm = _normalize_for_edital(merged)

    payload_state = {
        "nome_arquivo": getattr(uploaded_file, "name", "arquivo"),
        "artefato": artefato,
        "texto": texto,
        "campos_ai": campos_norm,
    }

    # Atualiza sessão e exporta
    if st is not None:
        st.session_state["last_insumo"] = payload_state

    _dump_json_safely(payload_state, f"{artefato}__{payload_state['nome_arquivo']}")

    # Propagação institucional para os módulos correspondentes
    _propagar_para_modulo(artefato, campos_norm)

    return campos_norm


# ==========================================================
# 🔁 Compatibilidade retroativa
# ==========================================================
def processar_insumo_dinamico(uploaded_file, artefato: str = "EDITAL"):
    """Wrapper de compatibilidade com versões anteriores."""
    return processar_insumo(uploaded_file, artefato=artefato)
