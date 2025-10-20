# ==========================================================
# SynapseNext – DFD (Documento de Formalização da Demanda)
# Fase Brasília – Passo 10A (com integração Auditoria.IA)
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# Ajuste de path para importações
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.next_pipeline import build_dfd_markdown, registrar_log, run_semantic_validation
    from utils.formatter_docx import markdown_to_docx
    from utils.auditoria_pipeline import audit_event
except Exception as e:
    st.error(f"Erro ao importar módulos utilitários: {e}")
    st.stop()

# Configuração da página
st.set_page_config(page_title="SynapseNext – DFD", layout="wide")
st.title("DFD — Documento de Formalização da Demanda")
st.caption("Preenchimento institucional, validação IA e trilha de auditoria.")

# Formulário de entrada
st.divider()
st.subheader("1️⃣ Entrada – Formulário institucional")

with st.form("form_dfd", clear_on_submit=False):
    unidade = st.text_input("Unidade solicitante")
    responsavel = st.text_input("Responsável pela demanda")
    objeto = st.text_area("Objeto da contratação")
    justificativa = st.text_area("Justificativa da necessidade")
    quantidade = st.text_area("Quantidade e escopo")
    urgencia = st.text_area("Grau de urgência")
    riscos = st.text_area("Riscos identificados")
    alinhamento = st.text_area("Alinhamento estratégico")
    submitted = st.form_submit_button("Gerar rascunho do DFD")

if submitted:
    respostas = {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "unidade": unidade.strip(),
        "responsavel": responsavel.strip(),
        "objeto": objeto.strip(),
        "justificativa": justificativa.strip(),
        "quantidade": quantidade.strip(),
        "urgencia": urgencia.strip(),
        "riscos": riscos.strip(),
        "alinhamento": alinhamento.strip(),
    }

    md = build_dfd_markdown(respostas)
    registrar_log("DFD", "gerar_rascunho")
    audit_event("DFD", "gerar_rascunho", md, meta={"usuario": "Sistema", "versao": "Fase Brasília"})

    st.success("✅ Rascunho gerado com sucesso!")
    st.divider()
    st.subheader("2️⃣ Rascunho – Preview")
    st.markdown(md)

    # Validação IA
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
    audit_event("DFD", "validacao_semantica", md, meta={"pontuacao": resultado.get("pontuacao", 0)})

    # Exportação DOCX
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
        audit_event("DFD", "exportar_docx", md, meta={"arquivo": docx_path.name})

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
