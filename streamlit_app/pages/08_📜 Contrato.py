import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# pages/08_📜 Contrato.py – SynapseNext / SAAB TJSP v2025.1
# ==========================================================
# Módulo final da jornada de contratação pública.
# Gera o Contrato Administrativo a partir de insumos cumulativos
# (DFD, ETP, TR, Edital) e ContratoAgent especializado.
# ==========================================================

import os
from io import BytesIO
from datetime import datetime
import streamlit as st

from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from home_utils.sidebar_organizer import apply_sidebar_grouping
from utils.integration_contrato import (
    processar_insumo_contrato,
    gerar_contrato_com_ia,
    gerar_contrato_docx,
    export_contrato_to_json,
    load_contrato_from_json,
    integrar_com_contexto,
)
from home_utils.refinamento_ia import render_refinamento_iterativo

# ==========================================================
# ⚙️ Configuração básica
# ==========================================================
st.set_page_config(page_title="📜 Contrato", layout="wide", page_icon="📜")
apply_sidebar_grouping()

# Estilo institucional PJe-inspired
st.markdown("""
<style>
/* ============================================
   PADRÃO VISUAL PJe-INSPIRED - SYNAPSE NEXT
   Versão: 2025.1-homolog
   ============================================ */

/* Título principal - tamanho reduzido para sobriedade */
h1 {
    font-size: 1.8rem !important;
    font-weight: 500 !important;
    color: #2c3e50 !important;
    margin-bottom: 0.3rem !important;
}

/* Caption institucional */
.caption {
    color: #6c757d;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* Bloco de IA - destaque sutil */
.ia-block {
    border: 1px solid #d0d7de;
    border-radius: 3px;
    padding: 1rem 1.2rem;
    background-color: #f0f2f5;
    margin: 1rem 0 1.2rem 0;
}
.ia-block h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 0.6rem 0;
    letter-spacing: -0.01em;
}

/* Seções com fundo cinza - contraste melhorado */
h3 {
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
    background-color: #e5e7eb !important;
    padding: 0.6rem 0.8rem !important;
    border-radius: 3px !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
}

/* Botões - destaque apenas para ações principais */
div.stButton > button {
    border-radius: 3px;
    font-weight: 500;
    border: 1px solid #d0d7de;
}
div.stButton > button[kind="primary"] {
    background-color: #0969da !important;
    border-color: #0969da !important;
}

/* Formulário clean */
.stTextInput label, .stTextArea label {
    font-weight: 500;
    color: #1f2937;
    font-size: 0.9rem;
}

/* Expander refinamento com destaque discreto */
details {
    border: 1px solid #d0d7de;
    border-radius: 3px;
    padding: 0.5rem;
    background-color: #ffffff;
}
summary {
    font-weight: 500;
    color: #0969da;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 📝 Definição dos campos do Contrato para refinamento iterativo
# ==========================================================
CAMPOS_CONTRATO = [
    "numero_contrato",
    "data_assinatura",
    "objeto",
    "partes_contratante",
    "partes_contratada",
    "fundamentacao_legal",
    "vigencia",
    "prazo_execucao",
    "valor_global",
    "forma_pagamento",
    "reajuste",
    "garantia_contratual",
    "obrigacoes_contratada",
    "obrigacoes_contratante",
    "fiscalizacao",
    "penalidades",
    "rescisao",
    "alteracoes",
    "foro",
    "disposicoes_gerais"
]

# ==========================================================
# 📥 Carregamento de dados persistidos (JSON)
# ==========================================================
dados_contrato_anterior = load_contrato_from_json()
if dados_contrato_anterior and "CONTRATO" in dados_contrato_anterior:
    st.session_state["contrato_campos_ai"] = dados_contrato_anterior["CONTRATO"]

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
st.markdown("<h1>Contrato Administrativo</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Consolidação final da jornada de contratação pública: DFD → ETP → TR → Edital → CONTRATO</p>", unsafe_allow_html=True)
st.divider()

# ==========================================================
# 🔗 Detecção automática de contexto
# ==========================================================
contexto_disponivel = {
    "DFD": "dfd_campos_ai" in st.session_state,
    "ETP": "etp_campos_ai" in st.session_state,
    "TR": "tr_campos_ai" in st.session_state,
    "Edital": "edital_campos_ai" in st.session_state,
}

modulos_disponiveis = sum(contexto_disponivel.values())

if modulos_disponiveis > 0:
    st.success(f"📎 **Contexto detectado**: {modulos_disponiveis}/4 módulos anteriores disponíveis")
    
    cols = st.columns(4)
    for idx, (modulo, status) in enumerate(contexto_disponivel.items()):
        with cols[idx]:
            if status:
                st.metric(modulo, "✅ OK")
            else:
                st.metric(modulo, "❌ Vazio")
    
    st.info("💡 O ContratoAgent utilizará automaticamente os dados dos módulos anteriores para enriquecer o contrato.")
else:
    st.info("ℹ️ Nenhum contexto detectado. Você pode processar um insumo ou preencher manualmente.")

st.divider()

# Upload de insumo (opcional)
arquivo_upload = None
with st.expander("📤 Upload de Insumo (opcional)", expanded=False):
    st.markdown("""
    **Opção 1**: Upload direto de arquivo (PDF/DOCX/TXT) de contrato ou minuta  
    **Opção 2**: Processar apenas com contexto (se DFD/ETP/TR/Edital disponíveis)  
    **Opção 3**: Preencher manualmente os campos abaixo
    """)
    
    arquivo_upload = st.file_uploader(
        "Envie um arquivo de referência:",
        type=["pdf", "docx", "txt"],
        help="O ContratoAgent processará este arquivo e integrará com o contexto disponível"
    )

# 🤖 Assistente IA (Bloco institucional PJe-inspired)
st.markdown("### 🤖 Assistente IA")
st.caption("Processamento automático: upload de arquivo ou geração a partir do contexto acumulado (DFD/ETP/TR/Edital)")

col_ia1, col_ia2, col_ia3 = st.columns(3)

with col_ia1:
    processar_arquivo = arquivo_upload is not None
    if st.button("⚡ Processar com IA", use_container_width=True, type="primary", disabled=not processar_arquivo and modulos_disponiveis == 0, key="btn_ia_processar"):
        if arquivo_upload is not None:
            with st.spinner("⏳ Processando com ContratoAgent especializado..."):
                try:
                    # Integrar contexto
                    contexto = integrar_com_contexto(st.session_state)
                    
                    # Processar com ContratoAgent
                    resultado = processar_insumo_contrato(arquivo_upload, contexto_previo=contexto)
                    
                    if "erro" in resultado:
                        st.error(f"❌ {resultado['erro']}")
                    elif resultado.get("status") == "processado":
                        # Salvar JSON
                        export_contrato_to_json(resultado)
                        
                        # Atualizar session_state
                        st.session_state["contrato_campos_ai"] = resultado["CONTRATO"]
                        
                        st.success(f"✅ Contrato processado com sucesso! {len(resultado['CONTRATO'])} campos extraídos.")
                        st.info(f"📄 Arquivo: {resultado.get('nome_arquivo', 'N/A')}")
                        
                        # Recarregar para mostrar dados
                        st.rerun()
                    else:
                        st.warning("⚠️ Status inesperado. Verifique os logs.")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao processar: {e}")
                    import traceback
                    st.code(traceback.format_exc())

        else:
            # Processar apenas com contexto
            with st.spinner("⏳ Gerando contrato a partir de DFD/ETP/TR/Edital..."):
                try:
                    # Integrar contexto
                    contexto = integrar_com_contexto(st.session_state)
                    
                    # Gerar com ContratoAgent
                    resultado = gerar_contrato_com_ia(contexto)
                    
                    if "erro" in resultado:
                        st.error(f"❌ {resultado['erro']}")
                    elif resultado.get("status") == "processado":
                        # Salvar
                        export_contrato_to_json(resultado)
                        
                        # Atualizar session_state
                        st.session_state["contrato_campos_ai"] = resultado["CONTRATO"]
                        
                        st.success(f"✅ Contrato gerado! {len(resultado['CONTRATO'])} campos criados a partir do contexto.")
                        
                        # Recarregar
                        st.rerun()
                    else:
                        st.warning("⚠️ Status inesperado.")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao gerar: {e}")
                    import traceback
                    st.code(traceback.format_exc())

with col_ia2:
    st.info("📋 **Campos**: 20 campos contratuais estruturados")

with col_ia3:
    if modulos_disponiveis > 0:
        st.success(f"✅ **Contexto**: {modulos_disponiveis}/4 módulos")
    else:
        st.warning("⚠️ **Contexto**: Nenhum módulo detectado")

st.divider()

# Refinamento iterativo
campos_ai = st.session_state.get("contrato_campos_ai", {})
campos_simples = ["numero_contrato", "data_assinatura", "vigencia", "prazo_execucao", 
                  "valor_global", "foro"]

campos_ai = render_refinamento_iterativo(
    secoes_disponiveis=CAMPOS_CONTRATO,
    dados_atuais=campos_ai if campos_ai else {},
    artefato="CONTRATO",
    campos_simples=campos_simples
)

st.session_state["contrato_campos_ai"] = campos_ai

st.divider()

# ==========================================================
# 🧾 Formulário – Campos contratuais (20 campos)
# ==========================================================
st.markdown("### Dados do Contrato Administrativo")

# Carregar dados processados
campos_ai = st.session_state.get("contrato_campos_ai", {})

# Identificação (3 colunas)
st.markdown("#### Identificação")
col_id1, col_id2, col_id3 = st.columns(3)
with col_id1:
    numero_contrato = st.text_input("Número do Contrato", value=campos_ai.get("numero_contrato", ""))
with col_id2:
    data_assinatura = st.text_input("Data de Assinatura", value=campos_ai.get("data_assinatura", ""))
with col_id3:
    foro = st.text_input("Foro Competente", value=campos_ai.get("foro", ""))

# Partes (2 colunas)
st.markdown("#### Partes Contratantes")
col_partes1, col_partes2 = st.columns(2)
with col_partes1:
    partes_contratante = st.text_area("Contratante", value=campos_ai.get("partes_contratante", ""), height=80)
with col_partes2:
    partes_contratada = st.text_area("Contratada", value=campos_ai.get("partes_contratada", ""), height=80)

# Objeto e Fundamentação (coluna única)
st.markdown("#### Objeto e Fundamentação")
objeto = st.text_area("Objeto do Contrato", value=campos_ai.get("objeto", ""), height=120)
fundamentacao_legal = st.text_area("Fundamentação Legal", value=campos_ai.get("fundamentacao_legal", ""), height=100)

# Valores e Prazos (3 colunas)
st.markdown("#### Valores e Prazos")
col_val1, col_val2, col_val3 = st.columns(3)

with col_val1:
    vigencia = st.text_input("Vigência", value=campos_ai.get("vigencia", ""))
with col_val2:
    prazo_execucao = st.text_input("Prazo de Execução", value=campos_ai.get("prazo_execucao", ""))
with col_val3:
    valor_global = st.text_input("Valor Global", value=campos_ai.get("valor_global", ""))

forma_pagamento = st.text_area("Forma de Pagamento", value=campos_ai.get("forma_pagamento", ""), height=80)
reajuste = st.text_area("Reajuste", value=campos_ai.get("reajuste", ""), height=70)
garantia_contratual = st.text_area("Garantia Contratual", value=campos_ai.get("garantia_contratual", ""), height=70)

# Obrigações (coluna única)
st.markdown("#### Obrigações das Partes")
obrigacoes_contratada = st.text_area("Obrigações da Contratada", value=campos_ai.get("obrigacoes_contratada", ""), height=120)
obrigacoes_contratante = st.text_area("Obrigações da Contratante", value=campos_ai.get("obrigacoes_contratante", ""), height=120)
fiscalizacao = st.text_area("Fiscalização", value=campos_ai.get("fiscalizacao", ""), height=100)

# Penalidades e Disposições (coluna única)
st.markdown("#### Penalidades e Disposições Finais")
penalidades = st.text_area("Penalidades", value=campos_ai.get("penalidades", ""), height=100)
rescisao = st.text_area("Rescisão", value=campos_ai.get("rescisao", ""), height=80)
alteracoes = st.text_area("Alterações Contratuais", value=campos_ai.get("alteracoes", ""), height=70)
disposicoes_gerais = st.text_area("Disposições Gerais", value=campos_ai.get("disposicoes_gerais", ""), height=70)

st.divider()

# Botões de ação
col_salvar, col_baixar = st.columns(2)

with col_salvar:
    if st.button("Salvar Contrato", type="secondary", use_container_width=True):
        campos_manuais = {
            "numero_contrato": numero_contrato,
            "data_assinatura": data_assinatura,
            "objeto": objeto,
            "partes_contratante": partes_contratante,
            "partes_contratada": partes_contratada,
            "fundamentacao_legal": fundamentacao_legal,
            "vigencia": vigencia,
            "prazo_execucao": prazo_execucao,
            "valor_global": valor_global,
            "forma_pagamento": forma_pagamento,
            "reajuste": reajuste,
            "garantia_contratual": garantia_contratual,
            "obrigacoes_contratada": obrigacoes_contratada,
            "obrigacoes_contratante": obrigacoes_contratante,
            "fiscalizacao": fiscalizacao,
            "penalidades": penalidades,
            "rescisao": rescisao,
            "alteracoes": alteracoes,
            "foro": foro,
            "disposicoes_gerais": disposicoes_gerais,
        }
        
        resultado_manual = {
            "artefato": "CONTRATO",
            "nome_arquivo": "edicao_manual",
            "status": "editado_manualmente",
            "timestamp": datetime.now().isoformat(),
            "CONTRATO": campos_manuais
        }
        
        export_contrato_to_json(resultado_manual)
        st.session_state["contrato_campos_ai"] = campos_manuais
        st.success("✅ Campos salvos com sucesso!")

with col_baixar:
    if st.button("Baixar Contrato (DOCX)", use_container_width=True):
        campos_atuais = {
            "numero_contrato": numero_contrato,
            "data_assinatura": data_assinatura,
            "objeto": objeto,
            "partes_contratante": partes_contratante,
            "partes_contratada": partes_contratada,
            "fundamentacao_legal": fundamentacao_legal,
            "vigencia": vigencia,
            "prazo_execucao": prazo_execucao,
            "valor_global": valor_global,
            "forma_pagamento": forma_pagamento,
            "reajuste": reajuste,
            "garantia_contratual": garantia_contratual,
            "obrigacoes_contratada": obrigacoes_contratada,
            "obrigacoes_contratante": obrigacoes_contratante,
            "fiscalizacao": fiscalizacao,
            "penalidades": penalidades,
            "rescisao": rescisao,
            "alteracoes": alteracoes,
            "foro": foro,
            "disposicoes_gerais": disposicoes_gerais,
        }
        
        with st.spinner("⏳ Gerando documento DOCX profissional..."):
            try:
                # Gerar DOCX usando função profissional
                caminho = gerar_contrato_docx(campos_atuais, session_state=st.session_state)
                
                # Verificar se buffer foi criado
                if "contrato_docx_buffer" in st.session_state:
                    buffer = st.session_state["contrato_docx_buffer"]
                    nome_arquivo = st.session_state.get("contrato_docx_nome", "Contrato_TJSP.docx")
                    
                    st.download_button(
                        label="📥 Baixar Contrato em DOCX",
                        data=buffer,
                        file_name=nome_arquivo,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )
                    
                    st.success("✅ Documento DOCX gerado com sucesso!")
                    st.info(f"📄 Arquivo: {nome_arquivo}")
                    
                    if caminho:
                        st.caption(f"💾 Salvo também em: `{caminho}`")
                else:
                    st.error("❌ Erro ao gerar buffer do documento.")
                    
            except Exception as e:
                st.error(f"❌ Erro ao gerar DOCX: {e}")
                import traceback
                st.code(traceback.format_exc())

st.divider()

# Dica institucional
st.caption("💡 **Dica**: Use o Assistente IA para preencher automaticamente os campos a partir do contexto disponível (DFD/ETP/TR/Edital)")

# ==========================================================
# 📊 Informações de diagnóstico
# ==========================================================
with st.expander("🔍 Informações de Diagnóstico"):
    st.json({
        "modulos_anteriores_disponiveis": contexto_disponivel,
        "campos_processados": len(campos_ai),
        "timestamp_ultima_atualizacao": dados_contrato_anterior.get("timestamp", "N/A") if dados_contrato_anterior else "N/A",
        "buffer_docx_disponivel": "contrato_docx_buffer" in st.session_state,
    })
