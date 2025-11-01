# ==========================================================
# utils/integration_insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Funções de integração entre o módulo INSUMOS e os módulos
# DFD / ETP / TR / EDITAL, com persistência em sessão e disco.
# ==========================================================

import os
import json
from datetime import datetime
from typing import Dict, Any
import streamlit as st

# ==========================================================
# 🔧 Diretórios de exportação
# ==========================================================
EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")
os.makedirs(EXPORTS_JSON_DIR, exist_ok=True)

# ==========================================================
# 🧩 Função auxiliar – Propagação direta via sessão
# ==========================================================
def _propagar_para_modulo(artefato: str, campos_ai: Dict[str, Any]):
    """Propaga campos processados para o módulo de destino via st.session_state."""
    chave = f"{artefato.lower()}_campos_ai"
    st.session_state[chave] = campos_ai
    st.session_state["last_insumo_destino"] = artefato
    st.toast(f"📤 Insumo {artefato} encaminhado com sucesso.", icon="✅")


# ==========================================================
# 💾 Salvamento persistente
# ==========================================================
def salvar_insumo_processado(artefato: str, descricao: str, campos_ai: Dict[str, Any]) -> bool:
    """
    Salva o insumo processado tanto na sessão quanto em disco (formato JSON).
    Estrutura padronizada e compatível com os módulos de destino.
    """
    try:
        dados_insumo = {
            "artefato": artefato,
            "descricao": descricao,
            "campos_ai": campos_ai if isinstance(campos_ai, dict) else {},
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # 🔹 Atualiza sessão
        chave_sessao = f"{artefato.lower()}_campos_ai"
        st.session_state[chave_sessao] = dados_insumo["campos_ai"]

        # 🔹 Persiste em disco
        nome_arquivo = f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        caminho = os.path.join(EXPORTS_JSON_DIR, nome_arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados_insumo, f, ensure_ascii=False, indent=2)

        st.success(f"✅ Insumo '{artefato}' processado e encaminhado com sucesso.")
        return True

    except Exception as e:
        st.error(f"Erro ao salvar insumo processado: {e}")
        return False


# ==========================================================
# 🧠 Processamento principal do insumo
# ==========================================================
def processar_insumo(uploaded_file, artefato: str = "EDITAL") -> Dict[str, Any]:
    """
    Processa o arquivo enviado no módulo INSUMOS e identifica
    campos relevantes para os módulos DFD, ETP, TR ou EDITAL.
    """
    artefato = (artefato or "EDITAL").upper()

    try:
        # 🔹 Lê o conteúdo do arquivo de forma segura (UTF-8)
        conteudo = uploaded_file.getvalue()
        texto = conteudo.decode("utf-8", errors="ignore")

        # ==========================================================
        # 🔍 Simulação de extração semântica (substituir por IA real)
        # ==========================================================
        campos_norm = {
            "objeto": f"Objeto identificado a partir do insumo '{uploaded_file.name}'",
            "unidade_solicitante": "Departamento de Administração e Planejamento",
            "responsavel_tecnico": "Responsável Institucional (IA)",
            "justificativa_tecnica": "Justificativa técnica preliminar extraída automaticamente.",
            "criterios_julgamento": "Menor preço global.",
            "riscos": "Risco operacional moderado.",
            "prazo_execucao": "90 dias",
            "estimativa_valor": "R$ 150.000,00",
            "fonte_recurso": "Orçamento ordinário TJSP",
        }

        # ==========================================================
        # 🧱 Estrutura padronizada do payload
        # ==========================================================
        payload = {
            "nome_arquivo": uploaded_file.name,
            "artefato": artefato,
            "texto": texto[:5000],
            "campos_ai": campos_norm,
        }

        # ==========================================================
        # 💾 Persistência
        # ==========================================================
        salvar_insumo_processado(
            artefato=artefato,
            descricao=f"Insumo {uploaded_file.name} processado automaticamente",
            campos_ai=campos_norm
        )

        # ==========================================================
        # 🔁 Propagação imediata (para preenchimento ao vivo)
        # ==========================================================
        _propagar_para_modulo(artefato, campos_norm)

        return payload

    except Exception as e:
        st.error(f"Erro ao processar insumo: {e}")
        return {}


# ==========================================================
# 🧾 Função de exportação manual (caso necessário)
# ==========================================================
def exportar_insumo_manual(artefato: str, campos_ai: Dict[str, Any]) -> str:
    """
    Exporta um insumo manualmente para testes ou auditoria.
    Retorna o caminho completo do arquivo JSON gerado.
    """
    try:
        dados = {
            "artefato": artefato,
            "campos_ai": campos_ai,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        nome_arquivo = f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        caminho = os.path.join(EXPORTS_JSON_DIR, nome_arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return caminho
    except Exception as e:
        st.error(f"Erro ao exportar insumo manual: {e}")
        return ""
