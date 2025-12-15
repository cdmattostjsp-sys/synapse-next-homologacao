# Guia de Padrão Visual PJe-Inspired - SynapseNext

**Versão:** 2025.1 (Homologação)  
**Status:** Padrão finalizado e validado  
**Módulos implementados:** DFD ✅ | ETP ✅  
**Pendentes:** TR, Edital, Contrato

---

## 1. Filosofia do Design

### Princípios Fundamentais
- **Sobriedade institucional**: Visual maduro adequado ao ambiente TJSP
- **Hierarquia clara**: Títulos proporcionais, sem peso visual excessivo
- **Funcionalidade visual**: Ícones discretos como apoio, não decoração
- **Contraste sutil**: Fundos cinza para agrupamento sem peso
- **Azul estratégico**: Cor reservada para ações principais

### Referência Conceitual
Sistema inspirado no **PJe (Processo Judicial Eletrônico - CNJ)**: equilibra sobriedade, funcionalidade e clareza visual para ambientes institucionais.

---

## 2. CSS Institucional (Padrão Completo)

### Bloco CSS para copiar em cada módulo

```css
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

/* Tabs institucionais (para módulos com múltiplas abas) */
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
```

---

## 3. Paleta de Cores Institucional

### Cores Principais

| Uso | Hex | Descrição |
|-----|-----|-----------|
| **Azul primário** | `#0969da` | Botões primary, links importantes |
| **Título principal** | `#2c3e50` | H1, títulos de página |
| **Texto seções** | `#374151` | H3, subtítulos |
| **Texto corpo** | `#1f2937` | Labels, texto normal |
| **Texto secundário** | `#6c757d` | Captions, hints |

### Cores de Fundo

| Elemento | Hex | Uso |
|----------|-----|-----|
| **Fundo seções** | `#e5e7eb` | H3, headers de seção |
| **Bloco IA** | `#f0f2f5` | Background do bloco Assistente IA |
| **Tabs inativas** | `#e5e7eb` | Abas não selecionadas |
| **Branco** | `#ffffff` | Background principal |

### Cores de Borda

| Elemento | Hex | Uso |
|----------|-----|-----|
| **Borda padrão** | `#d0d7de` | Botões, blocos, expanders |

---

## 4. Tipografia

### Hierarquia de Tamanhos

```css
H1: 1.8rem (título principal - reduzido para sobriedade)
H2: [Streamlit padrão, raramente usado]
H3: 1.1rem (títulos de seção com fundo cinza)
Corpo: 0.9rem (labels, captions)
```

### Pesos (font-weight)

```css
H1: 500 (médio, não bold)
H3: 500 (médio, não bold)
.ia-block h3: 600 (semi-bold)
Botões: 500
Labels: 500
```

### Ajustes Finos

```css
letter-spacing: -0.01em (para títulos do bloco IA)
```

---

## 5. Ícones Funcionais

### Princípios de Uso
- **Discretos e monocromáticos**: não chamam atenção excessiva
- **Apoio visual**: facilitam reconhecimento rápido da ação
- **Nunca decorativos**: cada ícone tem função específica

### Ícones Padronizados

| Ícone | Uso | Contexto |
|-------|-----|----------|
| ⚡ | Ações de IA/processamento | "Gerar rascunho automático", "Processar com IA" |
| 📤 | Transferência entre módulos | "Enviar para ETP", "Enviar para TR" |
| ⬇️ | Download de arquivo | "Download DOCX (completo)" |
| ⚠️ | Avisos ao usuário | Warnings sobre dados faltantes |

### Exemplos de Implementação

```python
# Botão de IA (primary action)
st.button("⚡ Gerar rascunho automático", type="primary")

# Botão de transferência
st.button("📤 Enviar para ETP", disabled=not dados)

# Botão de download (dentro de st.download_button)
st.download_button(label="⬇️ Download DOCX (completo)", ...)
```

---

## 6. Estrutura de Botões

### Bloco "Assistente IA"

**Layout padrão:** 3 colunas com proporções variáveis

```python
st.markdown("### Assistente IA")
st.caption("Processamento automático: requer insumos do módulo anterior")

col_ia1, col_ia2, col_ia3 = st.columns(3)

with col_ia1:
    # Botão PRIMARY: Ação principal de IA
    if st.button("⚡ Processar com IA", 
                 use_container_width=True, 
                 type="primary", 
                 key="btn_ia_processar"):
        # Lógica de processamento

with col_ia2:
    # Botão de transferência (disabled se não há dados)
    if st.button("📤 Enviar para [PRÓXIMO_MÓDULO]", 
                 use_container_width=True, 
                 disabled=not tem_dados, 
                 key="btn_enviar"):
        # Lógica de envio

with col_ia3:
    st.write("")  # Espaçamento ou info adicional
```

### Bloco "Salvar e Baixar"

**Layout padrão:** 2 colunas (1:1)

```python
st.divider()

col_salvar, col_baixar = st.columns(2)

with col_salvar:
    if st.button("Salvar [ARTEFATO]", 
                 type="secondary", 
                 use_container_width=True):
        # Salva JSON
        st.success("Salvo com sucesso")

with col_baixar:
    if st.button("Baixar [ARTEFATO] (DOCX)", 
                 use_container_width=True):
        # Gera DOCX
        doc = Document()
        # ... adiciona conteúdo
        
        st.download_button(
            label="⬇️ Download DOCX (completo)",
            data=buffer,
            file_name="[ARTEFATO]_completo.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
```

---

## 7. Bloco de IA Institucional

### HTML do Título

```python
# Usar HTML para título H1 com estilo customizado
st.markdown("<h1>[Nome do Módulo]</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>[Descrição do módulo]</p>", unsafe_allow_html=True)
```

### Container IA

```python
st.markdown('<div class="ia-block">', unsafe_allow_html=True)
st.markdown("<h3>Assistente IA</h3>", unsafe_allow_html=True)
st.caption("Processamento automático: requer insumos do módulo anterior")

# Botões do assistente (ver seção 6)

st.markdown('</div>', unsafe_allow_html=True)
```

---

## 8. Checklist de Implementação

### Para cada módulo (TR, Edital, Contrato):

#### Etapa 1: CSS Base
- [ ] Copiar bloco CSS completo (seção 2)
- [ ] Adicionar após `st.set_page_config()`
- [ ] Remover CSS antigo se existir

#### Etapa 2: Título e Caption
- [ ] Converter título para `<h1>` em HTML
- [ ] Adicionar caption com classe `.caption`
- [ ] Verificar tamanho (1.8rem)

#### Etapa 3: Seções do Formulário
- [ ] Garantir `### Título da Seção` para cada grupo
- [ ] Verificar fundo cinza `#e5e7eb` automático via CSS
- [ ] Confirmar hierarquia visual clara

#### Etapa 4: Bloco Assistente IA
- [ ] Criar container com classe `.ia-block`
- [ ] Layout de 3 colunas para botões
- [ ] Adicionar ícone ⚡ no botão primary
- [ ] Adicionar ícone 📤 no botão de envio
- [ ] Desabilitar botões quando não há dados

#### Etapa 5: Botões Salvar/Baixar
- [ ] Criar layout de 2 colunas (1:1)
- [ ] Botão "Salvar [ARTEFATO]" (secondary)
- [ ] Botão "Baixar [ARTEFATO] (DOCX)"
- [ ] Implementar download com `st.download_button`
- [ ] Adicionar ícone ⬇️ no label do download

#### Etapa 6: Refinamento Iterativo
- [ ] Verificar se já usa `render_refinamento_iterativo()`
- [ ] Se não, migrar código inline para componente
- [ ] Confirmar botões de uso rápido funcionais

#### Etapa 7: Validação
- [ ] Executar `get_errors()` no arquivo
- [ ] Testar visualmente cada seção
- [ ] Confirmar hierarquia e contraste
- [ ] Validar funcionalidade dos botões
- [ ] Testar download DOCX

---

## 9. Padrão de Documentação DOCX

### Estrutura do Documento Exportado

```python
doc = Document()

# 1. Cabeçalho principal
doc.add_heading("[Nome do Artefato]", level=1)
doc.add_paragraph("[Contexto legal ou institucional]")

# 2. Dados Administrativos
doc.add_heading("Dados Administrativos", level=2)
doc.add_paragraph(f"Unidade Demandante: {unidade}")
doc.add_paragraph(f"Responsável: {responsavel}")
doc.add_paragraph(f"Prazo Estimado: {prazo}")
doc.add_paragraph(f"Valor Estimado: R$ {valor}")

# 3. Seções estruturadas
doc.add_heading("Seções do [Artefato]", level=2)

for nome_secao, conteudo in secoes.items():
    doc.add_heading(nome_secao, level=3)
    if conteudo and conteudo.strip():
        doc.add_paragraph(conteudo)
    else:
        doc.add_paragraph("[Não preenchido]")

# 4. Exportação
buffer = BytesIO()
doc.save(buffer)
buffer.seek(0)
```

---

## 10. Mapeamento dos Módulos

### Status de Implementação

| Módulo | Arquivo | Status | Prioridade |
|--------|---------|--------|------------|
| **DFD** | `02_📄 DFD - Formalização da Demanda.py` | ✅ Finalizado | - |
| **ETP** | `03_📘 ETP – Estudo Técnico Preliminar.py` | ✅ Finalizado | - |
| **TR** | `05_📑 TR – Termo de Referência.py` | ⏳ Pendente | Alta |
| **Edital** | `06_📜Edital – Minuta do Edital.py` | ⏳ Pendente | Alta |
| **Contrato** | `07_📋 Contrato.py` | ⏳ Pendente | Alta |

### Workflow de Transferência

```
INSUMOS → DFD [📤] → ETP [📤] → TR [📤] → Edital [📤] → Contrato
```

Cada módulo deve ter:
1. Botão de processamento IA (⚡)
2. Botão de envio para próximo módulo (📤)
3. Botões de Salvar/Baixar

---

## 11. Comandos de Validação

### Verificar Erros de Sintaxe

```python
# Após editar qualquer módulo
get_errors(filePaths=["/caminho/para/modulo.py"])
```

### Commit Padrão

```bash
git add -A
git commit -m "refactor(ux): Aplica padrão PJe-inspired no módulo [NOME]

PADRÃO VISUAL INSTITUCIONAL:
- Tipografia: h1 1.8rem, hierarquia proporcional
- Fundos: cinza #e5e7eb para seções
- Ícones: ⚡ (IA), 📤 (envio), ⬇️ (download)
- Botões: azul #0969da apenas em primary
- Layout: 3 cols (IA), 2 cols (salvar/baixar)

Funcionalidades:
- Processamento IA com ícone discreto
- Transferência estruturada para [PRÓXIMO]
- Download DOCX completo

Refs: GUIA_PADRAO_VISUAL_PJe.md"

git push origin main
```

---

## 12. Troubleshooting

### Problema: Fundo cinza muito claro

**Solução:** Verificar se está usando `#e5e7eb` (correto) e não `#f3f4f6` (versão antiga)

### Problema: Título muito grande

**Solução:** Confirmar `h1 { font-size: 1.8rem !important; }`

### Problema: Botões de refinamento não funcionam

**Solução:** 
1. Verificar se usa `render_refinamento_iterativo()` do componente
2. Confirmar sync de session_state ANTES do expander
3. Ver referência: `home_utils/refinamento_ia.py`

### Problema: Download DOCX não aparece

**Solução:**
1. Verificar estrutura de 2 colunas (col_salvar, col_baixar)
2. Confirmar importação: `from io import BytesIO`
3. Verificar se `st.download_button` está DENTRO do bloco `if st.button()`

---

## 13. Exemplos de Referência

### Arquivos Modelo (implementação completa)

```
streamlit_app/pages/02_📄 DFD - Formalização da Demanda.py
streamlit_app/pages/03_📘 ETP – Estudo Técnico Preliminar.py
```

**Usar como referência para:**
- Estrutura CSS completa
- Layout de botões
- Implementação de download
- Integração com `render_refinamento_iterativo()`

### Componente Compartilhado

```
streamlit_app/home_utils/refinamento_ia.py
```

**Função:** `render_refinamento_iterativo()`  
**Uso:** Bloco de refinamento por seção com botões de uso rápido

---

## 14. Boas Práticas

### CSS
- ✅ Sempre incluir `!important` em overrides do Streamlit
- ✅ Usar `border-radius: 3px` (mais técnico que 4px)
- ✅ Preferir `font-weight: 500` ao invés de `bold`
- ❌ Não usar cores decorativas ou gradientes

### Ícones
- ✅ Máximo 1 ícone por botão
- ✅ Ícones Unicode (não imagens)
- ✅ Monocromáticos e discretos
- ❌ Evitar emojis coloridos ou decorativos

### Botões
- ✅ `type="primary"` apenas para ação principal
- ✅ `use_container_width=True` para uniformidade
- ✅ `disabled=not dados` para ações que requerem dados
- ❌ Nunca múltiplos botões primary na mesma tela

### Layout
- ✅ Usar `st.columns()` para organização horizontal
- ✅ `st.divider()` entre blocos funcionais distintos
- ✅ Captions para hints e dicas contextuais
- ❌ Evitar espaçamentos excessivos

---

## 15. Contato e Suporte

**Versão do Guia:** 1.0 (15/12/2025)  
**Última Atualização:** Commit `72348d2`  
**Padrão Base:** Módulos DFD e ETP

Para dúvidas sobre implementação, consultar:
- `GUIA_PADRAO_VISUAL_PJe.md` (este arquivo)
- Arquivos de referência: `02_*.py` e `03_*.py`
- Componente: `home_utils/refinamento_ia.py`

---

**🎯 Objetivo:** Visual maduro, funcional e institucional adequado ao ambiente TJSP, inspirado em sistemas judiciais consolidados como o PJe (CNJ).
