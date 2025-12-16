# Design System TJSP - Padrão PJe-Inspired (Referência)

> **Propósito**: CSS e padrões visuais institucionais para aplicações Streamlit do TJSP  
> **Versão**: 2025.1-homolog  
> **Baseado em**: PJe (Processo Judicial Eletrônico) + CNJ  
> **Data**: Dezembro 2025

---

## 1. PALETA DE CORES INSTITUCIONAL

### Cores Principais:

```css
/* Primária - Azul GitHub (ações principais) */
#0969da

/* Texto Principal */
#2c3e50  /* Títulos h1 */
#374151  /* Seções h2/h3 */
#1f2937  /* Labels de formulário */

/* Fundos e Seções */
#e5e7eb  /* Fundo de seções (h2/h3) */
#f0f2f5  /* Bloco IA, tabs ativas */
#ffffff  /* Cards, expanders */

/* Bordas e Separadores */
#d0d7de  /* Bordas sutis */
#e8e8e8  /* Dividers */

/* Feedback */
#6c757d  /* Captions, textos secundários */
```

### Cores TJSP (Uso Específico):

```css
/* Vinho TJSP - Apenas para Home/Branding */
#990000  /* NÃO usar em módulos operacionais */
```

---

## 2. CSS COMPLETO COPIÁVEL (PADRÃO PJe)

### Bloco CSS para Páginas Streamlit:

```python
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

/* Tabs institucionais (quando aplicável) */
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
```

---

## 3. TIPOGRAFIA

### Hierarquia de Títulos:

```python
# H1 - Título da Página (usar com HTML)
st.markdown("<h1>Título Principal</h1>", unsafe_allow_html=True)
# Font: 1.8rem, Weight: 500, Color: #2c3e50

# H2/H3 - Seções (usar com markdown)
st.markdown("### Nome da Seção")
# Font: 1.1rem, Weight: 500, Color: #374151, Background: #e5e7eb

# Caption - Subtítulo/Descrição
st.markdown("<p class='caption'>Descrição da funcionalidade</p>", unsafe_allow_html=True)
# Font: 0.9rem, Color: #6c757d

# st.caption() - Notas de rodapé
st.caption("💡 Dica: Use este campo para...")
# Streamlit native, cor #6c757d
```

### Pesos de Fonte:

```css
font-weight: 500;  /* Padrão institucional (medium) */
font-weight: 600;  /* Apenas para destaque em cards */
font-weight: 700;  /* NÃO usar (muito pesado) */
```

---

## 4. COMPONENTES VISUAIS

### 4.1 Cabeçalho de Página (Padrão):

```python
# Cabeçalho institucional
st.markdown("<h1>🔧 Nome do Módulo</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Descrição clara do propósito e funcionalidade</p>", unsafe_allow_html=True)
st.divider()
```

### 4.2 Seções (Padrão):

```python
# Usar markdown para seções
st.markdown("### 📋 Nome da Seção")

# NÃO usar st.subheader() ou st.header()
```

### 4.3 Botões (Padrões de Uso):

```python
# Botão PRIMARY - Ações principais (azul #0969da)
st.button("⚡ Processar com IA", type="primary", use_container_width=True)

# Botão SECONDARY - Ações secundárias (cinza)
st.button("Salvar Rascunho", type="secondary", use_container_width=True)

# Botão Normal - Ações terciárias
st.button("🔄 Limpar", use_container_width=False)

# Download Button - Sempre com ícone ⬇️
st.download_button("⬇️ Baixar DOCX", data=buffer, file_name="arquivo.docx")
```

### 4.4 Layouts de Colunas:

```python
# 2 colunas (Salvar + Baixar)
col_salvar, col_baixar = st.columns(2)
with col_salvar:
    st.button("Salvar", type="secondary", use_container_width=True)
with col_baixar:
    st.button("Baixar DOCX", use_container_width=True)

# 3 colunas (Assistente IA)
col_ia1, col_ia2, col_ia3 = st.columns(3)
with col_ia1:
    st.button("⚡ Processar com IA", type="primary", use_container_width=True)
with col_ia2:
    st.info("📋 Informação relevante")
with col_ia3:
    st.success("✅ Status")

# 1 coluna (Campos de conteúdo extenso)
objeto = st.text_area("Objeto do Contrato", height=120)
```

### 4.5 Expanders (Padrão):

```python
# Expander discreto com ícone
with st.expander("🔍 Ver Detalhes", expanded=False):
    st.json(dados)

# Expander de diagnóstico (sempre no final)
with st.expander("🔍 Informações de Diagnóstico"):
    st.json({"status": "ok", "timestamp": "..."})
```

### 4.6 Feedback Visual:

```python
# Sucesso
st.success("✅ Operação concluída com sucesso!")

# Informação
st.info("ℹ️ Contexto detectado: 3/4 módulos disponíveis")

# Aviso
st.warning("⚠️ Alguns campos estão vazios")

# Erro
st.error("❌ Erro ao processar arquivo")

# Spinner (durante processamento)
with st.spinner("⏳ Processando..."):
    resultado = processar()
```

---

## 5. ÍCONES FUNCIONAIS (Não Decorativos)

### Ícones Aprovados e Significado:

```python
⚡  # Processar com IA
📤  # Enviar/Transferir para próximo módulo
⬇️  # Download/Baixar
💾  # Salvar
🔄  # Recarregar/Reset
🔍  # Visualizar/Detalhes
📋  # Informação/Checklist
✅  # Sucesso/Concluído
❌  # Erro/Falha
⚠️  # Aviso/Atenção
ℹ️  # Informação
📊  # Métricas/Dashboard
🧩  # Validação
🔧  # Configuração/Ferramentas
📜  # Documento/Contrato
📘  # Manual/Documentação
```

### Onde NÃO Usar Ícones:
- Dentro de labels de formulário
- Em textos longos (apenas no início)
- Em títulos H2/H3 (usar markdown puro)

---

## 6. RESPONSIVIDADE

### Breakpoints e Comportamento:

```python
# Desktop (>= 1024px)
st.columns(3)  # 3 colunas funcionam bem

# Tablet (768px - 1023px)
st.columns(2)  # Reduzir para 2 colunas

# Mobile (< 768px)
# Streamlit colapsa automaticamente para 1 coluna
```

### Testes Recomendados:
- Desktop: 1920x1080
- Tablet: 768x1024
- Mobile: 375x667 (iPhone SE)

---

## 7. ACESSIBILIDADE

### Checklist:

```python
✅ Contraste mínimo 4.5:1 (texto/fundo)
✅ Labels descritivos em todos os inputs
✅ Feedback visual para todas as ações
✅ Mensagens de erro claras e acionáveis
✅ Navegação por teclado funcional
✅ Ícones com significado claro
```

---

## 8. EXEMPLOS DE CÓDIGO COMPLETO

### Página Mínima com Padrão PJe:

```python
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import streamlit as st
from home_utils.sidebar_organizer import apply_sidebar_grouping

# Configuração
st.set_page_config(page_title="Módulo", layout="wide", page_icon="🔧")
apply_sidebar_grouping()

# CSS institucional PJe-inspired
st.markdown("""
<style>
/* [INSERIR CSS COMPLETO AQUI] */
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1>🔧 Nome do Módulo</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Descrição do módulo</p>", unsafe_allow_html=True)
st.divider()

# Conteúdo principal
st.markdown("### 📋 Seção Principal")

campo1 = st.text_input("Campo 1")
campo2 = st.text_area("Campo 2", height=100)

# Botões
col1, col2 = st.columns(2)
with col1:
    if st.button("Salvar", type="secondary", use_container_width=True):
        st.success("✅ Dados salvos!")
with col2:
    if st.button("Baixar", use_container_width=True):
        st.download_button("⬇️ Download", data="...", file_name="arquivo.txt")

# Rodapé
st.divider()
st.caption("💡 Dica: Use este módulo para...")
```

---

## 9. ANTI-PADRÕES (NÃO FAZER)

### ❌ CSS Incorreto:

```python
# NÃO usar cores personalizadas
background-color: #ff0000;  # ❌

# NÃO usar font-weight 700 (muito pesado)
font-weight: 700;  # ❌

# NÃO usar border-radius grande demais
border-radius: 20px;  # ❌ (usar 3px)
```

### ❌ Componentes Errados:

```python
# NÃO usar st.subheader() ou st.header()
st.subheader("Título")  # ❌

# Usar markdown
st.markdown("### Título")  # ✅

# NÃO usar type="primary" em todos os botões
st.button("Qualquer Coisa", type="primary")  # ❌

# Usar apenas em ações principais
st.button("⚡ Processar com IA", type="primary")  # ✅
```

---

## 10. CHECKLIST DE IMPLEMENTAÇÃO

Ao criar uma nova página, verificar:

```
□ CSS institucional completo copiado
□ Cabeçalho com <h1> HTML + caption
□ Seções com st.markdown("###...")
□ Botões com type apropriado (primary apenas em ações principais)
□ use_container_width=True em botões importantes
□ Ícones funcionais (não decorativos)
□ Cores da paleta oficial (#0969da, #e5e7eb, etc)
□ font-weight: 500 (não 700)
□ border-radius: 3px (não 10px+)
□ Expanders para conteúdo secundário
□ st.divider() entre seções principais
□ st.caption() para dicas e rodapé
```

---

## 11. REFERÊNCIAS

- **Arquitetura**: Ver `ARCHITECTURE_PATTERNS.md`
- **Integração**: Ver `INTEGRATION_BLUEPRINT.md`
- **Código**: Ver `CODE_STANDARDS.md`
- **Guia Visual Original**: `/GUIA_PADRAO_VISUAL_PJe.md` (raiz do projeto)

---

## 12. MANUTENÇÃO

### Quando Atualizar Este Documento:

- Novos componentes aprovados
- Mudanças na paleta de cores
- Novos padrões de layout
- Feedback de usabilidade

### Versionamento:

- **v2025.1**: Versão inicial homologada (Dezembro 2025)
- Próximas versões seguirão padrão `v2025.X`

---

**Última atualização**: 16/12/2025  
**Mantido por**: Engenheiro Synapse | SAAB/TJSP  
**Aplicável a**: Todos os projetos Streamlit do TJSP
