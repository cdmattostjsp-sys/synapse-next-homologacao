# utils/next_pipeline.py
# Funções puras deste passo:
# - build_dfd_markdown(respostas: dict) -> str
# - save_log(artefato: str, payload: dict) -> Path
#
# Observações:
# - Cria/garante diretórios: exports/logs e exports/rascunhos
# - Logs mínimos em JSON com timestamp
# - Markdown institucional com cabeçalhos e linguagem padrão

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, Any

# =========================
# Diretórios base
# =========================
def _base_dir() -> Path:
    # Estrutura esperada: .../synapse-next/utils/next_pipeline.py
    # base = .../synapse-next
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
    Campos esperados em `respostas`:
      - unidade, responsavel, objeto, justificativa, quantidade_escopo, urgencia, riscos, alinhamento, anexos(list)
    """
    _ensure_output_dirs()
    ts = respostas.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    unidade = respostas.get("unidade", "").strip()
    responsavel = respostas.get("responsavel", "").strip()
    objeto = respostas.get("objeto", "").strip()
    justificativa = respostas.get("justificativa", "").strip()
    quantidade_escopo = respostas.get("quantidade_escopo", "").strip()
    urgencia = respostas.get("urgencia", "Sem urgência")
    riscos = respostas.get("riscos", "").strip()
    alinhamento = respostas.get("alinhamento", "").strip()
    anexos = respostas.get("anexos", []) or []

    # Linguagem institucional e estruturação clara
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
    Retorna o Path do arquivo salvo.
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
