import json
from typing import Any, Dict

import streamlit as st
from utils.integration_dfd import (
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
    Normaliza diferentes formatos possíveis de retorno da IA para um
    dicionário plano de campos.

    Aceita, por exemplo:
      { "DFD": {...} }
      { "secoes": {...} }
      { "campos_ai": {...} }
      { ...campos soltos... }
    """
    if not isinstance(dados, dict):
        return {}

    # Camadas mais comuns
    if "campos_ai" in dados and isinstance(dados["campos_ai"], dict):
        dados = dados["campos_ai"]
    elif "DFD" in dados and isinstance(dados["DFD"], dict):
        dados = dados["DFD"]
    elif "secoes" in dados and isinstance(dados["secoes"], dict):
        # Em muitos casos "secoes" já é um mapa de textos por seção
        dados = dados["secoes"]

    return dados


def mapear_campos_para_form(dados_brutos: Dict[str, Any]) -> Dict[str, str]:
    """
    Converte o dicionário bruto (vindo da IA / insumos) em campos planos
    para o formulário institucional do DFD.
    """
    campos = _normalizar_campos(dados_brutos)

    # Unidade / responsável
    unidade = (
        campos.get("unidade_demandante")
        or campos.get("unidade")
        or ""
    )
    responsavel = campos.get("responsavel", "")

    # Prazo
    prazo = (
        campos.get("prazo_estimado")
        or campos.get("prazo")
        or ""
    )

    # Estimativa de valor
    valor_estimado = (
        campos.get("valor_estimado")
        or campos.get("estimativa_valor")
        or ""
    )

    # Descrição e motivação – heurísticas a partir de diversas chaves
    descricao_partes = []
    motivacao_partes = []

    # Descrição da necessidade
    desc_necess = campos.get("descricao_necessidade") or campos.get("descricao")
    if desc_necess:
        descricao_partes.append(_to_str(desc_necess))

    # Secções genéricas – tenta classificar por nome da chave
    for chave, valor in campos.items():
        if not valor:
            continue
        chave_lower = str(chave).lower()

        if any(tok in chave_lower for tok in ["motiv", "justific", "objetivo"]):
            motivacao_partes.append(_to_str(valor))
        elif any(tok in chave_lower for tok in ["descr", "necess", "objeto"]):
            descricao_partes.append(_to_str(valor))

    descricao = "\n\n".join(partes for partes in descricao_partes if partes).strip()
    motivacao = "\n\n".join(partes for partes in motivacao_partes if partes).strip()

    return {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "valor_estimado": valor_estimado if valor_estimado else "0,00",
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
