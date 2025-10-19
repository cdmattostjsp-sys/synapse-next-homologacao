# utils/next_pipeline.py
# ==========================================================
# SynapseNext – Fase Brasília
# Pipelines utilitários para geração e validação de artefatos
# ==========================================================

from datetime import datetime
from pathlib import Path
import json
import os
from openai import OpenAI
from validator_engine_vNext import validate_document


# ==========================================================
# Função 1 – build_dfd_markdown
# ==========================================================
def build_dfd_markdown(respostas: dict) -> str:
    """
    Monta o conteúdo institucional em Markdown com base nas respostas do formulário DFD.
    """
    md = f"""# Documento de Formalização da Demanda (DFD)

**Unidade solicitante:** {respostas.get("unidade", "")}  
**Responsável pelo pedido:** {respostas.get("responsavel", "")}  
**Objeto da contratação:** {respostas.get("objeto", "")}  
**Urgência:** {respostas.get("urgencia", "")}  
**Data de geração:** {respostas.get("timestamp", "")}

---

### Justificativa da necessidade
{respostas.get("justificativa", "—")}

### Quantidade / Escopo
{respostas.get("quantidade_escopo", "—")}

### Riscos identificados
{respostas.get("riscos", "—")}

### Alinhamento institucional
{respostas.get("alinhamento", "—")}

---

**Anexos:**  
{", ".join(respostas.get("anexos", [])) if respostas.get("anexos") else "Nenhum anexo informado."}

---

_Rascunho gerado automaticamente pelo SynapseNext – SAAB 5.0 (Fase Brasília)._
"""
    return md


# ==========================================================
# Função 2 – save_log
# ==========================================================
def save_log(artefato: str, dados: dict):
    """
    Registra logs das ações do usuário (geração, exportação, validação, etc.).
    Cada artefato é registrado em JSON, com data e hora.
    """
    base = Path(__file__).resolve().parents[1]
    logs_dir = base / "exports" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "artefato": artefato,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dados": dados,
    }

    log_path = logs_dir / f"log_{datetime.now().strftime('%Y%m%d')}.json"

    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)


# ==========================================================
# Função 3 – run_semantic_validation
# ==========================================================
def run_semantic_validation(artefato: str, markdown_text: str, client=None) -> dict:
    """
    Executa a validação semântica com o motor validator_engine_vNext.
    Retorna dict com rigid_score, semantic_score, guided_markdown, etc.
    """
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Chave OPENAI_API_KEY não configurada nas secrets.")
        client = OpenAI(api_key=api_key)

    result = validate_document(markdown_text, artefato, client)

    # Registra log resumido
    save_log(
        artefato,
        {
            "acao": "validar_semantico",
            "scores": {
                "rigid_score": result.get("rigid_score"),
                "semantic_score": result.get("semantic_score"),
            },
        },
    )
    return result


# ==========================================================
# Função 4 – build_etp_markdown
# ==========================================================
def build_etp_markdown(respostas: dict, dfd_data: dict | None = None) -> str:
    """
    Monta o Estudo Técnico Preliminar (ETP) em Markdown,
    reutilizando informações do DFD quando disponíveis.
    """
    dfd_trecho = ""
    if dfd_data:
        dfd_trecho = f"""
**Origem (DFD):**  
- Unidade solicitante: {dfd_data.get('unidade', '—')}  
- Responsável: {dfd_data.get('responsavel', '—')}  
- Objeto do DFD: {dfd_data.get('objeto', '—')}  
"""

    md = f"""# Estudo Técnico Preliminar (ETP)

**Data de geração:** {respostas.get("timestamp", "")}

{dfd_trecho}

---

## 1. Objeto da contratação
{respostas.get("objeto", "—")}

## 2. Necessidade da contratação
{respostas.get("necessidade", "—")}

## 3. Requisitos técnicos essenciais
{respostas.get("requisitos", "—")}

## 4. Soluções/alternativas estudadas
{respostas.get("alternativas", "—")}

## 5. Riscos e medidas de mitigação
{respostas.get("riscos", "—")}

## 6. Estimativa de custo
R$ {respostas.get("estimativa", "—")}

---

_Rascunho gerado automaticamente pelo SynapseNext – SAAB 5.0 (Fase Brasília)._
"""
    return md


# ==========================================================
# Função 5 – build_tr_markdown
# ==========================================================
def build_tr_markdown(respostas: dict, etp_data: dict | None = None) -> str:
    """
    Monta o Termo de Referência (TR) em Markdown,
    reutilizando informações do ETP quando disponíveis.
    """
    etp_trecho = ""
    if etp_data:
        etp_trecho = f"""
**Origem (ETP):**  
- Objeto: {etp_data.get('objeto', '—')}  
- Requisitos: {etp_data.get('requisitos', '—')}  
- Estimativa: R$ {etp_data.get('estimativa', '—')}  
"""

    md = f"""# Termo de Referência (TR)

**Data de geração:** {respostas.get("timestamp", "")}

{etp_trecho}

---

## 1. Objeto da contratação
{respostas.get("objeto", "—")}

## 2. Justificativa técnica
{respostas.get("justificativa", "—")}

## 3. Especificações técnicas detalhadas
{respostas.get("especificacoes", "—")}

## 4. Metodologia de execução
{respostas.get("metodologia_execucao", "—")}

## 5. Critérios de julgamento
{respostas.get("criterios_julgamento", "—")}

## 6. Fontes da pesquisa de preços
{respostas.get("fonte_precos", "—")}

## 7. Estimativa final de custo
R$ {respostas.get("estimativa_final", "—")}

## 8. Prazo estimado de execução
{respostas.get("prazo_execucao", "—")}

## 9. Condições contratuais principais
{respostas.get("condicoes_contrato", "—")}

---

_Rascunho gerado automaticamente pelo SynapseNext – SAAB 5.0 (Fase Brasília)._
"""
    return md
