# ==========================================================
# pages/02_📄 DFD – Formalização da Demanda.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

import sys, os, json
import streamlit as st
from io import BytesIO
from docx import Document

# Caminhos base e imports institucionais
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

from utils.integration_dfd import export_dfd_to_json
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.agents_bridge import AgentsBridge

# ==========================================================
# ⚙️ Configuração da Página
# ==========================================================
st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide", page_icon="📄")
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "📄 Documento de Formalização da Demanda (DFD)",
    "Pré-preenchimento automático a partir de insumos + validação IA"
)
st.divider()

# ==========================================================
# 🔍 Detecção e normalização do Insumo Ativo
# ==========================================================
defaults = {}

# 🔹 Dados vindos da IA (integração direta da página Insumos)
if "dfd_campos_ai" in st.session_state and isinstance(st.session_state["dfd_campos_ai"], dict):
    defaults = st.session_state["dfd_campos_ai"]
    st.success("📎 Dados recebidos automaticamente do módulo INSUMOS (IA institucional ativa).")

# 🔹 Compatibilidade com formato anterior
elif "last_insumo_dfd" in st.session_state:
    last = st.session_state["last_insumo_dfd"]
    resultado = last.get("resultado", {})
    defaults = resultado.get("campos_ai", {})
    st.info(f"📎 Dados carregados a partir do histórico de insumos: {last.get('nome','—')}")

# 🔹 Caso nenhum dado seja encontrado
else:
    st.info("Nenhum insumo ativo encontrado. Você pode preencher manualmente ou enviar um documento na aba **🔧 Insumos**.")


# ==========================================================
# 🎨 Estilo institucional SAAB (mantido)
# ==========================================================
st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #003366;
            color: white;
            border-radius: 8px;
            height: 2.8em;
            width: 100%;
            font-weight: 500;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #002244;
            color: white;
            transition: 0.2s;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 🧾 Formulário Institucional
# ==========================================================
st.subheader("1️⃣ Entrada – Formulário Institucional")

with st.form("form_dfd"):
    unidade = st.text_input("Unidade solicitante", value=defaults.get("unidade_solicitante", ""))
    responsavel = st.text_input("Responsável pela demanda", value=defaults.get("responsavel", ""))
    objeto = st.text_area("Objeto da contratação", value=defaults.get("objeto", ""), height=100)
    justificativa = st.text_area("Justificativa da necessidade", value=defaults.get("justificativa", ""), height=100)
    quantidade = st.text_area("Quantidade e escopo", value=defaults.get("quantidade", ""), height=80)
    urgencia = st.text_area("Urgência (se aplicável)", value=defaults.get("urgencia", ""), height=80)
    riscos = st.text_area("Riscos identificados", value=defaults.get("riscos", ""), height=80)
    alinhamento = st.text_area("Alinhamento estratégico", value=defaults.get("alinhamento_planejamento", ""), height=80)

    col1, col2 = st.columns(2)
    with col1:
        gerar_ia = st.form_submit_button("⚙️ Gerar rascunho com IA institucional")
    with col2:
        submitted = st.form_submit_button("💾 Gerar rascunho manual")

st.caption("💡 O botão '⚙️ Gerar rascunho com IA institucional' usa o agente DFD.IA com base nos metadados preenchidos.")

# ==========================================================
# 💡 Geração IA Institucional
# ==========================================================
if gerar_ia:
    st.info("Executando agente DFD institucional...")
    metadata = {
        "unidade": unidade,
        "descricao": objeto,
        "justificativa": justificativa,
        "quantidade": quantidade,
        "riscos": riscos,
        "responsavel": responsavel,
        "alinhamento": alinhamento,
    }
    try:
        bridge = AgentsBridge("DFD")
        resultado = bridge.generate(metadata)
        st.success("✅ Rascunho gerado com sucesso pelo agente institucional DFD.IA!")
        st.json(resultado)
        st.session_state["last_dfd"] = resultado.get("secoes", {})
    except Exception as e:
        st.error(f"Erro ao gerar rascunho com IA: {e}")

# ==========================================================
# 💾 Resultado Manual
# ==========================================================
if submitted:
    dfd_data = {
        "unidade_solicitante": unidade,
        "responsavel": responsavel,
        "objeto": objeto,
        "justificativa": justificativa,
        "quantidade": quantidade,
        "urgencia": urgencia,
        "riscos": riscos,
        "alinhamento_planejamento": alinhamento,
    }
    st.success("✅ Rascunho de DFD gerado manualmente!")
    st.json(dfd_data)
    st.session_state["last_dfd"] = dfd_data

# ==========================================================
# 📤 Exportação
# ==========================================================
if "last_dfd" in st.session_state and st.session_state["last_dfd"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Baixe o último DFD gerado em formato Word editável.")

    dfd_data = st.session_state["last_dfd"]
    doc = Document()
    doc.add_heading("Documento de Formalização da Demanda (DFD)", level=1)
    for k, v in dfd_data.items():
        p = doc.add_paragraph()
        p.add_run(f"{k}: ").bold = True
        p.add_run(str(v) or "—")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    st.download_button("💾 Baixar DFD_rascunho.docx", buffer, file_name="DFD_rascunho.docx")

    st.markdown("---")
    if st.button("📦 Exportar DFD (JSON)"):
        dfd_payload = {
            "unidade": dfd_data.get("unidade_solicitante", ""),
            "descricao": dfd_data.get("objeto", ""),
            "motivacao": dfd_data.get("justificativa", ""),
            "quantidade": dfd_data.get("quantidade", ""),
            "responsavel": dfd_data.get("responsavel", ""),
            "riscos": dfd_data.get("riscos", ""),
            "alinhamento": dfd_data.get("alinhamento_planejamento", "")
        }
        try:
            path = export_dfd_to_json(dfd_payload)
            st.success(f"✅ DFD exportado com sucesso para {path}")
        except Exception as e:
            st.error(f"Falha ao exportar DFD: {e}")

st.caption("💡 *Dica:* O botão '⚙️ Gerar rascunho com IA institucional' usa o agente DFD.IA com base nos metadados preenchidos.")
