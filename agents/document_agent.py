# ==========================================================
# agents/document_agent.py — Versão D2 (Modo B – Equilibrado)
# SynapseNext – SAAB / Tribunal de Justiça do Estado de São Paulo
# Revisão: 2025-11-24
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
    except Exception as e:
        return f"ERRO_LOG: {e}"


# ==========================================================
# 🔒 Filtro anti-alucinação numérica
# ==========================================================
def _sanear_numeros_na_resposta(resposta_dict: dict, conteudo_fonte: str) -> dict:
    if not isinstance(resposta_dict, dict):
        return resposta_dict

    fonte = str(conteudo_fonte or "")
    padrao_numeros = re.compile(r"\d[\d\.\,]*")

    def limpar(txt: str) -> str:
        if not isinstance(txt, str):
            return txt

        def sub(m: re.Match) -> str:
            token = m.group(0)
            return token if token in fonte else "[VALOR A DEFINIR]"

        return padrao_numeros.sub(sub, txt)

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
# 🔒 SANEAR SEÇÕES OBRIGATÓRIAS (Modo B – Elaborado)
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
    """
    Garante que todas as 11 seções existam.
    Se faltar alguma, insere placeholder institucional.
    """

    secoes = resposta.get("secoes", {})
    if not isinstance(secoes, dict):
        secoes = {}

    for s in SECOES_OBRIGATORIAS:
        if s not in secoes or not isinstance(secoes[s], str) or len(secoes[s].strip()) < 5:
            secoes[s] = "Conteúdo não identificado explicitamente no insumo."

    resposta["secoes"] = secoes
    return resposta


# ==========================================================
# 🔒 SANEAR TEXTO NARRATIVO
# ==========================================================
def _sanear_texto_narrativo(texto: str) -> str:
    if not isinstance(texto, str) or len(texto.strip()) < 10:
        return "Conteúdo não identificado de forma suficiente no insumo."
    return texto.strip()


# ==========================================================
# 🤖 DOCUMENT AGENT D2 – Geração Final
# ==========================================================
class DocumentAgent:
    """
    Agente institucional para geração de artefatos administrativos.
    Compatível com AIClient (response_format=json_object).
    """

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()

    # ======================================================
    # 🧠 EXECUTAR GERAÇÃO VIA IA
    # ======================================================
    def generate(self, conteudo_base: str) -> dict:
        print("\n>>> DocumentAgent(D2) – Iniciando geração")
        print(f"Artefato: {self.artefato}")
        print(f"Tamanho do insumo: {len(conteudo_base)}")

        prompt = self._montar_prompt_institucional()

        # --------------------------------------------------
        # 🔥 CHAMADA AO CLIENTE IA
        # --------------------------------------------------
        try:
            resposta_raw = self.ai.ask(
                prompt=prompt,
                conteudo=conteudo_base,
                artefato=self.artefato,
            )
        except Exception as e:
            return {"erro": f"Falha na chamada IA: {e}"}

        print(">>> Resposta RAW recebida da IA.")

        # --------------------------------------------------
        # 1) IA já retornou JSON válido
        # --------------------------------------------------
        if isinstance(resposta_raw, dict) and "DFD" in resposta_raw:
            resposta = resposta_raw["DFD"]

        # --------------------------------------------------
        # 2) IA retornou dicionário genérico
        # --------------------------------------------------
        elif isinstance(resposta_raw, dict):
            resposta = resposta_raw

        else:
            # fallback improvável
            resposta = {"texto_narrativo": str(resposta_raw)}

        # --------------------------------------------------
        # 3) Sanitização TOTAL
        # --------------------------------------------------
        if not isinstance(resposta, dict):
            resposta = {"texto_narrativo": str(resposta)}

        # 3.1 texto narrativo
        resposta["texto_narrativo"] = _sanear_texto_narrativo(
            resposta.get("texto_narrativo", "")
        )

        # 3.2 seções obrigatórias
        resposta = _sanear_secoes(resposta)

        # 3.3 filtro anti-alucinação numérica
        resposta = _sanear_numeros_na_resposta(resposta, conteudo_base)

        # 3.4 lacunas
        lacunas = resposta.get("lacunas", [])
        if not isinstance(lacunas, list):
            lacunas = []
        resposta["lacunas"] = lacunas

        print(">>> DocumentAgent(D2) – Sanitização concluída.")
        return resposta

    # ======================================================
    # 📌 PROMPT – MODO B (Equilibrado)
    # ======================================================
    def _montar_prompt_institucional(self) -> str:
        if self.artefato == "DFD":
            return (
                "Você é o agente institucional responsável por elaborar a Formalização da "
                "Demanda (DFD) conforme práticas de governança do TJSP. "
                "Com base EXCLUSIVA no texto do insumo, produza um DFD completo e profissional, "
                "permitindo apenas complementações institucionais genéricas quando coerentes "
                "e nunca inventando valores numéricos, prazos ou quantidades.\n\n"
                "=== ENTREGAS ===\n"
                "Você deve retornar APENAS JSON com estrutura:\n"
                "{\n"
                "  \"DFD\": {\n"
                "     \"texto_narrativo\": \"...\",\n"
                "     \"secoes\": {\n"
                "        \"Contexto Institucional\": \"...\",\n"
                "        \"Diagnóstico da Situação Atual\": \"...\",\n"
                "        \"Fundamentação da Necessidade\": \"...\",\n"
                "        \"Objetivos da Contratação\": \"...\",\n"
                "        \"Escopo Inicial da Demanda\": \"...\",\n"
                "        \"Resultados Esperados\": \"...\",\n"
                "        \"Benefícios Institucionais\": \"...\",\n"
                "        \"Justificativa Legal\": \"...\",\n"
                "        \"Riscos da Não Contratação\": \"...\",\n"
                "        \"Requisitos Mínimos\": \"...\",\n"
                "        \"Critérios de Sucesso\": \"...\"\n"
                "     },\n"
                "     \"lacunas\": []\n"
                "  }\n"
                "}\n\n"
                "=== INSTRUÇÕES ===\n"
                "- Não invente valores numéricos.\n"
                "- Não utilize informações externas ao insumo.\n"
                "- Permita complementações institucionais gerais, sem criar dados.\n"
                "- Texto deve ser robusto, coerente e bem redigido.\n"
                "- Responda somente JSON.\n"
            )

        return (
            f"Você é o agente institucional para o artefato {self.artefato}. "
            "Retorne APENAS JSON estruturado."
        )


# ======================================================
# 🔌 Função pública usada pelo pipeline INSUMOS
# ======================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}

    agente = DocumentAgent("DFD")
    resultado = agente.generate(conteudo_textual)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resultado_ia": resultado,
    }
