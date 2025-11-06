# ==========================================================
# utils/integration_ai_engine_new.py
# SynapseNext – Motor Institucional de IA (v3)
# Revisão: Engenheiro Synapse – 2025-11-05 (versão corrigida)
# ==========================================================

from __future__ import annotations
import json
from utils.ai_client import AIClient

# ==========================================================
# 🧠 Função principal – processar_insumo
# ==========================================================
def processar_insumo(uploaded_file, artefato: str) -> dict:
    """
    Processa um arquivo de insumo via motor IA institucional.
    Compatível com objetos do tipo streamlit.UploadedFile.
    """

    try:
        # ✅ Leitura segura do conteúdo enviado via Streamlit
        if hasattr(uploaded_file, "read"):
            conteudo = uploaded_file.read()
            if isinstance(conteudo, bytes):
                conteudo = conteudo.decode("utf-8", errors="ignore")
        else:
            return {"erro": "Arquivo inválido ou corrompido."}

        # ✅ Inicializa o cliente IA institucional
        client = AIClient()

        # ✅ Prompt institucional padronizado
        prompt = (
            f"Analise o seguinte documento administrativo e gere um resumo estruturado "
            f"para o módulo {artefato}. Responda em formato JSON válido e bem formado."
        )

        # ✅ Chamada segura à API OpenAI encapsulada
        resposta = client.ask(prompt=prompt, conteudo=conteudo, artefato=artefato)

        # ✅ Retorno padronizado para leitura pelos módulos DFD/ETP/TR/Edital
        return {
            "artefato": artefato,
            "arquivo": getattr(uploaded_file, 'name', 'sem_nome'),
            "campos_ai": resposta,
        }

    except Exception as e:
        return {"erro": str(e)}
