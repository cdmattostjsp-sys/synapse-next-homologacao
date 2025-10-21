# ==========================================================
# 📊 SynapseNext – ETP (Estudo Técnico Preliminar)
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
    from utils.next_pipeline import build_etp_markdown, registrar_log, run_semantic_validation
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
    page_title="ETP – Estudo Técnico Preliminar",
    layout="wide",
    page_icon="📊"
)
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "ETP – Estudo Técnico Preliminar",
    "Módulo de apoio técnico e integração com base de requisitos"
)
st.divider()

# ==========================================================
# 📘 Conteúdo funcional
# ==========================================================
st.subheader("1️⃣ Entrada – Formulário do ETP")

with st.form("form_etp", clear_on_submit=False):
    unidade = st.text_input("Unidade solicitante")
    responsavel = st.text_input("Responsável técnico")
    objeto = st.text_area("Objeto da contratação")
    justificativa = st.text_area("Justificativa da necessidade")
    alternativas = st.text_area("Alternativas de solução avaliadas")
    impacto = st.text_area("Impacto esperado da contratação")
    riscos = st.text_area("Riscos associados")
    sustentabilidade = st.text_area("Critérios de sustentabilidade")
    resultado = st.text_area("Resultados pretendidos")
    submitted = st.form_submit_button("Gerar rascunho do ETP")

if submitted:
    respostas = {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "unidade": unidade.strip(),
        "responsavel": responsavel.strip(),
        "objeto": objeto.strip(),
        "justificativa": justificativa.strip(),
        "alternativas": alternativas.strip(),
        "impacto": impacto.strip(),
        "riscos": riscos.strip(),
        "sustentabilidade": sustentabilidade.strip(),
        "resultado": resultado.strip(),
    }

    md = build_etp_markdown(respostas)
    registrar_log("ETP", "gerar_rascunho")
    audit_event("ETP", "gerar_rascunho", md, meta={"usuario": "Sistema", "versao": "Fase Brasília"})

    st.success("✅ Rascunho gerado com sucesso!")
    st.divider()
    st.subheader("2️⃣ Rascunho – Preview")
    st.markdown(md)

    # ======================================================
    # 🔍 Validação IA
    # ======================================================
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

    registrar_log("ETP", "validacao_semantica")
    audit_event("ETP", "validacao_semantica", md, meta={"pontuacao": resultado.get("pontuacao", 0)})

    # ======================================================
    # 📤 Exportação DOCX
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
    st.info("Preencha o formulário e clique em **Gerar rascunho do ETP**.")

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption("SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)")

