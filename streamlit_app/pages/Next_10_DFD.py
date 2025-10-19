# ==========================================================
# SynapseNext – Fase Brasília
# DFD → Form → Markdown → Validação IA → Exportação com/sugestões
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# Correção de caminho robusta (local e cloud)
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.next_pipeline import (
        build_dfd_markdown,
        registrar_log,
        run_semantic_validation,
    )
    from utils.formatter_docx import markdown_to_docx
except Exception as e:
    st.error(f"❌ Erro ao importar módulos utilitários: {e}")
    st.stop()

# ==========================================================
# Configurações gerais
# ==========================================================
st.set_page_config(page_title="SynapseNext – DFD", layout="wide")

st.title("DFD — Documento de Formalização da Demanda")
st.caption(
    "Formulário interativo para geração de rascunho institucional (Markdown), "
    "validação semântica e exportação em `.docx` (modo com/sugestões)."
)

# ==========================================================
# Bloco 1 – Formulário institucional
# ==========================================================
st.divider()
st.subheader("1️⃣ Entrada – Formulário institucional")

with st.form("form_dfd", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        unidade = st.text_input("Unidade solicitante", placeholder="Ex.: Fórum de Sorocaba / Secretaria do Foro")
        responsavel = st.text_input("Responsável pelo pedido", placeholder="Ex.: Carlos Darwin de Mattos (cargo/setor)")
        objeto = st.text_input("Objeto da contratação", placeholder="Ex.: Fornecimento de água mineral em garrafões")
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

# ==========================================================
# Bloco 2 – Processamento
# ==========================================================
if submitted:
    respostas = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "unidade": unidade.strip(),
        "responsavel": responsavel.strip(),
        "objeto": objeto.strip(),
        "quantidade_escopo": quantidade_escopo.strip(),
        "justificativa": justificativa.strip(),
        "urgencia": urgencia,
        "riscos": riscos.strip(),
        "alinhamento": alinhamento.strip(),
        "anexos": [f.name for f in anexos] if anexos else [],
    }

    md = build_dfd_markdown(respostas)
    registrar_log("DFD", "gerar_rascunho")

    st.success("✅ Rascunho gerado com sucesso!")
    st.divider()

    # ----------------------------------------------------------
    # Preview Markdown
    # ----------------------------------------------------------
    st.subheader("2️⃣ Rascunho – Preview (Markdown)")
    st.markdown(md)
    st.divider()

    # ----------------------------------------------------------
    # Exportação .docx
    # ----------------------------------------------------------
    st.divider()
    st.subheader("4️⃣ Exportação – `.docx`")

    base = Path(__file__).resolve().parents[2]
    rascunhos_dir = base / "exports" / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)

    filename_base = f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar para .docx"):
        markdown_to_docx(md, str(docx_path))
        registrar_log("DFD", "exportar_docx")
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
    st.info("Preencha o formulário e clique em **Gerar rascunho do DFD**.")
