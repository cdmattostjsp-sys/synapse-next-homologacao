# utils/relatorio_consolidado_pipeline.py
# ==========================================================
# SynapseNext – Fase Brasília (Passo 10C – Relatório Técnico Consolidado)
# Consolida: Auditoria.IA + Validação Semântica + Comparador.IA
# Gera um .docx institucional com capa/cabeçalho via formatter_docx
# ==========================================================

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import os

# Imports internos (sem depender de Streamlit aqui)
# Ajuste de path relativo ao projeto
def _root() -> Path:
    return Path(__file__).resolve().parents[1]

# --- Importa utilitários existentes ---
try:
    from utils.comparador_pipeline import carregar_snapshots, analisar_coerencia
except Exception:
    # Carregamento tardio, se necessário
    import sys
    sys.path.append(str(_root()))
    from utils.comparador_pipeline import carregar_snapshots, analisar_coerencia  # type: ignore

try:
    from utils.auditoria_pipeline import read_last_audit
except Exception:
    import sys
    sys.path.append(str(_root()))
    from utils.auditoria_pipeline import read_last_audit  # type: ignore

try:
    from utils.next_pipeline import run_semantic_validation
except Exception:
    import sys
    sys.path.append(str(_root()))
    from utils.next_pipeline import run_semantic_validation  # type: ignore

try:
    from utils.formatter_docx import markdown_to_docx
except Exception:
    import sys
    sys.path.append(str(_root()))
    from utils.formatter_docx import markdown_to_docx  # type: ignore


# ----------------------------------------------------------
# Diretórios de saída
# ----------------------------------------------------------
def _ensure_dirs() -> Dict[str, Path]:
    base = _root()
    out = {
        "analises": base / "exports" / "analises",
        "relatorios": base / "exports" / "relatorios",
    }
    for p in out.values():
        p.mkdir(parents=True, exist_ok=True)
    return out


# ----------------------------------------------------------
# Coleta integral dos dados (auditoria + coerência + IA)
# ----------------------------------------------------------
def coletar_dados_relatorio() -> Dict[str, Any]:
    """
    Coleta os dados necessários ao relatório consolidado:
    - Snapshots mais recentes (DFD, ETP, TR, Edital)
    - Auditoria (hash, snapshot_relpath, word_count)
    - Validação semântica (resumo, pontuação, sugestões) executada agora
    - Comparador.IA (coerência global e divergências)
    """
    artefatos_md = carregar_snapshots(recente=True)  # textos limpos
    artefatos_ordem = ["DFD", "ETP", "TR", "Edital"]

    # Auditoria por artefato (último do dia corrente)
    auditoria: Dict[str, Any] = {}
    for art in artefatos_ordem:
        auditoria[art] = read_last_audit(art) or {}

    # Validação IA por artefato (se houver texto)
    validacoes: Dict[str, Any] = {}
    for art, text in artefatos_md.items():
        try:
            validacoes[art] = run_semantic_validation(text)
        except Exception as e:
            validacoes[art] = {"erro": str(e), "resumo": "", "pontuacao": 0, "sugestoes": []}

    # Comparador.IA
    coerencia = analisar_coerencia(artefatos_md) if artefatos_md else {
        "coerencia_global": 0,
        "comparacoes": {},
        "divergencias": [{"campo": "geral", "descricao": "Não há snapshots auditados suficientes."}],
        "ausencias": []
    }

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "artefatos_texto": artefatos_md,
        "auditoria": auditoria,
        "validacoes": validacoes,
        "coerencia": coerencia,
        "ordem": artefatos_ordem,
    }


# ----------------------------------------------------------
# Construção do Markdown institucional do relatório
# ----------------------------------------------------------
def _mk_section_validacao(nome: str, val: Dict[str, Any]) -> List[str]:
    linhas = [f"### 📄 {nome} — Validação Semântica"]
    if val.get("erro"):
        linhas.append(f"- ⚠️ **Erro**: {val.get('erro')}")
        return linhas
    resumo = val.get("resumo", "")
    pontos = val.get("pontuacao", 0)
    linhas.append(f"- **Resumo:** {resumo}")
    linhas.append(f"- **Pontuação de completude:** **{pontos}%**")
    sugestoes = val.get("sugestoes", [])
    if sugestoes:
        linhas.append("- **Sugestões de melhoria:**")
        for s in sugestoes:
            linhas.append(f"  - {s}")
    return linhas


def _mk_section_auditoria(nome: str, aud: Dict[str, Any]) -> List[str]:
    linhas = [f"### 🔐 {nome} — Auditoria Digital"]
    if not aud:
        linhas.append("- ❌ Sem registro de auditoria para o dia corrente.")
        return linhas
    short_hash = aud.get("sha256", "")[:10] if aud.get("sha256") else "—"
    linhas.append(f"- **Hash (SHA-256):** `{short_hash}`")
    linhas.append(f"- **Palavras (word_count):** {aud.get('word_count', 0)}")
    snap_rel = aud.get("snapshot_relpath", "—")
    linhas.append(f"- **Snapshot:** `{snap_rel}`")
    return linhas


def _mk_section_coerencia(coe: Dict[str, Any]) -> List[str]:
    linhas = ["## 🧩 Coerência Global (Comparador.IA)"]
    linhas.append(f"- **Coerência Global:** **{coe.get('coerencia_global', 0)}%**")
    if coe.get("comparacoes"):
        linhas.append("\n### 🔎 Comparações diretas")
        for par, val in coe["comparacoes"].items():
            linhas.append(f"- **{par}** → Similaridade: `{val}%`")
    if coe.get("divergencias"):
        linhas.append("\n### ⚠️ Divergências")
        for d in coe["divergencias"]:
            linhas.append(f"- {d.get('descricao', '')}")
    if coe.get("ausencias"):
        linhas.append("\n### ❌ Ausências")
        for a in coe["ausencias"]:
            linhas.append(f"- {a.get('descricao', '')}")
    return linhas


def _construir_markdown(dados: Dict[str, Any]) -> str:
    linhas: List[str] = []
    linhas.append("# 📘 Relatório Técnico Consolidado — Fase Interna (SynapseNext)")
    linhas.append(f"**Data de geração:** {dados.get('timestamp', '')}")
    linhas.append("")
    linhas.append("Este relatório consolida as evidências técnicas do SynapseNext (Fase Brasília), abrangendo:")
    linhas.append("- Auditoria Digital (hash, snapshots e métricas)")
    linhas.append("- Validação Semântica por IA (resumo, pontuação e sugestões)")
    linhas.append("- Análise de Coerência entre artefatos (Comparador.IA)")
    linhas.append("---\n")

    # Seções por artefato na ordem institucional
    ordem = dados.get("ordem", ["DFD", "ETP", "TR", "Edital"])
    validacoes = dados.get("validacoes", {})
    auditoria = dados.get("auditoria", {})

    for nome in ordem:
        linhas.append(f"## {nome}")
        linhas += _mk_section_auditoria(nome, auditoria.get(nome, {}))
        linhas.append("")
        linhas += _mk_section_validacao(nome, validacoes.get(nome, {}))
        linhas.append("\n---\n")

    # Coerência global
    linhas += _mk_section_coerencia(dados.get("coerencia", {}))
    linhas.append("\n---\n")
    linhas.append("_Relatório gerado automaticamente pelo SynapseNext — SAAB 5.0 / TJSP (Fase Brasília)._")

    return "\n".join(linhas)


# ----------------------------------------------------------
# Geração do DOCX institucional
# ----------------------------------------------------------
def gerar_relatorio_docx(dados: Dict[str, Any]) -> str:
    """
    Constrói o markdown do relatório consolidado e gera um .docx institucional
    usando utils.formatter_docx.markdown_to_docx. Retorna o caminho do arquivo.
    """
    out_dirs = _ensure_dirs()
    md_text = _construir_markdown(dados)

    # Caminho de saída
    fname = f"Relatorio_Tecnico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    out_path = out_dirs["relatorios"] / fname

    # Gera DOCX com capa/cabeçalho institucional
    markdown_to_docx(md_text, str(out_path), artefato_nome="Relatório Técnico Consolidado")

    return str(out_path)
