# ==========================================================
# utils/integration_tr.py
# SynapseNext – Integração do Termo de Referência (TR)
# Revisão segura: 2025-11-09 – compatível com utils.ai_client.AIClient.ask
# ==========================================================

import os
import json
from datetime import datetime
from pathlib import Path

from utils.ai_client import AIClient  # usa .ask()


EXPORT_DIR = Path("exports") / "insumos" / "json"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _get_tr_path() -> Path:
    """Retorna o caminho padrão do último TR gerado."""
    return EXPORT_DIR / "TR_ultimo.json"


def carregar_tr_existente() -> dict | None:
    """Carrega o último TR salvo, se existir."""
    path = _get_tr_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def salvar_tr(dados: dict) -> Path:
    """Persiste o TR processado para uso pelo Streamlit."""
    path = _get_tr_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return path


def gerar_tr_com_ia(conteudo_base: str, metadados: dict | None = None) -> dict:
    """
    Gera um TR estruturado a partir de texto base e metadados opcionais.
    Substitui a chamada antiga client.chat(...) por AIClient.ask(...).
    """
    metadados = metadados or {}
    try:
        ai = AIClient()
        prompt = (
            "Analise o conteúdo a seguir e produza um Termo de Referência (TR) institucional "
            "do TJSP, estruturado em JSON, contendo: Objeto, Justificativa, Fundamentação Legal, "
            "Descrição do Objeto, Obrigações da Contratada, Obrigações da Contratante, Prazos, "
            "Critérios de Aceitação e Anexos. "
            "Se algum dado não estiver nos metadados nem no texto, liste em 'lacunas'."
        )

        resposta = ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="TR",
        )

        # a IA pode devolver ou JSON direto ou {"resposta_texto": "...json..."}
        if isinstance(resposta, dict) and "resposta_texto" in resposta:
            raw = resposta["resposta_texto"].strip()
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = {
                    "TR": raw,
                    "lacunas": ["IA retornou texto não 100% JSON – revisar."],
                }
        else:
            parsed = resposta

        resultado_final = {
            "artefato": "TR",
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metadados": metadados,
            "resultado_ia": parsed,
        }

        salvar_tr(resultado_final)
        return resultado_final

    except Exception as e:
        return {
            "erro": f"Falha ao gerar TR com IA: {e}",
            "artefato": "TR",
        }
