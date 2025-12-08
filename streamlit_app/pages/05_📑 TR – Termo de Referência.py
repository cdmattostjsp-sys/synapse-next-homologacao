import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==============================
# pages/05_📑 TR – Termo de Referência.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==============================

import streamlit as st
from datetime import datetime
import os, sys, json
from io import BytesIO
from docx import Document
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.integration_tr import export_tr_to_json, ler_modelos_tr

# ==========================================================
# 🔄 Lazy Loading da OpenAI Client
# ==========================================================
def _get_openai_client():
    """Carrega OpenAI client sob demanda (lazy loading)."""
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"⚠️ Erro ao carregar OpenAI client: {e}")
        return None

# ==========================================================
# ⚙️ Configuração
# ==========================================================
st.set_page_config(page_title="📑 Termo de Referência", layout="wide", page_icon="📑")
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "📑 Termo de Referência (TR)",
    "Pré-preenchimento automático a partir de insumos + geração IA institucional"
)
st.divider()

# ==========================================================
# 🔍 Carregamento inteligente: INSUMOS → TRAgent → Formulário
# ==========================================================

# Paths dos arquivos
INSUMO_TR_PATH = os.path.join("exports", "insumos", "json", "TR_ultimo.json")
TR_JSON_PATH = os.path.join("exports", "tr_data.json")

tr_salvo = {}
insumo_detectado = False

# 1️⃣ Verificar se existe TR processado
if os.path.exists(TR_JSON_PATH):
    try:
        with open(TR_JSON_PATH, "r", encoding="utf-8") as f:
            dados_tr = json.load(f)
            tr_salvo = dados_tr.get("TR", {})
            if tr_salvo and any(v for v in tr_salvo.values() if v):
                st.success("📎 TR processado carregado (exports/tr_data.json)")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar TR: {e}")

# 2️⃣ Se não houver TR processado, verificar INSUMO bruto
if not tr_salvo or not any(v for v in tr_salvo.values() if v):
    if os.path.exists(INSUMO_TR_PATH):
        insumo_detectado = True
        st.info("📄 Insumo TR detectado. Use o botão **'Processar com IA'** para extrair as 9 seções automaticamente.")
        
        # Carregar texto bruto do insumo (para preview)
        try:
            with open(INSUMO_TR_PATH, "r", encoding="utf-8") as f:
                insumo_data = json.load(f)
                texto_bruto = insumo_data.get("conteudo_textual", "")
                
                if texto_bruto and len(texto_bruto) > 100:
                    with st.expander("👁️ Preview do insumo carregado", expanded=False):
                        st.text_area(
                            "Texto extraído do PDF/DOCX:",
                            texto_bruto[:1000] + "..." if len(texto_bruto) > 1000 else texto_bruto,
                            height=200,
                            disabled=True
                        )
        except Exception as e:
            st.warning(f"⚠️ Erro ao ler insumo: {e}")

# 3️⃣ Nenhum dado disponível
if not tr_salvo and not insumo_detectado:
    st.info("ℹ️ Nenhum TR ou insumo detectado. Faça upload no módulo **🔧 Insumos** ou preencha manualmente.")

# ==========================================================
# 🧾 Formulário TR – 9 Seções Estruturadas
# ==========================================================
st.subheader("📘 Entrada – Termo de Referência")

# ==========================================================
# Formulário com 9 seções estruturadas
# ==========================================================
st.markdown("### 📋 Seções do Termo de Referência")

# Seção 1: Objeto
objeto = st.text_area(
    "1. Objeto da Contratação",
    value=tr_salvo.get("objeto", ""),
    height=120,
    key="tr_objeto",
    help="Descrição do objeto a ser contratado"
)

col1, col2 = st.columns(2)
with col1:
    # Seção 2: Justificativa Técnica
    justificativa_tecnica = st.text_area(
        "2. Justificativa Técnica",
        value=tr_salvo.get("justificativa_tecnica", ""),
        height=150,
        key="tr_just",
        help="Fundamentação da necessidade da contratação"
    )
    
    # Seção 4: Critérios de Julgamento
    criterios_julgamento = st.text_area(
        "4. Critérios de Julgamento",
        value=tr_salvo.get("criterios_julgamento", ""),
        height=120,
        key="tr_crit",
        help="Critérios para avaliação das propostas"
    )
    
    # Seção 6: Observações Finais
    observacoes_finais = st.text_area(
        "6. Observações Finais",
        value=tr_salvo.get("observacoes_finais", ""),
        height=120,
        key="tr_obs",
        help="Informações complementares e observações"
    )

with col2:
    # Seção 3: Especificações Técnicas
    especificacao_tecnica = st.text_area(
        "3. Especificações Técnicas",
        value=tr_salvo.get("especificacao_tecnica", ""),
        height=150,
        key="tr_espec",
        help="Detalhamento técnico dos serviços/produtos"
    )
    
    # Seção 5: Riscos
    riscos = st.text_area(
        "5. Riscos Associados",
        value=tr_salvo.get("riscos", ""),
        height=120,
        key="tr_riscos",
        help="Identificação e mitigação de riscos"
    )

st.divider()

# ==========================================================
# Campos complementares (Seções 7-9)
# ==========================================================
st.markdown("### 📊 Informações Complementares")

col3, col4, col5 = st.columns(3)
with col3:
    prazo_execucao = st.text_input(
        "7. Prazo de Execução",
        value=tr_salvo.get("prazo_execucao", ""),
        key="tr_prazo",
        help="Prazo estimado para execução"
    )
with col4:
    estimativa_valor = st.text_input(
        "8. Estimativa de Valor (R$)",
        value=tr_salvo.get("estimativa_valor", ""),
        key="tr_valor",
        help="Valor estimado da contratação"
    )
with col5:
    fonte_recurso = st.text_input(
        "9. Fonte de Recurso",
        value=tr_salvo.get("fonte_recurso", ""),
        key="tr_fonte",
        help="Origem do recurso orçamentário"
    )

# ==========================================================
# Métricas de preenchimento
# ==========================================================
secoes_preenchidas = sum([
    1 if objeto else 0,
    1 if justificativa_tecnica else 0,
    1 if especificacao_tecnica else 0,
    1 if criterios_julgamento else 0,
    1 if riscos else 0,
    1 if observacoes_finais else 0,
    1 if prazo_execucao else 0,
    1 if estimativa_valor else 0,
    1 if fonte_recurso else 0,
])

col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
with col_m1:
    st.metric("📊 Seções preenchidas", f"{secoes_preenchidas}/9")
with col_m2:
    if prazo_execucao:
        st.metric("⏱️ Prazo", prazo_execucao)
with col_m3:
    if estimativa_valor:
        st.metric("💰 Valor Estimado", f"R$ {estimativa_valor}")

# ==========================================================
# ⚙️ Botão de Processamento IA
# ==========================================================
st.divider()
st.subheader("⚙️ Processamento com IA Institucional")

if st.button("✨ Processar com IA", type="primary"):
    with st.spinner("🤖 Processando TR com IA especializada..."):
        from utils.integration_tr import gerar_tr_com_ia
        
        resultado = gerar_tr_com_ia()
        
        if "erro" in resultado:
            st.error(f"❌ {resultado['erro']}")
        else:
            st.success("✅ TR processado com sucesso!")
            
            # Exibir métricas do processamento
            tr_processado = resultado.get("TR", {})
            secoes_ia = sum(1 for v in tr_processado.values() if v and v.strip())
            
            col_ia1, col_ia2, col_ia3 = st.columns(3)
            with col_ia1:
                st.metric("🤖 Seções processadas pela IA", f"{secoes_ia}/9")
            with col_ia2:
                if tr_processado.get("prazo_execucao"):
                    st.metric("⏱️ Prazo Identificado", tr_processado["prazo_execucao"])
            with col_ia3:
                if tr_processado.get("estimativa_valor"):
                    st.metric("💰 Valor Identificado", tr_processado["estimativa_valor"])
            
            st.info("🔄 Recarregue a página para visualizar os dados processados no formulário.")
            st.rerun()

st.caption("💡 O botão acima processa o TR carregado do módulo INSUMOS com IA especializada do TJSP.")

# ==========================================================
# 💾 Exportação do artefato (DOCX) - REMOVIDO
# (agora o TRAgent gera JSON estruturado, não documento Word)
# ==========================================================
