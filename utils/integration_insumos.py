# ==============================
# utils/integration_insumos.py
# SynapseNext – SAAB / TJSP
# Revisão vNext: integração estável INSUMOS → EDITAL
# ==============================

from __future__ import annotations

import os
import io
import re
import json
import datetime as dt
from typing import Dict, Any, Optional

# Importa Streamlit somente em runtime (evita falhas em testes sem Streamlit)
try:
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover
    st = None  # Permite testes de unidade sem UI

# ==============================
# Dependências opcionais de leitura de arquivos
# ==============================
# PDF: preferimos PyMuPDF (fitz); fallback para PyPDF2
try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover
    fitz = None

try:
    from PyPDF2 import PdfReader  # fallback PDF
except Exception:  # pragma: no cover
    PdfReader = None

# DOCX: preferimos docx2txt; fallback para python-docx
try:
    import docx2txt
except Exception:  # pragma: no cover
    docx2txt = None

try:
    import docx  # python-docx
except Exception:  # pragma: no cover
    docx = None

# ==============================
# OpenAI – criação tardia do cliente (opcional)
# ==============================
def _get_openai_client():
    """
    Cria cliente OpenAI apenas quando necessário.
    Não falha se não houver chave/pacote – a IA passa a ser opcional.
    """
    api_key = None
    if st and getattr(st, "secrets", None):
        api_key = st.secrets.get("OPENAI_API_KEY")
    api_key = api_key or os.getenv("OPENAI_API_KEY")

    try:
        from openai import OpenAI  # openai>=1.x
    except Exception:
        return None, None  # sem pacote

    if not api_key:
        return None, None  # sem chave

    try:
        return OpenAI(api_key=api_key), "gpt-4o-mini"
    except Exception:
        return None, None


# ==============================
# Utilitários de E/S
# ==============================
_EXPORTS_DIR = os.path.join("exports", "insumos")
_EXPORTS_JSON_DIR = os.path.join(_EXPORTS_DIR, "json")
os.makedirs(_EXPORTS_DIR, exist_ok=True)
os.makedirs(_EXPORTS_JSON_DIR, exist_ok=True)


def salvar_insumo(uploaded_file, artefato: str) -> str:
    """
    Persiste o arquivo original em exports/insumos/ com carimbo de data.
    """
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = f"{ts}__{artefato.upper()}__{uploaded_file.name}"
    path = os.path.join(_EXPORTS_DIR, base_name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def listar_insumos() -> list[str]:
    """
    Lista arquivos persistidos em exports/insumos/.
    """
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


# ==============================
# Extração de texto – PDF / DOCX / TXT
# ==============================
def _read_all(uploaded_file) -> bytes:
    pos = uploaded_file.tell()
    uploaded_file.seek(0)
    data = uploaded_file.read()
    uploaded_file.seek(pos)
    return data


def extrair_texto_arquivo(uploaded_file) -> str:
    """
    Extrai texto puro de PDF, DOCX e TXT.
    Tenta múltiplas bibliotecas para robustez.
    """
    nome = uploaded_file.name.lower()
    data = _read_all(uploaded_file)

    # TXT direto
    if nome.endswith(".txt"):
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return data.decode("latin-1", errors="ignore")

    # PDF
    if nome.endswith(".pdf"):
        # 1) PyMuPDF
        if fitz is not None:
            try:
                pdf = fitz.open(stream=data, filetype="pdf")
                return "".join(page.get_text() for page in pdf)
            except Exception:
                pass
        # 2) PyPDF2 (fallback)
        if PdfReader is not None:
            try:
                reader = PdfReader(io.BytesIO(data))
                texto = []
                for page in getattr(reader, "pages", []):
                    try:
                        texto.append(page.extract_text() or "")
                    except Exception:
                        continue
                return "\n".join(texto)
            except Exception:
                pass
        return ""

    # DOCX
    if nome.endswith(".docx"):
        # 1) docx2txt
        if docx2txt is not None:
            try:
                return docx2txt.process(io.BytesIO(data)) or ""
            except Exception:
                pass
        # 2) python-docx
        if docx is not None:
            try:
                document = docx.Document(io.BytesIO(data))
                return "\n".join(p.text for p in document.paragraphs)
            except Exception:
                pass
        return ""

    # Demais extensões não suportadas
    return ""


# ==============================
# Normalização de chaves – foco EDITAL
# ==============================
_EDITAL_KEYMAP = {
    # principais
    "unidade_solicitante": ["unidade", "unidade_solicitante", "setor", "orgao"],
    "responsavel_tecnico": ["responsavel", "responsavel_tecnico", "gestor", "fiscal"],
    "objeto": ["objeto", "descricao", "escopo", "especificacao"],
    "modalidade": ["modalidade", "modalidade_licitacao", "tipo_modalidade"],
    "regime_execucao": ["regime_execucao", "regime", "modelo_execucao"],
    "base_legal": ["base_legal", "fundamentacao_legal", "justificativa_legal", "amparo_legal"],
    "justificativa_modalidade": ["justificativa_modalidade", "motivacao", "justificativa"],
    "habilitacao": ["habilitacao", "condicoes_participacao", "documentacao_habilitacao"],
    "criterios_julgamento": ["criterios_julgamento", "criterio", "criterios"],
    "prazo_execucao": ["prazo_execucao", "prazos", "prazo"],
    "forma_pagamento": ["forma_pagamento", "pagamento", "condicoes_pagamento"],
    "penalidades": ["penalidades", "sancoes", "multas", "penalidade"],
    "observacoes_finais": ["observacoes_finais", "observacoes", "notas", "comentarios"],
    # auxiliares
    "cnpj": ["cnpj"],
    "processo": ["processo", "n_processo", "numero_processo", "proc_adm"],
}

def _norm_key(key: str) -> Optional[str]:
    k = key.strip().lower()
    for target, aliases in _EDITAL_KEYMAP.items():
        if k == target or k in aliases:
            return target
    return None


def _normalize_for_edital(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte chaves variadas (vindo da IA/regex) para o conjunto canônico do EDITAL.
    Mantém apenas chaves reconhecidas, sem inserir valores vazios automaticamente.
    """
    out: Dict[str, Any] = {}
    for k, v in (raw or {}).items():
        nk = _norm_key(str(k))
        if nk:
            out[nk] = v
    return out


# ==============================
# Heurísticas institucionais (regex) – fallback sem IA
# ==============================
_RE_CNPJ = re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b")
_RE_PROCESSO = re.compile(r"(processo(?: administrativo)?\s*[:\-]?\s*)([\w./-]+)", re.I)
_RE_MODALIDADE = re.compile(r"\b(concorr[eê]ncia|preg[aã]o|tomada de preços|leil[aã]o|dispensa|inexigibilidade)\b", re.I)

def _parser_institucional(texto: str) -> Dict[str, Any]:
    d: Dict[str, Any] = {}
    if not texto:
        return d

    cnpj = _RE_CNPJ.search(texto)
    if cnpj:
        d["cnpj"] = cnpj.group(0)

    proc = _RE_PROCESSO.search(texto)
    if proc:
        d["processo"] = proc.group(2).strip()

    mod = _RE_MODALIDADE.search(texto)
    if mod:
        d["modalidade"] = mod.group(1).strip().lower()

    # Heurísticas simples
    if "habilita" in texto.lower():
        d.setdefault("habilitacao", "Conforme condições de participação descritas no edital.")
    if "julgamento" in texto.lower() or "critério" in texto.lower() or "criterio" in texto.lower():
        d.setdefault("criterios_julgamento", "Menor preço ou melhor técnica, conforme o caso.")
    return d


# ==============================
# IA opcional – extração assistida
# ==============================
def _analisar_insumo_ia(texto: str, artefato: str) -> Dict[str, Any]:
    client, model = _get_openai_client()
    if client is None or not model or not texto.strip():
        return {}

    prompt = (
        "Você é um redator técnico do TJSP (SAAB). "
        f"Extraia, do texto abaixo, os campos relevantes para o artefato '{artefato.upper()}'. "
        "Priorize chaves do EDITAL quando aplicável: "
        "['unidade_solicitante','responsavel_tecnico','objeto','modalidade','regime_execucao',"
        "'base_legal','justificativa_modalidade','habilitacao','criterios_julgamento','prazo_execucao',"
        "'forma_pagamento','penalidades','observacoes_finais','cnpj','processo'].\n\n"
        "Responda exclusivamente em JSON válido (um único objeto). "
        "Se algum campo não for encontrado, omita-o (não invente valores).\n\n"
        f"TEXTO:\n{texto[:12000]}\n"
    )

    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": "Você segue o padrão redacional SAAB/TJSP e a Lei 14.133/2021."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
        )
        content = resp.choices[0].message.content or ""
        # Tenta parsear diretamente; se vier dentro de bloco, extrai com regex
        json_str = content
        m = re.search(r"\{.*\}", content, re.S)
        if m:
            json_str = m.group(0)
        data = json.loads(json_str)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


# ==============================
# Orquestração principal
# ==============================
def processar_insumo(uploaded_file, artefato: str = "EDITAL") -> Dict[str, Any]:
    """
    Processa um insumo:
      1) extrai texto,
      2) aplica heurísticas institucionais,
      3) tenta extração por IA (se disponível),
      4) normaliza chaves para EDITAL,
      5) atualiza st.session_state["last_insumo"],
      6) grava JSON em exports/insumos/json/.
    Retorna o dicionário final (campos_ai).
    """
    artefato = (artefato or "EDITAL").upper()
    texto = extrair_texto_arquivo(uploaded_file)

    heur = _parser_institucional(texto)
    via_ia = _analisar_insumo_ia(texto, artefato)

    # Merge: IA tem precedência; heurísticas complementam
    merged: Dict[str, Any] = {**heur, **via_ia} if via_ia else heur
    campos_norm = _normalize_for_edital(merged)

    payload_state = {
        "nome_arquivo": getattr(uploaded_file, "name", "arquivo"),
        "artefato": artefato,
        "texto": texto,
        "campos_ai": campos_norm,
    }

    # Atualiza sessão para consumo imediato por EDITAL/TR/ETP
    if st is not None:
        st.session_state["last_insumo"] = payload_state

    # Persistência JSON
    _dump_json_safely(payload_state, f"{artefato}__{payload_state['nome_arquivo']}")

    return campos_norm

# ==============================================================
# 🔁 Compatibilidade retroativa – processar_insumo_dinamico
# ==============================================================

def processar_insumo_dinamico(uploaded_file, artefato: str = "EDITAL"):
    """
    Wrapper de compatibilidade com versões anteriores.
    Encaminha a chamada para processar_insumo().
    """
    return processar_insumo(uploaded_file, artefato=artefato)
