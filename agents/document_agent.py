# ==========================================================
# agents/document_agent.py — VERSÃO 2025-D10 (ESTÁVEL)
# Totalmente compatível com AIClient (responses.create)
# ==========================================================

from __future__ import annotations

import json
from datetime import datetime
from utils.ai_client import AIClient


SECOES = [
    "Contexto Institucional",
    "Diagnóstico da Situação Atual",
    "Fundamentação da Necessidade",
    "Objetivos da Contratação",
    "Escopo Inicial da Demanda",
    "Resultados Esperados",
    "Benefícios Institucionais",
    "Justificativa Legal",
    "Riscos da Não Contratação",
    "Requisitos Mínimos",
    "Critérios de Sucesso",
]


class DocumentAgent:

    def __init__(self, artefato="DFD"):
        self.artefato = artefato
        self.ai = AIClient()

    # ==========================================================
    # Processamento principal
    # ==========================================================
    def generate(self, conteudo_base: str) -> dict:

        prompt = self._montar_prompt()

        resposta = self.ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="DFD",
        )

        # Se a IA retornou erro → propagar
        if "erro" in resposta:
            return resposta

        # Extração da raiz {"DFD": {...}}
        if "DFD" in resposta and isinstance(resposta["DFD"], dict):
            d = resposta["DFD"]
        else:
            d = resposta

        # Sanitização mínima
        d.setdefault("texto_narrativo", "")
        d.setdefault("secoes", {})
        d.setdefault("lacunas", [])
        d.setdefault("descricao_necessidade", "")
        d.setdefault("motivacao", "")
        d.setdefault("unidade_demandante", "")
        d.setdefault("responsavel", "")
        d.setdefault("prazo_estimado", "")
        d.setdefault("valor_estimado", "0,00")

        # Garantir 11 seções
        secoes = d.get("secoes", {})
        for s in SECOES:
            secoes.setdefault(s, "Conteúdo não identificado no documento.")
        d["secoes"] = secoes

        d["gerado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d["origem"] = "document_agent_D10"

        return d

    # ==========================================================
    # Prompt institucional
    # ==========================================================
    def _montar_prompt(self) -> str:
        return (
            "Você é o agente institucional do TJSP responsável por gerar um "
            "DFD completo, mesmo quando o texto fornecido é um ETP, TR, edital "
            "ou qualquer documento. "
            "Responda SOMENTE com JSON no formato:\n\n"
            "{\n"
            "  \"DFD\": {\n"
            "    \"unidade_demandante\": \"\",\n"
            "    \"responsavel\": \"\",\n"
            "    \"prazo_estimado\": \"\",\n"
            "    \"valor_estimado\": \"0,00\",\n"
            "    \"descricao_necessidade\": \"...\",\n"
            "    \"motivacao\": \"...\",\n"
            "    \"texto_narrativo\": \"...\",\n"
            "    \"secoes\": {\n"
            "      \"Contexto Institucional\": \"...\",\n"
            "      \"Diagnóstico da Situação Atual\": \"...\",\n"
            "      \"Fundamentação da Necessidade\": \"...\",\n"
            "      \"Objetivos da Contratação\": \"...\",\n"
            "      \"Escopo Inicial da Demanda\": \"...\",\n"
            "      \"Resultados Esperados\": \"...\",\n"
            "      \"Benefícios Institucionais\": \"...\",\n"
            "      \"Justificativa Legal\": \"...\",\n"
            "      \"Riscos da Não Contratação\": \"...\",\n"
            "      \"Requisitos Mínimos\": \"...\",\n"
            "      \"Critérios de Sucesso\": \"...\"\n"
            "    },\n"
            "    \"lacunas\": []\n"
            "  }\n"
            "}"
        )

# ==========================================================
# Função universal — chamada pelo integration_dfd
# ==========================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    """
    Wrapper universal utilizado pelo integration_dfd.
    Recebe texto puro e retorna:
        { "timestamp": "...", "resultado_ia": { ...DFD... } }
    """

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {
            "erro": "Conteúdo insuficiente para processamento IA.",
            "conteudo_recebido": conteudo_textual,
        }

    try:
        agente = DocumentAgent("DFD")
        resultado = agente.generate(conteudo_textual)

        # Se houve erro interno → propagar
        if isinstance(resultado, dict) and "erro" in resultado:
            return {
                "erro": resultado["erro"],
                "conteudo_recebido": conteudo_textual[:500],
            }

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resultado_ia": resultado,
        }

    except Exception as e:
        return {
            "erro": f"Falha ao gerar DFD universal: {e}",
            "conteudo_recebido": conteudo_textual[:500],
        }
