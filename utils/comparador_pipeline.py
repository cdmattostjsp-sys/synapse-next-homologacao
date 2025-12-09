# ==========================================================
# SynapseNext – Fase Brasília (Passo 10B – Comparador.IA)
# ==========================================================
# Módulo de análise cruzada e coerência semântica entre os
# artefatos da fase interna (DFD → ETP → TR → Edital)
# ==========================================================

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json
import re
from difflib import SequenceMatcher

# ==========================================================
# 🧠 Funções utilitárias
# ==========================================================

def _root() -> Path:
    return Path(__file__).resolve().parents[1]

def _ensure_dirs() -> Dict[str, Path]:
    base = _root()
    dirs = {
        "snapshots": base / "exports" / "auditoria" / "snapshots",
        "analises": base / "exports" / "analises",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs

def _load_latest_snapshot(artefato: str) -> str | None:
    """
    Retorna o conteúdo mais recente do snapshot Markdown do artefato informado.
    """
    dirs = _ensure_dirs()
    snaps = sorted(dirs["snapshots"].glob(f"{artefato}_*.md"), reverse=True)
    if not snaps:
        return None
    with open(snaps[0], "r", encoding="utf-8") as f:
        return f.read()

def _clean_text(text: str) -> str:
    """Limpa formatação, títulos e espaçamento."""
    text = re.sub(r"[*#>\-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def _extract_keywords(text: str) -> set:
    """
    Extrai palavras-chave relevantes do texto (substantivos, verbos, termos técnicos).
    Remove stopwords e normaliza termos.
    """
    # Normalizar texto
    text = text.lower()
    
    # Stopwords básicas do português
    stopwords = {
        'a', 'o', 'e', 'é', 'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 
        'nos', 'nas', 'para', 'com', 'por', 'uma', 'um', 'os', 'as', 'ao', 'à',
        'aos', 'às', 'pelo', 'pela', 'pelos', 'pelas', 'que', 'se', 'ou', 'mas',
        'etc', 'ser', 'ter', 'estar', 'data', 'dia', 'mês', 'ano'
    }
    
    # Extrair palavras (mínimo 3 caracteres)
    palavras = re.findall(r'\b\w{3,}\b', text)
    
    # Filtrar stopwords e criar conjunto
    keywords = {p for p in palavras if p not in stopwords}
    
    return keywords

def _similarity(a: str, b: str) -> float:
    """
    Calcula similaridade (0–100) entre duas strings usando:
    1. Sobreposição de palavras-chave (85% do peso) - conceitos e termos técnicos
    2. Similaridade de sequência SequenceMatcher (15% do peso) - estrutura textual
    """
    if not a or not b:
        return 0.0
    
    # 1. Análise baseada em palavras-chave (mais inteligente)
    keywords_a = _extract_keywords(a)
    keywords_b = _extract_keywords(b)
    
    if not keywords_a or not keywords_b:
        # Fallback para SequenceMatcher se não houver keywords
        return round(SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100, 2)
    
    # Calcular Jaccard similarity (interseção / união)
    intersecao = keywords_a & keywords_b
    uniao = keywords_a | keywords_b
    jaccard_sim = (len(intersecao) / len(uniao)) * 100 if uniao else 0
    
    # 2. SequenceMatcher como complemento (detecta ordem e estrutura)
    sequence_sim = SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100
    
    # Combinar métricas: 85% keywords (conceitos), 15% sequence (estrutura)
    # Prioriza concordância conceitual sobre ordem exata das palavras
    similaridade_final = (jaccard_sim * 0.85) + (sequence_sim * 0.15)
    
    return round(similaridade_final, 2)


# ==========================================================
# 📘 Núcleo principal
# ==========================================================

def carregar_snapshots(recente: bool = True) -> Dict[str, str]:
    """
    Carrega os textos Markdown mais recentes de cada artefato.
    """
    artefatos = ["DFD", "ETP", "TR", "Edital"]
    dados = {}
    for art in artefatos:
        texto = _load_latest_snapshot(art)
        if texto:
            dados[art] = _clean_text(texto)
    return dados


def analisar_coerencia(artefatos: Dict[str, str]) -> Dict[str, Any]:
    """
    Compara os artefatos carregados e gera métricas de coerência textual.
    
    VALORES ESPERADOS DE COERÊNCIA:
    - 60-100%: Excelente coerência (vocabulário muito similar)
    - 40-60%:  Boa coerência (conceitos alinhados, formulação diferente)
    - 30-40%:  Coerência moderada (mesmo tema, diferentes níveis de detalhamento)
    - <30%:    Baixa coerência (possível desalinhamento ou falta de contexto)
    
    OBSERVAÇÃO: Documentos como DFD→ETP→TR→Edital naturalmente apresentam
    coerência moderada (35-45%) pois cada um tem propósito específico e 
    nível de detalhamento distinto, mesmo tratando do mesmo objeto.
    """
    resultados = {"coerencia_global": 0, "comparacoes": {}, "divergencias": [], "ausencias": []}

    pares = [("DFD", "ETP"), ("ETP", "TR"), ("TR", "Edital")]
    total_sim = 0
    total_pairs = 0

    for a1, a2 in pares:
        t1, t2 = artefatos.get(a1), artefatos.get(a2)
        if not t1 or not t2:
            resultados["ausencias"].append({
                "campo": f"{a1}-{a2}",
                "descricao": f"Não há conteúdo disponível para {a1} ou {a2}."
            })
            continue

        sim = _similarity(t1, t2)
        resultados["comparacoes"][f"{a1}-{a2}"] = sim
        total_sim += sim
        total_pairs += 1

        # Regras de alerta ajustadas para valores realistas
        # Documentos progressivos (DFD→ETP→TR→Edital) naturalmente têm 30-45% de coerência
        if sim < 25:
            resultados["divergencias"].append({
                "campo": f"{a1}-{a2}",
                "descricao": f"🔴 Coerência muito baixa entre {a1} e {a2} ({sim}%). Recomenda-se revisar urgentemente o alinhamento de informações, objeto e justificativa."
            })
        elif 25 <= sim < 35:
            resultados["divergencias"].append({
                "campo": f"{a1}-{a2}",
                "descricao": f"🟡 Coerência baixa entre {a1} e {a2} ({sim}%). Verificar se objeto, justificativa e especificações estão alinhados entre os documentos."
            })

    if total_pairs > 0:
        resultados["coerencia_global"] = round(total_sim / total_pairs, 2)

    return resultados


# ==========================================================
# 🧾 Geração de relatório
# ==========================================================

def gerar_relatorio(resultados: Dict[str, Any]) -> Dict[str, str]:
    """
    Gera relatório .json e .md com base nos resultados da análise de coerência.
    """
    dirs = _ensure_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"relatorio_coerencia_{timestamp}"
    json_path = dirs["analises"] / f"{base_name}.json"
    md_path = dirs["analises"] / f"{base_name}.md"

    # JSON estruturado
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(resultados, jf, indent=4, ensure_ascii=False)

    # Markdown legível
    md = [
        "# 🧩 Relatório de Coerência entre Artefatos",
        f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"**Coerência Global:** {resultados.get('coerencia_global', 0)}%",
        "",
        "## Comparações",
    ]
    for k, v in resultados.get("comparacoes", {}).items():
        md.append(f"- **{k}** → Similaridade: `{v}%`")

    if resultados.get("divergencias"):
        md.append("\n## ⚠️ Divergências")
        for d in resultados["divergencias"]:
            md.append(f"- {d['descricao']}")

    if resultados.get("ausencias"):
        md.append("\n## ❌ Ausências")
        for a in resultados["ausencias"]:
            md.append(f"- {a['descricao']}")

    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write("\n".join(md))

    return {
        "ok": True,
        "json_path": str(json_path),
        "md_path": str(md_path),
        "coerencia_global": resultados.get("coerencia_global", 0),
    }


# ==========================================================
# 🚀 Execução direta (teste rápido)
# ==========================================================
if __name__ == "__main__":
    dados = carregar_snapshots()
    if not dados:
        print("⚠️ Nenhum snapshot encontrado em exports/auditoria/snapshots/")
    else:
        print("🧩 Artefatos carregados:", list(dados.keys()))
        resultado = analisar_coerencia(dados)
        saida = gerar_relatorio(resultado)
        print(f"✅ Relatório salvo em: {saida['md_path']}")
