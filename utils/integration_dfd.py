# ==========================================================
# utils/integration_dfd.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão Engenheiro Synapse – vNext_2025.11.09 (Patch IA JSON)
# Compatibilidade: Streamlit 1.39.0 + openai 2.7.1
# ==========================================================

import json
import re
from pathlib import Path
import streamlit as st
from utils.ai_client import AIClient  # ✅ Cliente institucional padronizado


# ==========================================================
# 📁 Localização de arquivos
# ==========================================================
def get_possible_dfd_paths() -> list[Path]:
    """
    Retorna os caminhos possíveis onde o DFD_ultimo.json pode estar.
    Inclui tanto o modo persistente (exports) quanto o temporário (/tmp).
    """
    return [
        Path("exports/insumos/json/DFD_ultimo.json"),
        Path("/tmp/insumos/json/DFD_ultimo.json"),
    ]


# ==========================================================
# 🔍 Carregar DFD existente
# ==========================================================
def obter_dfd_da_sessao():
    """
    Tenta carregar o último DFD gerado.
    Verifica tanto exports/insumos/json quanto /tmp/insumos/json.
    """
    try:
        for caminho in get_possible_dfd_paths():
            if caminho.exists():
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                print(f"[SynapseNext][DFD] Dados importados de {caminho}")
                return dados

        print("[SynapseNext][DFD] Nenhum DFD encontrado em diretórios padrão.")
        return None

    except Exception as e:
        print(f"[ERRO][DFD] Falha ao carregar DFD: {e}")
        return None


# ==========================================================
# 💾 Salvar manualmente um DFD (opcional)
# ==========================================================
def salvar_dfd_manual(dados: dict, nome_arquivo: str = "DFD_ultimo.json"):
    """
    Salva o DFD consolidado tanto em exports quanto em /tmp (fallback).
    """
    try:
        for base in [Path("exports/insumos/json"), Path("/tmp/insumos/json")]:
            try:
                base.mkdir(parents=True, exist_ok=True)
                destino = base / nome_arquivo
                with open(destino, "w", encoding="utf-8") as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                print(f"[SynapseNext][DFD] Arquivo salvo com sucesso em: {destino}")
                return destino
            except Exception:
                continue

        print("[ERRO][DFD] Nenhum diretório disponível para salvar.")
        return None

    except Exception as e:
        print(f"[ERRO][DFD] Falha ao salvar DFD manualmente: {e}")
        return None


# ==========================================================
# 🧠 Geração do rascunho com IA institucional (versão estável)
# ==========================================================
def gerar_rascunho_dfd_com_ia():
    """
    Reaproveita o DFD_ultimo.json existente para gerar o rascunho com IA institucional.
    - Se o JSON já contiver resultado da IA, reutiliza.
    - Caso contrário, processa o texto extraído e atualiza o arquivo.
    - Faz o parse automático do campo 'resposta_texto' quando vier em formato Markdown JSON.
    """
    try:
        dfd_data = obter_dfd_da_sessao()
        if not dfd_data:
            st.warning("⚠️ Nenhum insumo DFD encontrado. Envie primeiro um documento no módulo 'Insumos'.")
            return None

        # ✅ 1. Reutiliza resultado existente (caso já tenha vindo da IA)
        if "resultado_ia" in dfd_data and dfd_data["resultado_ia"].get("resposta_texto"):
            texto_raw = dfd_data["resultado_ia"]["resposta_texto"]

            # --- Novo tratamento: extrair JSON de blocos markdown
            cleaned = re.sub(r"^```json|```$", "", texto_raw.strip(), flags=re.IGNORECASE).strip()

            try:
                parsed_json = json.loads(cleaned)
                print("[SynapseNext][DFD] Resposta IA convertida de Markdown JSON para objeto válido.")
                return parsed_json
            except Exception:
                print("[SynapseNext][DFD] Resposta IA mantida como texto (não pôde ser convertida).")
                return texto_raw

        # ✅ 2. Caso contrário, reprocessa com a IA institucional
        texto_base = dfd_data.get("texto_extraido", "")
        if not texto_base.strip():
            st.warning("⚠️ O insumo DFD não contém texto extraído válido.")
            return None

        st.info("🧠 Executando agente DFD institucional com base no insumo processado...")

        ai = AIClient()
        prompt = (
            "Analise o texto do Documento de Formalização de Demanda (DFD) "
            "e gere um rascunho JSON estruturado com os seguintes campos: "
            "Unidade Demandante, Descrição da Necessidade, Responsável, "
            "Motivação / Objetivos Estratégicos e Prazo Estimado para Atendimento."
        )

        resposta_ia = ai.ask(prompt=prompt, conteudo=texto_base, artefato="DFD")

        if not resposta_ia or not resposta_ia.get("resposta_texto"):
            st.warning("⚠️ A IA não retornou um rascunho válido.")
            return None

        # ✅ 3. Atualiza o JSON e salva novamente
        dfd_data["resultado_ia"] = resposta_ia
        salvar_dfd_manual(dfd_data)

        st.success("✅ Rascunho do DFD gerado e armazenado com sucesso.")
        return resposta_ia["resposta_texto"]

    except Exception as e:
        st.error(f"❌ Erro ao gerar rascunho com IA institucional: {e}")
        print(f"[ERRO][DFD] {e}")
        return None


# ==========================================================
# 🌐 Exibição no Streamlit (uso direto)
# ==========================================================
def exibir_dfd_em_pagina():
    """
    Exibe o conteúdo atual do DFD_ultimo.json na interface Streamlit.
    """
    dados = obter_dfd_da_sessao()

    if not dados:
        st.warning("⚠️ Nenhum DFD encontrado. Gere um insumo primeiro na página 'Insumos'.")
        return

    st.success("✅ DFD carregado com sucesso!")
    st.json(dados)

# ==========================================================
# 💾 Salvar DFD automaticamente (usado pelo módulo DFD)
# ==========================================================
def salvar_dfd_em_json(dados: dict):
    """
    Salva sempre como DFD_ultimo.json nos diretórios oficiais do pipeline.
    Compatível com Insumos → DFD → ETP → TR.
    """
    try:
        nome_arquivo = "DFD_ultimo.json"

        for base in [Path("exports/insumos/json"), Path("/tmp/insumos/json")]:
            try:
                base.mkdir(parents=True, exist_ok=True)
                destino = base / nome_arquivo
                with open(destino, "w", encoding="utf-8") as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                print(f"[SynapseNext][DFD] Arquivo atualizado em: {destino}")
            except Exception:
                continue

        return True

    except Exception as e:
        print(f"[ERRO][DFD] Falha ao salvar DFD (salvar_dfd_em_json): {e}")
        return False
