# utils/next_pipeline.py
# Funções do SynapseNext (Passo 1 + Passo 2)
# - build_dfd_markdown(respostas: dict) -> str
# - save_log(artefato, payload) -> Path
# - run_semantic_validation(artefato: str, markdown_text: str, client=None) -> dict   [NOVO]

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json

def _base_dir() -> Path:
    # Estrutura esperada: .../synapse-next/utils/next_pipeline.py
    return Path(__file__).resolve().parents[1]

def _ensure_output_dirs() -> dict[str, Path]:
    base = _base_dir()
    exports = base / "exports"
    logs = exports / "logs"
    rascunhos = exports / "rascunhos"
    logs.mkdir(parents=True, exist_ok=True)
    rascunhos.mkdir(parents=True, exist_ok=True)
    return {"base": base, "exports": exports, "logs": logs, "rascunhos": rascunhos}

# =========================
# Markdown Builder – DFD
# =========================
def build_dfd_markdown(respostas: Dict[str, Any]) -> str:
    """
    Constrói o rascunho institucional do DFD em Markdown.
    """
    _ensure_output_dirs()
    ts = respostas.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    unidade = (respostas.get("unidade") or "").strip()
    responsavel = (respostas.get("responsavel") or "").strip()
    objeto = (respostas.get("objeto") or "").strip()
    justificativa = (respostas.get("justificativa") or "").strip()
    quantidade_escopo = (respostas.get("quantidade_escopo") or "").strip()
    urgencia = respostas.get("urgencia", "Sem urgência")
    riscos = (respostas.get("riscos") or "").strip()
    alinhamento = (respostas.get("alinhamento") or "").strip()
    anexos = respostas.get("anexos") or []

    md = f"""# Documento de Formalização da Demanda (DFD)

**Data/Hora do registro:** {ts}

## 1. Identificação
- **Unidade solicitante:** {unidade or "_(não informado)_"}
- **Responsável pelo pedido:** {responsavel or "_(não informado)_"}

## 2. Objeto
{objeto or "_(não informado)_"}

## 3. Quantidade / Escopo
{quantidade_escopo or "_(não informado)_"}

## 4. Justificativa
{justificativa or "_(não informado)_"}

## 5. Urgência
{urgencia or "_(não informado)_"}

## 6. Riscos Identificados
{(riscos if riscos else "_(sem riscos informados)_")}

## 7. Alinhamento Institucional
{alinhamento or "_(não informado)_"}

## 8. Anexos (opcional)
{("- " + "\\n- ".join(anexos)) if anexos else "_(nenhum anexo informado)_"}

---

_Observação:_ Este rascunho foi gerado automaticamente no contexto do **SynapseNext (SAAB 5.0)** e deverá passar por **validação semântica** no passo seguinte.
"""
    return md

# =========================
# Logging mínimo
# =========================
def save_log(artefato: str, payload: Dict[str, Any]) -> Path:
    """
    Salva um log mínimo (JSON) em exports/logs, com timestamp no nome do arquivo.
    """
    dirs = _ensure_output_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = artefato.upper().replace(" ", "_")
    log_path = dirs["logs"] / f"{safe_name}_log_{ts}.json"

    body = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "artefato": artefato,
        "payload": payload,
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(body, f, ensure_ascii=False, indent=2)

    return log_path

# =========================
# Validação semântica (Passo 2)
# =========================
def run_semantic_validation(artefato: str, markdown_text: str, client=None) -> Dict[str, Any]:
    """
    Executa a validação semântica usando validator_engine_vNext.validate_document
    e salva registros e rascunho orientado.

    - artefato: "DFD", "ETP", "TR"...
    - markdown_text: texto a validar
    - client: instância do cliente OpenAI (opcional). Se None, tenta criar localmente.
    """
    dirs = _ensure_output_dirs()

    # 1) Cliente OpenAI (auto)
    if client is None:
        try:
            from openai import OpenAI  # pacote do SDK oficial
            client = OpenAI()
        except Exception as e:
            raise RuntimeError(
                "OpenAI client não configurado. Verifique instalação do pacote `openai` "
                "e variável de ambiente OPENAI_API_KEY."
            ) from e

    # 2) Importa o validador do projeto (assinatura confirmada no arquivo do usuário)
    from validator_engine_vNext import validate_document  # :contentReference[oaicite:1]{index=1}

    # 3) Executa validação
    result = validate_document(markdown_text, artefato, client)

    # 4) Salva rascunho orientado (.md) em exports/rascunhos
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    guided_md = result.get("guided_markdown", "")
    guided_rel = None
    if guided_md:
        guided_path = dirs["rascunhos"] / f"{artefato.upper()}_guided_{ts}.md"
        guided_path.write_text(guided_md, encoding="utf-8")
        guided_rel = str(guided_path.relative_to(dirs["base"]))
        result["guided_markdown_path"] = guided_rel

    # 5) Log consolidado
    save_log(artefato, {
        "acao": "validar_semantico",
        "scores": {
            "rigid_score": result.get("rigid_score"),
            "semantic_score": result.get("semantic_score"),
        },
        "debug": result.get("debug"),
        "guided_markdown_path": guided_rel,
    })

    return result
