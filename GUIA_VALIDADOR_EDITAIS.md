# 🧩 Guia do Validador de Editais v2025.1

## 📋 Visão Geral

O **Validador de Editais** é um módulo que analisa minutas de editais de licitação contra:
- **Lei Federal nº 14.133/2021** (Nova Lei de Licitações)
- **Checklist Institucional do TJSP** (knowledge/edital_checklist.yml)

Retorna um **score de conformidade** e relatório detalhado exportável.

---

## 🎯 Como Usar

### Opção 1: Edital Gerado Automaticamente ✅ **RECOMENDADO**

1. **Processar Edital no Módulo 06:**
   - Vá para **📜 Edital – Minuta do Edital**
   - Carregue insumo (ou use contexto DFD/ETP/TR)
   - Clique em **"🤖 Processar Edital com IA Especializada"**
   - Aguarde processamento

2. **Validar Automaticamente:**
   - Vá para **🧩 Validador de Editais**
   - Na aba **"📎 Edital Gerado"**, você verá:
     ```
     ✅ Edital detectado: Nº 90207/2025
     ```
   - Clique em **"🔄 Usar este Edital para Validação"**
   - Selecione o tipo de contratação (Serviços, Materiais, Obras, TI, Consultoria)
   - Clique em **"🔍 EXECUTAR VALIDAÇÃO COMPLETA"**

---

### Opção 2: Upload de Arquivo 📄

Use quando tiver um edital existente em PDF/DOCX/TXT:

1. Vá para **🧩 Validador de Editais**
2. Clique na aba **"📄 Upload de Arquivo"**
3. Clique em **"Browse files"** ou arraste o arquivo
4. Formatos aceitos: `.pdf`, `.docx`, `.txt`
5. Clique em **"📤 Processar Arquivo"**
6. Aguarde extração do texto (PyMuPDF para PDF, docx2txt para DOCX)
7. Selecione o tipo de contratação
8. Clique em **"🔍 EXECUTAR VALIDAÇÃO COMPLETA"**

**Requisitos:**
- PDF: precisa ter texto (não pode ser imagem escaneada)
- DOCX: formato Microsoft Word 2007+
- TXT: encoding UTF-8

---

### Opção 3: Entrada Manual ✍️

Use para testes rápidos ou quando não tiver arquivo:

1. Vá para **🧩 Validador de Editais**
2. Clique na aba **"✍️ Entrada Manual"**
3. Cole o texto do edital no campo (até ~100.000 caracteres)
4. Clique em **"✅ Usar Texto Manual"**
5. Selecione o tipo de contratação
6. Clique em **"🔍 EXECUTAR VALIDAÇÃO COMPLETA"**

---

## 📊 Entendendo os Resultados

### Métricas Principais

| Métrica | Descrição | Cálculo |
|---------|-----------|---------|
| **Campos Obrigatórios** | Conformidade com Lei 14.133/2021 | 9 campos essenciais detectados |
| **Checklist Institucional** | Conformidade com padrões TJSP | Itens base (13) + específicos (4-10) |
| **Score Geral** | Nota final ponderada | 40% campos + 60% checklist |

### Interpretação de Cores

- 🟢 **Verde (≥80%)**: Edital em excelente conformidade
- 🟡 **Amarelo (60-79%)**: Edital precisa de ajustes
- 🔴 **Vermelho (<60%)**: Edital com lacunas significativas

---

## 🔍 O Que é Validado?

### 1️⃣ Campos Obrigatórios (Lei 14.133/2021)

Detecta presença de:
- **objeto**: descrição da contratação
- **modalidade**: pregão, concorrência, etc.
- **criterio_julgamento**: menor preço, técnica e preço, etc.
- **prazo_execucao**: vigência do contrato
- **condicoes_pagamento**: formas e prazos
- **habilitacao**: documentação exigida
- **recursos**: prazos para impugnação
- **penalidades**: sanções administrativas
- **fundamentacao_legal**: citação da Lei 14.133/2021

### 2️⃣ Checklist Base (13 itens)

Comum a **todos** os tipos de edital:
- Preâmbulo com órgão, unidade, modalidade
- Objeto vinculado ao TR
- Fundamentação legal (Lei 14.133/2021)
- Local, data, horário de propostas
- Critério de julgamento definido
- Prazo de validade das propostas
- Condições de participação detalhadas
- Minuta contratual anexada
- Exigências de habilitação adequadas
- Cláusula de impugnações/esclarecimentos
- Matriz de responsabilidades
- Sanções administrativas (art. 156)
- Foro competente

### 3️⃣ Checklists Específicos

#### 🔧 Serviços (8 itens)
- Descrição por resultados (não insumos)
- Indicadores de desempenho
- Continuidade e prorrogação (até 60 meses)
- Plano de fiscalização
- Glosas e penalidades
- Substituição de profissionais
- Reajuste contratual
- Encargos trabalhistas discriminados

#### 📦 Materiais (8 itens)
- Especificações sem marcas (salvo justificativa)
- Amostragem/protótipo
- Garantia e assistência técnica
- Prazos de entrega e recebimento
- Penalidades para atraso
- Pagamentos compatíveis
- Substituição de defeituosos
- Logística reversa

#### 🏗️ Obras (10 itens)
- Projeto básico/executivo aprovado
- Orçamento detalhado e planilha
- Matriz de risco (art. 22)
- Responsável técnico (ART/RRT)
- Cronograma físico-financeiro
- Medições e reajustes
- Vistoria prévia
- Qualificação técnica (atestado)
- Garantia e seguro-garantia
- Termos de recebimento

#### 💻 TI & Software (8 itens)
- Diretrizes de segurança TJSP
- Interoperabilidade e LGPD
- Confidencialidade e propriedade intelectual
- SLA com métricas
- Continuidade e suporte
- Compatibilidade com sistemas TJSP
- Homologação e testes
- Capacitação da equipe

#### 📊 Consultoria (4 itens)
- Critério técnica e preço
- Qualificação da equipe
- TR específico com metodologia
- Confidencialidade e não concorrência

---

## 💾 Exportação de Relatórios

### PDF Profissional

**Conteúdo:**
- Cabeçalho institucional TJSP
- Data e metadados da validação
- Seção 1: Campos obrigatórios (lista encontrados/ausentes)
- Seção 2: Checklist base (13 itens com status ✅/⚠️)
- Seção 3: Checklist específico (4-10 itens com status)
- Formatação profissional com cores e espaçamento

**Como gerar:**
1. Após executar validação, role até **"💾 Exportar Relatório"**
2. Clique em **"📄 Gerar Relatório PDF"**
3. Aguarde geração (~5s)
4. Clique em **"⬇️ Baixar Relatório PDF"**
5. Arquivo salvo em: `exports/relatorios/validacao_edital_YYYYMMDD_HHMMSS.pdf`

### JSON Estruturado

**Conteúdo:**
```json
{
  "data_validacao": "2025-12-09T...",
  "tipo_contratacao": "Serviços",
  "origem": "Edital Gerado (Módulo 06)",
  "campos_obrigatorios": {
    "encontrados": [...],
    "faltantes": [...],
    "percentual": 88.9
  },
  "checklist": {
    "base": {...},
    "especifico": {...},
    "score": {...}
  },
  "score_geral": 85.3
}
```

**Como gerar:**
1. Após validação, clique em **"📥 Baixar Dados JSON"**
2. Arquivo baixado: `validacao_edital_YYYYMMDD_HHMMSS.json`

---

## 🧪 Fluxo de Trabalho Recomendado

### Cenário 1: Criar Edital do Zero

```
1. Módulo 02 (DFD) → Processar insumo
2. Módulo 03 (ETP) → Processar insumo
3. Módulo 05 (TR) → Processar insumo
4. Módulo 06 (Edital) → Processar com contexto ✨
5. Módulo 07 (Validador) → Validar edital gerado ✅
6. Ajustar edital baseado nos alertas ⚠️
7. Revalidar até score ≥80% 🎯
8. Exportar PDF final 📄
```

### Cenário 2: Validar Edital Existente

```
1. Módulo 07 (Validador) → Upload do arquivo PDF/DOCX
2. Executar validação
3. Analisar relatório
4. Corrigir lacunas no documento original
5. Revalidar
6. Exportar relatório de conformidade
```

---

## ⚠️ Limitações e Observações

### Heurísticas por Palavras-Chave

A validação usa **detecção de palavras-chave** para identificar itens do checklist. Isso significa:

**Falsos Positivos (✅ mas não deveria):**
- Item marcado como "encontrado" mas implementação é insuficiente
- Exemplo: "prazo" mencionado mas não especificado corretamente

**Falsos Negativos (⚠️ mas deveria ser ✅):**
- Item presente mas com terminologia diferente
- Exemplo: "fornecedor" em vez de "contratada"

**Recomendação:** Use o validador como **ferramenta de apoio**, não como substituto de revisão jurídica/técnica.

### Texto Não Estruturado

PDFs escaneados (imagens) não funcionam - use OCR antes (Tesseract, Adobe Acrobat).

### Tamanho do Texto

Limite prático: ~100.000 caracteres (~50 páginas). Textos maiores podem ser lentos.

---

## 🐛 Troubleshooting

### "Nenhum edital gerado encontrado"

**Causa:** Session state vazio (você não processou edital no Módulo 06).

**Solução:** 
1. Vá para **Módulo 06** primeiro
2. Processe um edital
3. Retorne para o Validador

---

### "Erro ao extrair PDF"

**Causas possíveis:**
1. PDF protegido com senha
2. PDF escaneado (imagem)
3. PyMuPDF não instalado

**Solução:**
- Remova proteção do PDF
- Use OCR para converter imagem em texto
- Verifique `requirements.txt` contém `PyMuPDF`

---

### "Score muito baixo (< 40%)"

**Causas possíveis:**
1. Documento não é um edital (é TR, contrato, etc.)
2. Tipo de contratação incorreto selecionado
3. Edital muito incompleto

**Solução:**
1. Verifique se o documento é realmente um edital
2. Selecione o tipo correto (Serviços, Materiais, etc.)
3. Revise o edital e preencha lacunas

---

### "Todos os itens como ⚠️"

**Causa:** Texto muito curto ou genérico.

**Solução:** 
- Use texto completo do edital (não resumo)
- Verifique se extração funcionou corretamente (aba "Visualizar Texto")

---

## 📚 Referências Legais

- **Lei Federal nº 14.133/2021**: Nova Lei de Licitações e Contratos
- **CNJ Resolução nº 452/2022**: Planejamento de contratações do Judiciário
- **IN 12/2025**: Instrução Normativa TJSP (fictícia para o exemplo)
- **Checklist TJSP**: `knowledge/edital_checklist.yml`

---

## 🚀 Próximas Melhorias (Roadmap)

### Versão 2.1 (Planejado)
- [ ] Validação semântica com IA (GPT-4o-mini)
- [ ] Sugestões automáticas de correção
- [ ] Comparador de editais (diff entre versões)
- [ ] Export em DOCX editável

### Versão 2.2 (Futuro)
- [ ] OCR integrado para PDFs escaneados
- [ ] Análise de riscos jurídicos
- [ ] Templates de edital por tipo
- [ ] Histórico de validações

---

## 💡 Dicas de Uso

1. **Sempre valide após gerar**: Use o Validador logo após criar o edital no Módulo 06
2. **Ajuste iterativo**: Corrija lacunas e revalide até atingir ≥80%
3. **Revise manualmente**: Validador é apoio, não substitui análise jurídica
4. **Use tipo correto**: Selecionar "Serviços" para "Materiais" gera alertas errados
5. **Exporte relatórios**: Mantenha histórico das validações para governança

---

## 📧 Suporte

**Dúvidas ou problemas?**
- Verifique os logs no Streamlit Cloud
- Consulte este guia
- Revise `knowledge/edital_checklist.yml` para entender critérios

---

**Última atualização:** 09/12/2025  
**Versão:** 2.0  
**Autor:** SynapseNext - SAAB/TJSP
