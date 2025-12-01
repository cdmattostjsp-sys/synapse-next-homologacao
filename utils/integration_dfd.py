# ======================================================================
# utils/integration_dfd.py — VERSÃO FINAL 2025-D6
# Compatível com:
#   - DocumentAgent(D3)
#   - AIClient vNext
#   - integration_insumos.py 2025-D4
#   - Página Streamlit DFD (dfd_moderno)
#
# Responsabilidades:
#   • Ler insumos (exports/insumos/json/DFD_ultimo.json)
#   • Ler DFD consolidados (campos_ai) e DFD gerados por IA
#   • Manter dfd_campos_ai em sessão
#   • Invocar a IA para gerar rascunho moderno do DFD
#   • Salvar DFD consolidados em JSON
# ======================================================================

from __future__ import annotations

import os
import json
import glob
from datetime import datetime

import streamlit as st


# ======================================================================
# 🔧 Sanitização simples de texto
# ======================================================================
def _limpar_markdown(texto: str) -> str:
    """Remove marcadores simples de Markdown/JSON em texto bruto."""
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
# 🔧 Derivar texto-base para IA a partir de um JSON qualquer
# ======================================================================
def _extrair_texto_base_para_ia(dados: dict) -> str:
    """
    Tenta obter o melhor texto-base para enviar à IA a partir de um JSON:

      1) conteudo_textual (insumo bruto)
      2) campos_ai.texto_narrativo
      3) campos_ai.descricao_necessidade
      4) concatenação de secoes
      5) fallback: string vazia
    """
    if not isinstance(dados, dict):
        return ""

    # 1) Insumo bruto
    texto = dados.get("conteudo_textual")
    if isinstance(texto, str) and len(texto.strip()) > 0:
        return _limpar_markdown(texto)

    # 2) DFD consolidado (campos_ai)
    campos_ai = dados.get("campos_ai")
    if isinstance(campos_ai, dict):
        # 2.1) texto_narrativo
        tn = campos_ai.get("texto_narrativo")
        if isinstance(tn, str) and len(tn.strip()) > 0:
            return _limpar_markdown(tn)

        # 2.2) descricao_necessidade
        desc = campos_ai.get("descricao_necessidade")
        if isinstance(desc, str) and len(desc.strip()) > 0:
            return _limpar_markdown(desc)

        # 2.3) concatenação das seções
        secoes = campos_ai.get("secoes")
        if isinstance(secoes, dict):
            partes = []
            for v in secoes.values():
                if isinstance(v, str) and v.strip():
                    partes.append(v.strip())
            if partes:
                return _limpar_markdown("\n\n".join(partes))

    # 3) DFD moderno diretamente em dados["DFD"]
    dfd_mod = dados.get("DFD")
    if isinstance(dfd_mod, dict):
        tn = dfd_mod.get("texto_narrativo")
        if isinstance(tn, str) and len(tn.strip()) > 0:
            return _limpar_markdown(tn)

    return ""


# ======================================================================
# 🔧 Conversão de insumo puro → esqueleto de DFD
# ======================================================================
def _criar_dfd_basico_a_partir_de_insumo(texto: str, origem: str = "insumo_raw") -> dict:
    """
    Cria um DFD básico, preenchendo apenas descrição e texto narrativo
    com o conteúdo bruto do insumo.
    """
    texto = _limpar_markdown(texto)
    return {
        "unidade_demandante": "",
        "responsavel": "",
        "prazo_estimado": "",
        "valor_estimado": "0,00",
        "descricao_necessidade": texto,
        "motivacao": "",
        "texto_narrativo": texto,
        "secoes": {},
        "lacunas": [],
        "origem": origem,
        "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ======================================================================
# 📥 Leitura de arquivos DFD / insumos
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    """
    Carrega um JSON e tenta extrair o melhor "pacote DFD" possível.
    Suporta:
      • payloads com campos_ai (DFD consolidado)
      • payloads com resultado_ia (saída de DocumentAgent)
      • payloads com DFD (raiz moderna)
      • payloads de insumo puro (conteudo_textual)
    """
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Falha ao ler {caminho}: {e}")
        return {}

    # Caso 1 — formulário consolidado
    if isinstance(dados.get("campos_ai"), dict):
        return dados["campos_ai"]

    # Caso 2 — resultado da IA moderno
    if isinstance(dados.get("resultado_ia"), dict):
        bruto = dados["resultado_ia"]
        if isinstance(bruto, dict) and "DFD" in bruto and isinstance(bruto["DFD"], dict):
            return bruto["DFD"]
        if isinstance(bruto, dict):
            return bruto

    # Caso 3 — objeto moderno já no nível raiz
    if isinstance(dados.get("DFD"), dict):
        return dados["DFD"]

    # Caso 4 — insumo puro com texto
    texto = dados.get("conteudo_textual")
    if isinstance(texto, str) and len(texto.strip()) > 20:
        origem = dados.get("origem", "insumo_raw")
        return _criar_dfd_basico_a_partir_de_insumo(texto, origem=origem)

    return {}


# ======================================================================
# 🔄 Obter DFD carregado (sessão → último arquivo → histórico)
# ======================================================================
def obter_dfd_da_sessao() -> dict:
    """
    Fonte de verdade para a página DFD:

      1) Se houver dfd_campos_ai na sessão → usa.
      2) Caso contrário, tenta ler exports/insumos/json/DFD_ultimo.json.
      3) Se ainda não houver, varre o histórico DFD_*.json.
    """

    # 1) Sessão
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # 2) Último arquivo
    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    # 3) Histórico
    if os.path.exists(base):
        arquivos = sorted(
            glob.glob(os.path.join(base, "DFD_*.json")),
            key=os.path.getmtime,
            reverse=True,
        )
        for arq in arquivos:
            dados = _carregar_dfd_de_arquivo(arq)
            if dados:
                st.session_state["dfd_campos_ai"] = dados
                return dados

    return {}


# ======================================================================
# 💾 Salvar DFD consolidado
# ======================================================================
def salvar_dfd_em_json(campos: dict, origem: str = "formulario_dfd_moderno_streamlit") -> str:
    """
    Salva o DFD consolidado (preenchido via formulário) em:
      exports/insumos/json/DFD_ultimo.json
      exports/insumos/json/DFD_<timestamp>.json
    no formato:

      {
        "artefato": "DFD",
        "origem": "...",
        "campos_ai": { ... DFD moderno ... },
        "data_salvamento": "YYYY-MM-DD HH:MM:SS"
      }
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
# 🧾 Status exibido na página DFD
# ======================================================================
def status_dfd() -> str:
    """
    Mensagem amigável exibida no topo da página DFD.
    """

    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ DFD carregado automaticamente (sessão ativa)"

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        return "🗂️ DFD disponível a partir dos insumos processados"

    return "⚠️ Nenhum DFD disponível — envie um insumo pelo módulo INSUMOS."


# ======================================================================
# 🧠 IA → Gerar rascunho do DFD (VERSÃO FINAL COMPATÍVEL)
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:
    """
    Lê o insumo (ou DFD consolidado), extrai um texto-base
    e aciona o DocumentAgent(D3) para gerar um DFD moderno completo.

    Resultado:
      • Atualiza st.session_state["dfd_campos_ai"]
      • Retorna o dict com o DFD moderno
    """
    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("⚠️ Nenhum insumo encontrado para DFD (DFD_ultimo.json não existe).")
        return {}

    # 1) Leitura do arquivo
    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        st.error(f"❌ Falha ao ler insumo: {e}")
        return {}

    # 2) Extrair texto-base
    texto = _extrair_texto_base_para_ia(dados)
    if len(texto.strip()) < 20:
        st.error("⚠️ Texto insuficiente para geração automática do DFD pela IA.")
        return {}

    # 3) Chamada da IA
    try:
        from agents.document_agent import processar_dfd_com_ia

        bruto = processar_dfd_com_ia(texto)

        # unwrap padrão {"timestamp": "...", "resultado_ia": {...}}
        if isinstance(bruto, dict) and "resultado_ia" in bruto:
            bruto = bruto["resultado_ia"]

        # Se ainda vier no formato {"DFD": {...}}
        if isinstance(bruto, dict) and "DFD" in bruto and isinstance(bruto["DFD"], dict):
            dfd_final = bruto["DFD"]
        elif isinstance(bruto, dict):
            dfd_final = bruto
        else:
            st.error("❌ A IA não retornou um JSON estruturado de DFD.")
            return {}

        # 4) Persistência em sessão
        st.session_state["dfd_campos_ai"] = dfd_final
        return dfd_final

    except Exception as e:
        st.error(f"❌ Erro ao gerar DFD com IA: {e}")
        return {}
