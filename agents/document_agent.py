# ==========================================================
# utils/document_agent.py
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

            # Limpeza de delimitadores Markdown (```json ... ```)
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
                "- Unidade Demandante (órgão ou setor responsável pela solicitação)\n"
                "- Responsável pela Demanda (nome e cargo do solicitante institucional)\n"
                "- Prazo Estimado para Atendimento (mês/ano ou período estratégico)\n"
                "- Descrição da Necessidade (contextualize a situação ou problema identificado)\n"
                "- Motivação / Objetivos Estratégicos (relacione com o Planejamento Estratégico 2021–2026)\n"
                "- Estimativa de Valor (informe se disponível ou mantenha 0,00)\n"
                "- Justificativa Legal (artigos aplicáveis da Lei 14.133/2021)\n"
                "- Escopo (principais entregas, produtos ou serviços)\n"
                "- Resultados Esperados (efeitos esperados após a execução)\n"
                "- Critérios de Sucesso (como o resultado será medido)\n\n"
                "🧾 Regras de redação:\n"
                "1. Use linguagem formal, impessoal e técnica.\n"
                "2. Mantenha coerência com o texto original do insumo (PDF processado).\n"
                "3. Evite repetir trechos ou incluir instruções do usuário.\n"
                "4. Gere a resposta **em formato JSON** com a estrutura:\n\n"
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
                "```\n\n"
                "Responda apenas com o JSON final, sem texto adicional."
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
