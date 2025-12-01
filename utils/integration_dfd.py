# ======================================================================
# utils/integration_dfd.py — VERSÃO FINAL 2025-D7 (ESTÁVEL)
# Compatível com DocumentAgent(D2) + IAClient vNext
# Corrige:
#   - DFD vazio sobrescrevendo insumo
#   - Carregamento correto do conteúdo textual
#   - Formulário iniciando vazio
#   - Fluxo completo Insumos → DFD → IA
# ======================================================================

from __future__ import annotations

import os
import json
import glob
import streamlit as st
from datetime import datetime


# ======================================================================
# 🔧 SANITIZAÇÃO DE TEXTO
# ======================================================================
def _limpar_markdown(texto: str) -> str:
    """Remove blocos markdown e normaliza aspas."""
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
# 🔧 CRIA UM DFD BÁSICO A PARTIR DE INSUMO
# ======================================================================
def _criar_dfd_basico_a_partir_de_insumo(texto: str, origem: str = "insumo_raw") -> dict:
    """Constrói um DFD mínimo apenas para carregar o formulário."""
    secoes = {
        "Contexto Institucional": texto,
        "Diagnóstico da Situação Atual": "",
        "Fundamentação da Necessidade": "",
        "Objetivos da Contratação": "",
        "Escopo Inicial da Demanda": "",
        "Resultados Esperados": "",
        "Benefícios Institucionais": "",
        "Justificativa Legal": "",
        "Riscos da Não Contratação": "",
        "Requisitos Mínimos": "",
        "Critérios de Sucesso": "",
    }

    return {
        "unidade_demandante": "",
        "responsavel": "",
        "prazo_estimado": "",
        "valor_estimado": "0,00",
        "descricao_necessidade": texto,
        "motivacao": "",
        "texto_narrativo": texto,
        "secoes": secoes,
        "lacunas": [],
        "origem": origem,
    }


# ======================================================================
# 🧩 CONVERSÃO DO MODELO MODERNO → CAMPOS TRADICIONAIS
# ======================================================================
def _mapear_moderno_para_campos_legados(dfd: dict) -> dict:
    """Compatibiliza DFD moderno vindo da IA com o formulário legado."""
    if not isinstance(dfd, dict):
        return {}

    # Caso venha envolto em {"DFD": {...}}
    if "DFD" in dfd and isinstance(dfd["DFD"], dict):
        dfd = dfd["DFD"]

    secoes = dfd.get("secoes", {})
    if not isinstance(secoes, dict):
        secoes = {}

    descricao = "\n\n".join([
        secoes.get("Contexto Institucional", ""),
        secoes.get("Diagnóstico da Situação Atual", ""),
        secoes.get("Fundamentação da Necessidade", ""),
    ]).strip()

    motivacao = "\n\n".join([
        secoes.get("Objetivos da Contratação", ""),
        secoes.get("Resultados Esperados", ""),
        secoes.get("Benefícios Institucionais", ""),
        secoes.get("Justificativa Legal", ""),
        secoes.get("Riscos da Não Contratação", ""),
    ]).strip()

    return {
        "unidade_demandante": dfd.get("unidade_demandante", ""),
        "responsavel": dfd.get("responsavel", ""),
        "prazo_estimado": dfd.get("prazo_estimado", ""),
        "descricao_necessidade": descricao or dfd.get("descricao_necessidade", ""),
        "motivacao": motivacao or dfd.get("motivacao", ""),
        "valor_estimado": dfd.get("valor_estimado", "0,00"),
        "texto_narrativo": dfd.get("texto_narrativo", ""),
        "secoes": secoes,
        "lacunas": dfd.get("lacunas", []),
    }


# ======================================================================
# 📥 LEITURA UNIVERSAL DE ARQUIVO
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return {}

    # ✔️ Caso seja um formulário consolidado
    if isinstance(dados.get("campos_ai"), dict):
        return dados["campos_ai"]

    # ✔️ Caso seja retorno da IA moderna
    if isinstance(dados.get("resultado_ia"), dict):
        return _mapear_moderno_para_campos_legados(dados["resultado_ia"])

    # ✔️ Caso seja insumo puro (PDF, DOCX, TXT)
    if isinstance(dados.get("conteudo_textual"), str):
        texto = dados["conteudo_textual"].strip()
        if len(texto) > 20:
            return _criar_dfd_basico_a_partir_de_insumo(texto)

    return {}


# ======================================================================
# 🔄 OBTÉM O DFD CARREGADO (sessão → último arquivo → histórico)
# ======================================================================
def obter_dfd_da_sessao() -> dict:

    # 1. Sessão
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    # 2. Último arquivo
    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    # 3. Histórico
    arquivos = sorted(
        glob.glob(os.path.join(base, "DFD_*.json")),
        key=os.path.getmtime,
        reverse=True,
    )
    for arq in arquivos:
        if "DFD_ultimo.json" in arq:
            continue
        dados = _carregar_dfd_de_arquivo(arq)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    return {}


# ======================================================================
# ❌ NUNCA SALVAR FORMULÁRIO VAZIO
# ======================================================================
def _formulario_vazio(campos: dict) -> bool:
    if not campos:
        return True
    if not campos.get("texto_narrativo") and not campos.get("descricao_necessidade"):
        return True
    return False


# ======================================================================
# 💾 SALVAR DFD CONSOLIDADO
# ======================================================================
def salvar_dfd_em_json(campos: dict, origem: str = "dfd_moderno_streamlit") -> str:

    if _formulario_vazio(campos):
        print("[DFD] Salvamento CANCELADO — formulário vazio.")
        return ""

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
# 🧾 STATUS EXIBIDO NA PÁGINA DFD
# ======================================================================
def status_dfd() -> str:
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ DFD carregado a partir do último insumo ou IA."

    base = os.path.join("exports", "insumos", "json")
    if os.path.exists(os.path.join(base, "DFD_ultimo.json")):
        return "🗂️ DFD disponível a partir dos insumos processados."

    return "⚠️ Nenhum DFD disponível — envie um documento pelo módulo INSUMOS."


# ======================================================================
# 🧠 IA — GERAR RASCUNHO COMPLETO
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("⚠️ Nenhum insumo encontrado.")
        return {}

    try:
        dados = json.load(open(ultimo, "r", encoding="utf-8"))
        texto = dados.get("conteudo_textual", "").strip()
    except Exception as e:
        st.error(f"❌ Falha ao ler insumo: {e}")
        return {}

    if len(texto) < 20:
        st.error("⚠️ Texto insuficiente para IA.")
        return {}

    try:
        from agents.document_agent import processar_dfd_com_ia
        bruto = processar_dfd_com_ia(texto)

        if isinstance(bruto, dict) and "resultado_ia" in bruto:
            bruto = bruto["resultado_ia"]

        if isinstance(bruto, dict) and (
            "secoes" in bruto or "texto_narrativo" in bruto
        ):
            dfd_final = bruto
        else:
            dfd_final = _mapear_moderno_para_campos_legados(bruto)

        st.session_state["dfd_campos_ai"] = dfd_final
        return dfd_final

    except Exception as e:
        st.error(f"❌ Erro IA: {e}")
        return {}
