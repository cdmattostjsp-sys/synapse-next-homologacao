# streamlit_app/pages/Next_40_Contrato.py
# ==========================================================
# SynapseNext – Fase Brasília
# Contrato → Reuso do TR → Formulário → Markdown → Exportação .docx
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
    from utils.next_pipeline import build_contrato_markdown, registrar_log
    from utils.formatter_docx import markdown_to_docx
except Exception as e:
    st.error(f"❌ Erro ao importar módulos utilitários: {e}")
    st.stop()

# ==========================================================
# Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – Contrato", layout="wide")

st.title("Contrato Administrativo")
st.caption(
    "Última etapa da Fase Interna: formalização contratual com base no Termo de Referência (TR)."
)

# ==========================================================
# Bloco 1 — Reuso de dados do TR
# ==========================================================
st.divider()
st.subheader("1️⃣ Reaproveitamento do TR")

base = Path(__file__).resolve().parents[2]
logs_dir = base / "exports" / "logs"
tr_data = None

if logs_dir.exists():
    log_files = sorted(logs_dir.glob("log_*.json"), reverse=True)
    if log_files:
        last_log = log_files[0]
        with open(last_log, "r", encoding="utf-8") as f:
            logs = json.load(f)
        tr_entries = [l for l in logs if l.get("artefato") == "TR" and "gerar_rascunho" in str(l)]
        if tr_entries:
            tr_data = tr_entries[-1].get("dados", {}).get("respostas")
            st.success("✅ Dados do TR carregados automaticamente.")
        else:
            st.info("Nenhum registro de TR encontrado nos logs.")
    else:
        st.info("Nenhum log encontrado.")
else:
    st.info("A pasta de logs ainda não foi criada.")

# ==========================================================
# Bloco 2 — Formulário Contrato
# ==========================================================
st.divider()
st.subheader("2️⃣ Dados Contratuais")

with st.form("form_contrato", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        objeto = st.text_area(
            "Objeto do contrato",
            value=tr_data.get("objeto", "") if tr_data else "",
            height=100,
        )
        partes = st.text_area(
            "Partes contratantes",
            placeholder="Ex.: O Tribunal de Justiça do Estado de São Paulo e a empresa XYZ Ltda.",
            height=80,
        )
        valor_global = st.text_input(
            "Valor global (R$)",
            value=tr_data.get("estimativa_final", "") if tr_data else "",
        )
        prazo_execucao = st.text_input(
            "Prazo de execução",
            value=tr_data.get("prazo_execucao", "") if tr_data else "",
        )
        vigencia = st.text_input(
            "Vigência contratual",
            placeholder="Ex.: 12 meses contados da assinatura.",
        )
    with col2:
        obrigacoes_contratada = st.text_area(
            "Obrigações da contratada",
            placeholder="Liste de forma resumida as principais obrigações do fornecedor.",
            height=120,
        )
        obrigacoes_contratante = st.text_area(
            "Obrigações da contratante",
            placeholder="Liste as obrigações do TJSP como contratante.",
            height=120,
        )
        garantias = st.text_area(
            "Garantias e penalidades",
            placeholder="Descreva as garantias exigidas e as penalidades aplicáveis.",
            height=100,
        )
        fiscalizacao = st.text_area(
            "Fiscalização e acompanhamento",
            placeholder="Identifique o servidor ou unidade responsável pelo acompanhamento do contrato.",
            height=80,
        )
        assinatura = st.text_area(
            "Assinaturas / Representantes",
            placeholder="Informe nomes, cargos e funções dos signatários.",
            height=80,
        )

    enviado = st.form_submit_button("Gerar rascunho do Contrato")

# ==========================================================
# Bloco 3 — Geração e visualização
# ==========================================================
if enviado:
    respostas_contrato = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "objeto": objeto,
        "partes": partes,
        "valor_global": valor_global,
        "prazo_execucao": prazo_execucao,
        "vigencia": vigencia,
        "obrigacoes_contratada": obrigacoes_contratada,
        "obrigacoes_contratante": obrigacoes_contratante,
        "garantias": garantias,
        "fiscalizacao": fiscalizacao,
        "assinatura": assinatura,
    }

    md = build_contrato_markdown(respostas_contrato, tr_data)
    save_log("CONTRATO", {"acao": "gerar_rascunho", "respostas": respostas_contrato})

    st.success("✅ Rascunho do Contrato gerado com sucesso.")
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
    filename_base = f"Contrato_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar para .docx"):
        markdown_to_docx(md, str(docx_path))
        save_log("CONTRATO", {"acao": "exportar_docx", "arquivo": str(docx_path.relative_to(base))})
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
    st.info("Preencha o formulário e clique em **Gerar rascunho do Contrato**.")
