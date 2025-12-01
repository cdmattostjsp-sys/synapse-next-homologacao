import streamlit as st
import json
from typing import Any, Dict, List
from datetime import datetime

from utils.integration_dfd import (
    obter_dfd_da_sessao,
    salvar_dfd_em_json,
    gerar_rascunho_dfd_com_ia,
    status_dfd,
)

from docx import Document
import io

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


def _extrair_secoes(dados_brutos: Dict[str, Any]) -> Dict[str, str]:
    """
    Extrai as 11 seções padrão do DFD Moderno-Governança.
    Se não existirem, retorna dicionário com chaves padrão vazias.
    """
    secoes_orig = dados_brutos.get("secoes")
    secoes_final: Dict[str, str] = {}

    if not isinstance(secoes_orig, dict):
        secoes_orig = {}

    for nome in SECOES_DFD:
        valor = secoes_orig.get(nome, "")
        if not isinstance(valor, str):
            valor = _to_str(valor)
        secoes_final[nome] = valor.strip()

    return secoes_final


def _extrair_lacunas(dados_brutos: Dict[str, Any]) -> List[str]:
    lac = dados_brutos.get("lacunas", [])
    if isinstance(lac, list):
        return [str(x) for x in lac]
    return []


def _extrair_admin_e_campos_tradicionais(dados_brutos: Dict[str, Any]) -> Dict[str, str]:
    """
    Extrai os campos administrativos e os dois campos tradicionais
    (descrição + motivação), mantendo compatibilidade com formatos antigos.
    """
    campos = dados_brutos or {}
    if not isinstance(campos, dict):
        campos = {}

    secoes = campos.get("secoes") if isinstance(campos.get("secoes"), dict) else {}

    # ------------------------------------------------------------
    # CAMPOS ADMINISTRATIVOS
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
    # (Contexto + Diagnóstico + Fundamentação)
    # ------------------------------------------------------------
    descricao_txt = ""

    if isinstance(campos.get("descricao_necessidade"), str) and campos["descricao_necessidade"].strip():
        descricao_txt = campos["descricao_necessidade"].strip()

    elif secoes:
        partes_desc = []
        for chave in [
            "Contexto Institucional",
            "Diagnóstico da Situação Atual",
            "Fundamentação da Necessidade",
        ]:
            v = secoes.get(chave)
            if isinstance(v, str) and v.strip():
                partes_desc.append(v.strip())

        descricao_txt = "\n\n".join(partes_desc).strip()

    if not descricao_txt:
        descricao_txt = _to_str(campos.get("conteudo") or campos.get("descricao") or "")

    # ------------------------------------------------------------
    # MOTIVAÇÃO / OBJETIVOS / JUSTIFICATIVA
    # (Objetivos + Resultados + Benefícios + Justificativa + Riscos)
    # ------------------------------------------------------------
    motivacao_txt = ""

    if isinstance(campos.get("motivacao"), str) and campos["motivacao"].strip():
        motivacao_txt = campos["motivacao"].strip()

    elif secoes:
        partes_mot = []
        for chave in [
            "Objetivos da Contratação",
            "Resultados Esperados",
            "Benefícios Institucionais",
            "Justificativa Legal",
            "Riscos da Não Contratação",
        ]:
            v = secoes.get(chave)
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


def _montar_texto_narrativo_inicial(
    dados_brutos: Dict[str, Any],
    secoes: Dict[str, str],
    campos_tradicionais: Dict[str, str],
) -> str:
    """
    Monta o texto_narrativo inicial. Se já existir no JSON, usa direto.
    Caso contrário, monta uma versão numerada a partir das seções,
    ou, em último caso, a partir de descrição + motivação.
    """
    existente = dados_brutos.get("texto_narrativo")
    if isinstance(existente, str) and existente.strip():
        return existente.strip()

    # Tentar construir com base nas 11 seções
    partes = []
    idx = 1
    for nome in SECOES_DFD:
        texto_secao = secoes.get(nome, "").strip()
        if texto_secao:
            partes.append(f"{idx}. {texto_secao}")
            idx += 1

    if partes:
        return "\n\n".join(partes)

    # Fallback: descrição + motivação
    descricao = campos_tradicionais.get("descricao", "").strip()
    motivacao = campos_tradicionais.get("motivacao", "").strip()

    partes = []
    if descricao:
        partes.append(f"1. {descricao}")
    if motivacao:
        partes.append(f"2. {motivacao}")

    return "\n\n".join(partes).strip()


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
dfd_dados = obter_dfd_da_sessao()

if not dfd_dados:
    st.error("Nenhum DFD encontrado. Envie um documento no módulo INSUMOS e processe como DFD.")
    st.stop()

# Caso venha algo como {"DFD": {...}}, normalizar para o interior
if isinstance(dfd_dados, dict) and "DFD" in dfd_dados:
    dfd_dados = dfd_dados.get("DFD") or {}

campos_trad = _extrair_admin_e_campos_tradicionais(dfd_dados)
secoes_iniciais = _extrair_secoes(dfd_dados)
lacunas_iniciais = _extrair_lacunas(dfd_dados)
texto_narrativo_inicial = _montar_texto_narrativo_inicial(
    dfd_dados,
    secoes_iniciais,
    campos_trad,
)

with st.expander("🔍 Visualizar dados brutos importados (JSON completo)", expanded=False):
    st.json(dfd_dados)


# ---------------------------------------------------------------
# 2️⃣ Formulário administrativo + estrutura completa do DFD
# ---------------------------------------------------------------
st.subheader("🧾 DFD – Dados Administrativos e Estrutura Completa")

with st.form(key="form_dfd_moderno"):

    st.markdown("### 1. Dados Administrativos")

    col1, col2 = st.columns(2)
    unidade = col1.text_input("Unidade Demandante", value=campos_trad["unidade_demandante"])
    responsavel = col2.text_input("Responsável pela Demanda", value=campos_trad["responsavel"])

    col3, col4 = st.columns(2)
    prazo = col3.text_input("Prazo Estimado para Atendimento", value=campos_trad["prazo_estimado"])
    valor_estimado = col4.text_input("Estimativa de Valor (R$)", value=campos_trad["valor_estimado"])

    st.markdown("---")
    st.markdown("### 2. Síntese Tradicional do DFD")

    descricao = st.text_area(
        "Descrição da Necessidade (síntese)",
        value=campos_trad["descricao"],
        height=180,
    )

    motivacao = st.text_area(
        "Motivação / Objetivos Estratégicos / Justificativa (síntese)",
        value=campos_trad["motivacao"],
        height=180,
    )

    st.markdown("---")
    st.markdown("### 3. Texto Narrativo Consolidado (DFD Moderno-Governança)")

    texto_narrativo = st.text_area(
        "Texto narrativo completo (numerado, pronto para dossiê)",
        value=texto_narrativo_inicial,
        height=260,
    )

    st.markdown("---")
    st.markdown("### 4. Seções Estruturadas do DFD (11 seções)")

    secoes_editadas: Dict[str, str] = {}

    with st.expander("✏️ Editar seções individualmente (estrutura Moderno-Governança)", expanded=False):
        for nome_secao in SECOES_DFD:
            secoes_editadas[nome_secao] = st.text_area(
                nome_secao,
                value=secoes_iniciais.get(nome_secao, ""),
                height=140,
            )

    st.markdown("---")
    st.markdown("### 5. Lacunas identificadas pela IA")

    if lacunas_iniciais:
        for item in lacunas_iniciais:
            st.markdown(f"- {item}")
    else:
        st.caption("Nenhuma lacuna foi identificada automaticamente pela IA para este DFD.")

    submit = st.form_submit_button("💾 Salvar DFD consolidado")


# ---------------------------------------------------------------
# 3️⃣ Salvamento final (JSON completo – modelo moderno)
# ---------------------------------------------------------------
if submit:
    dfd_final = {
        # Administrativos
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "valor_estimado": valor_estimado,
        # Campo tradicional (síntese)
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        # Estrutura moderna
        "texto_narrativo": texto_narrativo,
        "secoes": secoes_editadas,
        "lacunas": lacunas_iniciais,
        # Metadado auxiliar opcional
        "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origem": "dfd_moderno_streamlit",
    }

    caminho = salvar_dfd_em_json(dfd_final, origem="formulario_dfd_moderno_streamlit")

    st.success("✅ DFD consolidado salvo com sucesso!")
    st.caption(f"Arquivo salvo em: `{caminho}`")
    st.json(dfd_final)


# ---------------------------------------------------------------
# 📥 Exportação DOCX (completo)
# ---------------------------------------------------------------
st.subheader("📥 Exportar DFD em DOCX")

if st.button("📄 Baixar DFD em DOCX"):
    doc = Document()

    doc.add_heading("Formalização da Demanda (DFD)", level=1)

    # 1. Dados Administrativos
    doc.add_heading("1. Dados Administrativos", level=2)
    doc.add_paragraph(f"Unidade Demandante: {unidade}")
    doc.add_paragraph(f"Responsável pela Demanda: {responsavel}")
    doc.add_paragraph(f"Prazo Estimado: {prazo}")
    doc.add_paragraph(f"Estimativa de Valor: R$ {valor_estimado}")

    # 2. Texto narrativo consolidado
    doc.add_heading("2. Texto Narrativo Consolidado", level=2)
    doc.add_paragraph(texto_narrativo)

    # 3. Síntese tradicional
    doc.add_heading("3. Síntese Tradicional do DFD", level=2)
    doc.add_heading("3.1 Descrição da Necessidade", level=3)
    doc.add_paragraph(descricao)
    doc.add_heading("3.2 Motivação / Objetivos / Justificativa", level=3)
    doc.add_paragraph(motivacao)

    # 4. Seções estruturadas
    doc.add_heading("4. Seções Estruturadas (Modelo Moderno-Governança)", level=2)
    for nome_secao in SECOES_DFD:
        doc.add_heading(nome_secao, level=3)
        doc.add_paragraph(secoes_editadas.get(nome_secao, ""))

    # 5. Lacunas
    doc.add_heading("5. Lacunas Identificadas", level=2)
    if lacunas_iniciais:
        for item in lacunas_iniciais:
            doc.add_paragraph(f"- {item}")
    else:
        doc.add_paragraph("Não foram identificadas lacunas relevantes pela IA para este DFD.")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download DOCX (DFD completo)",
        data=buffer,
        file_name="DFD_consolidado_moderno.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
