# ==========================================================
# 📜 SynapseNext – Minuta do Edital
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
    from utils.next_pipeline import build_edital_markdown, registrar_log, run_semantic_validation
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
st.set_page_config(page_title="SynapseNext – Minuta do Edital", page_icon="📜", layout="wide")
aplicar_estilo_institucional()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_institucional(
    "Minuta do Edital",
    "Módulo de elaboração, validação IA e exportação institucional"
)

# ==========================================================
# 🧩 Formulário de entrada
# ==========================================================
st.subheader("1️⃣ Entrada – Formulário Institucional")

with st.form("form_edital", clear_on_submit=False):
    modalidade = st.selectbox(
        "Modalidade de licitação",
        ["Pregão Eletrônico", "Concorrência", "Dispensa de Licitação", "Inexigibilidade", "Outros"],
        index=0
    )
    objeto = st.text_area("Objeto do certame")
    justificativa = st.text_area("Justificativa da escolha da modalidade e critérios adotados")
    fundamentacao = st.text_area("Fundamentação legal e normativa (Lei nº 14.133/21, art. 54 e seguintes)")
    criterios = st.text_area("Critérios de julgamento e habilitação")
    prazos = st.text_area("Prazos de entrega e execução contratual")
    recursos = st.text_area("Fontes de recursos e estimativas orçamentárias")
    penalidades = st.text_area("Penalidades e sanções administrativas aplicáveis")
    assinatura = st.text_input("Responsável pela elaboração (nome e cargo)")
    submitted = st.form_submit_button("Gerar minuta do Edital")

# ==========================================================
# 🧾 Geração e validação
# ==========================================================
if submitted:
    respostas = {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "modalidade": modalidade,
        "objeto": objeto.strip(),
        "justificativa": justificativa.strip(),
        "fundamentacao": fundamentacao.strip(),
        "criterios": criterios.strip(),
        "prazos": prazos.strip(),
        "recursos": recursos.strip(),
        "penalidades": penalidades.strip(),
        "assinatura": assinatura.strip(),
    }

    md = build_edital_markdown(respostas)
    registrar_log("MINUTA_EDITAL", "gerar_minuta")
    audit_event("MINUTA_EDITAL", "gerar_minuta", md, meta={"usuario": assinatura, "modalidade": modalidade})

    st.success("✅ Minuta do edital gerada com sucesso!")
    st.divider()

    st.subheader("2️⃣ Minuta – Pré-visualização")
    st.markdown(md)

    # ======================================================
    # 🔍 Validação semântica
    # ======================================================
    st.divider()
    st.subheader("3️⃣ Validação Semântica – IA TJSP")
    with st.spinner("Executando validação semântica..."):
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

    registrar_log("MINUTA_EDITAL", "validacao_semantica")
    audit_event("MINUTA_EDITAL", "validacao_semantica", md, meta={"pontuacao": resultado.get("pontuacao", 0)})

    # ======================================================
    # 📤 Exportação DOCX
    # ======================================================
    st.divider()
    st.subheader("4️⃣ Exportação – `.docx`")

    base = Path(__file__).resolve().parents[2]
    rascunhos_dir = base / "exports" / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)
    filename_base = f"MINUTA_EDITAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_path = rascunhos_dir / f"{filename_base}.docx"

    if st.button("📄 Exportar para .docx"):
        markdown_to_docx(md, str(docx_path))
        registrar_log("MINUTA_EDITAL", "exportar_docx")
        audit_event("MINUTA_EDITAL", "exportar_docx", md, meta={"arquivo": docx_path.name})

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
    st.info("Preencha o formulário e clique em **Gerar minuta do Edital** para iniciar o processo.")

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
exibir_rodape_institucional()
