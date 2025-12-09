import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==============================
# pages/06_📜 Edital – Minuta do Edital.py  –  SynapseNext / SAAB TJSP
# ==============================

import os, sys, json
from datetime import datetime
from io import BytesIO
from pathlib import Path
import streamlit as st
from docx import Document

# ==========================================================
# 🔍 Imports e configuração de ambiente
# ==========================================================

from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.integration_edital import integrar_com_contexto, gerar_edital_com_ia

st.set_page_config(page_title="📜 Edital – Minuta", layout="wide", page_icon="📜")
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "📜 Minuta do Edital de Licitação",
    "Geração automatizada com IA institucional a partir dos artefatos DFD, ETP e TR"
)
st.divider()

# ==========================================================
# 🔍 Carregamento inteligente: INSUMOS + Contexto → EditalAgent → Formulário
# ==========================================================

# Paths dos arquivos
INSUMO_EDITAL_PATH = os.path.join("exports", "insumos", "json", "EDITAL_ultimo.json")
EDITAL_JSON_PATH = os.path.join("exports", "edital_data.json")

# Integrar contexto de DFD/ETP/TR
contexto = integrar_com_contexto(st.session_state)
if contexto:
    st.success(f"📎 Contexto integrado: {', '.join(contexto.keys())}")

edital_salvo = {}
insumo_detectado = False

# 1️⃣ Verificar se existe Edital processado
if os.path.exists(EDITAL_JSON_PATH):
    try:
        with open(EDITAL_JSON_PATH, "r", encoding="utf-8") as f:
            dados_edital = json.load(f)
            edital_salvo = dados_edital.get("EDITAL", {})
            if edital_salvo and any(v for v in edital_salvo.values() if v):
                st.success("📎 Edital processado carregado (exports/edital_data.json)")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar Edital: {e}")

# 2️⃣ Se não houver Edital processado, verificar INSUMO bruto
if not edital_salvo or not any(v for v in edital_salvo.values() if v):
    if os.path.exists(INSUMO_EDITAL_PATH):
        insumo_detectado = True
        st.info("📄 Insumo EDITAL detectado. Use o botão **'Processar com IA'** para extrair os 12 campos automaticamente.")
        
        # Carregar texto bruto do insumo (para preview)
        try:
            with open(INSUMO_EDITAL_PATH, "r", encoding="utf-8") as f:
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
if not edital_salvo and not insumo_detectado and not contexto:
    st.info("ℹ️ Nenhum Edital ou insumo detectado. Faça upload no módulo **🔧 Insumos** ou preencha dados em DFD/ETP/TR primeiro.")

# ==========================================================
# 🧾 Formulário Edital – 12 Campos Estruturados
# ==========================================================
st.subheader("📘 Entrada – Edital de Licitação")

st.markdown("### 📋 Identificação")
col1, col2 = st.columns(2)
with col1:
    numero_edital = st.text_input(
        "Número do Edital",
        value=edital_salvo.get("numero_edital", ""),
        key="ed_numero",
        help="Identificação única do edital"
    )
    
with col2:
    data_publicacao = st.text_input(
        "Data de Publicação",
        value=edital_salvo.get("data_publicacao", ""),
        key="ed_data",
        help="Data de divulgação do edital"
    )

st.markdown("### 📋 Objeto e Modalidade")

objeto = st.text_area(
    "1. Objeto da Licitação",
    value=edital_salvo.get("objeto", ""),
    height=120,
    key="ed_objeto",
    help="Descrição do que será licitado"
)

col3, col4 = st.columns(2)
with col3:
    tipo_licitacao = st.text_input(
        "2. Tipo de Licitação",
        value=edital_salvo.get("tipo_licitacao", ""),
        key="ed_tipo",
        help="Pregão eletrônico, concorrência, etc."
    )
    
with col4:
    criterio_julgamento = st.text_input(
        "3. Critério de Julgamento",
        value=edital_salvo.get("criterio_julgamento", ""),
        key="ed_criterio",
        help="Menor preço, melhor técnica, etc."
    )

st.markdown("### 📋 Requisitos e Condições")

col5, col6 = st.columns(2)
with col5:
    condicoes_participacao = st.text_area(
        "4. Condições de Participação",
        value=edital_salvo.get("condicoes_participacao", ""),
        height=120,
        key="ed_cond",
        help="Requisitos para participar"
    )
    
    obrigacoes_contratada = st.text_area(
        "6. Obrigações da Contratada",
        value=edital_salvo.get("obrigacoes_contratada", ""),
        height=120,
        key="ed_obrig",
        help="Deveres da empresa vencedora"
    )

with col6:
    exigencias_habilitacao = st.text_area(
        "5. Exigências de Habilitação",
        value=edital_salvo.get("exigencias_habilitacao", ""),
        height=120,
        key="ed_exig",
        help="Documentação necessária"
    )
    
    observacoes_gerais = st.text_area(
        "10. Observações Gerais",
        value=edital_salvo.get("observacoes_gerais", ""),
        height=120,
        key="ed_obs",
        help="Informações complementares"
    )

st.markdown("### 📋 Informações Administrativas")

col7, col8, col9 = st.columns(3)
with col7:
    prazo_execucao = st.text_input(
        "7. Prazo de Execução",
        value=edital_salvo.get("prazo_execucao", ""),
        key="ed_prazo"
    )
    
with col8:
    fontes_recursos = st.text_input(
        "8. Fontes de Recursos",
        value=edital_salvo.get("fontes_recursos", ""),
        key="ed_fonte"
    )
    
with col9:
    gestor_fiscal = st.text_input(
        "9. Gestor/Fiscal",
        value=edital_salvo.get("gestor_fiscal", ""),
        key="ed_gestor"
    )

# ==========================================================
# Métricas de preenchimento
# ==========================================================
campos_preenchidos = sum([
    1 if numero_edital else 0,
    1 if data_publicacao else 0,
    1 if objeto else 0,
    1 if tipo_licitacao else 0,
    1 if criterio_julgamento else 0,
    1 if condicoes_participacao else 0,
    1 if exigencias_habilitacao else 0,
    1 if obrigacoes_contratada else 0,
    1 if prazo_execucao else 0,
    1 if fontes_recursos else 0,
    1 if gestor_fiscal else 0,
    1 if observacoes_gerais else 0,
])

col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
with col_m1:
    st.metric("📊 Campos preenchidos", f"{campos_preenchidos}/12")
with col_m2:
    if tipo_licitacao:
        st.metric("📋 Modalidade", tipo_licitacao)
with col_m3:
    if criterio_julgamento:
        st.metric("⚖️ Critério", criterio_julgamento)

# ==========================================================
# ⚙️ Botão de Processamento IA
# ==========================================================
st.divider()
st.subheader("⚙️ Processamento com IA Institucional")

if st.button("✨ Processar com IA", type="primary"):
    with st.spinner("🤖 Processando Edital com IA especializada..."):
        resultado = gerar_edital_com_ia(contexto_previo=contexto)
        
        if "erro" in resultado:
            st.error(f"❌ {resultado['erro']}")
        else:
            st.success("✅ Edital processado com sucesso!")
            
            # Exibir métricas do processamento
            edital_processado = resultado.get("EDITAL", {})
            campos_ia = sum(1 for v in edital_processado.values() if v and v.strip())
            
            col_ia1, col_ia2, col_ia3 = st.columns(3)
            with col_ia1:
                st.metric("🤖 Campos processados pela IA", f"{campos_ia}/12")
            with col_ia2:
                if edital_processado.get("numero_edital"):
                    st.metric("📋 Número Edital", edital_processado["numero_edital"])
            with col_ia3:
                if edital_processado.get("tipo_licitacao"):
                    st.metric("📝 Modalidade", edital_processado["tipo_licitacao"])
            
            # CRITICAL: Salvar dados do edital para integração com Validador
            st.session_state["edital_campos_ai"] = edital_processado
            st.session_state["edital_processado_agora"] = True
            
            st.info("⬇️ Role para baixo para visualizar os botões de download do documento.")
            st.success("✅ Edital disponível para validação no módulo **🧩 Validador de Editais**")

st.caption("💡 O botão acima processa o Edital carregado do módulo INSUMOS + contexto DFD/ETP/TR com IA especializada do TJSP.")

# ==========================================================
# 📥 Exportação de Documentos
# ==========================================================
st.divider()
st.subheader("📥 Exportação de Documentos")

# Alerta se acabou de processar
if st.session_state.get("edital_processado_agora"):
    st.success("🎉 Documento processado com sucesso! Botões de download disponíveis abaixo.")
    # Limpar flag para próxima vez
    if st.button("🔄 Atualizar formulário com dados processados"):
        st.session_state.pop("edital_processado_agora", None)
        st.rerun()

# Verificar se existe edital processado com DOCX gerado
docx_disponivel = False
docx_bytes = None
docx_nome = "Edital_Minuta.docx"

# DEBUG: Mostrar estado do session_state (remover depois)
with st.expander("🔍 Debug - Estado da Sessão", expanded=False):
    st.write("**Buffer disponível:**", "edital_docx_buffer" in st.session_state)
    st.write("**Nome disponível:**", "edital_docx_nome" in st.session_state)
    if os.path.exists(EDITAL_JSON_PATH):
        try:
            with open(EDITAL_JSON_PATH, "r", encoding="utf-8") as f:
                dados = json.load(f)
            st.write("**docx_path no JSON:**", dados.get("docx_path"))
            st.write("**docx_buffer_disponivel no JSON:**", dados.get("docx_buffer_disponivel"))
        except Exception as e:
            st.write("**Erro ao ler JSON:**", str(e))

# 1. Tentar carregar DOCX do buffer (Streamlit Cloud) - PRIORIDADE
if "edital_docx_buffer" in st.session_state:
    try:
        buffer = st.session_state.get("edital_docx_buffer")
        docx_nome = st.session_state.get("edital_docx_nome", docx_nome)
        if buffer and hasattr(buffer, 'getvalue'):
            docx_bytes = buffer.getvalue()
            if docx_bytes and len(docx_bytes) > 0:
                docx_disponivel = True
                st.info(f"✅ Buffer carregado: {len(docx_bytes)} bytes")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar buffer: {e}")

# 2. Fallback: tentar carregar do arquivo (Codespaces)
if not docx_disponivel and os.path.exists(EDITAL_JSON_PATH):
    try:
        with open(EDITAL_JSON_PATH, "r", encoding="utf-8") as f:
            dados_edital = json.load(f)
            
        docx_path = dados_edital.get("docx_path")
        
        if docx_path and os.path.exists(docx_path):
            with open(docx_path, "rb") as f:
                docx_bytes = f.read()
            docx_disponivel = True
            docx_nome = os.path.basename(docx_path)
    except Exception as e:
        pass

# Exibir botões de download se DOCX disponível
if docx_disponivel and docx_bytes:
    st.download_button(
        label="📤 Baixar Edital Oficial (DOCX)",
        data=docx_bytes,
        file_name=docx_nome,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary"
    )
    
    st.success(f"✅ Documento disponível para download ({docx_nome})")
    
    # Botão de download do JSON (se existir)
    if os.path.exists(EDITAL_JSON_PATH):
        try:
            with open(EDITAL_JSON_PATH, "r", encoding="utf-8") as f:
                dados_edital = json.load(f)
            
            json_bytes = json.dumps(dados_edital, ensure_ascii=False, indent=2).encode('utf-8')
            st.download_button(
                label="📊 Baixar Dados Estruturados (JSON)",
                data=json_bytes,
                file_name=f"Edital_Dados_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        except Exception:
            pass
else:
    st.info("💡 Processe o Edital com IA para gerar o documento DOCX para download.")
