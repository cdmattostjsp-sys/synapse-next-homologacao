import os
from datetime import datetime
import streamlit as st

from utils.parser_pdf import extract_text_from_pdf, summarize_text
from utils.formatter_docx import markdown_to_docx

# ===========================================
# 🔧 CONFIGURAÇÕES INICIAIS
# ===========================================

st.set_page_config(
    page_title="SynapseNext – Analisador de Artefatos",
    layout="wide",
    page_icon="🧭"
)

st.title("🧭 SynapseNext — Ambiente de Processamento de Artefatos")
st.markdown("""
O **SynapseNext** faz parte do Ecossistema **SAAB 5.0** e permite processar documentos 
de forma automatizada, a partir de PDFs ou textos extraídos, aplicando validação semântica,
formatação institucional e geração automática em formato `.docx`.

---
""")

# ===========================================
# 📂 UPLOAD DE DOCUMENTOS
# ===========================================

st.header("📄 Envio e Extração de Documentos (PDF)")
st.markdown("Envie um ou mais arquivos PDF que contenham as informações do processo administrativo ou da fase interna da contratação.")

uploaded_files = st.file_uploader(
    "Selecione os arquivos PDF...",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} arquivo(s) carregado(s). Clique abaixo para processar.")

    if st.button("🚀 Processar Documentos"):
        for file in uploaded_files:
            with st.spinner(f"Processando {file.name}..."):
                result = extract_text_from_pdf(file)

                if result["success"]:
                    st.success(f"✅ {file.name} processado com sucesso!")

                    # Exibir metadados detectados
                    st.subheader("📌 Metadados Identificados")
                    st.json(result["metadata"])

                    # Exibir trecho do texto extraído
                    st.subheader("🧾 Prévia do Conteúdo Extraído")
                    st.text_area(
                        label="Trecho do Documento",
                        value=summarize_text(result["text"]),
                        height=200
                    )

                    # Gerar documento Word padronizado
                    st.subheader("💾 Exportar Documento Formatado")
                    buffer, path = markdown_to_docx(
                        markdown_text=result["text"],
                        title=f"Rascunho {file.name}",
                        summary="Documento processado automaticamente a partir de upload PDF via SynapseNext."
                    )

                    st.download_button(
                        label="⬇️ Baixar DOCX formatado",
                        data=buffer,
                        file_name=os.path.basename(path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                    st.divider()

                else:
                    st.error(f"Erro ao processar {file.name}: {result['error']}")
else:
    st.warning("⚠️ Nenhum arquivo carregado. Por favor, envie um PDF para iniciar o processamento.")

# ===========================================
# ℹ️ RODAPÉ INSTITUCIONAL
# ===========================================

st.divider()
st.markdown("""
**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
Secretaria de Administração e Abastecimento (SAAB) – Projeto Synapse.IA  
Desenvolvido em ambiente experimental • Uso restrito institucional.
""")
