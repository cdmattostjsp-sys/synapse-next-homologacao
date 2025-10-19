# streamlit_app/pages/Next_10_DFD.py
# SynapseNext – Fase Brasília
# DFD → Entrada (form) → Rascunho (markdown) → Exportação (.docx)

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ============================================================
# Corrige o caminho de importação para execução no Streamlit Cloud
# ============================================================
sys.path.append(str(Path(__file__).resolve().parents[2]))  # sobe 2 níveis até a raiz

from utils.next_pipeline import build_dfd_markdown, save_log
from utils.formatter_docx import markdown_to_docx

# ============================================================
# Configurações de página
# ============================================================
st.set_page_config(page_title="SynapseNext – DFD", layout="wide")

# ============================================================
# Cabeçalho institucional
# ============================================================
st.title("DFD — Documento de Formalização da Demanda")
st.caption(
    "Preencha o formulário com as informações essenciais, gere o rascunho institucional "
    "em formato Markdown e exporte para `.docx` com registro automático em logs."
)

st.divider()
st.subheader("1️⃣ Entrada – Formulário institucional")

# ============================================================
# Formulário de entrada
# ============================================================
with st.form("form_dfd", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        unidade = st.text_input(
            "Unidade solicitante",
            placeholder="Ex.: Fórum de Sorocaba / Secretaria do Foro",
            max_chars=200,
        )
        responsavel = st.text_input(
            "Responsável pelo pedido",
            placeholder="Ex.: Carlos Darwin de Mattos (cargo/setor)",
            max_chars=200,
        )
        objeto = st.text_input(
            "Objeto da contratação",
            placeholder="Ex.: Fornecimento de água mineral em garrafões",
            max_chars=200,
        )
        quantidade_escopo = st.text_area(
            "Quantidade / Escopo (resumo objetivo)",
            placeholder="Ex.: 500 garrafões de 20L/mês, abrangendo 12 prédios da RAJ X.",
            height=120,
        )
    with col2:
        justificativa = st.text_area(
            "Justificativa da necessidade",
            placeholder=(
                "Ex.: Garantir abastecimento contínuo de água potável aos servidores e jurisdicionados."
            ),
            height=120,
        )
        urgencia = st.selectbox("Urgência", ["Sem urgência", "Baixa", "Média", "Alta"], index=0)
        riscos = st.text_area(
            "Riscos identificados (se houver)",
            placeholder="Ex.: desabastecimento, atraso logístico, não conformidade sanitária.",
            height=120,
        )
        alinhamento = st.text_area(
            "Alinhamento institucional",
            placeholder="Ex.: Alinhado ao planejamento estratégico, sustentabilidade e bem-estar.",
            height=120,
        )

    anexos = st.file_uploader(
        "Anexos (opcional, múltiplos arquivos)", accept_multiple_files=True
    )

    submitted = st.form_submit_button("Gerar rascunho do DFD")

# ============================================================
# Processamento após envio do formulário
# ============================================================
if submitted:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    respostas = {
        "timestamp": ts,
        "unidade": unidade.strip() if unidade else "",
        "responsavel": responsavel.strip() if responsavel else "",
        "objeto": objeto.strip() if objeto else "",
        "quantidade_escopo": quantidade_escopo.strip() if quantidade_escopo else "",
        "justificativa": justificativa.strip() if justificativa else "",
        "urgencia": urgencia,
        "riscos": riscos.strip() if riscos else "",
        "alinhamento": alinhamento.strip() if alinhamento else "",
        "anexos": [f.name for f in anexos] if anexos else [],
    }

    # Gera o markdown institucional do DFD
    md = build_dfd_markdown(respostas)
    save_log("DFD", {"acao": "gerar_rascunho", "respostas": respostas})

    st.success("✅ Rascunho gerado com sucesso.")
    st.divider()

    # ============================================================
    # Preview do Markdown
    # ============================================================
    st.subheader("2️⃣ Rascunho – Visualização (Markdown)")
    st.markdown(md)
    st.divider()

    # ============================================================
    # Exportação do DFD para .docx
    # ============================================================
    st.subheader("3️⃣ Exportação – Gerar arquivo `.docx`")

    base = Path(__file__).resolve().parents[2]
    exports_dir = base / "exports"
    rascunhos_dir = exports_dir / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)

    filename_base = f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar rascunho para .docx"):
        try:
            markdown_to_docx(md, str(docx_path))
        except TypeError:
            markdown_to_docx(markdown=md, output_path=str(docx_path))

        save_log("DFD", {"acao": "exportar_docx", "arquivo": str(docx_path.relative_to(base))})

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

    # ============================================================
    # Placeholder para Validação Semântica (Passo 2)
    # ============================================================
    st.divider()
    st.subheader("4️⃣ Validação Semântica (em desenvolvimento)")
    st.info(
        "O módulo de **validação semântica** será acoplado no próximo passo, "
        "integrando o motor `validator_engine_vNext` para análise automatizada de conformidade."
    )

else:
    st.info("Preencha o formulário e clique em **Gerar rascunho do DFD** para iniciar o processamento.")
