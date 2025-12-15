import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# pages/03_📘 ETP – Estudo Técnico Preliminar.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

import os
import json
from io import BytesIO
from docx import Document
import streamlit as st

# ==========================================================
# 📦 Imports institucionais
# ==========================================================
from utils.integration_etp import obter_etp_da_sessao, status_etp, salvar_etp_em_json, gerar_etp_com_ia
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from home_utils.sidebar_organizer import apply_sidebar_grouping
from home_utils.refinamento_ia import render_refinamento_iterativo

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(page_title="ETP – Estudo Técnico Preliminar", layout="wide")
apply_sidebar_grouping()

# Estilo institucional PJe-inspired
st.markdown("""
<style>
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
/* Tabs institucionais */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #e5e7eb;
    border-radius: 3px;
    padding: 0.5rem 1rem;
    font-weight: 500;
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

st.markdown("<h1>Estudo Técnico Preliminar (ETP)</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Pré-preenchimento automático a partir de insumos ou preenchimento manual</p>", unsafe_allow_html=True)
st.info(status_etp())

defaults = obter_etp_da_sessao()

if defaults:
    st.success("Campos carregados do módulo anterior")
else:
    st.info("Preencha manualmente ou envie documento no módulo Insumos")

# ==========================================================
# ASSISTENTE IA – Ferramentas de automação
# ==========================================================
st.markdown('<div class="ia-block">', unsafe_allow_html=True)
st.markdown("### Assistente IA")
st.caption("Processamento automático: requer insumos do módulo anterior")

col_ia1, col_ia2, col_ia3 = st.columns(3)

with col_ia1:
    if st.button("⚡ Processar com IA", use_container_width=True, type="primary", key="btn_ia_processar"):
        try:
            with st.spinner("Processando documento..."):
                resultado = gerar_etp_com_ia()
            
            if resultado:
                st.success("ETP estruturado com sucesso")
                
                # Exibir resumo
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    st.metric("Unidade", (resultado.get("unidade_demandante", "N/A")[:25] + "...") if len(resultado.get("unidade_demandante", "")) > 25 else resultado.get("unidade_demandante", "N/A"))
                with col_b:
                    st.metric("Responsável", (resultado.get("responsavel", "N/A")[:25] + "...") if len(resultado.get("responsavel", "")) > 25 else resultado.get("responsavel", "N/A"))
                with col_c:
                    st.metric("Prazo", resultado.get("prazo_estimado", "N/A")[:20])
                with col_d:
                    st.metric("Valor", f"R$ {resultado.get('valor_estimado', '0,00')}")
                
                secoes = resultado.get("secoes", {})
                secoes_preenchidas = sum(1 for v in secoes.values() if v and v.strip())
                st.info(f"Seções preenchidas: {secoes_preenchidas}/27")
                
                st.rerun()
            else:
                st.warning("Nenhum insumo encontrado")
                
        except Exception as e:
            st.error(f"Erro ao processar: {e}")

with col_ia2:
    if st.button("📤 Enviar para TR", use_container_width=True, disabled=not defaults, key="btn_enviar_tr"):
        try:
            from datetime import datetime
            
            base = os.path.join("exports", "insumos", "json")
            os.makedirs(base, exist_ok=True)
            
            payload = {
                "artefato": "TR",
                "origem": "ETP_estruturado",
                "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "ok",
                "campos_ai": defaults,
                "conteudo_textual": "",  # TR não precisa de texto narrativo
            }
            
            arq_ultimo = os.path.join(base, "TR_ultimo.json")
            with open(arq_ultimo, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            
            st.success("Dados enviados para o módulo TR")
            st.info("Acesse o módulo TR para continuar")
            
        except Exception as e:
            st.error(f"Erro: {e}")

with col_ia3:
    st.write("")  # Espaçamento

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# REFINAMENTO ITERATIVO
# ==========================================================
# Definir seções do ETP
SECOES_ETP = [
    "objeto", "descricao_necessidade", "previsao_pca", "planejamento_estrategico",
    "catalogo_padronizacao", "requisitos_contratacao", "condicoes_recebimento",
    "condicoes_execucao_pagamento", "garantias", "modalidade_licitacao",
    "estimativa_quantidades", "levantamento_mercado", "estimativa_valor",
    "descricao_solucao", "justificativa_parcelamento", "resultados_pretendidos",
    "providencias_previas", "contratacoes_correlatas", "impactos_ambientais",
    "possibilidade_compra_locacao", "participacao_consorcio", "vistoria_visita_tecnica",
    "cumprimento_resolucoes_cnj", "plano_riscos", "equipe_planejamento",
    "estimativa_prazo_vigencia", "avaliacao_conclusiva"
]

# Verificar se houve atualização via refinamento
defaults = render_refinamento_iterativo(
    secoes_disponiveis=SECOES_ETP,
    dados_atuais=defaults if defaults else {},
    artefato="ETP",
    campos_simples=["unidade_demandante", "responsavel", "prazo_estimado", "valor_estimado"]
)

st.divider()

# Extrair seções do defaults
secoes = defaults.get("secoes", {}) if isinstance(defaults.get("secoes"), dict) else {}

# Dados administrativos
st.markdown("### Dados Administrativos")
col1, col2 = st.columns(2)
with col1:
    unidade = st.text_input("Unidade Demandante", value=defaults.get("unidade_demandante", ""))
    prazo = st.text_input("Prazo Estimado", value=defaults.get("prazo_estimado", ""))
with col2:
    responsavel = st.text_input("Responsável", value=defaults.get("responsavel", ""))
    valor = st.text_input("Valor Estimado (R$)", value=defaults.get("valor_estimado", "0,00"))

st.divider()

# 27 Seções estruturadas em tabs
st.markdown("### Seções do ETP (Lei 14.133/2021)")

# Criar 5 grupos de tabs para organizar melhor
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Seções 1-6", 
    "Seções 7-12", 
    "Seções 13-18", 
    "Seções 19-24", 
    "Seções 25-27"
])

with tab1:
    st.text_area("1. Objeto", value=secoes.get("objeto", ""), height=120, key="s1")
    st.text_area("2. Descrição da Necessidade", value=secoes.get("descricao_necessidade", ""), height=150, key="s2")
    st.text_area("3. Previsão no PCA", value=secoes.get("previsao_pca", ""), height=100, key="s3")
    st.text_area("4. Planejamento Estratégico", value=secoes.get("planejamento_estrategico", ""), height=120, key="s4")
    st.text_area("5. Catálogo de Padronização", value=secoes.get("catalogo_padronizacao", ""), height=100, key="s5")
    st.text_area("6. Requisitos da Contratação", value=secoes.get("requisitos_contratacao", ""), height=150, key="s6")

with tab2:
    st.text_area("7. Condições de Recebimento", value=secoes.get("condicoes_recebimento", ""), height=120, key="s7")
    st.text_area("8. Condições de Execução e Pagamento", value=secoes.get("condicoes_execucao_pagamento", ""), height=120, key="s8")
    st.text_area("9. Garantias", value=secoes.get("garantias", ""), height=100, key="s9")
    st.text_area("10. Modalidade de Licitação", value=secoes.get("modalidade_licitacao", ""), height=120, key="s10")
    st.text_area("11. Estimativa de Quantidades", value=secoes.get("estimativa_quantidades", ""), height=100, key="s11")
    st.text_area("12. Levantamento de Mercado", value=secoes.get("levantamento_mercado", ""), height=150, key="s12")

with tab3:
    st.text_area("13. Estimativa de Valor", value=secoes.get("estimativa_valor", ""), height=120, key="s13")
    st.text_area("14. Descrição da Solução", value=secoes.get("descricao_solucao", ""), height=150, key="s14")
    st.text_area("15. Justificativa de Parcelamento", value=secoes.get("justificativa_parcelamento", ""), height=150, key="s15")
    st.text_area("16. Resultados Pretendidos", value=secoes.get("resultados_pretendidos", ""), height=120, key="s16")
    st.text_area("17. Providências Prévias", value=secoes.get("providencias_previas", ""), height=100, key="s17")
    st.text_area("18. Contratações Correlatas", value=secoes.get("contratacoes_correlatas", ""), height=100, key="s18")

with tab4:
    st.text_area("19. Impactos Ambientais", value=secoes.get("impactos_ambientais", ""), height=120, key="s19")
    st.text_area("20. Possibilidade de Compra/Locação", value=secoes.get("possibilidade_compra_locacao", ""), height=100, key="s20")
    st.text_area("21. Participação em Consórcio", value=secoes.get("participacao_consorcio", ""), height=150, key="s21")
    st.text_area("22. Vistoria/Visita Técnica", value=secoes.get("vistoria_visita_tecnica", ""), height=120, key="s22")
    st.text_area("23. Cumprimento de Resoluções CNJ", value=secoes.get("cumprimento_resolucoes_cnj", ""), height=100, key="s23")
    st.text_area("24. Plano de Riscos", value=secoes.get("plano_riscos", ""), height=100, key="s24")

with tab5:
    st.text_area("25. Equipe de Planejamento", value=secoes.get("equipe_planejamento", ""), height=150, key="s25")
    st.text_area("26. Estimativa de Prazo de Vigência", value=secoes.get("estimativa_prazo_vigencia", ""), height=120, key="s26")
    st.text_area("27. Avaliação Conclusiva", value=secoes.get("avaliacao_conclusiva", ""), height=120, key="s27")

st.divider()

# Botão de salvar manual
if st.button("Salvar ETP", type="secondary", use_container_width=True):
    etp_completo = {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "valor_estimado": valor,
        "secoes": {
            "objeto": st.session_state.get("s1", ""),
            "descricao_necessidade": st.session_state.get("s2", ""),
            "previsao_pca": st.session_state.get("s3", ""),
            "planejamento_estrategico": st.session_state.get("s4", ""),
            "catalogo_padronizacao": st.session_state.get("s5", ""),
            "requisitos_contratacao": st.session_state.get("s6", ""),
            "condicoes_recebimento": st.session_state.get("s7", ""),
            "condicoes_execucao_pagamento": st.session_state.get("s8", ""),
            "garantias": st.session_state.get("s9", ""),
            "modalidade_licitacao": st.session_state.get("s10", ""),
            "estimativa_quantidades": st.session_state.get("s11", ""),
            "levantamento_mercado": st.session_state.get("s12", ""),
            "estimativa_valor": st.session_state.get("s13", ""),
            "descricao_solucao": st.session_state.get("s14", ""),
            "justificativa_parcelamento": st.session_state.get("s15", ""),
            "resultados_pretendidos": st.session_state.get("s16", ""),
            "providencias_previas": st.session_state.get("s17", ""),
            "contratacoes_correlatas": st.session_state.get("s18", ""),
            "impactos_ambientais": st.session_state.get("s19", ""),
            "possibilidade_compra_locacao": st.session_state.get("s20", ""),
            "participacao_consorcio": st.session_state.get("s21", ""),
            "vistoria_visita_tecnica": st.session_state.get("s22", ""),
            "cumprimento_resolucoes_cnj": st.session_state.get("s23", ""),
            "plano_riscos": st.session_state.get("s24", ""),
            "equipe_planejamento": st.session_state.get("s25", ""),
            "estimativa_prazo_vigencia": st.session_state.get("s26", ""),
            "avaliacao_conclusiva": st.session_state.get("s27", "")
        }
    }
    salvar_etp_em_json(etp_completo, origem="formulario_manual")
    st.success("ETP salvo com sucesso")

st.caption("Dica: Use o Assistente IA para preencher automaticamente as 27 seções a partir dos insumos carregados")
