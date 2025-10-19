# ==========================================================
# SynapseNext – Fase Brasília (Passo 10B-2)
# Comparador.IA – Análise cruzada entre artefatos da Fase Interna
# ==========================================================
# Interface institucional para análise de coerência semântica
# entre DFD → ETP → TR → Edital, com geração de relatórios.
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# Caminhos e importações
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.comparador_pipeline import carregar_snapshots, analisar_coerencia, gerar_relatorio
except Exception as e:
    st.error(f"❌ Erro ao importar módulo comparador_pipeline: {e}")
    st.stop()

# ==========================================================
# Configurações da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – Comparador.IA", layout="wide")
st.title("🧩 Comparador.IA — Coerência entre Artefatos da Fase Interna")
st.caption("Verificação cruzada entre DFD, ETP, TR e Edital com base nos snapshots auditados.")
st.divider()

# ==========================================================
# Seção de carregamento
# ==========================================================
st.subheader("1️⃣ Carregar artefatos")
st.markdown(
    "O sistema buscará automaticamente os **últimos snapshots** gerados e auditados "
    "dos artefatos DFD, ETP, TR e Edital em `exports/auditoria/snapshots/`."
)

if st.button("🔄 Carregar snapshots auditados"):
    artefatos = carregar_snapshots()

    if not artefatos:
        st.warning("⚠️ Nenhum snapshot encontrado. Gere e audite os artefatos antes de rodar esta análise.")
        st.stop()

    st.success(f"✅ {len(artefatos)} artefatos carregados: {', '.join(artefatos.keys())}")

    st.divider()
    st.subheader("2️⃣ Conteúdo pré-processado")
    with st.expander("Visualizar textos limpos (pré-processados)", expanded=False):
        for nome, texto in artefatos.items():
            st.markdown(f"### 🗂️ {nome}")
            st.text_area(f"Texto do {nome}", texto[:2500], height=180)

    st.divider()
    st.subheader("3️⃣ Análise de coerência")
    with st.spinner("Executando análise comparativa entre os artefatos..."):
        resultado = analisar_coerencia(artefatos)

    # ==========================================================
    # Exibição dos resultados
    # ==========================================================
    st.success("✅ Análise concluída.")
    st.markdown(f"### 📊 Coerência Global: **{resultado.get('coerencia_global', 0)}%**")

    st.divider()
    st.subheader("4️⃣ Comparações Diretas")

    comparacoes = resultado.get("comparacoes", {})
    if comparacoes:
        for par, valor in comparacoes.items():
            if valor >= 75:
                cor = "🟩"
            elif 50 <= valor < 75:
                cor = "🟨"
            else:
                cor = "🟥"
            st.markdown(f"- {cor} **{par}** → Similaridade: `{valor}%`")

    # Divergências
    if resultado.get("divergencias"):
        st.markdown("### ⚠️ Divergências Encontradas")
        for d in resultado["divergencias"]:
            st.markdown(f"- {d['descricao']}")

    # Ausências
    if resultado.get("ausencias"):
        st.markdown("### ❌ Ausências de Artefato")
        for a in resultado["ausencias"]:
            st.markdown(f"- {a['descricao']}")

    st.divider()
    st.subheader("5️⃣ Exportação do Relatório")

    with st.spinner("Gerando relatório de coerência..."):
        saida = gerar_relatorio(resultado)

    if saida["ok"]:
        st.success("📄 Relatórios gerados com sucesso!")
        with open(saida["md_path"], "r", encoding="utf-8") as f:
            md_text = f.read()

        st.download_button(
            label="⬇️ Baixar relatório em Markdown (.md)",
            data=md_text,
            file_name=Path(saida["md_path"]).name,
            mime="text/markdown",
            use_container_width=True,
        )

        with open(saida["json_path"], "r", encoding="utf-8") as jf:
            json_data = jf.read()

        st.download_button(
            label="⬇️ Baixar relatório em JSON (.json)",
            data=json_data,
            file_name=Path(saida["json_path"]).name,
            mime="application/json",
            use_container_width=True,
        )

        st.info(f"Arquivos salvos em: `exports/analises/{Path(saida['md_path']).name}`")

else:
    st.info("Clique no botão acima para iniciar a análise.")
