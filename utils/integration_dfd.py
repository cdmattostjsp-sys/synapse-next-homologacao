# ======================================================================
# utils/integration_dfd.py — VERSÃO REFORÇADA 2025-D2
# Compatível com DocumentAgent vNext (DFD Moderno + Governança)
# Mantém compatibilidade total com o fluxo anterior do Streamlit
# ======================================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime


# ======================================================================
# 🔧 Remover blocos Markdown
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
# 🧩 Converter JSON moderno para formato tradicional do formulário
# ======================================================================
def _mapear_moderno_para_campos_legados(dfd: dict) -> dict:

    if not isinstance(dfd, dict):
        return {}

    if "DFD" in dfd and isinstance(dfd["DFD"], dict):
        dfd = dfd["DFD"]

    secoes = dfd.get("secoes", {})
    if not isinstance(secoes, dict):
        secoes = {}

    # -----------------------------
    # 1) Descrição (Contexto + Diagnóstico + Fundamentação)
    # -----------------------------
    descricao = "\n\n".join([
        secoes.get("Contexto Institucional", "").strip(),
        secoes.get("Diagnóstico da Situação Atual", "").strip(),
        secoes.get("Fundamentação da Necessidade", "").strip(),
    ]).strip()

    # fallback
    if not descricao:
        descricao = dfd.get("descricao_necessidade") or ""

    # -----------------------------
    # 2) Motivação / Objetivos / Justificativa
    # -----------------------------
    motivacao = "\n\n".join([
        secoes.get("Objetivos da Contratação", "").strip(),
        secoes.get("Resultados Esperados", "").strip(),
        secoes.get("Benefícios Institucionais", "").strip(),
        secoes.get("Justificativa Legal", "").strip(),
        secoes.get("Riscos da Não Contratação", "").strip(),
    ]).strip()

    valor = dfd.get("valor_estimado") or "0,00"

    return {
        "unidade_demandante": dfd.get("unidade_demandante") or "",
        "responsavel": dfd.get("responsavel") or "",
        "prazo_estimado": dfd.get("prazo_estimado") or "",
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        "valor_estimado": valor,
    }


# ======================================================================
# 📥 Ler arquivos (insumo / IA / consolidado)
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Falha ao ler {caminho}: {e}")
        return {}

    # 1) Arquivo consolidado do formulário
    if isinstance(dados.get("campos_ai"), dict):
        return dados["campos_ai"]

    # 2) Saída da IA
    if isinstance(dados.get("resultado_ia"), dict):
        bruto = dados["resultado_ia"]
        return _mapear_moderno_para_campos_legados(bruto)

    # 3) Insumo puro
    texto = dados.get("conteudo_textual")
    if isinstance(texto, str) and len(texto.strip()) > 15:
        return {
            "unidade_demandante": "",
            "responsavel": "",
            "prazo_estimado": "",
            "descricao_necessidade": texto.strip(),
            "motivacao": "",
            "valor_estimado": "0,00",
        }

    return {}


# ======================================================================
# 🔄 Obter DFD carregado
# ======================================================================
def obter_dfd_da_sessao() -> dict:

    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

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
# 💾 Salvar DFD consolidado
# ======================================================================
def salvar_dfd_em_json(campos: dict, origem: str = "formulario_dfd_streamlit") -> str:
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
# 🧠 Gerar DFD com IA
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("⚠️ Nenhum insumo encontrado.")
        return {}

    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        texto = (dados.get("conteudo_textual") or "").strip()
    except Exception:
        st.error("❌ Falha ao ler insumo.")
        return {}

    if len(texto) < 30:
        st.error("⚠️ Texto insuficiente.")
        return {}

    try:
        from agents.document_agent import processar_dfd_com_ia
        bruto = processar_dfd_com_ia(texto)

        if "resultado_ia" in bruto:
            bruto = bruto["resultado_ia"]

        dfd_norm = _mapear_moderno_para_campos_legados(bruto)
        if not dfd_norm:
            st.warning("⚠️ A IA não retornou estrutura válida.")
            return {}

        st.session_state["dfd_campos_ai"] = dfd_norm
        return dfd_norm

    except Exception as e:
        st.error(f"❌ Erro IA: {e}")
        return {}
