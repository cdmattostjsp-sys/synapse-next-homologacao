# ==============================
# pages/05_📑 TR – Termo de Referência.py  –  SynapseNext / SAAB TJSP
# ==============================

import streamlit as st
from datetime import datetime
import os, sys
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

# ==========================================================
# 🔍 Importações compatíveis
# ==========================================================
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

try:
    from utils.integration_tr import export_tr_to_json
except ModuleNotFoundError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.insert(0, base_dir)
    from utils.integration_tr import export_tr_to_json

# ==========================================================
# ⚙️ Configuração
# ==========================================================
st.set_page_config(page_title="📑 Termo de Referência", layout="wide", page_icon="📑")
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "📑 Termo de Referência (TR)",
    "Pré-preenchimento automático a partir de insumos + validação IA institucional"
)

st.divider()

# ==========================================================
# 🔗 Verificação de integração ativa
# ==========================================================
defaults = {}

if "tr_campos_ai" in st.session_state:
    defaults = st.session_state["tr_campos_ai"]
    st.success("📎 Dados recebidos automaticamente do módulo **INSUMOS** (IA institucional ativa).")
else:
    st.info("Nenhum insumo ativo detectado. Você pode preencher manualmente ou aguardar integração via módulo **INSUMOS**.")

# ==========================================================
# 🧾 Formulário TR – Estrutura institucional
# ==========================================================
st.subheader("📘 Entrada – Termo de Referência")

col1, col2 = st.columns(2)
with col1:
    objeto = st.text_area("Objeto da contratação", value=defaults.get("objeto", ""), height=120)
    justificativa_tecnica = st.text_area("Justificativa técnica", value=defaults.get("justificativa_tecnica", ""), height=120)
    especificacao_tecnica = st.text_area("Especificações técnicas", value=defaults.get("especificacao_tecnica", ""), height=120)
with col2:
    criterios_julgamento = st.text_area("Critérios de julgamento", value=defaults.get("criterios_julgamento", ""), height=120)
    riscos = st.text_area("Riscos associados", value=defaults.get("riscos", ""), height=120)
    observacoes_finais = st.text_area("Observações finais", value=defaults.get("observacoes_finais", ""), height=120)

st.divider()

col3, col4, col5 = st.columns(3)
with col3:
    prazo_execucao = st.text_input("Prazo de execução", value=defaults.get("prazo_execucao", ""))
with col4:
    estimativa_valor = st.text_input("Estimativa de valor (R$)", value=defaults.get("estimativa_valor", ""))
with col5:
    fonte_recurso = st.text_input("Fonte de recurso", value=defaults.get("fonte_recurso", ""))

# ==========================================================
# 🧩 Salvamento / Exportação
# ==========================================================
st.divider()
st.subheader("⚙️ Gerar rascunho com IA institucional")

if st.button("💾 Salvar rascunho TR"):
    tr_data = {
        "artefato": "TR",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "campos": {
            "objeto": objeto,
            "justificativa_tecnica": justificativa_tecnica,
            "especificacao_tecnica": especificacao_tecnica,
            "criterios_julgamento": criterios_julgamento,
            "riscos": riscos,
            "observacoes_finais": observacoes_finais,
            "prazo_execucao": prazo_execucao,
            "estimativa_valor": estimativa_valor,
            "fonte_recurso": fonte_recurso,
        },
    }

    try:
        export_tr_to_json(tr_data)
        st.success("✅ Rascunho salvo com sucesso em `exports/tr_data.json`.")
    except Exception as e:
        st.error(f"Erro ao salvar rascunho: {e}")

st.caption("📎 Os dados acima podem ser revisados, salvos ou enviados para os módulos subsequentes (ex: Contrato).")
