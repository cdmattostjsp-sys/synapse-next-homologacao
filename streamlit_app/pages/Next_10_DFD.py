# streamlit_app/pages/Next_10_DFD.py
# DFD — Entrada (form) → Rascunho (markdown) → Exportação (.docx) → Validação semântica

import sys
from pathlib import Path
# .../synapse-next/streamlit_app/pages/Next_10_DFD.py -> sobe 2 níveis até a raiz
sys.path.append(str(Path(__file__).resolve().parents[2]))

import streamlit as st
from datetime import datetime

from utils.next_pipeline import (
    build_dfd_markdown,
    save_log,
    run_semantic_validation,  # Passo 2: integração de validação
)
from utils.formatter_docx import markdown_to_docx

st.set_page_config(page_title="SynapseNext – DFD", layout="wide")

# ==================================
# Cabeçalho institucional
# ==================================
st.title("DFD — Documento de Formalização da Demanda")
st.caption(
    "Preencha o formulário com as informações essenciais. "
    "Gere o rascunho em Markdown, exporte para `.docx` e execute a **validação semântica**."
)

st.divider()
st.subheader("1) Entrada – Formulário institucional")

# ==================================
# Formulário
# ==================================
with st.form("form_dfd", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        unidade = st.text_input("Unidade solicitante", placeholder="Ex.: Fórum de Sorocaba / Secretaria do Foro", max_chars=200)
        responsavel = st.text_input("Responsável pelo pedido", placeholder="Ex.: Carlos Darwin de Mattos (cargo/setor)", max_chars=200)
        objeto = st.text_input("Objeto da contratação", placeholder="Ex.: Fornecimento de água mineral em garrafões", max_chars=200)
        quantidade_escopo = st.text_area(
            "Quantidade / Escopo (resumo objetivo)",
            placeholder="Ex.: 500 garrafões de 20L/mês, abrangendo 12 prédios da RAJ X.",
            height=120
        )
    with col2:
        justificativa = st.text_area(
            "Justificativa da necessidade",
            placeholder="Ex.: Garantir abastecimento contínuo de água potável aos servidores e jurisdicionados.",
            height=120
        )
        urgencia = st.selectbox("Urgência", ["Sem urgência", "Baixa", "Média", "Alta"], index=0)
        riscos = st.text_area(
            "Riscos identificados (se houver)",
            placeholder="Ex.: desabastecimento, atraso logístico, não conformidade sanitária.",
            height=120
        )
        alinhamento = st.text_area(
            "Alinhamento institucional",
            placeholder="Ex.: Alinhado ao planejamento estratégico, sustentabilidade e bem-estar.",
            height=120
        )

    anexos = st.file_uploader("Anexos (opcional, múltiplos arquivos)", accept_multiple_files=True)

    submitted = st.form_submit_button("Gerar rascunho do DFD")

# ==================================
# Processamento
# ==================================
if submitted:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    respostas = {
        "timestamp": ts,
        "unidade": (unidade or "").strip(),
        "responsavel": (responsavel or "").strip(),
        "objeto": (objeto or "").strip(),
        "quantidade_escopo": (quantidade_escopo or "").strip(),
        "justificativa": (justificativa or "").strip(),
        "urgencia": urgencia,
        "riscos": (riscos or "").strip(),
        "alinhamento": (alinhamento or "").strip(),
        "anexos": [f.name for f in anexos] if anexos else [],
    }

    md = build_dfd_markdown(respostas)
    save_log("DFD", {"acao": "gerar_rascunho", "respostas": respostas})

    st.success("Rascunho gerado com sucesso.")
    st.divider()

    # ============================
    # Rascunho – Preview Markdown
    # ============================
    st.subheader("2) Rascunho – Preview (Markdown)")
    st.markdown(md)

    st.divider()
    st.subheader("3) Exportação – `.docx`")

    base = Path(__file__).resolve().parents[2]  # .../synapse-next
    exports_dir = base / "exports"
    rascunhos_dir = exports_dir / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)

    filename_base = f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("Exportar para .docx"):
        try:
            markdown_to_docx(md, str(docx_path))
        except TypeError:
            markdown_to_docx(markdown=md, output_path=str(docx_path))
        save_log("DFD", {"acao": "exportar_docx", "arquivo": str(docx_path.relative_to(base))})
        with open(docx_path, "rb") as f:
            data = f.read()
        st.download_button(
            label="Baixar arquivo .docx",
            data=data,
            file_name=docx_path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        st.info(f"Arquivo salvo em: `exports/rascunhos/{docx_path.name}`")

    # ==========================================
    # Passo 2 — Validação semântica (integração)
    # ==========================================
    st.divider()
    st.subheader("4) Validação semântica")

    st.caption(
        "Executa `validator_engine_vNext.validate_document(markdown_text, 'DFD', client)` "
        "e exibe o sumário de conformidade e recomendações."
    )

    if st.button("Executar validação semântica"):
        try:
            result = run_semantic_validation("DFD", md)  # encapsula cliente e logs
        except Exception as e:
            st.error(f"Falha na validação: {e}")
            st.stop()

        rigid = float(result.get("rigid_score", 0.0))
        semantic = float(result.get("semantic_score", 0.0))
        rigid_result = result.get("rigid_result", [])
        semantic_result = result.get("semantic_result", [])
        guided_md = result.get("guided_markdown", "")
        guided_md_path = result.get("guided_markdown_path")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Checklist rígido (presença obrigatória)", f"{rigid:.0f}%")
        with c2:
            st.metric("Adequação semântica (qualidade do conteúdo)", f"{semantic:.0f}%")

        with st.expander("📋 Detalhamento — Itens rígidos (checklist)", expanded=False):
            st.write(rigid_result or "Sem dados retornados para o checklist rígido.")

        with st.expander("🧠 Recomendações — Avaliação semântica", expanded=True):
            st.write(semantic_result or "Sem dados retornados para a avaliação semântica.")

        with st.expander("📝 Rascunho Orientado (guided_markdown)", expanded=False):
            if guided_md:
                st.markdown(guided_md)
                if guided_md_path:
                    st.info(f"Arquivo salvo em: `{guided_md_path}`")
            else:
                st.write("O motor não retornou guided_markdown.")

else:
    st.info("Preencha o formulário e clique em **Gerar rascunho do DFD** para liberar exportação e validação.")
