# ==========================================================
# utils/dfd/integration_dfd.py — VERSÃO ESTÁVEL 2025
# Compatível com novo fluxo do módulo INSUMOS + DFD
# ==========================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime


# ----------------------------------------------------------
# 🔧 Remover blocos de markdown de IA (```json)
# ----------------------------------------------------------
def _limpar_markdown(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    return texto.replace("```json", "").replace("```", "").strip()


# ----------------------------------------------------------
# 📥 Carregar arquivo JSON bruto de insumo ou DFD salvo
# ----------------------------------------------------------
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    """
    Interpreta diferentes formatos de DFD / insumo:

    1) Arquivo já consolidado pelo formulário:
       {
         "artefato": "DFD",
         "origem": "...",
         "campos_ai": { ...campos do DFD... }
       }

    2) Arquivo gerado pela IA (processar_dfd_com_ia):
       {
         "timestamp": "...",
         "resultado_ia": { "DFD": {...} }  OU  { ... }
       }

    3) Arquivo puro do módulo INSUMOS (texto OCR):
       {
         "arquivo": "...",
         "tipo": "pdf|docx|txt",
         "conteudo_textual": "texto integral...",
         "data_processamento": "..."
       }
    """
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Não foi possível ler {caminho}: {e}")
        return {}

    # 1️⃣ DFD já consolidado (salvo pelo formulário)
    if isinstance(dados.get("campos_ai"), dict):
        return dados["campos_ai"]

    # 2️⃣ Resposta da IA (processar_dfd_com_ia)
    if isinstance(dados.get("resultado_ia"), dict):
        r = dados["resultado_ia"]

        # Se vier no formato {"DFD": {...}}
        if isinstance(r, dict):
            if "DFD" in r and isinstance(r["DFD"], dict):
                return r["DFD"]
            return r

    # 3️⃣ INSUMO puro com texto OCR
    texto = dados.get("conteudo_textual")

    if isinstance(texto, str) and len(texto.strip()) > 10:
        texto_limpo = texto.strip()

        # ⚠️ IMPORTANTE:
        # Aqui já devolvemos num formato que o formulário entende,
        # preenchendo diretamente "descricao_necessidade" e deixando
        # os demais campos em branco para edição manual.
        return {
            "unidade_demandante": "",
            "responsavel": "",
            "prazo_estimado": "",
            "descricao_necessidade": texto_limpo,
            "motivacao": "",
            "valor_estimado": "0,00",
        }

    # Caso não seja nenhum dos formatos conhecidos
    return {}


# ----------------------------------------------------------
# 🔄 Obter DFD carregado (sessão / arquivos)
# ----------------------------------------------------------
def obter_dfd_da_sessao() -> dict:
    """
    Prioridade:
      1) Dados já carregados na sessão (dfd_campos_ai)
      2) Arquivo exports/insumos/json/DFD_ultimo.json
      3) Arquivos mais antigos DFD_*.json
    """

    # 1️⃣ Sessão já tem DFD carregado
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # 2️⃣ Carregamento direto do último arquivo
    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    # 3️⃣ Busca arquivos antigos DFD_*.json (backup / histórico)
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


# ----------------------------------------------------------
# 💾 Salvar DFD consolidado
# ----------------------------------------------------------
def salvar_dfd_em_json(campos_dfd: dict, origem: str = "formulario") -> str:
    """
    Salva o DFD consolidado (formulário) em:
      - exports/insumos/json/DFD_ultimo.json
      - exports/insumos/json/DFD_YYYYMMDD_HHMMSS.json
    """
    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    payload = {
        "artefato": "DFD",
        "origem": origem,
        "campos_ai": campos_dfd,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arq1 = os.path.join(base, "DFD_ultimo.json")
    arq2 = os.path.join(base, f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arq1, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arq2, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        # Atualiza sessão com o DFD consolidado
        st.session_state["dfd_campos_ai"] = campos_dfd

        return arq1

    except Exception as e:
        st.error(f"❌ Falha ao salvar DFD: {e}")
        return ""


# ----------------------------------------------------------
# 🧾 Status do DFD (mensagem exibida no topo da página)
# ----------------------------------------------------------
def status_dfd() -> str:
    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ DFD carregado automaticamente (sessão ativa)"

    if os.path.exists(ultimo):
        return "🗂️ DFD disponível a partir dos insumos processados"

    return "⚠️ Nenhum DFD disponível — envie um insumo pelo módulo INSUMOS."


# ----------------------------------------------------------
# 🧠 Chamada ao Agente IA – gerar rascunho estruturado
# ----------------------------------------------------------
def gerar_rascunho_dfd_com_ia() -> dict:
    """
    Usa o texto bruto do último insumo para gerar um DFD estruturado via IA.
    Não sobrescreve insumo; apenas atualiza a sessão.
    """

    # Caminho correto do insumo
    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # Caso não exista arquivo de insumo
    if not os.path.exists(ultimo):
        st.warning("⚠️ Nenhum insumo encontrado para gerar o DFD pela IA.")
        return {}

    # 🔥 LEITURA CORRETA DO TEXTO BRUTO
    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # PONTO CRÍTICO CORRIGIDO:
        # Sempre usa conteudo_textual, nunca outra chave.
        texto = (dados.get("conteudo_textual") or "").strip()

    except Exception:
        st.error("❌ Falha ao ler o insumo para a IA.")
        return {}

    if len(texto) < 20:
        st.error("⚠️ Texto insuficiente para processamento pela IA.")
        return {}

    # -------------------------------------------------------
    # 🧠 Execução da IA (apenas este trecho chama o agente)
    # -------------------------------------------------------
    try:
        from agents.document_agent import processar_dfd_com_ia

        resposta = processar_dfd_com_ia(texto)

        # Normaliza saída:
        if isinstance(resposta, dict) and "resultado_ia" in resposta:
            r = resposta["resultado_ia"]
        else:
            r = resposta

        # Caso a IA retorne {"DFD": {...}}
        if isinstance(r, dict):
            dfd_struct = r.get("DFD", r)
        else:
            dfd_struct = {}

        if not dfd_struct:
            st.warning("⚠️ A IA não retornou um DFD estruturado.")
            return {}

        # Atualiza sessão
        st.session_state["dfd_campos_ai"] = dfd_struct

        return dfd_struct

    except Exception as e:
        st.error(f"❌ Erro ao executar IA para o DFD: {e}")
        return {}
