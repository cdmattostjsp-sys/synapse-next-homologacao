# ==========================================================
# 🧾 SynapseNext – Relatório Técnico Consolidado
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# 🔧 Setup de caminhos e imports institucionais
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.relatorio_consolidado_pipeline import coletar_dados_relatorio, gerar_relatorio_docx
except Exception as e:
    st.error(f"❌ Erro ao importar o pipeline do Relatório Consolidado: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="Relatório Técnico Consolidado – SynapseNext", layout="wide", page_icon="🧾")

# ==========================================================
# 🎨 Importa estilo institucional
# ==========================================================
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "Relatório Técnico Consolidado",
    "Auditoria Digital + Validação Semântica + Comparador.IA • SAAB 5.0 / TJSP"
)
st.divider()

# ==========================================================
# 1️⃣ Compilação de evidências
# ==========================================================
st.subheader("1️⃣ Compilação de Evidências")

st.markdown("""
Ao clicar no botão abaixo, o sistema irá:

1. Ler os **últimos snapshots auditados** dos artefatos (DFD, ETP, TR, Edital);
2. Executar **Validação Semântica IA** para cada artefato;
3. Rodar o **Comparador.IA** para aferir a **Coerência Global**;
4. Consolidar tudo em um **Relatório Técnico institucional**.
""")

if st.button("🔎 Compilar dados do relatório", type="primary"):
    with st.spinner("Coletando dados e executando análises..."):
        dados = coletar_dados_relatorio()

    st.success("✅ Dados compilados com sucesso.")
    st.divider()

    # ======================================================
    # 2️⃣ Resumo dos Resultados
    # ======================================================
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

    # ======================================================
    # 3️⃣ Alertas — Divergências e Ausências
    # ======================================================
    st.divider()
    st.subheader("3️⃣ Alertas — Divergências e Ausências")

    if coe.get("divergencias"):
        st.markdown("**⚠️ Divergências detectadas:**")
        for d in coe["divergencias"]:
            st.markdown(f"- {d.get('descricao', '')}")
    else:
        st.info("Nenhuma divergência relevante apontada.")

    if coe.get("ausencias"):
        st.markdown("**❌ Ausências identificadas:**")
        for a in coe["ausencias"]:
            st.markdown(f"- {a.get('descricao', '')}")
    else:
        st.info("Nenhuma ausência registrada.")

    # ======================================================
    # 4️⃣ Geração do Relatório Institucional (.docx)
    # ======================================================
    st.divider()
    st.subheader("4️⃣ Geração do Relatório Institucional (.docx)")

    if st.button("📄 Gerar Relatório Técnico (.docx)"):
        with st.spinner("Gerando documento institucional..."):
            out_path = gerar_relatorio_docx(dados)

        st.success("📁 Relatório gerado com sucesso.")
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

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption(
    f"SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Relatório Técnico Consolidado • Gerado em {datetime.now():%d/%m/%Y %H:%M}"
)
