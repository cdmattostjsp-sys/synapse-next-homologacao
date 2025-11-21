# ==========================================================
# agents/document_agent.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: 2025-11-20 – vNext (DFD Moderno-Governança)
# ==========================================================

from __future__ import annotations
import json
from datetime import datetime
from utils.ai_client import AIClient


class DocumentAgent:
    """
    Agente responsável por coordenar a geração de documentos
    formais via IA institucional (DFD, ETP, TR, Edital etc.).
    Compatível com o pipeline atual e AIClient padronizado.
    """

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()  # Cliente IA institucional


    # ======================================================
    # 🧠 GERAÇÃO DE CONTEÚDO VIA IA
    # ======================================================
    def generate(self, conteudo_base: str) -> dict:
        """
        Envia o conteúdo bruto para IA usando o prompt institucional.
        Retorna dicionário JSON estruturado.
        """

        prompt = self._montar_prompt_institucional()

        try:
            resposta = self.ai.ask(
                prompt=prompt,
                conteudo=conteudo_base,
                artefato=self.artefato
            )

            if not resposta or not isinstance(resposta, dict):
                return {"erro": "Resposta IA inválida ou vazia."}

            texto_bruto = resposta.get("resposta_texto", "").strip()
            if not texto_bruto:
                return {"erro": "IA não retornou conteúdo textual."}

            # Limpeza de blocos ```json
            if texto_bruto.startswith("```json"):
                texto_bruto = (
                    texto_bruto.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            # -----------------------------------------------------
            # 🎯 TENTATIVA DE INTERPRETAÇÃO JSON
            # -----------------------------------------------------
            try:
                parsed = json.loads(texto_bruto)

                # O formato institucional é {"DFD": {...}}
                if isinstance(parsed, dict) and "DFD" in parsed:
                    return parsed["DFD"]

                return parsed

            except Exception:
                # IA devolveu texto puro – retorna bruto
                return {"Conteúdo": texto_bruto}

        except Exception as e:
            return {"erro": f"Falha na geração do documento ({e})"}


    # ======================================================
    # 🧩 PROMPT INSTITUCIONAL – *vNext* (Modernizado)
    # ======================================================
    def _montar_prompt_institucional(self) -> str:

        # ======================================================
        # 📌 PROMPT ESPECIALIZADO PARA DFD
        # ======================================================
        if self.artefato == "DFD":
            return (
                "Você é o agente de Formalização da Demanda (DFD) da Secretaria de Administração e Abastecimento "
                "(SAAB) do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                "Com base exclusivamente no texto fornecido (insumo), produza um DFD completo, institucional, "
                "em conformidade com a Lei nº 14.133/2021 e boas práticas de governança.\n\n"

                "=== OBJETIVO ===\n"
                "Gerar um documento robusto, organizado e pronto para análise administrativa, contendo:\n"
                "1) Texto narrativo numerado ('texto_narrativo'), com 11 seções formais.\n"
                "2) Objeto 'secoes' contendo as mesmas 11 seções individualmente.\n"
                "3) Lista 'lacunas' com informações ausentes relevantes.\n\n"

                "=== SEÇÕES OBRIGATÓRIAS ===\n"
                "As seguintes 11 seções DEVERÃO existir em 'secoes', com esses títulos exatos:\n"
                "- Contexto Institucional\n"
                "- Diagnóstico da Situação Atual\n"
                "- Fundamentação da Necessidade\n"
                "- Objetivos da Contratação\n"
                "- Escopo Inicial da Demanda\n"
                "- Resultados Esperados\n"
                "- Benefícios Institucionais\n"
                "- Justificativa Legal\n"
                "- Riscos da Não Contratação\n"
                "- Requisitos Mínimos\n"
                "- Critérios de Sucesso\n\n"

                "=== TEXTO NARRATIVO (CAMPO 'texto_narrativo') ===\n"
                "Elabore um texto contínuo, claro e administrativo, numerado de 1 a 11, seguindo a ordem das seções.\n"
                "Não use bullets, tabelas, emojis, elementos gráficos ou formatações especiais.\n"
                "Use apenas texto limpo.\n\n"

                "=== LACUNAS ===\n"
                "Inclua em 'lacunas' as informações administrativas importantes que NÃO aparecem claramente no insumo, "
                "por exemplo:\n"
                "- Unidade demandante não identificada.\n"
                "- Responsável não informado.\n"
                "- Prazo estimado ausente.\n"
                "- Estimativa de valor não localizada.\n"
                "Somente registre lacunas reais.\n\n"

                "=== REGRAS DE ESCRITA ===\n"
                "• Linguagem formal, técnica, impessoal e institucional.\n"
                "• Nada de floreios, firulas, figuras ou linguagem subjetiva.\n"
                "• Não invente dados sensíveis (nomes, números de processo, valores reais).\n"
                "• Utilize parágrafos curtos e coerentes.\n\n"

                "=== FORMATO EXATO DE SAÍDA ===\n"
                "A resposta deve ser APENAS um JSON válido, seguindo exatamente este modelo:\n"
                "{\n"
                "  \"DFD\": {\n"
                "    \"texto_narrativo\": \"1. ... 2. ... 3. ...\",\n"
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
                "    \"lacunas\": [\"...\"]\n"
                "  }\n"
                "}\n\n"
                "Não inclua comentários, explicações ou qualquer conteúdo fora do JSON final."
            )

        # ======================================================
        # PROMPT PADRÃO (ETP, TR, EDITAL, CONTRATO)
        # ======================================================
        return (
            f"Você é o agente institucional do TJSP responsável pelo artefato {self.artefato}. "
            "Produza um documento administrativo formal e retorne APENAS JSON estruturado."
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
