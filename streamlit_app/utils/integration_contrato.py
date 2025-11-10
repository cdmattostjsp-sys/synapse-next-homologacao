# ==========================================================
# utils/integration_contrato.py
# SynapseNext – Integração do Contrato Administrativo
# Revisão segura: 2025-11-09 – compatível com utils.ai_client.AIClient.ask
# ==========================================================

import os
import json
from datetime import datetime
from pathlib import Path

from utils.ai_client import AIClient  # usa .ask()


EXPORT_DIR = Path("exports") / "insumos" / "json"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _get_contrato_path() -> Path:
    return EXPORT_DIR / "CONTRATO_ultimo.json"


def carregar_contrato_existente() -> dict | None:
    path = _get_contrato_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def salvar_contrato(dados: dict) -> Path:
    path = _get_contrato_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return path


def gerar_contrato_com_ia(conteudo_base: str, metadados: dict | None = None) -> dict:
    """
    Gera contrato administrativo a partir de conteúdo base e metadados.
    Substitui resp = ai.chat([...]) pela nova chamada ai.ask(...).
    """
    metadados = metadados or {}
    try:
        ai = AIClient()
        prompt = (
            "Você é um assistente institucional do TJSP. Com base no conteúdo a seguir, "
            "gere um CONTRATO ADMINISTRATIVO estruturado em JSON, contendo: Partes, Objeto, "
            'Fundamentação Legal, Prazo, Valor, Obrigações da Contratada, Obrigações da Contratante, '
            "Fiscalização e Penalidades. Liste campos ausentes em 'lacunas'."
        )

        resposta = ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="CONTRATO",
        )

        if isinstance(resposta, dict) and "resposta_texto" in resposta:
            raw = resposta["resposta_texto"].strip()
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = {
                    "CONTRATO": raw,
                    "lacunas": ["IA retornou texto não totalmente JSON – revisar."],
                }
        else:
            parsed = resposta

        resultado_final = {
            "artefato": "CONTRATO",
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metadados": metadados,
            "resultado_ia": parsed,
        }

        salvar_contrato(resultado_final)
        return resultado_final

    except Exception as e:
        return {
            "erro": f"Falha ao gerar CONTRATO com IA: {e}",
            "artefato": "CONTRATO",
        }
