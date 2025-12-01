# ======================================================================
# utils/integration_dfd.py — VERSÃO FINAL 2025-D9 (ULTRA-ESTÁVEL)
# Compatível com DocumentAgent(D3) + IAClient vNext
# Preserva integralmente o DFD moderno (sem “achatar” JSON)
# Import seguro no Streamlit Cloud
# ======================================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime


# ======================================================================
# 🔧 Remover blocos Markdown/formatadores
# ======================================================================
def _limpar_markdown(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    return (
        texto.replace("```json", "")
        .replace("```", "")
        .replace("“", '"')
        .replace("”", '"')
        .strip()
    )


# ======================================================================
# 🧩 Conversão para legado (apenas quando necessário)
# ======================================================================
def _converter_para_legado_se_necessario(dfd: dict) -> dict:
    """
    Mantém o modelo moderno. Só converte quando o JSON é legado.
    """
    if not isinstance(dfd, dict):
        return {}

    # Modelo moderno detectado → manter integral
    if (
        "secoes" in dfd
        or "texto_narrativo" in dfd
        or "lacunas" in dfd
    ):
        return dfd

    # Modelo legado → montar minimal moderado
    secoes = dfd.get("secoes", {}) if isinstance(dfd.get("secoes"), dict) else {}

    descricao = dfd.get("descricao_necessidade", "")
    motivacao = dfd.get("motivacao", "")

    # Montar texto narrativo legado
    texto_narrativo = ""
    partes = []
    for sec in [
        "Contexto Institucional",
        "Diagnóstico da Situação Atual",
        "Fundamentação da Necessidade",
        "Objetivos da Contratação",
        "Escopo Inicial da Demanda",
        "Resultados Esperados",
        "Benefícios Institucionais",
        "Justificativa Legal",
        "Riscos da Não Contratação",
        "Requisitos Mínimos",
        "Critérios de Sucesso",
    ]:
        if sec in secoes and isinstance(secoes[sec], str) and secoes[sec].strip():
            partes.append(secoes[sec].strip())

    if partes:
        texto_narrativo = "\n\n".join(partes)

    return {
        "unidade_demandante": dfd.get("unidade_demandante", ""),
        "responsavel": dfd.get("responsavel", ""),
        "prazo_estimado": dfd.get("prazo_estimado", ""),
        "valor_estimado": str(dfd.get("valor_estimado", "0,00")),
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        "texto_narrativo": texto_narrativo,
        "secoes": secoes,
        "lacunas": dfd.get("lacunas", []),
    }


# ======================================================================
# 📥 Leitura de arquivos
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    """
    Lê qualquer arquivo salvo em exports/insumos/json/
    e converte automaticamente para modelo moderno.
    """
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Falha ao ler {caminho}: {e}")
        return {}

    # 1 — Formulário moderno salvo via Streamlit
    if isinstance(dados.get("campos_ai"), dict):
        return _converter_para_legado_se_necessario(dados["campos_ai"])

    # 2 — Resultado da IA moderna
    if "resultado_ia" in dados and isinstance(dados["resultado_ia"], dict):
        bruto = dados["resultado_ia"]

        if "DFD" in bruto and isinstance(bruto["DFD"], dict):
            bruto = bruto["DFD"]

        return _converter_para_legado_se_necessario(bruto)

    # 3 — Insumo bruto via módulo INSUMOS
    texto = dados.get("conteudo_textual")
    if isinstance(texto, str) and len(texto.strip()) > 20:
        return {
            "unidade_demandante": "",
            "responsavel": "",
            "prazo_estimado": "",
            "valor_estimado": "0,00",
            "descricao_necessidade": texto.strip(),
            "motivacao": "",
            "texto_narrativo": texto.strip(),
            "secoes": {},
            "lacunas": [],
        }

    return {}


# ======================================================================
# 🔄 Obter DFD (sessão → arquivo → histórico)
# ======================================================================
def obter_dfd_da_sessao() -> dict:

    # Sessão
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # Último arquivo
    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    # Histórico
    arquivos = sorted(
        glob.glob(os.path.join(base, "DFD_*.json")),
        key=os.path.getmtime,
        reverse=True,
    )

    for arq in arquivos:
        if arq.endswith("DFD_ultimo.json"):
            continue
        dados = _carregar_dfd_de_arquivo(arq)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    return {}


# ======================================================================
# 💾 Salvar DFD consolidado (modelo moderno)
# ======================================================================
def salvar_dfd_em_json(campos: dict, origem: str = "dfd_moderno_streamlit") -> str:
    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    payload = {
        "artefato": "DFD",
        "origem": origem,
        "campos_ai": campos,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arq1 = os.path.join(base, "DFD_ultimo.json")
    arq2 = os.path.join(base, f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arq1, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arq2, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.session_state["dfd_campos_ai"] = campos
        return arq1

    except Exception as e:
        st.error(f"❌ Falha ao salvar DFD: {e}")
        return ""


# ======================================================================
# 🧠 IA → Gerar rascunho do DFD (modelo moderno integral)
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:
    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("⚠️ Nenhum insumo encontrado.")
        return {}

    # 1 — Carregar texto do insumo
    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        texto = (dados.get("conteudo_textual") or "").strip()
    except Exception as e:
        st.error(f"❌ Falha ao ler insumo: {e}")
        return {}

    if len(texto) < 20:
        st.error("⚠️ Texto insuficiente para IA.")
        return {}

    # 2 — Chamada IA → DocumentAgent(D3)
    try:
        from agents.document_agent import processar_dfd_com_ia
        bruto = processar_dfd_com_ia(texto)

        if "resultado_ia" in bruto and isinstance(bruto["resultado_ia"], dict):
            bruto = bruto["resultado_ia"]

        if "DFD" in bruto and isinstance(bruto["DFD"], dict):
            bruto = bruto["DFD"]

        dfd_moderno = bruto

        # 3 — armazenar moderno integral
        st.session_state["dfd_campos_ai"] = dfd_moderno
        return dfd_moderno

    except Exception as e:
        st.error(f"❌ Erro IA: {e}")
        return {}



