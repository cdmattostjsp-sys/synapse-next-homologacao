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
