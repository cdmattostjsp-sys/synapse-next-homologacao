# ==========================================================
# utils/integration_etp.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Integração entre o processamento de INSUMOS e o módulo ETP.
# Recupera automaticamente dados da sessão ativa ou do último JSON salvo.
# Compatível com o motor IA institucional v3 e persistência híbrida.
# ==========================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime


# ==========================================================
# 🔧 Fallback: construir campos básicos a partir de conteudo_textual
# ==========================================================
def _construir_campos_basicos_a_partir_do_texto(texto: str) -> dict:
    """
    Quando não houver 'campos_ai' nem 'campos' no JSON de insumo,
    usamos o texto bruto como ponto de partida para pré-preencher o formulário.

    Estratégia simples (mas funcional):
      - requisitos  <- texto completo
      - custos      <- vazio
      - riscos      <- vazio
      - responsavel_tecnico <- vazio

    Isso permite demonstrar a viabilidade do sistema:
    o usuário já recebe o formulário preenchido com o texto do ETP,
    e pode editar/refinar, além de acionar a IA institucional depois.
    """
    texto = (texto or "").strip()
    if not texto:
        return {}

    return {
        "requisitos": texto,
        "custos": "",
        "riscos": "",
        "responsavel_tecnico": "",
    }


# ==========================================================
# 🧠 Função principal – obter ETP ativo
# ==========================================================
def obter_etp_da_sessao() -> dict:
    """
    Recupera o dicionário de campos do ETP ativo.

    Prioridades:
    1️⃣ st.session_state["etp_campos_ai"]
    2️⃣ exports/insumos/json/ETP_ultimo.json
    3️⃣ Último arquivo ETP_*.json no diretório de insumos
    4️⃣ Fallback: usar 'conteudo_textual' do insumo bruto
    """

    # 1️⃣ Sessão ativa
    if "etp_campos_ai" in st.session_state and st.session_state["etp_campos_ai"]:
        return st.session_state["etp_campos_ai"]

    # Diretório base
    base_dir = os.path.join("exports", "insumos", "json")
    ultimo_json = os.path.join(base_dir, "ETP_ultimo.json")

    # 2️⃣ Último insumo salvo (ETP_ultimo.json)
    if os.path.exists(ultimo_json):
        try:
            with open(ultimo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)

            # Caso já exista estrutura consolidada
            campos = dados.get("campos_ai") or dados.get("campos")
            if isinstance(campos, dict) and campos:
                st.session_state["etp_campos_ai"] = campos
                return campos

            # Fallback: usar conteudo_textual do insumo bruto
            texto = (dados.get("conteudo_textual") or "").strip()
            if texto:
                campos_fallback = _construir_campos_basicos_a_partir_do_texto(texto)
                if campos_fallback:
                    st.session_state["etp_campos_ai"] = campos_fallback
                    return campos_fallback

        except Exception as e:
            st.warning(f"⚠️ Falha ao ler ETP_ultimo.json: {e}")

    # 3️⃣ Busca o arquivo mais recente (fallback final)
    try:
        arquivos = sorted(
            glob.glob(os.path.join(base_dir, "ETP_*.json")),
            key=os.path.getmtime,
            reverse=True,
        )
        for arquivo in arquivos:
            if "ETP_ultimo.json" in arquivo:
                continue
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)

                campos = dados.get("campos_ai") or dados.get("campos")
                if isinstance(campos, dict) and campos:
                    st.session_state["etp_campos_ai"] = campos
                    return campos

                texto = (dados.get("conteudo_textual") or "").strip()
                if texto:
                    campos_fallback = _construir_campos_basicos_a_partir_do_texto(texto)
                    if campos_fallback:
                        st.session_state["etp_campos_ai"] = campos_fallback
                        return campos_fallback

            except Exception:
                # Se der erro em um arquivo, tenta o próximo
                continue

    except Exception as e:
        st.warning(f"⚠️ Nenhum ETP válido encontrado ({e})")

    # 4️⃣ Fallback seguro
    return {}


# ==========================================================
# 💾 Função auxiliar – salvar ETP gerado pelo formulário
# ==========================================================
def salvar_etp_em_json(campos_etp: dict, origem: str = "formulario") -> str:
    """
    Salva o conteúdo atual do formulário ETP em /exports/insumos/json.
    Utilizado tanto para IA quanto para preenchimento manual.
    """
    base_dir = os.path.join("exports", "insumos", "json")
    os.makedirs(base_dir, exist_ok=True)

    payload = {
        "artefato": "ETP",
        "origem": origem,
        "campos_ai": campos_etp,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arquivo_ultimo = os.path.join(base_dir, "ETP_ultimo.json")
    arquivo_timestamp = os.path.join(base_dir, f"ETP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arquivo_ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        with open(arquivo_timestamp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        st.session_state["etp_campos_ai"] = campos_etp
        return arquivo_ultimo
    except Exception as e:
        st.warning(f"⚠️ Falha ao salvar ETP: {e}")
        return ""


# ==========================================================
# 🧠 IA → Gerar ETP estruturado (preserva dados existentes)
# ==========================================================
def gerar_etp_com_ia() -> dict:
    """
    Enriquece o ETP existente com processamento IA.
    PRESERVA os dados brutos já extraídos do insumo.
    """
    
    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "ETP_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("Nenhum insumo encontrado.")
        return {}

    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados_completos = json.load(f)
        
        # Preservar dados existentes
        dados_existentes = dados_completos.get("campos_ai", {})
        texto = (dados_completos.get("conteudo_textual") or "").strip()
        
    except Exception:
        st.error("Erro ao ler insumo.")
        return {}

    if len(texto) < 20:
        st.error("Texto insuficiente para IA.")
        return {}

    try:
        from agents.etp_agent import processar_etp_com_ia
        resultado_ia = processar_etp_com_ia(texto)

        # Verificar se houve erro
        if "erro" in resultado_ia:
            st.error(f"Erro na IA: {resultado_ia['erro']}")
            # Retornar dados existentes mesmo com erro
            return dados_existentes if dados_existentes else {}

        # Extrair resultado da IA
        bruto = resultado_ia.get("resultado_ia", {})
        
        if "ETP" in bruto and isinstance(bruto["ETP"], dict):
            bruto = bruto["ETP"]

        # MESCLAR dados existentes com resultado da IA
        # Dados da IA têm prioridade (mais estruturados)
        dados_finais = {}
        
        # Primeiro: dados existentes como base
        if isinstance(dados_existentes, dict):
            dados_finais.update(dados_existentes)
        
        # Segundo: sobrescrever com dados da IA (mais estruturados)
        if isinstance(bruto, dict):
            # Campos administrativos
            for campo in ["unidade_demandante", "responsavel", "prazo_estimado", "valor_estimado"]:
                if campo in bruto and bruto[campo] and bruto[campo] not in ["", "Não especificado", "0,00"]:
                    dados_finais[campo] = bruto[campo]
            
            # Seções estruturadas
            if "secoes" in bruto and isinstance(bruto["secoes"], dict):
                if "secoes" not in dados_finais:
                    dados_finais["secoes"] = {}
                dados_finais["secoes"].update(bruto["secoes"])
            
            # Lacunas
            if "lacunas" in bruto:
                dados_finais["lacunas"] = bruto["lacunas"]

        st.session_state["etp_campos_ai"] = dados_finais
        return dados_finais

    except Exception as e:
        st.error(f"Erro IA: {e}")
        # Retornar dados existentes em caso de erro
        return dados_existentes if dados_existentes else {}


# ==========================================================
# 🧩 Função utilitária – status legível
# ==========================================================
def status_etp():
    """Retorna uma string de status para exibição no topo do módulo ETP."""
    if "etp_campos_ai" in st.session_state and st.session_state["etp_campos_ai"]:
        return "✅ Dados carregados automaticamente (sessão ativa ou JSON)."

    base_dir = os.path.join("exports", "insumos", "json")
    if os.path.exists(os.path.join(base_dir, "ETP_ultimo.json")):
        return "🗂️ Dados disponíveis no último processamento de INSUMOS."

    return "⚠️ Nenhum ETP ativo encontrado – envie um insumo em '🔧 Insumos'."
