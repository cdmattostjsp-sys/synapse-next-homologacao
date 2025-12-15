import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# 🧩 Validador de Editais – SynapseNext v2025.1
# Secretaria de Administração e Abastecimento (SAAB/TJSP)
# ==========================================================
# Função: validar minuta do edital contra Lei 14.133/2021 e modelos TJSP
# Suporta: upload de arquivo, integração com Edital gerado, checklist institucional
# ==========================================================

import streamlit as st
import json
import os
import yaml
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from home_utils.sidebar_organizer import apply_sidebar_grouping

# Importar extração de texto (mesmo módulo usado em Insumos)
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import docx2txt
except ImportError:
    docx2txt = None

# ----------------------------------------------------------
# ⚙️ Configuração de Página
# ----------------------------------------------------------
st.set_page_config(page_title="🧩 Validador de Editais", layout="wide", page_icon="🧩")
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

/* Seções com fundo cinza - contraste melhorado */
h2, h3 {
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
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-weight: 500;
    color: #1f2937;
    font-size: 0.9rem;
}

/* Expander com destaque discreto */
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

/* Tabs institucionais */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #f0f2f5;
    border-radius: 3px 3px 0 0;
    padding: 0.5rem 1rem;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background-color: #e5e7eb;
    border-bottom: 2px solid #0969da;
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho institucional
st.markdown("<h1>🧩 Validador de Editais</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Validação de conformidade legal (Lei 14.133/2021) e checklist institucional TJSP</p>", unsafe_allow_html=True)
st.divider()

# ==========================================================
# 🔧 Funções Auxiliares
# ==========================================================

def extrair_texto_pdf(arquivo) -> str:
    """Extrai texto de PDF usando PyMuPDF."""
    if fitz is None:
        return ""
    try:
        doc = fitz.open(stream=arquivo.read(), filetype="pdf")
        texto = ""
        for page in doc:
            texto += page.get_text()
        return texto
    except Exception as e:
        st.error(f"Erro ao extrair PDF: {e}")
        return ""

def extrair_texto_docx(arquivo) -> str:
    """Extrai texto de DOCX usando docx2txt."""
    if docx2txt is None:
        return ""
    try:
        return docx2txt.process(arquivo)
    except Exception as e:
        st.error(f"Erro ao extrair DOCX: {e}")
        return ""

def extrair_texto_txt(arquivo) -> str:
    """Extrai texto de TXT."""
    try:
        return arquivo.read().decode("utf-8", errors="ignore")
    except Exception as e:
        st.error(f"Erro ao extrair TXT: {e}")
        return ""

def carregar_checklist() -> dict:
    """Carrega checklist institucional do YAML."""
    checklist_path = ROOT / "knowledge" / "edital_checklist.yml"
    if not checklist_path.exists():
        return {}
    
    try:
        with open(checklist_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Erro ao carregar checklist: {e}")
        return {}

def validar_campos_obrigatorios(texto: str) -> dict:
    """
    Valida presença de campos obrigatórios da Lei 14.133/2021.
    Retorna dicionário com campos encontrados e faltantes.
    """
    texto_lower = texto.lower()
    
    # Campos obrigatórios conforme Lei 14.133/2021
    campos_obrigatorios = {
        "objeto": ["objeto", "contratação"],
        "modalidade": ["pregão", "concorrência", "concurso", "leilão"],
        "criterio_julgamento": ["menor preço", "melhor técnica", "técnica e preço"],
        "prazo_execucao": ["prazo", "vigência", "meses"],
        "condicoes_pagamento": ["pagamento", "fatura", "nota fiscal"],
        "habilitacao": ["habilitação", "documentação", "certidões"],
        "recursos": ["recurso", "impugnação", "esclarecimento"],
        "penalidades": ["penalidade", "sanção", "multa"],
        "fundamentacao_legal": ["lei 14.133", "lei nº 14.133", "lei federal"],
    }
    
    encontrados = []
    faltantes = []
    
    for campo, termos in campos_obrigatorios.items():
        if any(termo in texto_lower for termo in termos):
            encontrados.append(campo)
        else:
            faltantes.append(campo)
    
    return {
        "encontrados": encontrados,
        "faltantes": faltantes,
        "percentual": len(encontrados) / len(campos_obrigatorios) * 100
    }

def aplicar_checklist(texto: str, tipo_contratacao: str, checklist_data: dict) -> dict:
    """
    Aplica checklist institucional baseado no tipo de contratação.
    Retorna análise de conformidade.
    """
    if not checklist_data or "checklist" not in checklist_data:
        return {"erro": "Checklist não disponível"}
    
    checklist = checklist_data["checklist"]
    texto_lower = texto.lower()
    
    # Mapeamento de tipos
    tipo_map = {
        "Serviços": "servicos",
        "Materiais": "materiais",
        "Obras": "obras",
        "TI & Software": "ti",
        "Consultorias": "consultoria"
    }
    
    tipo_key = tipo_map.get(tipo_contratacao, "servicos")
    
    # Aplicar checklist base + específico
    resultados = {
        "base": {"title": checklist["base"]["title"], "items": []},
        "especifico": {"title": checklist.get(tipo_key, {}).get("title", "N/A"), "items": []}
    }
    
    # Validar itens base
    for item in checklist["base"]["items"]:
        # Heurística simples: verificar se palavras-chave do item estão no texto
        palavras_chave = extrair_palavras_chave(item)
        encontrado = any(palavra in texto_lower for palavra in palavras_chave)
        resultados["base"]["items"].append({
            "descricao": item,
            "status": "✅" if encontrado else "⚠️",
            "encontrado": encontrado
        })
    
    # Validar itens específicos do tipo
    if tipo_key in checklist:
        for item in checklist[tipo_key]["items"]:
            palavras_chave = extrair_palavras_chave(item)
            encontrado = any(palavra in texto_lower for palavra in palavras_chave)
            resultados["especifico"]["items"].append({
                "descricao": item,
                "status": "✅" if encontrado else "⚠️",
                "encontrado": encontrado
            })
    
    # Calcular score geral
    total_itens = len(resultados["base"]["items"]) + len(resultados["especifico"]["items"])
    itens_ok = sum(1 for item in resultados["base"]["items"] if item["encontrado"])
    itens_ok += sum(1 for item in resultados["especifico"]["items"] if item["encontrado"])
    
    resultados["score"] = {
        "total": total_itens,
        "aprovados": itens_ok,
        "percentual": (itens_ok / total_itens * 100) if total_itens > 0 else 0
    }
    
    return resultados

def extrair_palavras_chave(texto: str) -> list:
    """Extrai palavras-chave relevantes de um item do checklist."""
    # Remove pontuação e palavras comuns
    stop_words = {"o", "a", "e", "de", "do", "da", "com", "para", "por", "está", "estão", "há"}
    palavras = texto.lower().split()
    return [p.strip(".,;:\"'()[]") for p in palavras if len(p) > 3 and p not in stop_words]

def gerar_relatorio_pdf(resultado_validacao: dict, resultado_checklist: dict, tipo: str) -> str:
    """Gera relatório PDF profissional da validação."""
    os.makedirs("exports/relatorios", exist_ok=True)
    arquivo = f"exports/relatorios/validacao_edital_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    doc = SimpleDocTemplate(arquivo, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=30,
        alignment=1  # Center
    )
    story.append(Paragraph("RELATÓRIO DE VALIDAÇÃO DE EDITAL", title_style))
    story.append(Paragraph("Tribunal de Justiça do Estado de São Paulo", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Metadados
    story.append(Paragraph(f"<b>Data:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"<b>Tipo de Contratação:</b> {tipo}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Seção 1: Campos Obrigatórios
    story.append(Paragraph("<b>1. CAMPOS OBRIGATÓRIOS (Lei 14.133/2021)</b>", styles['Heading2']))
    story.append(Paragraph(f"Conformidade: {resultado_validacao['percentual']:.1f}%", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    if resultado_validacao['faltantes']:
        story.append(Paragraph("<b>Campos ausentes:</b>", styles['Normal']))
        for campo in resultado_validacao['faltantes']:
            story.append(Paragraph(f"  ⚠️ {campo.replace('_', ' ').title()}", styles['Normal']))
    else:
        story.append(Paragraph("✅ Todos os campos obrigatórios presentes", styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Seção 2: Checklist Institucional
    story.append(Paragraph("<b>2. CHECKLIST INSTITUCIONAL TJSP</b>", styles['Heading2']))
    story.append(Paragraph(f"Score: {resultado_checklist['score']['aprovados']}/{resultado_checklist['score']['total']} ({resultado_checklist['score']['percentual']:.1f}%)", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Itens base
    story.append(Paragraph(f"<b>{resultado_checklist['base']['title']}</b>", styles['Heading3']))
    for item in resultado_checklist['base']['items']:
        story.append(Paragraph(f"{item['status']} {item['descricao']}", styles['Normal']))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Itens específicos
    if resultado_checklist['especifico']['items']:
        story.append(Paragraph(f"<b>{resultado_checklist['especifico']['title']}</b>", styles['Heading3']))
        for item in resultado_checklist['especifico']['items']:
            story.append(Paragraph(f"{item['status']} {item['descricao']}", styles['Normal']))
    
    doc.build(story)
    return arquivo

# ==========================================================
# 🧠 Interface Principal
# ==========================================================

# Inicializar estado
if "validacao_texto" not in st.session_state:
    st.session_state["validacao_texto"] = ""
if "validacao_origem" not in st.session_state:
    st.session_state["validacao_origem"] = None


# ==========================================================
# 📥 Origem do Edital (3 opções)
# ==========================================================

st.markdown("### 📥 Selecione a origem do Edital")

tab1, tab2, tab3 = st.tabs(["📎 Edital Gerado", "📄 Upload de Arquivo", "✍️ Entrada Manual"])

with tab1:
    st.info("**Opção 1:** Use o edital gerado automaticamente no módulo anterior")
    
    if st.session_state.get("edital_campos_ai"):
        edital_data = st.session_state["edital_campos_ai"]
        st.success(f"✅ Edital detectado: Nº {edital_data.get('numero_edital', 'N/A')}")
        
        # Construir texto do edital gerado
        texto_edital = f"""
EDITAL Nº {edital_data.get('numero_edital', '')}
Data: {edital_data.get('data_publicacao', '')}

OBJETO: {edital_data.get('objeto', '')}

MODALIDADE: {edital_data.get('tipo_licitacao', '')}
CRITÉRIO: {edital_data.get('criterio_julgamento', '')}

CONDIÇÕES DE PARTICIPAÇÃO:
{edital_data.get('condicoes_participacao', '')}

EXIGÊNCIAS DE HABILITAÇÃO:
{edital_data.get('exigencias_habilitacao', '')}

OBRIGAÇÕES DA CONTRATADA:
{edital_data.get('obrigacoes_contratada', '')}

PRAZO DE EXECUÇÃO:
{edital_data.get('prazo_execucao', '')}

RECURSOS:
{edital_data.get('fontes_recursos', '')}

GESTOR/FISCAL:
{edital_data.get('gestor_fiscal', '')}

OBSERVAÇÕES:
{edital_data.get('observacoes_gerais', '')}
"""
        
        if st.button("🔄 Usar este Edital para Validação", key="usar_gerado"):
            st.session_state["validacao_texto"] = texto_edital
            st.session_state["validacao_origem"] = "Edital Gerado (Módulo 06)"
            st.rerun()
    else:
        st.warning("⚠️ Nenhum edital gerado encontrado. Processe um edital no módulo anterior primeiro.")

with tab2:
    st.info("**Opção 2:** Faça upload de um arquivo PDF, DOCX ou TXT contendo o edital")
    
    arquivo_upload = st.file_uploader(
        "Selecione o arquivo do edital:",
        type=["pdf", "docx", "txt"],
        help="Formatos aceitos: PDF, DOCX, TXT"
    )
    
    if arquivo_upload:
        st.success(f"📄 Arquivo carregado: {arquivo_upload.name}")
        
        if st.button("📤 Processar Arquivo", key="processar_upload"):
            with st.spinner("Extraindo texto do arquivo..."):
                # Detectar tipo e extrair
                if arquivo_upload.name.endswith('.pdf'):
                    texto_extraido = extrair_texto_pdf(arquivo_upload)
                elif arquivo_upload.name.endswith('.docx'):
                    texto_extraido = extrair_texto_docx(arquivo_upload)
                else:  # .txt
                    texto_extraido = extrair_texto_txt(arquivo_upload)
                
                if texto_extraido:
                    st.session_state["validacao_texto"] = texto_extraido
                    st.session_state["validacao_origem"] = f"Upload: {arquivo_upload.name}"
                    st.success(f"✅ Texto extraído: {len(texto_extraido)} caracteres")
                    st.rerun()
                else:
                    st.error("❌ Não foi possível extrair texto do arquivo")

with tab3:
    st.info("**Opção 3:** Cole o texto do edital manualmente")
    
    texto_manual = st.text_area(
        "Cole o conteúdo do edital aqui:",
        height=300,
        placeholder="Exemplo: EDITAL Nº 123/2025\n\nO TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO torna público...",
        key="texto_manual_input"
    )
    
    if texto_manual and st.button("✅ Usar Texto Manual", key="usar_manual"):
        st.session_state["validacao_texto"] = texto_manual
        st.session_state["validacao_origem"] = "Entrada Manual"
        st.rerun()

# ==========================================================
# 📊 Execução da Validação
# ==========================================================

if st.session_state["validacao_texto"]:
    st.divider()
    st.markdown("### 📋 Edital Carregado para Validação")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(f"**Origem:** {st.session_state['validacao_origem']}")
        st.caption(f"**Tamanho:** {len(st.session_state['validacao_texto'])} caracteres")
    with col2:
        if st.button("🗑️ Limpar", key="limpar_validacao"):
            st.session_state["validacao_texto"] = ""
            st.session_state["validacao_origem"] = None
            st.rerun()
    
    # Visualizar preview
    with st.expander("👁️ Visualizar Texto Completo"):
        st.text_area("Texto do edital:", st.session_state["validacao_texto"], height=300, disabled=True)
    
    st.divider()
    
    # Seleção de tipo
    tipo_contratacao = st.selectbox(
        "🏷️ Selecione o tipo de contratação:",
        ["Serviços", "Materiais", "Obras", "TI & Software", "Consultorias"],
        help="Isso determina quais itens do checklist serão aplicados"
    )
    
    # Botão de validação
    if st.button("🔍 EXECUTAR VALIDAÇÃO COMPLETA", type="primary", use_container_width=True):
        with st.spinner("Analisando edital contra Lei 14.133/2021 e checklist TJSP..."):
            
            # 1. Validar campos obrigatórios
            resultado_campos = validar_campos_obrigatorios(st.session_state["validacao_texto"])
            
            # 2. Carregar e aplicar checklist
            checklist_data = carregar_checklist()
            resultado_checklist = aplicar_checklist(
                st.session_state["validacao_texto"],
                tipo_contratacao,
                checklist_data
            )
            
            # Salvar resultados na sessão
            st.session_state["resultado_validacao"] = resultado_campos
            st.session_state["resultado_checklist"] = resultado_checklist
            st.session_state["tipo_validacao"] = tipo_contratacao
            
            st.success("✅ Validação concluída!")
            st.rerun()

# ==========================================================
# 📈 Exibição de Resultados
# ==========================================================

if "resultado_validacao" in st.session_state and "resultado_checklist" in st.session_state:
    st.divider()
    st.markdown("## 📊 RESULTADO DA VALIDAÇÃO")
    
    resultado_campos = st.session_state["resultado_validacao"]
    resultado_checklist = st.session_state["resultado_checklist"]
    tipo = st.session_state.get("tipo_validacao", "Serviços")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Campos Obrigatórios",
            f"{resultado_campos['percentual']:.0f}%",
            f"{len(resultado_campos['encontrados'])}/{len(resultado_campos['encontrados']) + len(resultado_campos['faltantes'])}"
        )
    
    with col2:
        st.metric(
            "Checklist Institucional",
            f"{resultado_checklist['score']['percentual']:.0f}%",
            f"{resultado_checklist['score']['aprovados']}/{resultado_checklist['score']['total']}"
        )
    
    with col3:
        # Score geral (média ponderada)
        score_geral = (resultado_campos['percentual'] * 0.4 + resultado_checklist['score']['percentual'] * 0.6)
        cor = "🟢" if score_geral >= 80 else "🟡" if score_geral >= 60 else "🔴"
        st.metric(
            "Score Geral",
            f"{cor} {score_geral:.0f}%",
            "Aprovado" if score_geral >= 70 else "Atenção"
        )
    
    st.divider()
    
    # Detalhamento - Campos Obrigatórios
    st.markdown("### 1️⃣ Campos Obrigatórios (Lei 14.133/2021)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**✅ Encontrados ({len(resultado_campos['encontrados'])}):**")
        for campo in resultado_campos['encontrados']:
            st.markdown(f"- {campo.replace('_', ' ').title()}")
    
    with col2:
        if resultado_campos['faltantes']:
            st.warning(f"**⚠️ Ausentes ({len(resultado_campos['faltantes'])}):**")
            for campo in resultado_campos['faltantes']:
                st.markdown(f"- {campo.replace('_', ' ').title()}")
        else:
            st.success("**✅ Todos os campos obrigatórios presentes!**")
    
    st.divider()
    
    # Detalhamento - Checklist Base
    st.markdown(f"### 2️⃣ {resultado_checklist['base']['title']}")
    
    itens_ok_base = sum(1 for item in resultado_checklist['base']['items'] if item['encontrado'])
    st.progress(itens_ok_base / len(resultado_checklist['base']['items']))
    st.caption(f"{itens_ok_base}/{len(resultado_checklist['base']['items'])} itens atendidos")
    
    with st.expander("📋 Ver itens do checklist base", expanded=False):
        for item in resultado_checklist['base']['items']:
            if item['encontrado']:
                st.success(f"{item['status']} {item['descricao']}")
            else:
                st.warning(f"{item['status']} {item['descricao']}")
    
    st.divider()
    
    # Detalhamento - Checklist Específico
    if resultado_checklist['especifico']['items']:
        st.markdown(f"### 3️⃣ {resultado_checklist['especifico']['title']}")
        
        itens_ok_esp = sum(1 for item in resultado_checklist['especifico']['items'] if item['encontrado'])
        st.progress(itens_ok_esp / len(resultado_checklist['especifico']['items']))
        st.caption(f"{itens_ok_esp}/{len(resultado_checklist['especifico']['items'])} itens atendidos")
        
        with st.expander("📋 Ver itens do checklist específico", expanded=False):
            for item in resultado_checklist['especifico']['items']:
                if item['encontrado']:
                    st.success(f"{item['status']} {item['descricao']}")
                else:
                    st.warning(f"{item['status']} {item['descricao']}")
    
    st.divider()
    
    # Exportação
    st.markdown("### 💾 Exportar Relatório")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Gerar Relatório PDF", type="primary", use_container_width=True):
            with st.spinner("Gerando relatório PDF..."):
                try:
                    arquivo_pdf = gerar_relatorio_pdf(resultado_campos, resultado_checklist, tipo)
                    st.success(f"✅ Relatório gerado: `{arquivo_pdf}`")
                    
                    # Oferecer download
                    with open(arquivo_pdf, "rb") as f:
                        st.download_button(
                            "⬇️ Baixar Relatório PDF",
                            f.read(),
                            file_name=os.path.basename(arquivo_pdf),
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")
    
    with col2:
        # Exportar JSON
        dados_export = {
            "data_validacao": datetime.now().isoformat(),
            "tipo_contratacao": tipo,
            "origem": st.session_state.get("validacao_origem"),
            "campos_obrigatorios": resultado_campos,
            "checklist": resultado_checklist,
            "score_geral": score_geral
        }
        
        st.download_button(
            "📥 Baixar Dados JSON",
            json.dumps(dados_export, ensure_ascii=False, indent=2),
            file_name=f"validacao_edital_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

else:
    st.info("👆 Selecione a origem do edital acima e execute a validação para ver os resultados.")

st.divider()
st.caption("💡 **Sobre o Validador:** Analisa editais contra a Lei 14.133/2021 e checklist institucional do TJSP. Heurísticas baseadas em palavras-chave podem gerar falsos positivos/negativos - sempre revise manualmente.")