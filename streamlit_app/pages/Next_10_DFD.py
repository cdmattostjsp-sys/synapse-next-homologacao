# streamlit_app/pages/Next_10_DFD.py
# DFD — Entrada (form) → Rascunho (markdown) → Exportação (.docx)
# Requisitos deste passo:
# - sem validação semântica ainda (Passo 2)
# - usar utils/formatter_docx.markdown_to_docx
# - gerar logs mínimos em exports/logs
# - salvar rascunho em exports/rascunhos

import streamlit as st
from datetime import datetime
from io import BytesIO
from pathlib import Path
import json

from utils.next_pipeline import build_dfd_markdown, save_log  # funções puras deste passo
from utils.formatter_docx import markdown_to_docx  # exportação .docx

st.set_page_config(page_title="SynapseNext – DFD", layout="wide")

# ==================================
# Cabeçalho institucional
# ==================================
st.title("DFD — Documento de Formalização da Demanda")
st.caption("Preencha o formulário com as informações essenciais. Gere o rascunho em Markdown e exporte para `.docx`.")

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
        quantidade_escopo = st.text_area("Quantidade / Escopo (resumo objetivo)",
                                         placeholder="Ex.: 500 garrafões de 20L/mês, abrangendo 12 prédios da RAJ X.",
                                         height=120)
    with col2:
        justificativa = st.text_area("Justificativa da necessidade",
                                     placeholder="Ex.: Garantir abastecimento contínuo de água potável aos servidores e jurisdicionados.",
                                     height=120)
        urgencia = st.selectbox("Urgência", ["Sem urgência", "Baixa", "Média", "Alta"], index=0)
        riscos = st.text_area("Riscos identificados (se houver)",
                              placeholder="Ex.: risco de desabastecimento, atraso logístico, não conformidade com normas sanitárias.",
                              height=120)
        alinhamento = st.text_area("Alinhamento institucional",
                                   placeholder="Ex.: Ação alinhada ao planejamento estratégico, sustentabilidade e bem-estar.",
                                   height=120)

    anexos = st.file_uploader("Anexos (opcional, múltiplos arquivos)", accept_multiple_files=True)

    submitted = st.form_submit_button("Gerar rascunho do DFD")

# ==================================
# Processamento
# ==================================
if submitted:
    # Monta o dicionário de respostas
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    respostas = {
        "timestamp": ts,
        "unidade": unidade.strip(),
        "responsavel": responsavel.strip(),
        "objeto": objeto.strip(),
        "quantidade_escopo": quantidade_escopo.strip(),
        "justificativa": justificativa.strip(),
        "urgencia": urgencia,
        "riscos": riscos.strip(),
        "alinhamento": alinhamento.strip(),
        "anexos": [f.name for f in anexos] if anexos else []
    }

    # Gera markdown institucional a partir das respostas
    md = build_dfd_markdown(respostas)

    # Salva log mínimo (JSON simples) em exports/logs
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

    # Define caminhos de saída
    base = Path(__file__).resolve().parents[2]  # .../synapse-next
    exports_dir = base / "exports"
    rascunhos_dir = exports_dir / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)

    filename_base = f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    # Botão para exportar diretamente para o diretório e oferecer download
    if st.button("Exportar para .docx"):
        # Usa o utilitário institucional de exportação
        try:
            markdown_to_docx(md, str(docx_path))
        except TypeError:
            # Fallback: caso a assinatura do utilitário no seu projeto seja diferente
            # tente uma chamada alternativa comum (ex.: markdown_to_docx(markdown=md, output_path=str(docx_path)))
            markdown_to_docx(markdown=md, output_path=str(docx_path))

        save_log("DFD", {"acao": "exportar_docx", "arquivo": str(docx_path.relative_to(base))})

        # Oferece o arquivo para download imediato
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

else:
    st.info("Preencha o formulário e clique em **Gerar rascunho do DFD** para visualizar o preview e liberar a exportação.")
