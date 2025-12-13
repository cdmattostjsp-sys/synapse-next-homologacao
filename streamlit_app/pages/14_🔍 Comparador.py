# -*- coding: utf-8 -*-
"""
🔍 SynapseNext – Comparador.IA
Secretaria de Administração e Abastecimento – SAAB 5.0
==============================================================
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Configuração de caminhos ANTES de importar streamlit
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

# Import do Streamlit
import streamlit as st

# ==========================================================
# ⚙️ Configuração da página (DEVE SER A PRIMEIRA CHAMADA ST)
# ==========================================================
st.set_page_config(
    page_title="SynapseNext – Comparador.IA",
    layout="wide",
    page_icon="🔍"
)
apply_sidebar_grouping()

# ==========================================================
# 🔧 Imports institucionais
# ==========================================================
erro_import = None
try:
    from utils.comparador_pipeline import carregar_snapshots, analisar_coerencia, gerar_relatorio
except Exception as e:
    erro_import = str(e)

# ==========================================================
# 🎨 Estilo institucional padronizado
# ==========================================================
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from home_utils.sidebar_organizer import apply_sidebar_grouping
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "Comparador.IA – Coerência entre Artefatos",
    "Análise cruzada entre DFD, ETP, TR e Edital com base nos snapshots auditados"
)
st.divider()

# ==========================================================
# 🚨 Verificação de erros de import
# ==========================================================
if erro_import:
    st.error(f"❌ Erro ao importar módulo comparador_pipeline: {erro_import}")
    st.stop()

# ==========================================================
# 1️⃣ Carregar artefatos auditados
# ==========================================================
st.subheader("1️⃣ Carregar Artefatos")

st.markdown("""
O sistema buscará automaticamente os **últimos snapshots auditados** dos artefatos:
**DFD**, **ETP**, **TR** e **Edital**, localizados em  
`exports/auditoria/snapshots/`.
""")

if st.button("🔄 Carregar snapshots auditados", type="primary"):
    artefatos = carregar_snapshots()

    if not artefatos:
        st.warning("⚠️ Nenhum snapshot encontrado. Gere e audite os artefatos antes de executar a análise.")
        st.stop()

    st.success(f"✅ {len(artefatos)} artefatos carregados: {', '.join(artefatos.keys())}")
    st.divider()

    # ======================================================
    # 2️⃣ Conteúdo pré-processado
    # ======================================================
    st.subheader("2️⃣ Conteúdo Pré-Processado")
    with st.expander("Visualizar textos limpos (pré-processados)", expanded=False):
        for nome, texto in artefatos.items():
            st.markdown(f"#### 🗂️ {nome}")
            st.text_area(f"Texto auditado – {nome}", texto[:2500], height=180)

    st.divider()

    # ======================================================
    # 3️⃣ Análise de coerência entre artefatos
    # ======================================================
    st.subheader("3️⃣ Análise de Coerência")

    with st.spinner("Executando análise comparativa entre os artefatos..."):
        resultado = analisar_coerencia(artefatos)

    st.success("✅ Análise concluída com sucesso.")
    st.markdown(f"### 📊 **Coerência Global:** {resultado.get('coerencia_global', 0)}%")

    # ======================================================
    # 4️⃣ Comparações diretas e divergências
    # ======================================================
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
    else:
        st.info("Sem comparações diretas disponíveis.")

    # Divergências
    if resultado.get("divergencias"):
        st.markdown("### ⚠️ Divergências Encontradas")
        for d in resultado["divergencias"]:
            st.markdown(f"- {d.get('descricao', '')}")
    else:
        st.info("Nenhuma divergência registrada.")

    # Ausências
    if resultado.get("ausencias"):
        st.markdown("### ❌ Ausências de Artefato")
        for a in resultado["ausencias"]:
            st.markdown(f"- {a.get('descricao', '')}")
    else:
        st.info("Nenhuma ausência identificada.")

    # ======================================================
    # 5️⃣ Exportação dos relatórios
    # ======================================================
    st.divider()
    st.subheader("5️⃣ Exportação dos Relatórios")

    with st.spinner("Gerando relatórios de coerência..."):
        saida = gerar_relatorio(resultado)

    if saida.get("ok"):
        st.success("📄 Relatórios gerados com sucesso!")

        # Markdown
        with open(saida["md_path"], "r", encoding="utf-8") as f:
            md_text = f.read()
        st.download_button(
            label="⬇️ Baixar relatório em Markdown (.md)",
            data=md_text,
            file_name=Path(saida["md_path"]).name,
            mime="text/markdown",
            use_container_width=True,
        )

        # JSON
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
        st.error("Erro na geração dos relatórios.")

else:
    st.info("Clique em **Carregar snapshots auditados** para iniciar a análise.")

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption(
    f"Projeto SAAB-Tech • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Relatório de Comparação Gerado em {datetime.now():%d/%m/%Y %H:%M}"
)
