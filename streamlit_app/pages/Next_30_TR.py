# streamlit_app/pages/Next_30_TR.py
# ==========================================================
# SynapseNext – Fase Brasília
# TR → Reuso do ETP → Formulário → Markdown → Exportação .docx
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
    from utils.next_pipeline import build_tr_markdown, registrar_log
    from utils.formatter_docx import markdown_to_docx
except Exception as e:
    st.error(f"❌ Erro ao importar módulos utilitários: {e}")
    st.stop()

# ==========================================================
# Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – TR", layout="wide")

st.title("TR — Termo de Referência")
st.caption(
    "Reaproveite dados do ETP, insira critérios de julgamento e gere o Termo de Referência "
    "em formato institucional (.docx)."
)

# ==========================================================
# Bloco 1 — Reuso de dados do ETP
# ==========================================================
st.divider()
st.subheader("1️⃣ Reaproveitamento do ETP")

base = Path(__file__).resolve().parents[2]
logs_dir = base / "exports" / "logs"
etp_data = None

if logs_dir.exists():
    log_files = sorted(logs_dir.glob("log_*.json"), reverse=True)
    if log_files:
        last_log = log_files[0]
        with open(last_log, "r", encoding="utf-8") as f:
            logs = json.load(f)
        etp_entries = [l for l in logs if l.get("artefato") == "ETP" and "gerar_rascunho" in str(l)]
        if etp_entries:
            etp_data = etp_entries[-1].get("dados", {}).get("respostas")
            st.success("✅ Dados do ETP carregados automaticamente.")
        else:
            st.info("Nenhum registro de ETP encontrado nos logs.")
    else:
        st.info("Nenhum log encontrado.")
else:
    st.info("A pasta de logs ainda não foi criada.")

# ==========================================================
# Bloco 2 — Formulário TR
# ==========================================================
st.divider()
st.subheader("2️⃣ Dados Técnicos e Critérios do Termo de Referência")

with st.form("form_tr", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        objeto = st.text_area(
            "Objeto da contratação",
            value=etp_data.get("objeto", "") if etp_data else "",
            height=100,
        )
        justificativa = st.text_area(
            "Justificativa técnica",
            placeholder="Fundamente a necessidade e a adequação técnica da contratação.",
            height=100,
        )
        especificacoes = st.text_area(
            "Especificações técnicas detalhadas",
            placeholder="Descreva os requisitos mínimos, normas aplicáveis e parâmetros de qualidade.",
            height=150,
        )
        metodologia_execucao = st.text_area(
            "Metodologia de execução",
            placeholder="Explique como será executado o objeto (etapas, prazos, acompanhamento, etc.).",
            height=150,
        )
    with col2:
        criterios_julgamento = st.text_area(
            "Critérios de julgamento",
            placeholder="Ex.: Menor preço global, técnica e preço, maior desconto, etc.",
            height=100,
        )
        fonte_precos = st.text_area(
            "Fontes da pesquisa de preços",
            placeholder="Informe as fontes consultadas, data e valores estimados.",
            height=100,
        )
        estimativa_final = st.text_input(
            "Estimativa final de custo (R$)",
            value=etp_data.get("estimativa", "") if etp_data else "",
        )
        prazo_execucao = st.text_input(
            "Prazo estimado de execução",
            placeholder="Ex.: 12 meses, contados da assinatura do contrato.",
        )
        condicoes_contrato = st.text_area(
            "Condições contratuais principais",
            placeholder="Descreva prazos, garantias, responsabilidades e obrigações do contratado.",
            height=120,
        )

    enviado = st.form_submit_button("Gerar rascunho do TR")

# ==========================================================
# Bloco 3 — Geração e visualização
# ==========================================================
if enviado:
    respostas_tr = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "objeto": objeto,
        "justificativa": justificativa,
        "especificacoes": especificacoes,
        "metodologia_execucao": metodologia_execucao,
        "criterios_julgamento": criterios_julgamento,
        "fonte_precos": fonte_precos,
        "estimativa_final": estimativa_final,
        "prazo_execucao": prazo_execucao,
        "condicoes_contrato": condicoes_contrato,
    }

    md = build_tr_markdown(respostas_tr, etp_data)
    save_log("TR", {"acao": "gerar_rascunho", "respostas": respostas_tr})

    st.success("✅ Rascunho do TR gerado com sucesso.")
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
    filename_base = f"TR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar para .docx"):
        markdown_to_docx(md, str(docx_path))
        save_log("TR", {"acao": "exportar_docx", "arquivo": str(docx_path.relative_to(base))})
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
    st.info("Preencha o formulário e clique em **Gerar rascunho do TR**.")
