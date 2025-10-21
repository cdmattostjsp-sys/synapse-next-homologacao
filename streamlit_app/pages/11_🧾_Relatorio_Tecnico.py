# ==========================================================
# SynapseNext – Fase Brasília (Passo 10C)
# Relatório Técnico Consolidado — Interface Streamlit
# ==========================================================
# Consolida Auditoria.IA + Validação IA + Comparador.IA
# Gera .docx institucional para anexação no processo.
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# -----------------------------
# Setup de caminhos e imports
# -----------------------------
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.relatorio_consolidado_pipeline import coletar_dados_relatorio, gerar_relatorio_docx
except Exception as e:
    st.error(f"❌ Erro ao importar o pipeline do Relatório Consolidado: {e}")
    st.stop()

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="SynapseNext – Relatório Técnico", layout="wide")
st.title("📘 Relatório Técnico Consolidado — Fase Interna")
st.caption("Auditoria Digital + Validação Semântica + Comparador.IA • SynapseNext / SAAB 5.0 / TJSP")

st.divider()
st.subheader("1️⃣ Compilação de evidências")

st.markdown(
    "Ao clicar no botão abaixo, o sistema irá:\n"
    "1. Ler os **últimos snapshots auditados** dos artefatos (DFD, ETP, TR, Edital);\n"
    "2. Executar **Validação Semântica IA** para cada artefato;\n"
    "3. Rodar o **Comparador.IA** para aferir a **Coerência Global**;\n"
    "4. Consolidar tudo em um **Relatório Técnico institucional**."
)

if st.button("🔎 Compilar dados do relatório"):
    with st.spinner("Coletando dados e executando análises..."):
        dados = coletar_dados_relatorio()

    st.success("✅ Dados compilados com sucesso!")
    st.divider()

    # Resumo sintético
    st.subheader("2️⃣ Resumo dos Resultados")
    coe = dados.get("coerencia", {})
    st.markdown(f"**📊 Coerência Global:** **{coe.get('coerencia_global', 0)}%**")

    cols = st.columns(4)
    ordem = dados.get("ordem", ["DFD", "ETP", "TR", "Edital"])
    vals = dados.get("validacoes", {})
    for i, nome in enumerate(ordem):
        with cols[i % 4]:
            v = vals.get(nome, {})
            st.metric(label=f"{nome} – Pontuação IA", value=f"{v.get('pontuacao', 0)}%")

    # Divergências e Ausências
    st.divider()
    st.subheader("3️⃣ Alertas — Divergências e Ausências")
    if coe.get("divergencias"):
        st.markdown("**⚠️ Divergências**")
        for d in coe["divergencias"]:
            st.markdown(f"- {d.get('descricao', '')}")
    else:
        st.info("Nenhuma divergência relevante apontada.")

    if coe.get("ausencias"):
        st.markdown("**❌ Ausências**")
        for a in coe["ausencias"]:
            st.markdown(f"- {a.get('descricao', '')}")

    # Geração do DOCX
    st.divider()
    st.subheader("4️⃣ Geração do Relatório Institucional (.docx)")
    if st.button("📄 Gerar Relatório Técnico (.docx)"):
        with st.spinner("Gerando documento institucional..."):
            out_path = gerar_relatorio_docx(dados)

        st.success("📁 Relatório gerado com sucesso!")
        try:
            with open(out_path, "rb") as f:
                data = f.read()
            st.download_button(
                label="⬇️ Baixar Relatório Técnico (.docx)",
                data=data,
                file_name=Path(out_path).name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
            st.info(f"Arquivo salvo em: `exports/relatorios/{Path(out_path).name}`")
        except Exception as e:
            st.error(f"Erro ao preparar o download: {e}")

else:
    st.info("Clique em **Compilar dados do relatório** para iniciar.")
