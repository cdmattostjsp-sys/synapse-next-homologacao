# ======================================================================
# utils/integration_dfd.py — VERSÃO REFORÇADA 2025-D2-FIX
# Compatível com DocumentAgent D2 (DFD Moderno + Governança)
# Mantém compatibilidade total com o fluxo anterior do Streamlit
# ======================================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime


# ======================================================================
# 🔧 Remover blocos Markdown e aspas "tortas"
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
    """
    Converte a estrutura moderna da IA para o formato esperado
    pelo formulário DFD (unidade, responsável, descrição, motivação, etc.).

    Aceita:
      • {"DFD": {...}}  (formato "externo")
      • {...}           (DFD já interno, como retornado pelo DocumentAgent D2)
    """

    if not isinstance(dfd, dict):
        return {}

    # Se vier no formato {"DFD": {...}}, usa o interno
    if "DFD" in dfd and isinstance(dfd["DFD"], dict):
        dfd = dfd["DFD"]

    # Garantir que "secoes" seja dicionário
    secoes = dfd.get("secoes", {})
    if not isinstance(secoes, dict):
        secoes = {}

    def _get_secao(nome: str) -> str:
        val = secoes.get(nome, "")
        if isinstance(val, str):
            return val.strip()
        return ""

    # -----------------------------
    # 1) Descrição (Contexto + Diagnóstico + Fundamentação)
    # -----------------------------
    partes_desc = [
        _get_secao("Contexto Institucional"),
        _get_secao("Diagnóstico da Situação Atual"),
        _get_secao("Fundamentação da Necessidade"),
    ]
    partes_desc = [p for p in partes_desc if p]  # remove vazios
    descricao = "\n\n".join(partes_desc).strip()

    # fallback
    if not descricao:
        desc_raw = dfd.get("descricao_necessidade") or dfd.get("descricao") or ""
        if isinstance(desc_raw, str):
            descricao = desc_raw.strip()
        else:
            descricao = str(desc_raw)

    # -----------------------------
    # 2) Motivação / Objetivos / Justificativa
    # -----------------------------
    partes_mot = [
        _get_secao("Objetivos da Contratação"),
        _get_secao("Resultados Esperados"),
        _get_secao("Benefícios Institucionais"),
        _get_secao("Justificativa Legal"),
        _get_secao("Riscos da Não Contratação"),
    ]
    partes_mot = [p for p in partes_mot if p]
    motivacao = "\n\n".join(partes_mot).strip()

    # -----------------------------
    # 3) Valor estimado — sem alucinar
    # -----------------------------
    valor = dfd.get("valor_estimado") or "0,00"
    if not isinstance(valor, str):
        valor = str(valor)

    # -----------------------------
    # Resultado final compatível com formulário
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
# 📥 Ler arquivos (insumo / IA / consolidado)
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    """
    Interpreta automaticamente três tipos de arquivo:
      1) DFD consolidado pelo formulário:
         {
           "artefato": "DFD",
           "origem": "...",
           "campos_ai": { ... }
         }

      2) Saída da IA (processar_dfd_com_ia):
         {
           "timestamp": "...",
           "resultado_ia": { ... }  # pode ser {"DFD": {...}} ou já {...}
         }

      3) INSUMO puro:
         {
           "arquivo": "...",
           "conteudo_textual": "...."
         }
    """
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
        texto_limpo = _limpar_markdown(texto.strip())
        return {
            "unidade_demandante": "",
            "responsavel": "",
            "prazo_estimado": "",
            "descricao_necessidade": texto_limpo,
            "motivacao": "",
            "valor_estimado": "0,00",
        }

    return {}


# ======================================================================
# 🔄 Obter DFD carregado
# ======================================================================
def obter_dfd_da_sessao() -> dict:
    """
    Ordem de prioridade:
      1) Dados já carregados em st.session_state["dfd_campos_ai"]
      2) Arquivo exports/insumos/json/DFD_ultimo.json
      3) Arquivos históricos DFD_*.json (mais recente)
    """

    # 1) Sessão já possui DFD
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # 2) Último DFD salvo
    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    # 3) Históricos DFD_*.json
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
    """
    Salva o DFD consolidado em:
      • exports/insumos/json/DFD_ultimo.json
      • exports/insumos/json/DFD_YYYYMMDD_HHMMSS.json
    """
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
    """
    Fornece mensagem amigável para o topo da página DFD.
    Usado em: streamlit_app/pages/02_📄 DFD - Formalização da Demanda.py
    """
    # Sessão já tem algo carregado
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ DFD carregado automaticamente (sessão ativa)"

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        return "🗂️ DFD disponível a partir dos insumos processados"

    return "⚠️ Nenhum DFD disponível — envie um insumo pelo módulo 🔧 Insumos."


# ======================================================================
# 🧠 Gerar DFD com IA
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:
    """
    Usa o texto bruto do último insumo (conteudo_textual)
    para chamar o DocumentAgent D2 e gerar um DFD estruturado.
    """

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

    # Chamada ao DocumentAgent (processar_dfd_com_ia)
    try:
        from agents.document_agent import processar_dfd_com_ia

        bruto = processar_dfd_com_ia(texto)

        # Estrutura padrão: {"timestamp": "...", "resultado_ia": {...}}
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
