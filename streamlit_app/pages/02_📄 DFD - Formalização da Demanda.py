# ==========================================================
# 02_📄 DFD – Formalização da Demanda (Versão Final 2025-D7)
# Fluxo completo: Insumos → DFD → IA → DOCX
# Compatível com integration_dfd.py (D7) e DocumentAgent D2
# ==========================================================

import streamlit as st
import json
from typing import Any, Dict, List
from datetime import datetime
from docx import Document
import io

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
st.caption("📌 DFD carregado automaticamente a partir dos insumos enviados no módulo 🔧 Insumos.")
st.info(status_dfd())


# ---------------------------------------------------------------
# Constantes – padrão Moderno-Governança (11 seções)
# ---------------------------------------------------------------
SECOES_DFD: List[str] = [
    "Contexto Institucional",
    "Diagnóstico da Situação Atual",
    "Fundamentação da Necessidade",
    "Objetivos da Contratação",
    "Escopo Inicial da Demanda",
    "Resultados Esperados",
    "Benefícios Institucionais",
    "Justificativa Legal",
    "Riscos da Não Contratação",
    "Requisitos Mínimos",
    "Critérios de Sucesso",
]


# ---------------------------------------------------------------
# Helper para conversão genérica
# ---------------------------------------------------------------
def _to_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False, indent=2)
        except Exception:
            return str(value)
    return str(value)


# ---------------------------------------------------------------
# 1) Carregar DFD existente da sessão ou dos insumos
# ---------------------------------------------------------------
dfd_dados = obter_dfd_da_sessao()

if not dfd_dados:
    st.error("❌ Nenhum DFD disponível. Envie um documento no módulo INSUMOS e processe como DFD.")
    st.stop()

# 🔄 Compatibilidade: caso venha {"DFD": {...}}
if isinstance(dfd_dados, dict) and "DFD" in dfd_dados:
    dfd_dados = dfd_dados["DFD"]

# ---------------------------------------------------------------
# 2) Extrair campos
# ---------------------------------------------------------------
def extrair_campos(dados: dict) -> tuple:
    campos = {
        "unidade_demandante": dados.get("unidade_demandante", ""),
        "responsavel": dados.get("responsavel", ""),
        "prazo_estimado": dados.get("prazo_estimado", ""),
        "valor_estimado": dados.get("valor_estimado", "0,00"),
        "descricao_necessidade": dados.get("descricao_necessidade", ""),
        "motivacao": dados.get("motivacao", ""),
        "texto_narrativo": dados.get("texto_narrativo", ""),
        "secoes": dados.get("secoes", {}),
        "lacunas": dados.get("lacunas", []),
    }

    secoes = campos["secoes"]
    if not isinstance(secoes, dict):
        secoes = {s: "" for s in SECOES_DFD}

    texto_narr = campos["texto_narrativo"]
    if not isinstance(texto_narr, str) or len(texto_narr.strip()) < 5:
        texto_narr = "\n\n".join(
            f"{i+1}. {secoes.get(sec, '')}" for i, sec in enumerate(SECOES_DFD)
        )

    return campos, secoes, texto_narr


campos_trad, secoes_orig, texto_narrativo_inicial = extrair_campos(dfd_dados)


# ---------------------------------------------------------------
# DEBUG – Dados brutos (para inspeção)
# ---------------------------------------------------------------
with st.expander("🔍 Visualizar dados brutos importados (JSON completo)", expanded=False):
    st.json(dfd_dados)


# ---------------------------------------------------------------
# ✨ IA – Gerar rascunho (DFD moderno)
# ---------------------------------------------------------------
st.subheader("✨ Assistente IA")

if st.button("✨ Gerar rascunho completo com IA"):
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
# 3) Formulário completo do DFD
# ---------------------------------------------------------------
st.subheader("🧾 DFD – Dados Administrativos e Estrutura Completa")

with st.form(key="form_dfd_moderno"):

    # -----------------------------------------
    # Dados Administrativos
    # -----------------------------------------
    st.markdown("### 1. Dados Administrativos")

    col1, col2 = st.columns(2)
    unidade = col1.text_input("Unidade Demandante", value=campos_trad["unidade_demandante"])
    responsavel = col2.text_input("Responsável", value=campos_trad["responsavel"])

    col3, col4 = st.columns(2)
    prazo = col3.text_input("Prazo Estimado", value=campos_trad["prazo_estimado"])
    valor_estimado = col4.text_input("Valor Estimado (R$)", value=campos_trad["valor_estimado"])

    st.markdown("---")

    # -----------------------------------------
    # Síntese Tradicional (DFD clássico)
    # -----------------------------------------
    st.markdown("### 2. Síntese Tradicional")

    descricao = st.text_area(
        "Descrição da Necessidade",
        value=campos_trad["descricao_necessidade"],
        height=180,
    )

    motivacao = st.text_area(
        "Motivação / Justificativas",
        value=campos_trad["motivacao"],
        height=180,
    )

    st.markdown("---")

    # -----------------------------------------
    # Texto Narrativo
    # -----------------------------------------
    st.markdown("### 3. Texto Narrativo Consolidado")

    texto_narrativo = st.text_area(
        "Narrativa completa e numerada",
        value=texto_narrativo_inicial,
        height=260,
    )

    st.markdown("---")

    # -----------------------------------------
    # Seções Modernas (11 seções)
    # -----------------------------------------
    st.markdown("### 4. Estrutura Moderno-Governança")

    secoes_editadas: Dict[str, str] = {}
    with st.expander("✏️ Editar 11 Seções Individualmente", expanded=False):
        for nome_secao in SECOES_DFD:
            secoes_editadas[nome_secao] = st.text_area(
                nome_secao,
                value=secoes_orig.get(nome_secao, ""),
                height=140,
            )

    # -----------------------------------------
    # Lacunas apontadas pela IA
    # -----------------------------------------
    st.markdown("---")
    st.markdown("### 5. Lacunas Identificadas pela IA")

    if campos_trad["lacunas"]:
        for item in campos_trad["lacunas"]:
            st.markdown(f"- {item}")
    else:
        st.caption("Nenhuma lacuna identificada.")

    salvar = st.form_submit_button("💾 Salvar DFD consolidado")


# ---------------------------------------------------------------
# Salvamento final
# ---------------------------------------------------------------
if salvar:

    dfd_final = {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "valor_estimado": valor_estimado,
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        "texto_narrativo": texto_narrativo,
        "secoes": secoes_editadas,
        "lacunas": campos_trad["lacunas"],
        "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origem": "form_dfd_moderno_streamlit",
    }

    caminho = salvar_dfd_em_json(dfd_final)

    if caminho:
        st.success("✅ DFD consolidado salvo com sucesso!")
        st.caption(f"Arquivo salvo em: `{caminho}`")
        st.json(dfd_final)
    else:
        st.warning("⚠️ DFD não foi salvo (conteúdo vazio ou inválido).")


# ---------------------------------------------------------------
# Exportação para DOCX
# ---------------------------------------------------------------
st.subheader("📥 Exportar DFD em DOCX")

if st.button("📄 Baixar DFD em DOCX"):

    doc = Document()
    doc.add_heading("Formalização da Demanda (DFD)", level=1)

    # Administrativos
    doc.add_heading("Dados Administrativos", level=2)
    doc.add_paragraph(f"Unidade Demandante: {unidade}")
    doc.add_paragraph(f"Responsável: {responsavel}")
    doc.add_paragraph(f"Prazo Estimado: {prazo}")
    doc.add_paragraph(f"Estimativa de Valor: R$ {valor_estimado}")

    # Texto narrativo
    doc.add_heading("Texto Narrativo Consolidado", level=2)
    doc.add_paragraph(texto_narrativo)

    # Síntese tradicional
    doc.add_heading("Síntese Tradicional", level=2)
    doc.add_heading("Descrição da Necessidade", level=3)
    doc.add_paragraph(descricao)
    doc.add_heading("Motivação / Justificativa", level=3)
    doc.add_paragraph(motivacao)

    # Estrutura moderna
    doc.add_heading("Seções Moderno-Governança (11 seções)", level=2)
    for nome_secao in SECOES_DFD:
        doc.add_heading(nome_secao, level=3)
        doc.add_paragraph(secoes_editadas.get(nome_secao, ""))

    # Lacunas
    doc.add_heading("Lacunas Identificadas", level=2)
    if campos_trad["lacunas"]:
        for item in campos_trad["lacunas"]:
            doc.add_paragraph(f"- {item}")
    else:
        doc.add_paragraph("Nenhuma lacuna identificada.")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download DOCX",
        data=buffer,
        file_name="DFD_consolidado.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
