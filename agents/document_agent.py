# ==========================================================
# agents/document_agent.py — Versão D2 (Modo B – Equilibrado)
# SynapseNext – SAAB / Tribunal de Justiça do Estado de São Paulo
# Revisão Consolidada — 2025-11-24
# ==========================================================

from __future__ import annotations
import json
import os
import re
from datetime import datetime
from utils.ai_client import AIClient


# ==========================================================
# 🔧 SALVAR LOG OPCIONAL (não usado no fluxo principal)
# ==========================================================
def _registrar_log_document_agent(payload: dict) -> str:
    try:
        logs_dir = os.path.join("exports", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        filename = f"document_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(logs_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        return path
    except Exception:
        return ""


# ==========================================================
# 🔒 Filtro anti-alucinação numérica
# ==========================================================
def _sanear_numeros_na_resposta(resposta_dict: dict, conteudo_fonte: str) -> dict:
    if not isinstance(resposta_dict, dict):
        return resposta_dict

    fonte = str(conteudo_fonte or "")
    padrao = re.compile(r"\d[\d\.\,]*")

    def limpar(txt: str) -> str:
        if not isinstance(txt, str):
            return txt

        def replace_fn(m: re.Match) -> str:
            num = m.group(0)
            return num if num in fonte else "[VALOR A DEFINIR]"

        return padrao.sub(replace_fn, txt)

    def varrer(obj):
        if isinstance(obj, dict):
            return {k: varrer(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [varrer(v) for v in obj]
        if isinstance(obj, str):
            return limpar(obj)
        return obj

    return varrer(resposta_dict)


# ==========================================================
# 🔒 SEÇÕES OBRIGATÓRIAS
# ==========================================================
SECOES_OBRIGATORIAS = [
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


def _sanear_secoes(resposta: dict) -> dict:
    secoes = resposta.get("secoes", {})
    if not isinstance(secoes, dict):
        secoes = {}

    for s in SECOES_OBRIGATORIAS:
        if s not in secoes or not isinstance(secoes[s], str) or len(secoes[s].strip()) < 5:
            secoes[s] = "Conteúdo não identificado explicitamente no insumo."

    resposta["secoes"] = secoes
    return resposta


# ==========================================================
# 🔒 Sanitização do texto narrativo
# ==========================================================
def _sanear_texto_narrativo(txt: str) -> str:
    if not isinstance(txt, str) or len(txt.strip()) < 10:
        return "Conteúdo não identificado de forma suficiente no insumo."
    return txt.strip()


# ==========================================================
# 🤖 DOCUMENT AGENT – D2 (Equilibrado)
# ==========================================================
class DocumentAgent:

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()

    # ------------------------------------------------------
    # 🧠 GERAÇÃO PRINCIPAL
    # ------------------------------------------------------
    def generate(self, conteudo_base: str) -> dict:
        print("\n>>> DocumentAgent(D2) iniciado")
        print(f"Artefato: {self.artefato}")
        print(f"Tamanho do insumo: {len(conteudo_base)}")

        prompt = self._montar_prompt_institucional()

        try:
            resposta_raw = self.ai.ask(
                prompt=prompt,
                conteudo=conteudo_base,
                artefato=self.artefato,
            )
        except Exception as e:
            return {"erro": f"Falha na chamada IA: {e}"}

        print(">>> Resposta RAW recebida da IA")

        # normalização
        if isinstance(resposta_raw, dict) and "DFD" in resposta_raw:
            resposta = resposta_raw["DFD"]
        elif isinstance(resposta_raw, dict):
            resposta = resposta_raw
        else:
            resposta = {"texto_narrativo": str(resposta_raw)}

        if not isinstance(resposta, dict):
            resposta = {"texto_narrativo": str(resposta)}

        # sanitização
        resposta["texto_narrativo"] = _sanear_texto_narrativo(
            resposta.get("texto_narrativo", "")
        )

        resposta = _sanear_secoes(resposta)

        resposta = _sanear_numeros_na_resposta(resposta, conteudo_base)

        lac = resposta.get("lacunas", [])
        resposta["lacunas"] = lac if isinstance(lac, list) else []

        # 🔒 Garantir chaves administrativas
        resposta.setdefault("unidade_demandante", "")
        resposta.setdefault("responsavel", "")
        resposta.setdefault("prazo_estimado", "")
        resposta.setdefault("valor_estimado", "0,00")

        if not isinstance(resposta.get("valor_estimado"), str):
            resposta["valor_estimado"] = str(resposta["valor_estimado"])

        print(">>> DocumentAgent(D2) — Sanitização finalizada.")
        return resposta

    # ------------------------------------------------------
    # 🧩 PROMPT INSTITUCIONAL
    # ------------------------------------------------------
    def _montar_prompt_institucional(self) -> str:

        if self.artefato == "DFD":
            return (
                "Você é o agente de Formalização da Demanda (DFD) da Secretaria de Administração e Abastecimento "
                "(SAAB) do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                "Com base EXCLUSIVAMENTE no texto fornecido (insumo), produza um DFD completo, detalhado, formal e "
                "conforme a Lei nº 14.133/2021.\n\n"

                "=== ESTRUTURA OBRIGATÓRIA DO JSON ===\n"
                "O JSON final DEVE conter obrigatoriamente as chaves:\n"
                "- unidade_demandante\n"
                "- responsavel\n"
                "- prazo_estimado\n"
                "- valor_estimado\n"
                "- texto_narrativo\n"
                "- secoes\n"
                "- lacunas\n\n"

                "Use string vazia para campos administrativos ausentes. "
                "Use '0,00' para valor_estimado quando não houver valor no insumo.\n\n"

                "=== OBJETIVO ===\n"
                "Gerar texto robusto e coerente com o insumo, cobrindo as 11 seções obrigatórias.\n\n"

                "=== SEÇÕES OBRIGATÓRIAS ===\n"
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

                "=== FORMATO FINAL (OBRIGATÓRIO) ===\n"
                "Responda APENAS com JSON:\n"
                "{\n"
                "  \"DFD\": {\n"
                "    \"unidade_demandante\": \"\",\n"
                "    \"responsavel\": \"\",\n"
                "    \"prazo_estimado\": \"\",\n"
                "    \"valor_estimado\": \"0,00\",\n"
                "    \"texto_narrativo\": \"1. ... 11. ...\",\n"
                "    \"secoes\": { ... },\n"
                "    \"lacunas\": [ ... ]\n"
                "  }\n"
                "}"
            )

        return (
            f"Você é o agente institucional do TJSP responsável pelo artefato {self.artefato}. "
            "Produza APENAS JSON estruturado e formal."
        )


# ==========================================================
# 🔌 Função pública do pipeline INSUMOS
# ==========================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}

    agente = DocumentAgent("DFD")
    resultado = agente.generate(conteudo_textual)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resultado_ia": resultado,
    }
