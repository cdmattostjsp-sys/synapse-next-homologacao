# ==========================================================
# agents/document_agent.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: 2025-11-10 – Engenheiro Synapse
# ==========================================================
# Função: Controla a geração de documentos administrativos
# via IA institucional (v3) – compatível com AIClient.ask()
# ==========================================================

from __future__ import annotations
import json
import re
from datetime import datetime
from utils.ai_client import AIClient


class DocumentAgent:
    """
    Agente responsável por coordenar a geração de documentos
    formais (DFD, ETP, TR, Edital, etc.) via IA institucional.
    """

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()

    # ======================================================
    # 🧠 Geração de conteúdo IA
    # ======================================================
    def generate(self, conteudo_base: str, contexto_extra: dict | None = None) -> dict:
        """
        Gera o documento com base no texto processado (ex: PDF de insumo).
        Retorna um dicionário JSON estruturado.
        """

        prompt = self._montar_prompt_institucional()

        metadata = {
            "artefato": self.artefato,
            "contexto_extra": contexto_extra or {},
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        try:
            resposta = self.ai.ask(
                prompt=prompt,
                conteudo=conteudo_base,
                artefato=self.artefato,
                metadados=metadata,
            )

            if not resposta or not isinstance(resposta, dict):
                return {"erro": "Resposta IA inválida ou vazia."}

            texto_bruto = resposta.get("resposta_texto", "")
            if not texto_bruto:
                return {"erro": "IA não retornou conteúdo textual."}

            # Limpeza de delimitadores Markdown (```json ... ```).
            texto_bruto = texto_bruto.strip()
            if texto_bruto.startswith("```json"):
                texto_bruto = texto_bruto.replace("```json", "").replace("```", "").strip()

            # Tenta interpretar JSON
            try:
                parsed = json.loads(texto_bruto)
                if isinstance(parsed, dict) and "DFD" in parsed:
                    parsed = parsed["DFD"]
                return parsed
            except Exception:
                # Conteúdo não estruturado → devolve como texto
                return {"Conteúdo": texto_bruto}

        except Exception as e:
            return {"erro": f"Falha na geração do documento ({e})"}

    # ======================================================
    # 🧩 Prompt institucional aprimorado
    # ======================================================
    def _montar_prompt_institucional(self) -> str:
        """
        Monta um prompt administrativo institucional completo
        com linguagem formal e estrutura padronizada do TJSP.
        """

        if self.artefato == "DFD":
            return (
                "Você é um assistente técnico da Secretaria de Administração e Abastecimento do "
                "Tribunal de Justiça do Estado de São Paulo (TJSP). "
                "Com base no texto fornecido, elabore o documento **Formalização da Demanda (DFD)** "
                "conforme os padrões administrativos e a Lei nº 14.133/2021.\n\n"
                "O DFD deve conter os seguintes campos obrigatórios:\n"
                "- Unidade Demandante\n"
                "- Responsável pela Demanda\n"
                "- Prazo Estimado\n"
                "- Descrição da Necessidade\n"
                "- Motivação / Objetivos Estratégicos\n"
                "- Estimativa de Valor\n"
                "- Justificativa Legal\n"
                "- Escopo\n"
                "- Resultados Esperados\n"
                "- Critérios de Sucesso\n\n"
                "🧾 Regras de redação:\n"
                "1. Linguagem formal e técnica.\n"
                "2. Coerência com o insumo original.\n"
                "3. Responder apenas com JSON no formato:\n\n"
                "```json\n"
                "{\n"
                "  \"DFD\": {\n"
                "    \"secoes\": {\n"
                "      \"Contexto\": \"...\",\n"
                "      \"Necessidade\": \"...\",\n"
                "      \"Resultados Esperados\": \"...\",\n"
                "      \"Justificativa Legal\": \"...\",\n"
                "      \"Escopo\": \"...\",\n"
                "      \"Critérios de Sucesso\": \"...\"\n"
                "    },\n"
                "    \"lacunas\": [\"unidade\", \"responsavel\", \"prazo\", \"estimativa_valor\"]\n"
                "  }\n"
                "}\n"
                "```\n"
                "Sem texto adicional."
            )

        # ======================================================
        # Modelos futuros (ETP, TR, etc.)
        # ======================================================
        else:
            return (
                f"Você é um assistente técnico do Tribunal de Justiça de São Paulo. "
                f"Elabore o documento institucional correspondente ao artefato {self.artefato} "
                "seguindo linguagem formal e formato JSON padronizado."
            )


# ======================================================
# 🔌 FUNÇÃO PÚBLICA PARA O PIPELINE — **ESSENCIAL**
# ======================================================

def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    """
    Função utilizada pelo pipeline DFD.

    - Recebe o texto processado dos insumos (OCR/PDF/Upload)
    - Envia para o agente de documentos
    - Retorna o JSON estruturado da IA
    """

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}

    agente = DocumentAgent("DFD")
    resultado = agente.generate(conteudo_textual)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resultado_ia": resultado,
    }
