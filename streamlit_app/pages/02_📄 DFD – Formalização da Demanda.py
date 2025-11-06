# ==========================================================
# pages/02_📄 DFD – Formalização da Demanda.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: Engenheiro Synapse – vNext_2025.11.07
# Restabelecimento do fluxo INSUMOS → IA → DFD
# ==========================================================

import os
import json
import re
from pathlib import Path
from io import BytesIO
import streamlit as st
from docx import Document

# ==========================================================
# 📦 Imports institucionais
# ==========================================================
from utils.agents_bridge import AgentsBridge
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.integration_dfd import obter_dfd_da_sessao  # 🔹 Eng. Synapse: integração direta

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
# 🔹 Eng. Synapse – Mapeamento semântico do JSON gerado pela IA
# ==========================================================
def mapear_dfd_campos(dados_ia: dict) -> dict:
    """Transforma o JSON complexo retornado pela IA em um dicionário plano para o formulário DFD."""
    campos = {}
    etp = dados_ia.get("estudo_tecnico_preliminar", {})

    campos["processo_cpa"] = etp.get("processo_cpa", "")
    objeto = etp.get("objeto", {})
    necessidade = etp.get("necessidade_contratacao", {})

    campos["descricao_necessidade"] = objeto.get("descricao", "")
    campos["motivacao_contratacao"] = necessidade.get("descricao", "")
    campos["finalidade"] = objeto.get("finalidade", "")
    campos["localizacao"] = objeto.get("condicoes", {}).get("localizacao", "")
    campos["locais"] = ", ".join(necessidade.get("locais", []))
    campos["riscos"] = ", ".join(necessidade.get("riscos", []))
    campos["criterio_licitacoes"] = necessidade.get("criterio_licitações", "")

    return campos


# ==========================================================
# 🆕 Função de apoio – carregar insumo vindo do módulo INSUMOS
# ==========================================================
def _carregar_insumo_dfd() -> dict:
    """
    Carrega o último insumo processado e mapeia o JSON da IA
    para o formato esperado pelos campos do formulário DFD.
    """
    base_path = Path("exports") / "insumos" / "json" / "DFD_ultimo.json"
    if not base_path.exists():
        return {}

    try:
        with open(base_path, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # 🔹 Novo formato do integration_insumos.py
        if "resultado_ia" in dados:
            resposta = dados["resultado_ia"].get("resposta_texto", "")
            if resposta:
                match = re.search(r"```json(.*?)```", resposta, re.S)
                if match:
                    conteudo_json = match.group(1).strip()
                    try:
                        dados_ia = json.loads(conteudo_json)
                        return mapear_dfd_campos(dados_ia)
                    except Exception:
                        st.warning("⚠️ Falha ao interpretar JSON da IA. Exibindo campos vazios.")
                        return {}
        # 🔸 Fallback antigo
        return dados.get("campos_ai", {})

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar insumo DFD: {e}")
        return {}


def _carregar_lacunas_dfd() -> list[str]:
    """Carrega lacunas (itens não inferidos pela IA)."""
    base_path = Path("exports") / "insumos" / "json" / "DFD_ultimo.json"
    if base_path.exists():
        try:
            with open(base_path, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return dados.get("lacunas", []) or dados.get("campos_ai", {}).get("lacunas", [])
        except Exception:
            return []
    return []


# ==========================================================
# 🔍 Carregar dados inferidos pela IA
# ==========================================================
campos_ai = _carregar_insumo_dfd()
lacunas_ai = _carregar_lacunas_dfd()

# ==========================================================
# 🧾 Formulário DFD – pré-preenchido com os dados do insumo
# ==========================================================
st.subheader("1️⃣ Entrada – Formalização da Demanda")

descricao_default = campos_ai.get("descricao_necessidade", "")
motivacao_default = campos_ai.get("motivacao_contratacao", "")
prazo_default = campos_ai.get("prazo_execucao", "")
estimativa_default = 0.0

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
# 📝 Mostrar lacunas (caso existam)
# ==========================================================
if lacunas_ai:
    with st.expander("⚠️ Campos que a IA não conseguiu inferir do insumo"):
        for item in lacunas_ai:
            st.markdown(f"- {item}")

# ==========================================================
# 🤖 Geração IA Institucional – revalidação de rascunho
# ==========================================================
if gerar_ia:
    st.info("Executando agente DFD institucional com base no insumo processado...")
    metadata = {
        "unidade": unidade,
        "responsavel": responsavel,
        "prazo": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "estimativa_valor": estimativa_valor,
        "campos_ai": campos_ai,
        "origem": "pagina_dfd_streamlit",
    }
    try:
        bridge = AgentsBridge("DFD")
        resultado = bridge.generate(metadata)
        st.success("✅ Rascunho gerado com sucesso pelo agente DFD.IA!")
        st.json(resultado)

        st.session_state["last_dfd"] = resultado.get("secoes", resultado)

        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        json_path = exports_dir / "dfd_data.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        st.info(f"💾 Arquivo exportado: {json_path}")

    except Exception as e:
        st.error(f"Erro ao gerar rascunho com IA: {e}")

# ==========================================================
# 💾 Salvamento manual (fallback)
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
# 📤 Exportação – Word e JSON
# ==========================================================
if "last_dfd" in st.session_state and st.session_state["last_dfd"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Baixe o último DFD gerado em formato Word editável.")

    dfd_data = st.session_state["last_dfd"]
    doc = Document()
    doc.add_heading("Formalização da Demanda (DFD)", level=1)
    if isinstance(dfd_data, dict):
        for k, v in dfd_data.items():
            p = doc.add_paragraph()
            p.add_run(f"{k}: ").bold = True
            p.add_run(str(v) or "—")
    else:
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
