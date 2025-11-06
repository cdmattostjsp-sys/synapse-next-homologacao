# ==========================================================
# utils/integration_ai_engine_new.py
# SynapseNext – Motor Institucional de IA (v3)
# Revisão: Engenheiro Synapse – 2025-11-06 (versão final – Streamlit Cloud)
# ==========================================================

from __future__ import annotations
import json
from utils.ai_client import AIClient

# ==========================================================
# 🧠 Função principal – processar_insumo
# ==========================================================
def processar_insumo(uploaded_file, artefato: str) -> dict:
    """
    Processa um arquivo de insumo via motor IA institucional SynapseNext (v3).
    Compatível com objetos do tipo streamlit.UploadedFile.
    Gera saída padronizada com 'campos' e 'lacunas' para os módulos DFD/ETP/TR/Edital.
    """

    try:
        # ✅ Leitura segura do conteúdo (UploadedFile → texto)
        if hasattr(uploaded_file, "read"):
            conteudo_bytes = uploaded_file.read()
            if isinstance(conteudo_bytes, bytes):
                conteudo = conteudo_bytes.decode("utf-8", errors="ignore")
            else:
                conteudo = str(conteudo_bytes)
        else:
            return {"erro": "Arquivo inválido ou corrompido."}

        # ✅ Inicializa o cliente institucional de IA
        client = AIClient()

        # ==========================================================
        # 🧩 PROMPT INSTITUCIONAL – SynapseNext v3
        # ==========================================================
        prompt = f"""
        Você é o motor institucional de análise documental do Tribunal de Justiça de São Paulo.
        Analise o texto a seguir, identificado como artefato administrativo do tipo: {artefato}.

        Extraia os seguintes elementos (se existirem):
        - objeto: descrição resumida da demanda;
        - justificativa: motivos técnicos e administrativos;
        - prazo_execucao: período de execução, duração ou data limite;
        - setor_demandante: unidade solicitante ou origem da requisição.

        Retorne a resposta em JSON **válido e bem formatado**, seguindo este modelo:
        {{
            "modulo": "{artefato}",
            "campos": {{
                "objeto": "...",
                "justificativa": "...",
                "prazo_execucao": "...",
                "setor_demandante": "..."
            }},
            "lacunas": ["nome_do_campo_faltante_1", ...]
        }}

        Se algum campo não puder ser inferido, inclua-o dentro de "lacunas".
        """

        # ==========================================================
        # 🔗 Chamada segura ao cliente institucional
        # ==========================================================
        resposta_raw = client.ask(prompt=prompt, conteudo=conteudo, artefato=artefato)

        # Tenta interpretar a resposta como JSON (fallback se for texto)
        try:
            resposta_json = json.loads(resposta_raw) if isinstance(resposta_raw, str) else resposta_raw
        except Exception:
            resposta_json = {"resposta_bruta": resposta_raw}

        # ==========================================================
        # 🧱 Retorno padronizado para integração DFD / ETP / TR / Edital
        # ==========================================================
        return {
            "modulo": artefato,
            "campos": resposta_json.get("campos", {}),
            "lacunas": resposta_json.get("lacunas", []),
            "inferido_de": {
                "arquivo": getattr(uploaded_file, "name", "sem_nome"),
                "bytes": isinstance(conteudo_bytes, bytes),
            },
        }

    except Exception as e:
        return {"erro": f"Falha no processamento IA: {e}"}
