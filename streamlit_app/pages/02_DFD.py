import streamlit as st
import json
from typing import Any, Dict

from utils.dfd.integration_dfd import (
    obter_dfd_da_sessao,
    salvar_dfd_em_json,
    gerar_rascunho_dfd_com_ia,
    status_dfd,
)

# ---------------------------------------------------------------
# ⚙️ CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------------
st.set_page_config(
    page_title="📄 Formalização da Demanda (DFD)",
    layout="wide",
)

st.title("📄 Formalização da Demanda (DFD)")
st.caption("📌 DFD carregado a partir dos insumos processados no módulo 🔧 Insumos.")
st.info(status_dfd())


# ---------------------------------------------------------------
# Funções utilitárias
# ---------------------------------------------------------------
def _to_str(value: Any) -> str:
    """Converte qualquer estrutura em string legível para edição."""
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False, indent=2)
        except:
            return str(value)
    return str(value)


def _normalizar_campos(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza diferentes formatos possíveis vindos do pipeline:
      - { "DFD": {...} }
      - { "secoes": {...} }
      - { "campos_ai": {...} }
      - JSON direto da IA
    """
    if not isinstance(dados, dict):
        return {}

    if isinstance(dados.get("campos_ai"), dict):
        return dados["campos_ai"]

    if isinstance(dados.get("DFD"), dict):
        return dados["DFD"]

    if isinstance(dados.get("secoes"), dict):
        return dados["secoes"]

    return dados


# ---------------------------------------------------------------
# 🔥 Consolidar dados estruturados → texto administrativo
# ---------------------------------------------------------------
def mapear_campos_para_form(dados_brutos: Dict[str, Any]) -> Dict[str, str]:
    campos = _normalizar_campos(dados_brutos)

    # ------------------------------------------------------------
    # CAMPOS BÁSICOS
    # ------------------------------------------------------------
    unidade = campos.get("unidade_demandante") or campos.get("unidade") or ""
    responsavel = campos.get("responsavel", "")
    prazo = campos.get("prazo_estimado") or campos.get("prazo") or ""
    valor_estimado = campos.get("valor_estimado") or campos.get("estimativa_valor") or "0,00"

    # ------------------------------------------------------------
    # DESCRIÇÃO (texto consolidado)
    # ------------------------------------------------------------
    descricao_txt = ""

    if isinstance(campos.get("edificio"), dict):
        e = campos["edificio"]
        descricao_txt += (
            "Características do edifício:\n"
            f"- Pavimentos: {e.get('pavimentos','')}\n"
            f"- Área total: {e.get('area','')}\n"
            f"- Ano de inauguração: {e.get('ano_inauguracao','')}\n"
            f"- Estado de conservação: {e.get('estado_conservacao','')}\n\n"
        )

    if isinstance(campos.get("intervencao"), dict):
        i = campos["intervencao"]
        descricao_txt += "Adequações previstas:\n"

        if isinstance(i.get("detalhes"), list):
            for item in i["detalhes"]:
                descricao_txt += f"• {item}\n"

        if "normas" in i:
            descricao_txt += f"\nNormas aplicáveis: {i['normas']}\n"

    # fallback
    if not descricao_txt:
        descricao_txt = _to_str(
            campos.get("descricao_necessidade")
            or campos.get("descricao")
            or ""
        )

    # ------------------------------------------------------------
    # MOTIVAÇÃO
    # ------------------------------------------------------------
    motivacao_txt = ""

    if isinstance(campos.get("descricao"), str):
        motivacao_txt += campos["descricao"]

    if isinstance(campos.get("localizacao"), dict):
        loc = campos["localizacao"]
        motivacao_txt += "\n\nLocalização:\n"
        motivacao_txt += f"- Endereço: {loc.get('endereco','')}\n"
        motivacao_txt += f"- Tipo de edifício: {loc.get('tipo_edificio','')}\n"

    if isinstance(campos.get("disciplinas"), list):
        motivacao_txt += "\nDisciplinas envolvidas:\n"
        for d in campos["disciplinas"]:
            motivacao_txt += f"• {d}\n"

    if not motivacao_txt:
        motivacao_txt = _to_str(campos.get("motivacao") or "")

    return {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "descricao": descricao_txt.strip(),
        "motivacao": motivacao_txt.strip(),
        "valor_estimado": valor_estimado,
    }


# ---------------------------------------------------------------
# ✨ ASSISTENTE IA
# ---------------------------------------------------------------
st.subheader("✨ Assistente IA")

if st.button("✨ Gerar rascunho com IA"):
    try:
        dfd_ai = gerar_rascunho_dfd_com_ia()

        if dfd_ai:
            st.session_state["dfd_campos_ai"] = dfd_ai
            st.success("✨ Rascunho gerado com sucesso pela IA!")
            st.rerun()
        else:
            st.warning("⚠️ A IA não conseguiu gerar um DFD estruturado.")

    except Exception as e:
        st.error(f"❌ Erro ao gerar rascunho com IA: {e}")


# ---------------------------------------------------------------
# 1️⃣ Carregar dados já existentes (sessão ou arquivo)
# ---------------------------------------------------------------
dfd_campos_brutos = obter_dfd_da_sessao()

if not dfd_campos_brutos:
    st.error("Nenhum insumo DFD encontrado. Envie um documento no módulo INSUMOS.")
    st.stop()

campos_form = mapear_campos_para_form(dfd_campos_brutos)

with st.expander("🔍 Visualizar dados brutos importados", expanded=False):
    st.json(dfd_campos_brutos)


# ---------------------------------------------------------------
# 2️⃣ Formulário administrativo
# ---------------------------------------------------------------
st.subheader("🧾 Campos do DFD")

with st.form(key="form_dfd"):

    col1, col2 = st.columns(2)
    unidade = col1.text_input("Unidade Demandante", value=campos_form["unidade_demandante"])
    responsavel = col2.text_input("Responsável pela Demanda", value=campos_form["responsavel"])

    descricao = st.text_area("Descrição da Necessidade", value=campos_form["descricao"], height=230)
    motivacao = st.text_area("Motivação / Objetivos Estratégicos", value=campos_form["motivacao"], height=180)

    col3, col4 = st.columns(2)
    prazo = col3.text_input("Prazo Estimado para Atendimento", value=campos_form["prazo_estimado"])
    valor_estimado = col4.text_input("Estimativa de Valor (R$)", value=campos_form["valor_estimado"])

    submit = st.form_submit_button("💾 Salvar DFD consolidado")


# ---------------------------------------------------------------
# 3️⃣ Salvamento final
# ---------------------------------------------------------------
if submit:
    dfd_final = {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        "valor_estimado": valor_estimado,
    }

    caminho = salvar_dfd_em_json(dfd_final, origem="formulario_dfd_streamlit")

    st.success("✅ DFD salvo com sucesso!")
    st.caption(f"Arquivo salvo em: `{caminho}`")
    st.json(dfd_final)
