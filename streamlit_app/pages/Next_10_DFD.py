# streamlit_app/pages/Next_10_DFD.py
# SynapseNext – Fase Brasília
# DFD → Form → Markdown → Validação IA → Exportação com/sugestões

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# Corrige path no Streamlit Cloud
sys.path.append(str(Path(__file__).resolve().parents[2]))

from utils.next_pipeline import (
    build_dfd_markdown,
    save_log,
    run_semantic_validation,
)
from utils.formatter_docx import markdown_to_docx

# -------------------------------------------------------------
# Configurações gerais da página
# -------------------------------------------------------------
st.set_page_config(page_title="SynapseNext – DFD", layout="wide")

st.title("DFD — Documento de Formalização da Demanda")
st.caption(
    "Formulário interativo para geração de rascunho institucional (Markdown), "
    "validação semântica e exportação em `.docx` (modo com/sugestões)."
)

st.divider()
st.subheader("1️⃣ Entrada – Formulário institucional")

# -------------------------------------------------------------
# Formulário
# -------------------------------------------------------------
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

# -------------------------------------------------------------
# Processamento
# -------------------------------------------------------------
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
    save_log("DFD", {"acao": "gerar_rascunho", "respostas": respostas})

    st.success("✅ Rascunho gerado com sucesso!")
    st.divider()

    # ---------------------------------------------------------
    # Preview Markdown
    # ---------------------------------------------------------
    st.subheader("2️⃣ Rascunho – Preview (Markdown)")
    st.markdown(md)
    st.divider()

    # ---------------------------------------------------------
    # Validação semântica (IA)
    # ---------------------------------------------------------
    st.subheader("3️⃣ Validação semântica (IA)")
    st.caption("Executa `validator_engine_vNext.validate_document(markdown_text, 'DFD', client)`.")
    if st.button("🚀 Executar validação semântica"):
        with st.spinner("Avaliando o DFD com o motor de validação semântica..."):
            try:
                result = run_semantic_validation("DFD", md)
            except Exception as e:
                st.error(f"Erro na validação: {e}")
                st.stop()

        rigid = float(result.get("rigid_score", 0.0))
        semantic = float(result.get("semantic_score", 0.0))
        rigid_result = result.get("rigid_result", [])
        semantic_result = result.get("semantic_result", [])
        guided_md = result.get("guided_markdown", "")
        guided_md_path = result.get("guided_markdown_path")

        c1, c2 = st.columns(2)
        c1.metric("Checklist rígido (presença obrigatória)", f"{rigid:.0f}%")
        c2.metric("Adequação semântica (qualidade do conteúdo)", f"{semantic:.0f}%")

        with st.expander("📋 Itens obrigatórios (checklist rígido)", expanded=False):
            st.write(rigid_result or "Sem dados retornados.")

        with st.expander("💬 Recomendações semânticas (IA)", expanded=True):
            st.write(semantic_result or "Sem recomendações retornadas.")

        if guided_md:
            st.markdown("#### 🧠 Rascunho Orientado (versão IA)")
            st.markdown(guided_md)
            if guided_md_path:
                st.info(f"Arquivo salvo em: `{guided_md_path}`")

        save_log("DFD", {"acao": "validar_semantico", "scores": {"rigid": rigid, "semantic": semantic}})

    # ---------------------------------------------------------
    # Exportação (modo com/sugestões)
    # ---------------------------------------------------------
    st.divider()
    st.subheader("4️⃣ Exportação – `.docx` (modo com/sugestões)")

    base = Path(__file__).resolve().parents[2]
    rascunhos_dir = base / "exports" / "rascunhos"
    rascunhos_dir.mkdir(parents=True, exist_ok=True)

    filename_base = f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    docx_clean = rascunhos_dir / f"{filename_base}_limpo.docx"
    docx_suggested = rascunhos_dir / f"{filename_base}_sugestoes.docx"

    modo = st.radio("Escolha o modo de exportação:", ["Sem sugestões (institucional)", "Com sugestões IA"])
    texto_export = md if modo == "Sem sugestões (institucional)" else result.get("guided_markdown", md)

    if st.button("📄 Gerar arquivo `.docx`"):
        markdown_to_docx(texto_export, str(docx_clean if modo == "Sem sugestões (institucional)" else docx_suggested))
        nome_final = docx_clean.name if modo == "Sem sugestões (institucional)" else docx_suggested.name
        caminho_final = rascunhos_dir / nome_final

        with open(caminho_final, "rb") as f:
            data = f.read()

        st.download_button(
            label=f"⬇️ Baixar {nome_final}",
            data=data,
            file_name=nome_final,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
        st.info(f"Arquivo salvo em: `exports/rascunhos/{nome_final}`")

else:
    st.info("Preencha o formulário e clique em **Gerar rascunho do DFD** para liberar a validação e exportação.")
