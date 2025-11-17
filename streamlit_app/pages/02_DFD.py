import streamlit as st
import json
from typing import Any, Dict

from utils.dfd.integration_dfd import (
    obter_dfd_da_sessao,
    salvar_dfd_em_json,
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
    """Converte qualquer estrutura em string legível para o formulário."""
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False, indent=2)
        except Exception:
            return str(value)
    return str(value)


def _normalizar_campos(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza diferentes formatos possíveis do pipeline:
    - { "DFD": {...} }
    - { "secoes": {...} }
    - { "campos_ai": {...} }
    - { ...campos soltos... }
    """
    if not isinstance(dados, dict):
        return {}

    if "campos_ai" in dados and isinstance(dados["campos_ai"], dict):
        return dados["campos_ai"]
    if "DFD" in dados and isinstance(dados["DFD"], dict):
        return dados["DFD"]
    if "secoes" in dados and isinstance(dados["secoes"], dict):
        return dados["secoes"]

    return dados


# ---------------------------------------------------------------
# 🔥 Função NOVA – converte JSON estruturado em texto institucional
# ---------------------------------------------------------------
def mapear_campos_para_form(dados_brutos: Dict[str, Any]) -> Dict[str, str]:
    """
    Converte dicionários estruturados (JSON) em textos legíveis
    para o formulário institucional do DFD.
    """
    campos = _normalizar_campos(dados_brutos)

    # ------------------------------------------------------------
    # CAMPOS BÁSICOS
    # ------------------------------------------------------------
    unidade = campos.get("unidade_demandante") or campos.get("unidade") or ""
    responsavel = campos.get("responsavel", "")
    prazo = campos.get("prazo_estimado") or campos.get("prazo") or ""
    valor_estimado = campos.get("valor_estimado") or campos.get("estimativa_valor") or "0,00"

    # ------------------------------------------------------------
    # DESCRIÇÃO — texto consolidado a partir do JSON estruturado
    # ------------------------------------------------------------
    descricao_txt = ""

    # Informações do edifício
    if "edificio" in campos and isinstance(campos["edificio"], dict):
        e = campos["edificio"]
        descricao_txt += (
            "Características do edifício:\n"
            f"- Pavimentos: {e.get('pavimentos','')}\n"
            f"- Área total: {e.get('area','')}\n"
            f"- Ano de inauguração: {e.get('ano_inauguracao','')}\n"
            f"- Estado de conservação: {e.get('estado_conservacao','')}\n\n"
        )

    # Informações da intervenção
    if "intervencao" in campos and isinstance(campos["intervencao"], dict):
        i = campos["intervencao"]

        descricao_txt += "Adequações previstas para acessibilidade:\n"

        # detalhes
        if "detalhes" in i and isinstance(i["detalhes"], list):
            for item in i["detalhes"]:
                descricao_txt += f"• {item}\n"

        # normas
        if "normas" in i:
            descricao_txt += f"\nNormas aplicáveis: {i.get('normas','')}\n"

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

    if "descricao" in campos and isinstance(campos["descricao"], str):
        motivacao_txt += campos["descricao"]

    if "localizacao" in campos and isinstance(campos["localizacao"], dict):
        loc = campos["localizacao"]
        motivacao_txt += "\n\nLocalização da intervenção:\n"
        motivacao_txt += f"- Endereço: {loc.get('endereco','')}\n"
        motivacao_txt += f"- Tipo de edifício: {loc.get('tipo_edificio','')}\n"

    if "disciplinas" in campos and isinstance(campos["disciplinas"], list):
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
# 1️⃣ Carregar DFD processado (insumo + IA)
# ---------------------------------------------------------------
dfd_campos_brutos = obter_dfd_da_sessao()

if not dfd_campos_brutos:
    st.error(
        "⚠️ Nenhum insumo DFD encontrado.\n\n"
        "Envie primeiro um documento no módulo 🔧 **Insumos** "
        "e selecione o destino **DFD**."
    )
    st.stop()

campos_form = mapear_campos_para_form(dfd_campos_brutos)

with st.expander("🔍 Visualizar dados brutos importados", expanded=False):
    st.json(dfd_campos_brutos)

# ---------------------------------------------------------------
# 2️⃣ FORMULÁRIO STREAMLIT – edição do DFD
# ---------------------------------------------------------------
st.subheader("🧾 Campos do DFD")

with st.form(key="form_dfd"):

    col1, col2 = st.columns(2)

    unidade = col1.text_input(
        "Unidade Demandante",
        value=campos_form["unidade_demandante"],
    )
    responsavel = col2.text_input(
        "Responsável pela Demanda",
        value=campos_form["responsavel"],
    )

    descricao = st.text_area(
        "Descrição da Necessidade",
        value=campos_form["descricao"],
        height=230,
    )
    motivacao = st.text_area(
        "Motivação / Objetivos Estratégicos",
        value=campos_form["motivacao"],
        height=180,
    )

    col3, col4 = st.columns(2)

    prazo = col3.text_input(
        "Prazo Estimado para Atendimento",
        value=campos_form["prazo_estimado"],
    )
    valor_estimado = col4.text_input(
        "Estimativa de Valor (R$)",
        value=campos_form["valor_estimado"],
    )

    submit = st.form_submit_button("💾 Salvar DFD consolidado")

# ---------------------------------------------------------------
# 3️⃣ Salvamento do DFD consolidado
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

    st.success("✅ DFD salvo com sucesso.")
    st.caption(f"Arquivo atualizado em: `{caminho}`")
    st.json(dfd_final)
