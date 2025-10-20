# ==========================================================
# 🧭 SynapseNext – Módulo de Validação do Edital
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================

import streamlit as st
import sys
from pathlib import Path
import json

# ==========================================================
# 🔧 Configuração de compatibilidade de importação
# ==========================================================
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from validators.edital_validator import validar_edital

# ==========================================================
# 🧩 Configuração inicial da página
# ==========================================================
st.set_page_config(
    page_title="Validador de Edital – SynapseNext",
    layout="wide",
    page_icon="📜"
)

st.title("📜 Validador de Editais – SAAB 5.0")
st.markdown("""
Esta ferramenta auxilia as unidades do **TJSP** na verificação dos principais elementos
que devem constar no **Edital de Licitação**, conforme a **Lei nº 14.133/2021**
e as diretrizes da Secretaria de Administração e Abastecimento (SAAB 5.0).

Utilize este módulo para validar preliminarmente o edital elaborado,
identificando se os elementos essenciais foram atendidos.
---
""")

# ==========================================================
# 🧮 Entrada de dados
# ==========================================================
col1, col2 = st.columns([2, 1])

with col1:
    tipo = st.selectbox(
        "Selecione o tipo de contratação:",
        ["servicos", "obras", "materiais", "ti", "consultoria"],
        index=0
    )

with col2:
    modo_exibicao = st.radio(
        "Modo de exibição dos resultados:",
        ["Resumo", "Detalhado"],
        horizontal=True
    )

st.markdown("### 📝 Insira o conteúdo do Edital")
texto_edital = st.text_area(
    "Cole aqui o conteúdo (ou parte) do edital para validação:",
    height=250,
    placeholder="Exemplo: O presente edital tem por objeto a contratação de empresa especializada em serviços de manutenção predial..."
)

# ==========================================================
# 🧾 Execução da validação
# ==========================================================
if st.button("✅ Validar Edital"):
    if not texto_edital.strip():
        st.warning("Por favor, insira o conteúdo do edital antes de validar.")
    else:
        with st.spinner("Processando validação..."):
            dados = {"texto": texto_edital}
            resultado = validar_edital(tipo, dados)

        resumo = resultado.get("resumo", {})
        resultados = resultado.get("resultados", [])

        # ==================================================
        # 📊 Exibição dos resultados
        # ==================================================
        st.success("Validação concluída com sucesso!")

        st.markdown(f"""
        **Tipo de Contratação:** {resumo.get("tipo", "").capitalize()}  
        **Itens Atendidos:** {resumo.get("atendidos", 0)} / {resumo.get("total_itens", 0)}  
        **Percentual de Conformidade:** {resumo.get("percentual_conformidade", 0)}%
        """)

        st.progress(resumo.get("percentual_conformidade", 0) / 100)

        if modo_exibicao == "Detalhado":
            st.markdown("### 📋 Detalhamento dos Itens Avaliados")
            for item in resultados:
                emoji = "✅" if item["status"] == "Atendido" else "⚠️"
                st.markdown(f"- {emoji} **{item['item']}** — {item['status']}")

        # ==================================================
        # 💾 Opção de exportação
        # ==================================================
        json_export = json.dumps(resultado, indent=4, ensure_ascii=False)
        st.download_button(
            label="⬇️ Baixar resultado da validação (JSON)",
            data=json_export,
            file_name=f"resultado_validacao_edital_{tipo}.json",
            mime="application/json"
        )

# ==========================================================
# 🧩 Rodapé institucional
# ==========================================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "TJSP • Secretaria de Administração e Abastecimento • SynapseNext – SAAB 5.0<br>"
    "Versão institucional vNext • Desenvolvido em ambiente Python"
    "</p>",
    unsafe_allow_html=True
)
