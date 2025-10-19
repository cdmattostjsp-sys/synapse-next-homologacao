# ==========================================================
# SynapseNext – Fase Brasília (Passo 9)
# TR → Form → Markdown → Validação IA → Exportação
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.next_pipeline import (
        build_tr_markdown,
        registrar_log,
        run_semantic_validation
    )
    from utils.formatter_docx import markdown_to_docx
except Exception as e:
    st.error(f"❌ Erro ao importar módulos utilitários: {e}")
    st.stop()

st.set_page_config(page_title="SynapseNext – TR", layout="wide")
st.title("TR — Termo de Referência")
st.caption("Geração de rascunho, validação semântica e exportação institucional (.docx)")

st.divider()
st.subheader("1️⃣ Entrada – Formulário institucional")

with st.form("form_tr", clear_on_submit=False):
    objeto = st.text_area("Objeto")
    justificativa = st.text_area("Justificativa")
    fundamentacao = st.text_area("Fundamentação legal")
    descricao = st.text_area("Descrição do objeto")
    obrigacoes = st.text_area("Obrigações das partes")
    prazos = st.text_area("Prazos e condições")
    criterios = st.text_area("Critérios de aceitação")
    custos = st.text_area("Estimativa de custos")
    submitted = st.form_submit_button("Gerar rascunho do TR")

if submitted:
    respostas = {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "objeto": objeto.strip(),
        "justificativa": justificativa.strip(),
        "fundamentacao": fundamentacao.strip(),
        "descricao": descricao.strip(),
        "obrigacoes": obrigacoes.strip(),
        "prazos": prazos.strip(),
        "criterios": criterios.strip(),
        "custos": custos.strip(),
    }

    md = build_tr_markdown(respostas)
    registrar_log("TR", "gerar_rascunho")

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

    registrar_log("TR", "validacao_semantica")

    # ==========================================================
    # Exportação
    # ==========================================================
    st.divider()
    st.subheader("4️⃣ Exportação – `.docx`")

    base = Path(__file__).resolve().parents[2]
    rascunhos_dir = base / "exports" / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)
    filename_base = f"TR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar para .docx"):
        markdown_to_docx(md, str(docx_path))
        registrar_log("TR", "exportar_docx")
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
