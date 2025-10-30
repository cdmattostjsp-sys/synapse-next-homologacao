# -*- coding: utf-8 -*-
"""
🧮 Comparador – SynapseNext (vNext+)
SAAB/TJSP – Comparação interdocumental com fallback seguro.
"""

import sys, os, json
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

# === Estilo/UX institucional ===
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

aplicar_estilo_global()
st.set_page_config(page_title="🧮 Comparador – SynapseNext", layout="wide", page_icon="🧮")
exibir_cabecalho_padrao("🧮 Comparador", "Análise comparativa interdocumental com métricas de similaridade")

# === Tentativa de import do pipeline oficial ===
comparar_fn = None
try:
    from utils.comparador_pipeline import comparar_documentos as _comparar
    comparar_fn = _comparar
except Exception:
    pass

st.divider()

# === Utilidades locais (fallback) ===
def _ler_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _texto_do_doc(doc: dict) -> str:
    # Junta valores textuais para comparação simples
    partes = []
    for k, v in doc.items():
        if isinstance(v, str):
            partes.append(v)
        elif isinstance(v, (list, tuple)):
            partes += [x for x in v if isinstance(x, str)]
        elif isinstance(v, dict):
            partes += [x for x in v.values() if isinstance(x, str)]
    return " ".join(partes).lower()

def _jaccard_similarity(a: str, b: str) -> float:
    sa, sb = set(a.split()), set(b.split())
    inter = len(sa & sb)
    union = len(sa | sb) or 1
    return round(100 * inter / union, 2)

def _comparar_fallback(docA: dict, docB: dict) -> dict:
    ta, tb = _texto_do_doc(docA), _texto_do_doc(docB)
    sim = _jaccard_similarity(ta, tb)
    return {
        "similaridade_percentual": sim,
        "resumo": f"Similaridade Jaccard ≈ {sim}%",
        "detalhes": [
            {"chave": "tokens_A", "valor": len(set(ta.split()))},
            {"chave": "tokens_B", "valor": len(set(tb.split()))},
        ],
    }

# === Fonte dos dados: snapshots existentes ou upload ===
snap_dir = Path("exports/snapshots")
snapshots = list(snap_dir.glob("*_snapshot.json")) if snap_dir.exists() else []

st.subheader("Seleção de Artefatos")
col1, col2 = st.columns(2)

with col1:
    optA_mode = st.radio("Origem do Artefato A", ["Snapshot", "Upload"], horizontal=True)
    if optA_mode == "Snapshot" and snapshots:
        selA = st.selectbox("Selecione o Artefato A (snapshot)", options=[s.name for s in snapshots])
        pathA = snap_dir / selA
        docA = _ler_json(pathA)
    else:
        upA = st.file_uploader("Envie o Artefato A (.json)", type=["json"], key="upA")
        docA = json.load(upA) if upA else {}
with col2:
    optB_mode = st.radio("Origem do Artefato B", ["Snapshot", "Upload"], horizontal=True)
    if optB_mode == "Snapshot" and snapshots:
        selB = st.selectbox("Selecione o Artefato B (snapshot)", options=[s.name for s in snapshots], key="selB")
        pathB = snap_dir / selB
        docB = _ler_json(pathB)
    else:
        upB = st.file_uploader("Envie o Artefato B (.json)", type=["json"], key="upB")
        docB = json.load(upB) if upB else {}

st.divider()

if st.button("🔍 Executar Comparação", type="primary", use_container_width=True):
    if not docA or not docB:
        st.error("Forneça os dois artefatos (A e B).")
        st.stop()

    try:
        if comparar_fn:
            resultado = comparar_fn(docA, docB)
        else:
            resultado = _comparar_fallback(docA, docB)
    except Exception as e:
        st.warning(f"Pipeline oficial indisponível. Usando fallback. Detalhe: {e}")
        resultado = _comparar_fallback(docA, docB)

    st.success("✅ Comparação concluída.")
    st.metric("Similaridade Global (%)", f"{resultado.get('similaridade_percentual', 0)}%")

    if "detalhes" in resultado:
        df = pd.DataFrame(resultado["detalhes"])
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.json({"resumo": resultado.get("resumo", ""), "timestamp": datetime.now().isoformat()})
else:
    st.info("Selecione/Envie os artefatos e clique em **Executar Comparação**.")

st.markdown("---")
st.caption("Sistema SynapseNext • SAAB 5.0 – TJSP • Comparador vNext+")
