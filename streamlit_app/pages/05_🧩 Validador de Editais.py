# ==========================================================
# 🧩 SynapseNext – Validador de Editais
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================

import sys
from pathlib import Path
import streamlit as st

# ==========================================================
# 🔧 Configuração de paths e imports
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.ui_style import aplicar_estilo_institucional
    from utils.layout_institucional import exibir_cabecalho_institucional, exibir_rodape_institucional
    from utils.auditoria_pipeline import audit_event
    from validators.edital_validator import validar_edital
    from validators.edital_semantic_validator import validar_semantica_edital
except Exception as e:
    st.error(f"Erro ao importar módulos utilitários: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – Validador de Editais", page_icon="🧩", layout="wide")
aplicar_estilo_institucional()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_institucional(
    "Validador de Editais – SAAB 5.0",
    "Verifique a conformidade do edital com a Lei nº 14.133/21 e normas do TJSP"
)

# ==========================================================
# 📋 Interface principal
# ==========================================================
st.write("Esta ferramenta auxilia as unidades do TJSP na verificação dos principais elementos que devem constar no edital, conforme a Lei nº 14.133/2021 e as diretrizes da SAAB 5.0.")
st.divider()

tipo = st.selectbox("Selecione o tipo de contratação:", ["Serviços", "Obras", "Fornecimento de bens", "Consultoria"])
modo = st.radio("Modo de exibição dos resultados:", ["Resumo", "Detalhado"], horizontal=True)

st.markdown("### ✏️ Insira o conteúdo do edital para validação:")
conteudo = st.text_area("Cole o conteúdo (ou parte) do edital", height=250)

if st.button("▶️ Executar validação"):
    if not conteudo.strip():
        st.warning("Por favor, insira o conteúdo do edital antes de validar.")
    else:
        with st.spinner("Executando validações técnicas e semânticas..."):
            resultado_checklist = validar_edital(conteudo, tipo)
            resultado_semantico = validar_semantica_edital(conteudo)

        st.success("✅ Validação concluída com sucesso!")
        st.divider()

        if modo == "Resumo":
            st.markdown("### 📊 Resumo da Validação")
            st.write(resultado_checklist.get("resumo", "Nenhum resultado gerado."))
        else:
            st.markdown("### 📋 Resultados Detalhados")
            for item in resultado_checklist.get("itens", []):
                st.markdown(f"- **{item['descricao']}** → {item['status']}")

        st.divider()
        st.markdown("### 💬 Análise Semântica (IA TJSP)")
        st.write(resultado_semantico.get("resumo", "Sem resultados semânticos disponíveis."))

        audit_event("VALIDADOR_EDITAIS", "executar_validacao", conteudo, meta={"tipo": tipo, "modo": modo})

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
exibir_rodape_institucional()

