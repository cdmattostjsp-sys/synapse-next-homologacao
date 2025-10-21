# ==========================================================
# 📑 SynapseNext – TR (Termo de Referência)
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# 🔧 Ajuste de path e imports institucionais
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# 📦 Importa módulos funcionais
try:
    from utils.next_pipeline import build_tr_markdown, registrar_log, run_semantic_validation
    from utils.formatter_docx import markdown_to_docx
    from utils.auditoria_pipeline import audit_event
except Exception as e:
    st.error(f"Erro ao importar módulos utilitários: {e}")
    st.stop()

# 📦 Importa novo estilo institucional unificado
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    st.warning("⚠️ Módulo ui_components não encontrado. O estilo não será aplicado.")
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(
    page_title="TR – Termo de Referência",
    layout="wide",
    page_icon="📑"
)
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "TR – Termo de Referência",
    "Módulo de elaboração assistida e controle de coerência técnica"
)
st.divider()

# ==========================================================
# 🧩 Formulário de entrada
# ==========================================================
st.subheader("1️⃣ Entrada – Formulário institucional")

with st.form("form_tr", clear_on_submit=False):
    objeto = st.text_area("Objeto da contratação")
    justificativa = st.text_area("Justificativa da contratação")
    fundamentacao = st.text_area("Fundamentação legal e normativa")
    descricao = st.text_area("Descrição detalhada do objeto e metodologia de execução")
    obrigacoes = st.text_area("Obrigações da Administração e do contratado")
    prazos = st.text_area("Prazos e condições de execução")
    criterios = st.text_area("Critérios de aceitação e avaliação")
    custos = st.text_area("Estimativa de custos e fonte de recursos")
    submitted = st.form_submit_button("Gerar rascunho do TR")

# ==========================================================
# 🧾 Geração do rascunho e validação
# ==========================================================
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
    audit_event("TR", "gerar_rascunho", md, meta={"usuario": "Sistema", "versao": "Fase Brasília"})

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

    registrar_log("TR", "validacao_semantica")
    audit_event("TR", "validacao_semantica", md, meta={"pontuacao": resultado.get("pontuacao", 0)})

    # ======================================================
    # 📤 Exportação para DOCX
    # ======================================================
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
        audit_event("TR", "exportar_docx", md, meta={"arquivo": docx_path.name})

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
    st.info("Preencha o formulário e clique em **Gerar rascunho do TR** para iniciar o processo.")

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption("SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)")
