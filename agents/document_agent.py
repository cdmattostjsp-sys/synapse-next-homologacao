# ==========================================================
# agents/document_agent.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: 2025-11-18 – Compatível com AIClient atual (vNext)
# ==========================================================
# Função:
#   Controla a geração de documentos administrativos
#   (DFD, ETP, TR, Edital...) utilizando o AIClient padronizado.
# ==========================================================

from __future__ import annotations
import json
from datetime import datetime
from utils.ai_client import AIClient


class DocumentAgent:
    """
    Agente responsável por coordenar a geração de documentos
    formais via IA institucional (DFD, ETP, TR, Edital etc.).
    """

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()  # Instância do cliente IA institucional

    # ======================================================
    # 🧠 Geração de conteúdo IA
    # ======================================================
    def generate(self, conteudo_base: str) -> dict:
        """
        Gera o documento com base no texto processado (ex: PDF).
        Retorna um dicionário JSON estruturado.
        """

        prompt = self._montar_prompt_institucional()

        try:
            # -----------------------------------------------------
            # 🔥 CHAMADA ALINHADA AO AIClient ATUAL
            # (não suporta: metadados)
            # -----------------------------------------------------
            resposta = self.ai.ask(
                prompt=prompt,
                conteudo=conteudo_base,
                artefato=self.artefato
            )

            # Validação básica
            if not resposta or not isinstance(resposta, dict):
                return {"erro": "Resposta IA inválida ou vazia."}

            texto_bruto = resposta.get("resposta_texto", "")
            if not texto_bruto:
                return {"erro": "IA não retornou conteúdo textual."}

            # Limpeza de delimitadores Markdown
            texto_bruto = texto_bruto.strip()
            if texto_bruto.startswith("```json"):
                texto_bruto = (
                    texto_bruto
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            # -----------------------------------------------------
            # ⚙️ Tenta interpretar JSON estruturado retornado pela IA
            # -----------------------------------------------------
            try:
                parsed = json.loads(texto_bruto)

                # Se vier no formato {"DFD": {...}}
                if isinstance(parsed, dict) and "DFD" in parsed:
                    return parsed["DFD"]

                return parsed

            except Exception:
                # Conteúdo não era JSON → retorna como texto bruto
                return {"Conteúdo": texto_bruto}

        except Exception as e:
            return {"erro": f"Falha na geração do documento ({e})"}

    # ======================================================
    # 🧩 Prompt institucional padronizado (REVISADO)
    # ======================================================
    def _montar_prompt_institucional(self) -> str:
        """
        Monta um prompt formal com orientações administrativas.
        """

        # ======================================================
        # 📌 PROMPT REVISADO — DFD COMPLETO E ROBUSTO
        # ======================================================
        if self.artefato == "DFD":
            return (
                "Você é um assistente técnico da Secretaria de Administração e Abastecimento "
                "do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                "Com base no texto fornecido (insumo), elabore o documento "
                "Formalização da Demanda (DFD), seguindo os padrões administrativos "
                "do TJSP e a Lei nº 14.133/2021.\n\n"

                "Sua resposta deve ser um documento completo, detalhado e consistente, "
                "organizado nas seções previstas no DFD institucional.\n\n"

                "=== SEÇÕES OBRIGATÓRIAS DO DFD ===\n"
                "As seguintes seções DEVEM estar presentes e totalmente preenchidas:\n"
                "- Contexto: explique claramente a situação atual, o problema existente e o cenário institucional.\n"
                "- Necessidade: descreva o que motivou a demanda, relacionando com o interesse público.\n"
                "- Resultados Esperados: indique os efeitos concretos e mensuráveis esperados com a contratação.\n"
                "- Justificativa Legal: fundamente a contratação de maneira institucional, "
                "relacionando com a Lei nº 14.133/2021.\n"
                "- Escopo: delimite o objeto pretendido, descrevendo o que será entregue e o que está excluído.\n"
                "- Critérios de Sucesso: apresente critérios claros e verificáveis para mensurar o atendimento dos objetivos.\n\n"

                "=== REGRAS ADMINISTRATIVAS ===\n"
                "1. Linguagem formal, impessoal e administrativa.\n"
                "2. Nenhuma seção pode ficar vazia.\n"
                "3. Não invente dados sensíveis (nomes, valores exatos, processos reais).\n"
                "4. Se o insumo estiver incompleto, complemente com formulações institucionais adequadas.\n"
                "5. Retorne APENAS JSON válido, sem explicações antes ou depois.\n\n"

                "=== FORMATO EXATO DE RESPOSTA JSON ===\n"
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
                "Não inclua explicações adicionais."
            )

        # ======================================================
        # Artefatos futuros (ETP, TR, Edital, Contrato)
        # ======================================================
        return (
            f"Você é um assistente técnico do Tribunal de Justiça de São Paulo. "
            f"Elabore o documento institucional correspondente ao artefato {self.artefato}, "
            "em linguagem formal e retornando APENAS JSON estruturado."
        )


# ======================================================
# 🔌 Função pública usada pelo pipeline DFD
# ======================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    """
    Função chamada pelo pipeline de INSUMOS.
    Recebe o texto extraído do PDF e retorna o DFD estruturado.
    """

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}

    agente = DocumentAgent("DFD")
    resultado = agente.generate(conteudo_textual)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resultado_ia": resultado,
    }
