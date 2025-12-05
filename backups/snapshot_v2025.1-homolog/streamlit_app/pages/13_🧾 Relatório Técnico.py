import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# -*- coding: utf-8 -*-
"""
🧾 Relatório Técnico Consolidado – SynapseNext vNext+
==============================================================
Auditoria Digital + Validação Semântica + Comparador.IA
Integração total com pipelines de Governança e Alertas.

Autor: Equipe Synapse.Engineer
Instituição: Secretaria de Administração e Abastecimento – TJSP
Versão: vNext+ (SAAB 5.0)
==============================================================
"""

import sys, os
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd

# ==========================================================
# 🔧 Configuração de caminhos e imports
# ==========================================================

try:
    from utils.relatorio_consolidado_pipeline import coletar_dados_relatorio, gerar_relatorio_docx
    from utils.alertas_pipeline import gerar_alertas
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception as e:
    st.error(f"❌ Falha ao importar módulos institucionais: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da Página
# ==========================================================
st.set_page_config(page_title="🧾 Relatório Técnico Consolidado – SynapseNext", layout="wide", page_icon="🧾")
aplicar_estilo_global()
exibir_cabecalho_padrao(
    "Relatório Técnico Consolidado",
    "Auditoria Digital + Validação Semântica + Comparador.IA • SAAB 5.0 / TJSP"
)
st.divider()

# ==========================================================
# 1️⃣ Compilação de Evidências
# ==========================================================
st.subheader("1️⃣ Compilação de Evidências")

st.markdown("""
Ao clicar no botão abaixo, o sistema irá executar:

1. Leitura dos **últimos snapshots auditados** dos artefatos (DFD, ETP, TR, Edital);
2. Execução da **Validação Semântica IA** para cada artefato;
3. Aplicação do **Comparador.IA** para aferição da **Coerência Global**;
4. Consolidação de evidências em um **Relatório Técnico institucional (.docx)**.
""")

if st.button("🔍 Compilar dados do relatório", type="primary", use_container_width=True):
    with st.spinner("Executando auditoria técnica e consolidando evidências..."):
        try:
            dados = coletar_dados_relatorio()
        except Exception as e:
            st.error(f"Erro durante a coleta de dados: {e}")
            st.stop()

    st.success("✅ Dados compilados com sucesso.")
    st.divider()

    # ======================================================
    # 2️⃣ Resumo dos Resultados
    # ======================================================
    st.subheader("2️⃣ Resumo dos Resultados")
    coe = dados.get("coerencia", {})
    validacoes = dados.get("validacoes", {})
    ordem = dados.get("ordem", ["DFD", "ETP", "TR", "Edital"])

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Coerência Global", f"{coe.get('coerencia_global', 0)}%")
    col2.metric("📚 Artefatos Auditados", len(ordem))
    col3.metric("🧠 Validações Executadas", len(validacoes))
    col4.metric("⚙️ Pipeline", "vNext+")

    st.markdown("### Desempenho por Artefato")
    cols = st.columns(4)
    for i, nome in enumerate(ordem):
        v = validacoes.get(nome, {})
        with cols[i % 4]:
            st.metric(label=f"{nome}", value=f"{v.get('pontuacao', 0)}%")

    # ======================================================
    # 3️⃣ Alertas e Divergências
    # ======================================================
    st.divider()
    st.subheader("3️⃣ Alertas, Divergências e Ausências")

    alertas = []
    try:
        alertas = gerar_alertas()
    except Exception:
        st.info("⚠️ Nenhum alerta adicional detectado.")

    # Divergências
    if coe.get("divergencias"):
        st.markdown("**⚠️ Divergências identificadas:**")
        for d in coe["divergencias"]:
            st.markdown(f"- {d.get('descricao', 'Sem descrição disponível.')}")
    else:
        st.success("✅ Nenhuma divergência encontrada.")

    # Ausências
    if coe.get("ausencias"):
        st.markdown("**❌ Ausências registradas:**")
        for a in coe["ausencias"]:
            st.markdown(f"- {a.get('descricao', 'Sem descrição disponível.')}")
    else:
        st.info("Nenhuma ausência relevante.")

    # Alertas Proativos
    if alertas:
        st.markdown("**🔔 Alertas Proativos Integrados:**")
        df_alertas = pd.DataFrame(alertas)
        if not df_alertas.empty:
            st.dataframe(
                df_alertas[["titulo", "area", "severidade", "mensagem"]],
                use_container_width=True,
                hide_index=True,
            )

    # ======================================================
    # 4️⃣ Geração do Relatório Institucional (.docx)
    # ======================================================
    st.divider()
    st.subheader("4️⃣ Geração do Relatório Institucional (.docx)")

    if st.button("📄 Gerar Relatório Técnico (.docx)", use_container_width=True):
        with st.spinner("Gerando documento institucional..."):
            try:
                out_path = gerar_relatorio_docx(dados)
                with open(out_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Baixar Relatório Técnico (.docx)",
                        data=f,
                        file_name=Path(out_path).name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )
                st.success("📘 Relatório Técnico gerado com sucesso.")
            except Exception as e:
                st.error(f"Erro ao gerar relatório: {e}")

else:
    st.info("Clique em **Compilar dados do relatório** para iniciar a auditoria técnica.")

# ==========================================================
# 📅 Rodapé Institucional
# ==========================================================
st.markdown("---")
st.caption(
    f"SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Relatório Técnico Consolidado • Versão vNext+ • Gerado em {datetime.now():%d/%m/%Y %H:%M}"
)
