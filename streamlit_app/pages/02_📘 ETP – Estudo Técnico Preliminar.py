# ==========================================================
# 📘 SynapseNext – ETP (Estudo Técnico Preliminar)
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# 🔧 Configuração de paths e imports
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.next_pipeline import build_etp_markdown, registrar_log, run_semantic_validation
    from utils.formatter_docx import markdown_to_docx
    from utils.auditoria_pipeline import audit_event
    from utils.layout_institucional import exibir_cabecalho_institucional, exibir_rodape_institucional
    from utils.ui_style import aplicar_estilo_institucional
except Exception as e:
    st.error(f"Erro ao importar módulos utilitários: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – ETP", layout="wide", page_icon="📘")
aplicar_estilo_institucional()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_institucional(
    "ETP – Estudo Técnico Preliminar",
    "Módulo de elaboração institucional com trilha de auditoria e validação IA"
)

# ==========================================================
# 📘 Formulário de entrada
# ==========================================================
st.subheader("1️⃣ Entrada – Formulário institucional")

with st.form("form_etp", clear_on_submit=False):
    descricao = st.text_area("Descrição da necessidade")
    motivacao = st.text_area("Motivação da contratação")
    custos = st.text_area("Estimativa de custos e fontes de recurso")
    solucoes = st.text_area("Soluções avaliadas (inclusive inviáveis)")
    analise = st.text_area("Resultado da análise comparativa e justificativa da escolha")
    submitted = st.form_submit_button("Gerar rascunho do ETP")

# ==========================================================
# 🧾 Geração do rascunho e validação
# ==========================================================
if submitted:
    respostas = {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "descricao": descricao.strip(),
        "motivacao": motivacao.strip(),
        "custos": custos.strip(),
        "solucoes": solucoes.strip(),
        "analise": analise.strip(),
    }

    md = build_etp_markdown(respostas)
    registrar_log("ETP", "gerar_rascunho")
    audit_event("ETP", "gerar_rascunho", md)

    st.success("✅ Rascunho gerado com sucesso!")
    st.divider()

    st.subheader("2️⃣ Rascunho – Preview")
    st.markdown(md)

    # ======================================================
    # 🔍 Validação semântica
    # ======================================================
    st.divider()
    st.subheader("3️⃣ Validação Semântica – IA TJSP")
    with st.spinner("Executando análise semântica..."):
        resultado = run_semantic_validation(md)

    if "erro" in resultado and resultado["erro"]:
        st.error(f"⚠️ Erro na validação: {resultado['erro']}")
    else:
        st.markdown(f"**🪶 Resumo:** {resultado.get('resumo', '')}")
        st.markdown(f"**📊 Pontuação:** {resultado.get('pontuacao', 0)}%")
        if resultado.get("sugestoes"):
            st.markdown("### 💡 Sugestões de melhoria:")
            for s in resultado["sugestoes"]:
                st.markdown(f"- {s}")

    registrar_log("ETP", "validacao_semantica")
    audit_event("ETP", "validacao_semantica", md, meta={"pontuacao": resultado.get("pontuacao", 0)})

    # ======================================================
    # 📤 Exportação para DOCX
    # ======================================================
    st.divider()
    st.subheader("4️⃣ Exportação – `.docx`")

    base = Path(__file__).resolve().parents[2]
    rascunhos_dir = base / "exports" / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)
    filename_base = f"ETP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar para .docx"):
        markdown_to_docx(md, str(docx_path))
        registrar_log("ETP", "exportar_docx")
        audit_event("ETP", "exportar_docx", md, meta={"arquivo": docx_path.name})

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
    st.info("Preencha o formulário e clique em **Gerar rascunho do ETP** para iniciar o processo.")

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
exibir_rodape_institucional()
