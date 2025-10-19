# streamlit_app/pages/Next_20_ETP.py
# ==========================================================
# SynapseNext – Fase Brasília
# ETP → Reuso do DFD → Formulário → Markdown → Exportação .docx
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import json
import streamlit as st

# ==========================================================
# Correção de caminho robusta (local e cloud)
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.next_pipeline import build_etp_markdown, registrar_log
    from utils.formatter_docx import markdown_to_docx
except Exception as e:
    st.error(f"❌ Erro ao importar módulos utilitários: {e}")
    st.stop()

# ==========================================================
# Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – ETP", layout="wide")

st.title("ETP — Estudo Técnico Preliminar")
st.caption(
    "Reaproveite informações do DFD, complemente dados técnicos e gere o Estudo Técnico Preliminar "
    "em formato institucional (.docx)."
)

# ==========================================================
# Bloco 1 — Reuso de dados do DFD
# ==========================================================
st.divider()
st.subheader("1️⃣ Reaproveitamento do DFD")

base = Path(__file__).resolve().parents[2]
logs_dir = base / "exports" / "logs"
dfd_data = None

if logs_dir.exists():
    log_files = sorted(logs_dir.glob("log_*.json"), reverse=True)
    if log_files:
        last_log = log_files[0]
        with open(last_log, "r", encoding="utf-8") as f:
            logs = json.load(f)
        dfd_entries = [l for l in logs if l.get("artefato") == "DFD" and "gerar_rascunho" in str(l)]
        if dfd_entries:
            dfd_data = dfd_entries[-1].get("dados", {}).get("respostas")
            st.success("✅ Dados do DFD carregados automaticamente.")
        else:
            st.info("Nenhum registro de DFD encontrado nos logs.")
    else:
        st.info("Nenhum log encontrado.")
else:
    st.info("A pasta de logs ainda não foi criada.")

# ==========================================================
# Bloco 2 — Formulário do ETP
# ==========================================================
st.divider()
st.subheader("2️⃣ Complementação – Dados Técnicos do ETP")

with st.form("form_etp", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        objeto = st.text_area(
            "Objeto da contratação (ajuste técnico, se necessário)",
            value=dfd_data.get("objeto", "") if dfd_data else "",
            height=100,
        )
        necessidade = st.text_area(
            "Necessidade da contratação",
            placeholder="Descreva a motivação técnica que justifica a contratação.",
            height=100,
        )
        requisitos = st.text_area(
            "Requisitos técnicos essenciais",
            placeholder="Liste requisitos mínimos, padrões e normas aplicáveis.",
            height=120,
        )
    with col2:
        alternativas = st.text_area(
            "Soluções/alternativas estudadas",
            placeholder="Descreva as soluções avaliadas e critérios de seleção.",
            height=120,
        )
        riscos = st.text_area(
            "Riscos e mitigação",
            placeholder="Identifique riscos técnicos e medidas de mitigação.",
            height=120,
        )
        estimativa = st.text_input(
            "Estimativa de custo (R$)",
            placeholder="Ex.: 125.000,00",
        )

    enviado = st.form_submit_button("Gerar rascunho do ETP")

# ==========================================================
# Bloco 3 — Geração e visualização
# ==========================================================
if enviado:
    respostas_etp = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "objeto": objeto,
        "necessidade": necessidade,
        "requisitos": requisitos,
        "alternativas": alternativas,
        "riscos": riscos,
        "estimativa": estimativa,
    }

    md = build_etp_markdown(respostas_etp, dfd_data)
    save_log("ETP", {"acao": "gerar_rascunho", "respostas": respostas_etp})

    st.success("✅ Rascunho do ETP gerado com sucesso.")
    st.divider()

    st.subheader("3️⃣ Preview – Rascunho em Markdown")
    st.markdown(md)

    # -----------------------------------------------------
    # Exportação .docx
    # -----------------------------------------------------
    st.divider()
    st.subheader("4️⃣ Exportação – `.docx`")

    rascunhos_dir = base / "exports" / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)
    filename_base = f"ETP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar para .docx"):
        markdown_to_docx(md, str(docx_path))
        save_log("ETP", {"acao": "exportar_docx", "arquivo": str(docx_path.relative_to(base))})
        with open(docx_path, "rb") as f:
            data = f.read()
        st.download_button(
            label="⬇️ Baixar arquivo .docx",
            data=data,
            file_name=docx_path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
        st.info(f"Arquivo salvo em: `exports/rascunhos/{docx_path.name}`")

else:
    st.info("Preencha o formulário e clique em **Gerar rascunho do ETP**.")
