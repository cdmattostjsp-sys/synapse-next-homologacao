# ==========================================================
# SynapseNext – Fase Brasília (Passo 9)
# DFD → Form → Markdown → Validação IA → Exportação
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# Caminho e importações
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.next_pipeline import (
        build_dfd_markdown,
        registrar_log,
        run_semantic_validation
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
st.caption("Geração de rascunho, validação semântica e exportação institucional (.docx)")

# ==========================================================
# Formulário
# ==========================================================
st.divider()
st.subheader("1️⃣ Entrada – Formulário institucional")

with st.form("form_dfd", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        unidade = st.text_input("Unidade solicitante")
        responsavel = st.text_input("Responsável pelo pedido")
        objeto = st.text_input("Objeto da contratação")
        quantidade_escopo = st.text_area("Quantidade / Escopo")
    with col2:
        justificativa = st.text_area("Justificativa da necessidade")
        urgencia = st.selectbox("Urgência", ["Sem urgência", "Baixa", "Média", "Alta"])
        riscos = st.text_area("Riscos identificados (se houver)")
        alinhamento = st.text_area("Alinhamento institucional")
    anexos = st.file_uploader("Anexos (opcional)", accept_multiple_files=True)
    submitted = st.form_submit_button("Gerar rascunho do DFD")

# ==========================================================
# Processamento
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
    st.subheader("2️⃣ Rascunho – Preview")
    st.markdown(md)

    # ==========================================================
    # Validação IA
    # ==========================================================
    st.divider()
    st.subheader("3️⃣ Validação Semântica – IA TJSP")

    with st.spinner("Executando análise semântica..."):
        resultado = run_semantic_validation(md)

    if "erro" in resultado and resultado["erro"]:
        st.error(f"⚠️ Erro ao validar o documento: {resultado['erro']}")
    else:
        st.markdown(f"**🪶 Resumo:** {resultado.get('resumo', '')}")
        st.markdown(f"**📊 Pontuação:** {resultado.get('pontuacao', 0)}%")
        if resultado.get("sugestoes"):
            st.markdown("### 💡 Sugestões de melhoria:")
            for s in resultado["sugestoes"]:
                st.markdown(f"- {s}")

    registrar_log("DFD", "validacao_semantica")

    # ==========================================================
    # Exportação
    # ==========================================================
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
