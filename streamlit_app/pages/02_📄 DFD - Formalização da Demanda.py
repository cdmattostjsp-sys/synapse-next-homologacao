import streamlit as st
import json
from typing import Any, Dict

from utils.integration_dfd import (
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
        except Exception:
            return str(value)
    return str(value)


def mapear_campos_para_form(dados_brutos: Dict[str, Any]) -> Dict[str, str]:
    """
    Normaliza diferentes formatos de DFD para os campos do formulário.
    Aceita:
      - {"secoes": {...}, "lacunas": [...]}
      - {"unidade_demandante": ..., "descricao_necessidade": ...}
      - outros formatos simples.
    """

    campos = dados_brutos or {}
    if not isinstance(campos, dict):
        campos = {}

    # Núcleo de seções (quando vier do DocumentAgent)
    secoes = campos.get("secoes") if isinstance(campos.get("secoes"), dict) else {}

    # ------------------------------------------------------------
    # CAMPOS BÁSICOS (administrativos)
    # ------------------------------------------------------------
    unidade = (
        campos.get("unidade_demandante")
        or campos.get("unidade")
        or ""
    )
    responsavel = campos.get("responsavel", "")
    prazo = (
        campos.get("prazo_estimado")
        or campos.get("prazo")
        or ""
    )
    valor_estimado = (
        campos.get("valor_estimado")
        or campos.get("estimativa_valor")
        or "0,00"
    )

    # ------------------------------------------------------------
    # DESCRIÇÃO DA NECESSIDADE
    # ------------------------------------------------------------
    descricao_txt = ""

    # Se já houver descrição consolidada, priorizar
    if isinstance(campos.get("descricao_necessidade"), str) and campos["descricao_necessidade"].strip():
        descricao_txt = campos["descricao_necessidade"].strip()

    # Caso contrário, montar a partir das seções do DFD
    elif secoes:
        partes_desc = []
        for chave in ["Contexto", "Necessidade", "Escopo"]:
            v = (
                secoes.get(chave)
                or secoes.get(chave.lower())
                or secoes.get(chave.upper())
            )
            if isinstance(v, str) and v.strip():
                partes_desc.append(v.strip())
        descricao_txt = "\n\n".join(partes_desc).strip()

    # Fallback final
    if not descricao_txt:
        descricao_txt = _to_str(campos.get("descricao") or campos.get("conteudo") or "")

    # ------------------------------------------------------------
    # MOTIVAÇÃO / OBJETIVOS
    # ------------------------------------------------------------
    motivacao_txt = ""

    if isinstance(campos.get("motivacao"), str) and campos["motivacao"].strip():
        motivacao_txt = campos["motivacao"].strip()
    elif secoes:
        partes_mot = []
        for chave in ["Justificativa Legal", "Resultados Esperados", "Critérios de Sucesso"]:
            v = (
                secoes.get(chave)
                or secoes.get(chave.lower())
                or secoes.get(chave.upper())
            )
            if isinstance(v, str) and v.strip():
                partes_mot.append(v.strip())
        motivacao_txt = "\n\n".join(partes_mot).strip()

    return {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "descricao": descricao_txt,
        "motivacao": motivacao_txt,
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
            st.success("✨ Rascunho gerado com sucesso pela IA!")
            st.rerun()
        else:
            st.warning("⚠️ A IA não conseguiu gerar um DFD estruturado.")

    except Exception as e:
        st.error(f"❌ Erro ao gerar rascunho com IA: {e}")


# ---------------------------------------------------------------
# 1️⃣ Carregar dados já existentes (sessão ou arquivos)
# ---------------------------------------------------------------
dfd_campos_brutos = obter_dfd_da_sessao()

if not dfd_campos_brutos:
    st.error("Nenhum DFD encontrado. Envie um documento no módulo INSUMOS e processe como DFD.")
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

    descricao = st.text_area(
        "Descrição da Necessidade",
        value=campos_form["descricao"],
        height=230
    )
    motivacao = st.text_area(
        "Motivação / Objetivos Estratégicos / Justificativa",
        value=campos_form["motivacao"],
        height=180
    )

    col3, col4 = st.columns(2)
    prazo = col3.text_input("Prazo Estimado para Atendimento", value=campos_form["prazo_estimado"])
    valor_estimado = col4.text_input("Estimativa de Valor (R$)", value=campos_form["valor_estimado"])

    submit = st.form_submit_button("💾 Salvar DFD consolidado")


# ---------------------------------------------------------------
# 3️⃣ Salvamento final (em exports/dfd/json/)
# ---------------------------------------------------------------
if submit:
    dfd_final = {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        "valor_estimado": valor_estimado,
        # opcionalmente podemos guardar também o bruto original:
        # "origem_dados": dfd_campos_brutos,
    }

    caminho = salvar_dfd_em_json(dfd_final, origem="formulario_dfd_streamlit")

    st.success("✅ DFD consolidado salvo com sucesso!")
    st.caption(f"Arquivo salvo em: `{caminho}`")
    st.json(dfd_final)

from docx import Document
import io

st.subheader("📥 Exportar DFD")

if st.button("📄 Baixar DFD em DOCX"):
    doc = Document()

    doc.add_heading("Formalização da Demanda (DFD)", level=1)

    doc.add_heading("1. Dados Administrativos", level=2)
    doc.add_paragraph(f"Unidade Demandante: {unidade}")
    doc.add_paragraph(f"Responsável pela Demanda: {responsavel}")
    doc.add_paragraph(f"Prazo Estimado: {prazo}")
    doc.add_paragraph(f"Estimativa de Valor: R$ {valor_estimado}")

    doc.add_heading("2. Descrição da Necessidade", level=2)
    doc.add_paragraph(descricao)

    doc.add_heading("3. Motivação / Objetivos / Justificativa", level=2)
    doc.add_paragraph(motivacao)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download DOCX",
        data=buffer,
        file_name="DFD_consolidado.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
