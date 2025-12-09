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
from utils.integration_contrato import (
    processar_insumo_contrato,
    gerar_contrato_com_ia,
    gerar_contrato_docx,
    export_contrato_to_json,
    load_contrato_from_json,
    integrar_com_contexto,
)

# ==========================================================
# ⚙️ Configuração básica
# ==========================================================
st.set_page_config(page_title="📜 Contrato", layout="wide", page_icon="📜")
aplicar_estilo_global()

# ==========================================================
# 📥 Carregamento de dados persistidos (JSON)
# ==========================================================
dados_contrato_anterior = load_contrato_from_json()
if dados_contrato_anterior and "CONTRATO" in dados_contrato_anterior:
    st.session_state["contrato_campos_ai"] = dados_contrato_anterior["CONTRATO"]

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "📜 Contrato Administrativo TJSP",
    "Consolidação final da jornada de contratação pública: DFD → ETP → TR → Edital → CONTRATO"
)
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

# ==========================================================
# 📤 Upload de insumo (opcional)
# ==========================================================
st.subheader("📤 Upload de Insumo (opcional)")
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

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if arquivo_upload is not None:
        if st.button("🤖 Processar Insumo com ContratoAgent", type="primary"):
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

with col_btn2:
    if modulos_disponiveis > 0:
        if st.button("🧠 Gerar Contrato APENAS do Contexto", type="secondary"):
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

st.divider()

# ==========================================================
# 🧾 Formulário – Campos contratuais (20 campos)
# ==========================================================
st.subheader("📄 Dados do Contrato Administrativo")

# Carregar dados processados
campos_ai = st.session_state.get("contrato_campos_ai", {})

# Dividir em 3 colunas para melhor organização
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### 📋 Identificação")
    numero_contrato = st.text_input("Número do Contrato", value=campos_ai.get("numero_contrato", ""))
    data_assinatura = st.text_input("Data de Assinatura", value=campos_ai.get("data_assinatura", ""))
    
    st.markdown("##### 💰 Valores e Prazos")
    vigencia = st.text_input("Vigência", value=campos_ai.get("vigencia", ""))
    prazo_execucao = st.text_input("Prazo de Execução", value=campos_ai.get("prazo_execucao", ""))
    valor_global = st.text_input("Valor Global", value=campos_ai.get("valor_global", ""))
    forma_pagamento = st.text_area("Forma de Pagamento", value=campos_ai.get("forma_pagamento", ""), height=80)
    reajuste = st.text_area("Reajuste", value=campos_ai.get("reajuste", ""), height=70)
    garantia_contratual = st.text_area("Garantia Contratual", value=campos_ai.get("garantia_contratual", ""), height=70)

with col2:
    st.markdown("##### 👥 Partes e Fundamentação")
    partes_contratante = st.text_area("Partes Contratante", value=campos_ai.get("partes_contratante", ""), height=80)
    partes_contratada = st.text_area("Partes Contratada", value=campos_ai.get("partes_contratada", ""), height=80)
    fundamentacao_legal = st.text_area("Fundamentação Legal", value=campos_ai.get("fundamentacao_legal", ""), height=100)
    
    st.markdown("##### 📝 Objeto")
    objeto = st.text_area("Objeto do Contrato", value=campos_ai.get("objeto", ""), height=150)

with col3:
    st.markdown("##### ⚖️ Obrigações e Fiscalização")
    obrigacoes_contratada = st.text_area("Obrigações da Contratada", value=campos_ai.get("obrigacoes_contratada", ""), height=120)
    obrigacoes_contratante = st.text_area("Obrigações da Contratante", value=campos_ai.get("obrigacoes_contratante", ""), height=120)
    fiscalizacao = st.text_area("Fiscalização", value=campos_ai.get("fiscalizacao", ""), height=100)
    
    st.markdown("##### 🚨 Penalidades e Rescisão")
    penalidades = st.text_area("Penalidades", value=campos_ai.get("penalidades", ""), height=100)
    rescisao = st.text_area("Rescisão", value=campos_ai.get("rescisao", ""), height=80)

# Campos adicionais em linha cheia
st.markdown("##### 📌 Disposições Finais")
col_disp1, col_disp2 = st.columns(2)
with col_disp1:
    alteracoes = st.text_area("Alterações Contratuais", value=campos_ai.get("alteracoes", ""), height=70)
    foro = st.text_input("Foro Competente", value=campos_ai.get("foro", ""))

with col_disp2:
    disposicoes_gerais = st.text_area("Disposições Gerais", value=campos_ai.get("disposicoes_gerais", ""), height=70)

# ==========================================================
# 💾 Salvar manualmente campos editados
# ==========================================================
st.divider()
if st.button("💾 Salvar Campos Editados Manualmente", type="secondary"):
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

# ==========================================================
# 📄 Geração DOCX profissional
# ==========================================================
st.divider()
st.subheader("📄 Exportação do Contrato Administrativo")

if st.button("📤 Gerar DOCX Profissional", type="primary"):
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

st.divider()
st.caption("📎 Este módulo utiliza o **ContratoAgent especializado** com enriquecimento AGRESSIVO de 20 campos baseado na Lei Federal nº 14.133/2021.")

