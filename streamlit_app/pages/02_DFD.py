import json
import streamlit as st
from utils.integration_dfd import (
    obter_dfd_da_sessao,
    gerar_rascunho_dfd_com_ia,
    salvar_dfd_manual,
)

# ---------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------------
st.set_page_config(
    page_title="📄 Formalização da Demanda (DFD)",
    layout="wide",
)

st.title("📄 Formalização da Demanda (DFD)")
st.caption("📌 DFD carregado a partir dos insumos processados.")
st.write(
    "Esta página consolida automaticamente o Documento de Formalização da Demanda "
    "a partir do texto extraído no módulo 🔧 **Insumos** e do rascunho gerado pela IA institucional."
)

# ---------------------------------------------------------------
# Função utilitária para limpar blocos Markdown ```json ... ```
# ---------------------------------------------------------------
def limpar_markdown_json(texto: str) -> str:
    if not isinstance(texto, str):
        return texto

    cleaned = texto.strip()
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()
    return cleaned


# ---------------------------------------------------------------
# 1️⃣ Carregar DFD processado (insumo + IA)
# ---------------------------------------------------------------
dfd_data = obter_dfd_da_sessao()

if not dfd_data:
    st.error("⚠️ Nenhum insumo DFD encontrado. Envie primeiro um documento no módulo 🔧 **Insumos**.")
    st.stop()

rascunho_raw = dfd_data.get("resultado_ia", {}).get("resposta_texto")

# Se ainda não existe resposta da IA → tentar gerar agora
if not rascunho_raw:
    with st.spinner("🔄 Gerando rascunho com IA institucional..."):
        rascunho_raw = gerar_rascunho_dfd_com_ia()

    if not rascunho_raw:
        st.error("❌ Não foi possível gerar o rascunho do DFD com IA.")
        st.stop()


# ---------------------------------------------------------------
# 2️⃣ Sanitizar e converter JSON da IA
# ---------------------------------------------------------------
try:
    texto_limpo = limpar_markdown_json(rascunho_raw)
    rascunho_json = json.loads(texto_limpo)

except Exception as e:
    st.error("❌ O rascunho retornado pela IA não está em formato JSON válido.")
    st.code(f"Json Parse Error: {str(e)}")
    st.subheader("Conteúdo recebido da IA:")
    st.code(rascunho_raw)
    st.stop()

# Agora garantimos que o JSON final esteja dentro de uma chave raiz
if "DFD" in rascunho_json:
    campos = rascunho_json["DFD"]
else:
    campos = rascunho_json


# ---------------------------------------------------------------
# 3️⃣ Função de mapeamento para formulário
# ---------------------------------------------------------------
def mapear_campos_para_form(c: dict) -> dict:

    processo = c.get("processo", {}) or {}
    objeto = c.get("objeto", {}) or {}
    necessidade = c.get("necessidade_contratacao", {}) or {}

    unidade = c.get("unidade_demandante", "") or c.get("unidade", "")
    responsavel = c.get("responsavel", "")

    prazo = ""
    vigencia = necessidade.get("vigencia_atual_contrato") or {}
    if isinstance(vigencia, dict):
        prazo = vigencia.get("data_fim", "")

    descricao = (
        necessidade.get("descricao")
        or objeto.get("descricao")
        or ""
    )

    motivacao = ""
    if "justificativa" in necessidade:
        if isinstance(necessidade["justificativa"], list):
            motivacao = "\n".join(necessidade["justificativa"])
        else:
            motivacao = necessidade["justificativa"]

    valor_estimado = objeto.get("valor_estimado", "0,00")

    return {
        "unidade": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "valor_estimado": valor_estimado,
    }


form_data = mapear_campos_para_form(campos)


# ---------------------------------------------------------------
# 4️⃣ FORMULÁRIO STREAMLIT
# ---------------------------------------------------------------
st.subheader("📌 Entrada – Formalização da Demanda")

col1, col2 = st.columns(2)

with col1:
    unidade = st.text_input("Unidade Demandante", form_data["unidade"])
    responsavel = st.text_input("Responsável pela Demanda", form_data["responsavel"])
    prazo = st.text_input("Prazo Estimado para Atendimento", form_data["prazo_estimado"])

with col2:
    descricao = st.text_area("Descrição da Necessidade", form_data["descricao"], height=120)
    motivacao = st.text_area("Motivação / Objetivos Estratégicos", form_data["motivacao"], height=120)

valor = st.text_input("Estimativa de Valor (R$)", form_data["valor_estimado"])


# ---------------------------------------------------------------
# 5️⃣ BOTÃO DE SALVAMENTO
# ---------------------------------------------------------------
if st.button("💾 Salvar DFD consolidado"):
    dfd_final = {
        "DFD": {
            "unidade_demandante": unidade,
            "responsavel": responsavel,
            "prazo_estimado": prazo,
            "descricao_necessidade": descricao,
            "motivacao": motivacao,
            "estimativa_valor": valor,
        }
    }

    salvar_dfd_manual(dfd_final)

    st.success("✅ DFD salvo com sucesso!")
    st.json(dfd_final)
