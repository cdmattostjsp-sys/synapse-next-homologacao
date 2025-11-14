import streamlit as st
from utils.integration_dfd import (
    obter_dfd_da_sessao,
    salvar_dfd_em_json,
    status_dfd,
)

st.set_page_config(
    page_title="📄 Formalização da Demanda (DFD)",
    layout="wide",
)

st.title("📄 Formalização da Demanda (DFD)")
st.caption(status_dfd())
st.write("Registro institucional da demanda a partir do insumo processado no módulo 🔧 Insumos.")

# ---------------------------------------------------------------
# 1️⃣ Carregar DFD processado (campos vindos da IA)
# ---------------------------------------------------------------
dfd_campos = obter_dfd_da_sessao()

if not dfd_campos:
    st.info(
        "Nenhum DFD encontrado. "
        "Por favor, envie um documento na página '🔧 Insumos' com o artefato DFD."
    )
    st.stop()


# ---------------------------------------------------------------
# 2️⃣ Função de mapeamento: JSON da IA → campos do formulário
# ---------------------------------------------------------------
def mapear_campos_para_form(campos: dict) -> dict:
    """
    Converte a estrutura JSON retornada pela IA (DFD, objeto, necessidade_contratacao, etc.)
    em campos planos para o formulário do DFD.
    """

    processo = campos.get("processo", {}) or {}
    objeto = campos.get("objeto", {}) or {}
    necessidade = campos.get("necessidade_contratacao", {}) or {}

    # Unidade e responsável muitas vezes não vêm da IA – mantemos em branco por padrão
    unidade_demandante = campos.get("unidade_demandante", "") or campos.get("unidade", "") or ""
    responsavel = campos.get("responsavel", "")

    # Prazo estimado: usamos, se existir, a data de fim da vigência atual do contrato
    prazo_estimado = ""
    vigencia = necessidade.get("vigencia_atual_contrato") or {}
    if isinstance(vigencia, dict):
        prazo_estimado = vigencia.get("data_fim", "")

    # Descrição da necessidade: prioriza seção específica, depois o objeto
    descricao_necessidade = (
        necessidade.get("descricao")
        or objeto.get("descricao")
        or ""
    )

    # Motivação / objetivos: junta lista de justificativas, se houver
    motivacao = ""
    justificativa = necessidade.get("justificativa")
    if isinstance(justificativa, list):
        motivacao = " ".join(str(j) for j in justificativa)
    elif isinstance(justificativa, str):
        motivacao = justificativa

    # Estimativa de valor – se não vier nada, usamos 0.0
    estimativa_valor = 0.0
    bruto_est = campos.get("estimativa_valor")
    if bruto_est not in (None, ""):
        try:
            estimativa_valor = float(str(bruto_est).replace(".", "").replace(",", "."))
        except Exception:
            estimativa_valor = 0.0

    return {
        "unidade_demandante": unidade_demandante,
        "responsavel": responsavel,
        "prazo_estimado": prazo_estimado,
        "descricao_necessidade": descricao_necessidade,
        "motivacao": motivacao,
        "estimativa_valor": estimativa_valor,
    }


valores_iniciais = mapear_campos_para_form(dfd_campos)

# ---------------------------------------------------------------
# 3️⃣ Formulário editável
# ---------------------------------------------------------------
st.subheader("1️⃣ Entrada – Formalização da Demanda")

col1, col2 = st.columns(2)

with col1:
    unidade = st.text_input(
        "Unidade Demandante",
        value=valores_iniciais["unidade_demandante"],
    )
    responsavel = st.text_input(
        "Responsável pela Demanda",
        value=valores_iniciais["responsavel"],
    )
    prazo = st.text_input(
        "Prazo Estimado para Atendimento",
        value=valores_iniciais["prazo_estimado"],
    )

with col2:
    descricao = st.text_area(
        "Descrição da Necessidade",
        value=valores_iniciais["descricao_necessidade"],
        height=140,
    )
    motivacao = st.text_area(
        "Motivação / Objetivos Estratégicos",
        value=valores_iniciais["motivacao"],
        height=140,
    )
    estimativa_valor = st.number_input(
        "Estimativa de Valor (R$)",
        value=float(valores_iniciais["estimativa_valor"]),
        step=100.00,
        format="%.2f",
    )

st.markdown("---")

# ---------------------------------------------------------------
# 4️⃣ Ações: salvar DFD consolidado
# ---------------------------------------------------------------
if st.button("💾 Salvar DFD consolidado"):
    campos_atualizados = dict(dfd_campos)  # copia o que veio da IA
    campos_atualizados.update(
        {
            "unidade_demandante": unidade,
            "responsavel": responsavel,
            "prazo_estimado": prazo,
            "descricao_necessidade": descricao,
            "motivacao": motivacao,
            "estimativa_valor": estimativa_valor,
        }
    )

    caminho = salvar_dfd_em_json(campos_atualizados, origem="formulario")
    if caminho:
        st.success(f"DFD salvo com sucesso em: {caminho}")
    else:
        st.warning("⚠️ Não foi possível salvar o DFD em disco.")

# ---------------------------------------------------------------
# 5️⃣ Visualizar estrutura final que seguirá para ETP / TR / Edital
# ---------------------------------------------------------------
st.markdown("---")
st.subheader("📦 Estrutura DFD (campos_ai) consolidada")

st.json(dfd_campos)
