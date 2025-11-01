# ==========================================================
# utils/integration_insumos.py
# SynapseNext – SAAB / TJSP
# Versão vNext-Stable.2 (2025-11)
# ==========================================================

import os, io, re, json, datetime as dt
from typing import Any, Dict

try:
    import streamlit as st
except Exception:
    st = None

# ----------------------------------------------------------
# 📂 Estrutura de diretórios
# ----------------------------------------------------------
_EXPORTS_DIR = os.path.join("exports", "insumos")
_EXPORTS_JSON_DIR = os.path.join(_EXPORTS_DIR, "json")
os.makedirs(_EXPORTS_DIR, exist_ok=True)
os.makedirs(_EXPORTS_JSON_DIR, exist_ok=True)

# ----------------------------------------------------------
# 🧾 Utilidades
# ----------------------------------------------------------
def salvar_insumo(uploaded_file, artefato: str) -> str:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"{ts}__{artefato.upper()}__{uploaded_file.name}"
    path = os.path.join(_EXPORTS_DIR, fname)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def _dump_json_safely(payload: Dict[str, Any], hint: str):
    safe = re.sub(r"[^a-zA-Z0-9_\-]+", "_", hint)[:120]
    path = os.path.join(_EXPORTS_JSON_DIR, f"{safe}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path

# ----------------------------------------------------------
# 🧠 Propagação intermodular
# ----------------------------------------------------------
def _propagar_para_modulo(artefato: str, campos: Dict[str, Any]):
    if st is None:
        return
    artefato = artefato.upper()
    mapping = {
        "DFD": "dfd_campos_ai",
        "ETP": "etp_campos_ai",
        "TR": "tr_campos_ai",
        "EDITAL": "edital_campos_ai",
    }
    key = mapping.get(artefato)
    if key:
        st.session_state[key] = campos
        st.session_state["insumo_atual"] = artefato
        st.session_state["last_insumo"] = {"artefato": artefato, "campos_ai": campos}

# ----------------------------------------------------------
# 🧠 Processamento principal
# ----------------------------------------------------------
def processar_insumo(uploaded_file, artefato: str = "EDITAL") -> Dict[str, Any]:
    artefato = (artefato or "EDITAL").upper()

    # Extração bruta do texto (simplificada)
    data = uploaded_file.read()
    uploaded_file.seek(0)
    texto = data.decode("utf-8", errors="ignore")

    # Estrutura mínima para teste
    campos_norm = {
        "objeto": f"Conteúdo identificado no insumo {uploaded_file.name}",
        "unidade_solicitante": "Departamento de Teste",
        "responsavel_tecnico": "Responsável Automático",
    }

    payload = {
        "nome_arquivo": uploaded_file.name,
        "artefato": artefato,
        "texto": texto[:4000],
        "campos_ai": campos_norm,
    }

    _dump_json_safely(payload, f"{artefato}__{uploaded_file.name}")
    if st:
        _propagar_para_modulo(artefato, campos_norm)
    return campos_norm

def processar_insumo_dinamico(uploaded_file, artefato: str = "EDITAL"):
    return processar_insumo(uploaded_file, artefato)

# ==========================================================
# 🔽 Salvamento e persistência dos insumos processados
# ==========================================================

def salvar_insumo_processado(artefato, descricao, campos_ai):
    """
    Salva o insumo processado tanto na sessão quanto em disco (formato JSON).
    """
    try:
        # Garante estrutura correta
        dados_insumo = {
            "artefato": artefato,
            "descricao": descricao,
            "campos_ai": campos_ai if isinstance(campos_ai, dict) else {},
        }

        # Persiste em sessão
        chave_sessao = f"{artefato.lower()}_campos_ai"
        st.session_state[chave_sessao] = dados_insumo["campos_ai"]

        # Persiste em disco
        EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")
        os.makedirs(EXPORTS_JSON_DIR, exist_ok=True)
        nome_arquivo = f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        caminho = os.path.join(EXPORTS_JSON_DIR, nome_arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados_insumo, f, ensure_ascii=False, indent=2)

        st.success(f"✅ Insumo '{artefato}' processado e encaminhado com sucesso.")
        return True

    except Exception as e:
        st.error(f"Erro ao salvar insumo processado: {e}")
        return False
