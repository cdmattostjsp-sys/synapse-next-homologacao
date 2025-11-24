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
# 🔧 Utilitário — Remover blocos Markdown (```json)
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
# 🧩 Compatibilização com modelo Moderno-Governança da IA
# ======================================================================
def _mapear_moderno_para_campos_legados(dfd: dict) -> dict:
    """
    Recebe o objeto {"DFD": {...}} já validado e retorna um dicionário
    compatível com o formulário tradicional do DFD.
    """

    if not isinstance(dfd, dict):
        return {}

    # -----------------------------
    # Se vier dentro de {"DFD": {...}}
    # -----------------------------
    if "DFD" in dfd and isinstance(dfd["DFD"], dict):
        dfd = dfd["DFD"]

    secoes = dfd.get("secoes", {})
    if not isinstance(secoes, dict):
        secoes = {}

    # -----------------------------
    # 1) Descrição da Necessidade
    # -----------------------------
    descricao = ""
    partes_desc = []

    for chave in [
        "Contexto Institucional",
        "Diagnóstico da Situação Atual",
        "Fundamentação da Necessidade",
    ]:
        v = secoes.get(chave)
        if isinstance(v, str) and v.strip():
            partes_desc.append(v.strip())

    if partes_desc:
        descricao = "\n\n".join(partes_desc)

    # Se vier campo legível direto
    if not descricao:
        descricao = dfd.get("descricao_necessidade") or ""

    # -----------------------------
    # 2) Motivação / Objetivos / Justificativa
    # -----------------------------
    motivacao = ""
    partes_mot = []

    for chave in [
        "Objetivos da Contratação",
        "Resultados Esperados",
        "Benefícios Institucionais",
        "Justificativa Legal",
        "Riscos da Não Contratação",
    ]:
        v = secoes.get(chave)
        if isinstance(v, str) and v.strip():
            partes_mot.append(v.strip())

    if partes_mot:
        motivacao = "\n\n".join(partes_mot)

    # -----------------------------
    # Valor estimado — sem alucinar
    # -----------------------------
    valor = dfd.get("valor_estimado") or "0,00"
    if not isinstance(valor, str):
        valor = str(valor)

    # -----------------------------
    # Resultado consolidado
    # -----------------------------
    return {
        "unidade_demandante": dfd.get("unidade_demandante") or "",
        "responsavel": dfd.get("responsavel") or "",
        "prazo_estimado": dfd.get("prazo_estimado") or "",
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        "valor_estimado": valor,
    }


# ======================================================================
# 📥 Leitura de arquivos (insumo, IA, consolidado)
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Falha ao ler {caminho}: {e}")
        return {}

    # ------------------------------------------------------------
    # 1) Arquivo consolidado pelo formulário (formulário DFD)
    # ------------------------------------------------------------
    if isinstance(dados.get("campos_ai"), dict):
        return dados["campos_ai"]

    # ------------------------------------------------------------
    # 2) Resposta salva da IA
    # ------------------------------------------------------------
    if isinstance(dados.get("resultado_ia"), dict):
        r = dados["resultado_ia"]

        # Caso moderno (DFD Moderno-Governança)
        if isinstance(r, dict):
            if "DFD" in r and isinstance(r["DFD"], dict):
                return _mapear_moderno_para_campos_legados(r)
            # Se não tiver DFD mas tiver formato de IA antigo/genérico
            return _mapear_moderno_para_campos_legados(r)

    # ------------------------------------------------------------
    # 3) INSUMO puro (OCR / PDF)
    # ------------------------------------------------------------
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
# 🔄 Obter DFD carregado na sessão ou arquivo
# ======================================================================
def obter_dfd_da_sessao() -> dict:
    # Sessão já tem
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # Carrega o último
    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    # Arquivos anteriores (backup)
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
# 🧾 Status para o cabeçalho da página Streamlit
# ======================================================================
def status_dfd() -> str:
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ DFD carregado automaticamente (sessão ativa)"

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        return "🗂️ DFD disponível a partir dos insumos processados"

    return "⚠️ Nenhum DFD disponível — envie um insumo pelo módulo INSUMOS."


# ======================================================================
# 🧠 Chamar IA para gerar DFD estruturado
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:
    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("⚠️ Nenhum insumo encontrado para gerar o DFD pela IA.")
        return {}

    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        texto = (dados.get("conteudo_textual") or "").strip()
    except Exception:
        st.error("❌ Falha ao ler o insumo para a IA.")
        return {}

    if len(texto) < 30:
        st.error("⚠️ Texto insuficiente para processamento pela IA.")
        return {}

    # Chamada ao DocumentAgent
    try:
        from agents.document_agent import processar_dfd_com_ia

        bruto = processar_dfd_com_ia(texto)

        # Desempacota {"timestamp": ..., "resultado_ia": {...}}
        if isinstance(bruto, dict) and "resultado_ia" in bruto:
            bruto = bruto["resultado_ia"]

        dfd_norm = _mapear_moderno_para_campos_legados(bruto)
        if not dfd_norm:
            st.warning("⚠️ A IA não retornou um DFD estruturado.")
            return {}

        st.session_state["dfd_campos_ai"] = dfd_norm
        return dfd_norm

    except Exception as e:
        st.error(f"❌ Erro ao executar IA para o DFD: {e}")
        return {}
