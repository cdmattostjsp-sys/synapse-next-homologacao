# ==========================================================
# pages/02_📄 DFD – Formalização da Demanda.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: Engenheiro Synapse – restabelecer fluxo INSUMOS → IA → DFD
# ==========================================================

import os
import json
from pathlib import Path
from io import BytesIO

import streamlit as st
from docx import Document

# ==========================================================
# 📦 Imports institucionais
# ==========================================================
from utils.agents_bridge import AgentsBridge
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(
    page_title="📄 DFD – Formalização da Demanda",
    layout="wide",
    page_icon="📄",
)
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "📄 Formalização da Demanda (DFD)",
    "Registro institucional da demanda e geração de rascunho com IA",
)
st.divider()

# ==========================================================
# 🆕 Funções de apoio – carregar insumo vindo do módulo INSUMOS
# ==========================================================
def _carregar_insumo_dfd() -> dict:
    """
    Prioridade:
    1. Dados da sessão (setados por utils/integration_insumos.py ou integration_ai_engine.py)
    2. Arquivo exports/insumos/json/DFD_ultimo.json (salvo pelo módulo de Insumos)
    3. {} se nada for encontrado
    """
    # 1️⃣ sessão
    if "dfd_campos_ai" in st.session_state:
        return st.session_state.get("dfd_campos_ai", {})

    # 2️⃣ disco (fallback)
    ultimo_json = Path("exports") / "insumos" / "json" / "DFD_ultimo.json"
    if ultimo_json.exists():
        try:
            with open(ultimo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return dados.get("campos_ai", {})
        except Exception:
            return {}

    # 3️⃣ nada encontrado
    return {}


def _carregar_lacunas_dfd() -> list[str]:
    """
    Caso precisemos mostrar ao usuário o que a IA não conseguiu inferir.
    Vem do mesmo payload salvo pelo módulo de Insumos.
    """
    ultimo_json = Path("exports") / "insumos" / "json" / "DFD_ultimo.json"
    if ultimo_json.exists():
        try:
            with open(ultimo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
            # o integration_ai_engine devolve 'lacunas' no objeto principal; o integration_insumos
            # guarda isso dentro de 'campos_ai' apenas se vier assim. Mantemos o fallback duplo:
            return dados.get("lacunas", []) or dados.get("campos_ai", {}).get("lacunas", [])
        except Exception:
            return []
    return []


# dados inferidos pela IA (vêm do INSUMOS)
campos_ai = _carregar_insumo_dfd()
lacunas_ai = _carregar_lacunas_dfd()

# ==========================================================
# 🧾 Formulário DFD – agora pré-preenchido com o que a IA inferiu
# ==========================================================
st.subheader("1️⃣ Entrada – Formalização da Demanda")

# mapeamento mínimo entre o que a IA retorna e o que o formulário atual pede
descricao_default = (
    campos_ai.get("objeto")
    or campos_ai.get("justificativa")
    or ""
)
motivacao_default = campos_ai.get("justificativa", "")
prazo_default = campos_ai.get("prazo_execucao", "")
estimativa_default = 0.0  # IA não costuma trazer número pronto neste motor

with st.form("form_dfd"):
    col1, col2 = st.columns(2)

    with col1:
        unidade = st.text_input(
            "Unidade Demandante",
            placeholder="Ex.: Secretaria de Administração e Abastecimento – SAAB",
            key="dfd_unidade",
        )
        responsavel = st.text_input(
            "Responsável pela Demanda",
            key="dfd_responsavel",
        )
        prazo = st.text_input(
            "Prazo Estimado para Atendimento",
            value=prazo_default,
            key="dfd_prazo",
        )

    with col2:
        descricao = st.text_area(
            "Descrição da Necessidade",
            height=100,
            value=descricao_default,
            key="dfd_descricao",
        )
        motivacao = st.text_area(
            "Motivação da Contratação",
            height=100,
            value=motivacao_default,
            key="dfd_motivacao",
        )
        estimativa_valor = st.number_input(
            "Estimativa de Valor (R$)",
            min_value=0.0,
            step=1000.0,
            value=estimativa_default,
            key="dfd_estimativa_valor",
        )

    colb1, colb2 = st.columns(2)
    with colb1:
        gerar_ia = st.form_submit_button("⚙️ Gerar rascunho com IA institucional")
    with colb2:
        salvar_manual = st.form_submit_button("💾 Salvar dados manualmente")

# ==========================================================
# 🎨 Estilo institucional SAAB – botões
# (mantido do arquivo original)
# ==========================================================
st.markdown(
    """
<style>
div.stButton > button:first-child {
    background-color: #003366 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    height: 2.8em !important;
    font-weight: 500 !important;
}
div.stButton > button:first-child:hover {
    background-color: #002244 !important;
    color: white !important;
    transition: 0.2s;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# 📝 Mostrar ao usuário o que a IA não conseguiu inferir
# ==========================================================
if lacunas_ai:
    with st.expander("⚠️ Campos que a IA não conseguiu inferir do insumo"):
        for item in lacunas_ai:
            st.markdown(f"- {item}")

# ==========================================================
# 🤖 Geração IA Institucional (agente interno) – agora levando os campos da IA
# ==========================================================
if gerar_ia:
    st.info("Executando agente DFD institucional com base no insumo processado...")
    metadata = {
        # dados que o usuário viu/preencheu
        "unidade": unidade,
        "responsavel": responsavel,
        "prazo": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "estimativa_valor": estimativa_valor,
        # 🆕 dados vindos do motor IA institucional (integration_ai_engine.py)
        # isso faz o agente ficar mais completo
        "campos_ai": campos_ai,
        "origem": "pagina_dfd_streamlit",
    }
    try:
        bridge = AgentsBridge("DFD")
        resultado = bridge.generate(metadata)
        st.success("✅ Rascunho gerado com sucesso pelo agente DFD.IA!")
        st.json(resultado)

        # guarda na sessão para exportação
        st.session_state["last_dfd"] = resultado.get("secoes", resultado)

        # salva JSON institucional (mantido do original)
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        json_path = exports_dir / "dfd_data.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        st.info(f"💾 Arquivo exportado: {json_path}")

    except Exception as e:
        st.error(f"Erro ao gerar rascunho com IA: {e}")

# ==========================================================
# 💾 Salvamento manual (fallback) – mantido
# ==========================================================
if salvar_manual:
    dfd_data = {
        "unidade": unidade,
        "responsavel": responsavel,
        "prazo": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "estimativa_valor": estimativa_valor,
    }
    st.success("✅ Dados do DFD salvos manualmente.")
    st.json(dfd_data)
    st.session_state["last_dfd"] = dfd_data

# ==========================================================
# 📤 Exportação do Documento – mantido
# ==========================================================
if "last_dfd" in st.session_state and st.session_state["last_dfd"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Baixe o último DFD gerado em formato Word editável.")

    dfd_data = st.session_state["last_dfd"]
    doc = Document()
    doc.add_heading("Formalização da Demanda (DFD)", level=1)
    # se o agente devolveu em seções, percorremos o dicionário
    if isinstance(dfd_data, dict):
        for k, v in dfd_data.items():
            p = doc.add_paragraph()
            p.add_run(f"{k}: ").bold = True
            p.add_run(str(v) or "—")
    else:
        # fallback simples
        doc.add_paragraph(str(dfd_data))

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    st.download_button("💾 Baixar DFD_rascunho.docx", buffer, file_name="DFD_rascunho.docx")

    st.markdown("---")
    if st.button("📦 Exportar DFD (JSON)"):
        try:
            exports_dir = Path("exports")
            exports_dir.mkdir(exist_ok=True)
            json_path = exports_dir / "dfd_data.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dfd_data, f, ensure_ascii=False, indent=2)
            st.success(f"✅ DFD exportado com sucesso para {json_path}")
        except Exception as e:
            st.error(f"Falha ao exportar DFD: {e}")

st.caption(
    "💡 Este módulo aceita preenchimento manual, mas dá prioridade ao insumo pré-processado pelo módulo INSUMOS + IA institucional."
)
