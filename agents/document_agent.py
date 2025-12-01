# ==========================================================
# agents/document_agent.py — Versão D3 (Universal – DFD Moderno)
# SynapseNext – SAAB / Tribunal de Justiça do Estado de São Paulo
# Revisão Consolidada — 2025-11-30
# ==========================================================

from __future__ import annotations

import json
import os
import re
from datetime import datetime

from utils.ai_client import AIClient


# ==========================================================
# 🔧 SALVAR LOG OPCIONAL (para auditoria técnica)
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
    """
    Percorre todo o JSON de resposta e garante que números
    que não aparecem no texto-fonte sejam substituídos por
    um marcador neutro ("[VALOR A DEFINIR]").
    """
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
# 🔒 SEÇÕES OBRIGATÓRIAS (DFD Moderno – 11 seções)
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
# 🔧 Geração automática de descrição e motivação
# ==========================================================
def _preencher_descricao_e_motivacao(resposta: dict) -> dict:
    """
    Gera / completa os campos tradicionais:
      - descricao_necessidade
      - motivacao
    com base nas 11 seções estruturadas, caso venham vazios.
    """
    secoes = resposta.get("secoes", {})
    if not isinstance(secoes, dict):
        secoes = {}

    # ---------------- DESCRIÇÃO ----------------
    desc_existente = ""
    if isinstance(resposta.get("descricao_necessidade"), str):
        desc_existente = resposta["descricao_necessidade"].strip()

    if not desc_existente:
        partes_desc = []
        for chave in [
            "Contexto Institucional",
            "Diagnóstico da Situação Atual",
            "Fundamentação da Necessidade",
        ]:
            v = secoes.get(chave)
            if isinstance(v, str) and v.strip():
                partes_desc.append(v.strip())
        desc_calc = "\n\n".join(partes_desc).strip()
        resposta["descricao_necessidade"] = desc_calc

    # ---------------- MOTIVAÇÃO ----------------
    mot_existente = ""
    if isinstance(resposta.get("motivacao"), str):
        mot_existente = resposta["motivacao"].strip()

    if not mot_existente:
        partes_mot = []
        for chave in [
            "Objetivos da Contratação",
            "Resultados Esperados",
            "Benefícios Institucionais",
            "Justificativa Legal",
            "Riscos da Não Contratação",
        ]:
            v = secoes.get(chave)
            if isinstance(v, str) and v.strip():
                partes_mot.append(v.strip())
        mot_calc = "\n\n".join(partes_mot).strip()
        resposta["motivacao"] = mot_calc

    return resposta


# ==========================================================
# 🤖 DOCUMENT AGENT – D3
# ==========================================================
class DocumentAgent:
    """
    Agente de documentos institucional do TJSP.
    Nesta versão está focado no artefato DFD, mas já
    preparado para ser reutilizado em outros (ETP, TR, Edital).
    """

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()

    # ------------------------------------------------------
    # 🧠 GERAÇÃO PRINCIPAL
    # ------------------------------------------------------
    def generate(self, conteudo_base: str) -> dict:
        print("\n>>> DocumentAgent(D3) iniciado")
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

        # Normalização da raiz
        if isinstance(resposta_raw, dict) and "DFD" in resposta_raw:
            resposta = resposta_raw["DFD"]
        elif isinstance(resposta_raw, dict):
            resposta = resposta_raw
        else:
            resposta = {"texto_narrativo": str(resposta_raw)}

        if not isinstance(resposta, dict):
            resposta = {"texto_narrativo": str(resposta)}

        # Sanitização do texto narrativo
        resposta["texto_narrativo"] = _sanear_texto_narrativo(
            resposta.get("texto_narrativo", "")
        )

        # Garantir seções obrigatórias
        resposta = _sanear_secoes(resposta)

        # Garantir campos tradicionais de síntese
        resposta = _preencher_descricao_e_motivacao(resposta)

        # Anti-alucinação numérica
        resposta = _sanear_numeros_na_resposta(resposta, conteudo_base)

        # Lista de lacunas
        lac = resposta.get("lacunas", [])
        resposta["lacunas"] = lac if isinstance(lac, list) else []

        # 🔒 Garantir chaves administrativas
        resposta.setdefault("unidade_demandante", "")
        resposta.setdefault("responsavel", "")
        resposta.setdefault("prazo_estimado", "")
        resposta.setdefault("valor_estimado", "0,00")

        if not isinstance(resposta.get("valor_estimado"), str):
            resposta["valor_estimado"] = str(resposta["valor_estimado"])

        # Metadados mínimos
        resposta.setdefault("origem", "document_agent_D3")
        resposta.setdefault(
            "gerado_em",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        # Log opcional (pode ser comentado se não quiser gerar arquivos)
        _registrar_log_document_agent(
            {
                "artefato": self.artefato,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "entrada_tamanho": len(conteudo_base),
                "resposta": resposta,
            }
        )

        print(">>> DocumentAgent(D3) — Sanitização finalizada.")
        return resposta

    # ------------------------------------------------------
    # 🧩 PROMPT INSTITUCIONAL
    # ------------------------------------------------------
    def _montar_prompt_institucional(self) -> str:

        if self.artefato == "DFD":

            return (
                "Você é o agente institucional de Formalização da Demanda (DFD) do TJSP. "
                "Receberá QUALQUER TEXTO (ETP, TR, edital, contrato, parecer, PDF solto ou texto informal) "
                "e deverá PRODUZIR um DFD moderno completo, inferindo informações quando possível "
                "e registrando lacunas quando necessário.\n\n"
                "=== OBJETIVO ===\n"
                "Gerar texto formal, robusto, coerente e aderente ao modelo institucional do TJSP.\n\n"
                "=== FORMATO (OBRIGATÓRIO) ===\n"
                "Responda APENAS com JSON contendo:\n"
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

        # Fallback genérico para futuros artefatos
        return (
            f"Você é o agente institucional do TJSP responsável pelo artefato {self.artefato}. "
            "Produza APENAS JSON estruturado e formal, seguindo o padrão institucional."
        )


# ==========================================================
# 🟦 Função universal — interface usada pelo integration_dfd
# ==========================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    """
    Função UNIVERSAL: aceita qualquer texto como insumo.
    Não exige ser um DFD anterior.
    Não depende do tipo de documento.
    """

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}

    try:
        agente = DocumentAgent("DFD")
        resultado = agente.generate(conteudo_textual)

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resultado_ia": resultado,
        }

    except Exception as e:
        return {
            "erro": f"Falha ao gerar DFD universal: {e}",
            "conteudo_recebido": conteudo_textual[:500],
        }
