# 📘 Manual do Usuário – Projeto SAAB-Tech

## Manual 02: Módulos de Planejamento

**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Tribunal de Justiça do Estado de São Paulo**  
**Secretaria de Administração e Abastecimento (SAAB)**

---


---

## 1. Visão Geral

### 1.1 O que são Módulos de Planejamento?

Os **Módulos de Planejamento** constituem a **fase interna** da contratação pública, onde são elaborados os documentos fundamentais que justificam e especificam a necessidade da contratação.

Estes módulos correspondem aos **4 primeiros estágios** da jornada:

```
🔧 INSUMOS → 📄 DFD → 📘 ETP → 📑 TR
```

### 1.2 Base Legal

Todos os módulos de planejamento seguem:
- **Lei Federal nº 14.133/2021** (Art. 18 a 24 - Planejamento)
- **Decreto Federal nº 11.462/2023** (Regulamentação)
- **IN SEGES/ME nº 40/2020** (Estudos Técnicos Preliminares)
- **IN SEGES/ME nº 65/2021** (Termo de Referência)

### 1.3 Integração entre Módulos

```mermaid
graph LR
    A[Insumo Bruto] --> B[DFD]
    B --> C[ETP]
    C --> D[TR]
    D --> E[Edital]
```

**Cada módulo herda informações do anterior**, reduzindo retrabalho e garantindo consistência.

---

## 2. Módulo 01: Insumos

### 2.1 O que é o Módulo Insumos?

O módulo **🔧 Insumos** é o **ponto de entrada** do sistema. Ele permite:
- Upload de documentos administrativos (PDF, DOCX, TXT)
- Extração automática de texto
- Roteamento inteligente para outros módulos
- Processamento com agentes de IA especializados

### 2.2 Como Acessar

1. Na barra lateral, clique em **🔧 Insumos**
2. Aguarde o carregamento da interface

### 2.3 Interface do Módulo

#### **Seção 1: Upload de Documento**

```
┌─────────────────────────────────────────┐
│  📎 Envio de documento administrativo   │
│                                         │
│  [Selecione o arquivo de insumo]       │
│  Formatos aceitos: TXT, DOCX, PDF      │
│                                         │
│  [📁 Browse files...]                   │
└─────────────────────────────────────────┘
```

#### **Seção 2: Seleção de Destino**

```
┌─────────────────────────────────────────┐
│  🧭 Selecione o módulo de destino:      │
│                                         │
│  ▼ [DFD                            ]    │
│     ETP                                 │
│     TR                                  │
│     EDITAL                              │
│     CONTRATO                            │
└─────────────────────────────────────────┘
```

#### **Seção 3: Processamento**

```
┌─────────────────────────────────────────┐
│  [🚀 Processar e encaminhar para DFD]   │
└─────────────────────────────────────────┘
```

### 2.4 Passo a Passo Completo

#### **Passo 1: Preparar o Documento**

**Tipos de documentos aceitos:**
- 📄 **Memorandos** de solicitação de compra/serviço
- 📄 **Levantamentos técnicos** de necessidades
- 📄 **Atas de reunião** com definições
- 📄 **Orçamentos** preliminares
- 📄 **Estudos** de viabilidade
- 📄 **Contratos anteriores** (para renovação)

**Requisitos técnicos:**
- ✅ Arquivo em formato PDF, DOCX ou TXT
- ✅ Texto legível (não imagem escaneada sem OCR)
- ✅ Tamanho máximo: 10 MB
- ✅ Conteúdo em português

#### **Passo 2: Fazer Upload**

1. Clique no botão **"Browse files"**
2. Navegue até o arquivo no seu computador
3. Selecione o arquivo
4. Clique em **"Abrir"**

**Feedback visual:**
```
✅ Arquivo carregado na memória: memorando_compras.pdf (245 KB)
```

#### **Passo 3: Selecionar Destino**

Escolha para qual módulo o insumo será enviado:

| Destino | Quando usar |
|---------|-------------|
| **DFD** | Primeiro documento da contratação, necessidade inicial |
| **ETP** | Já tem DFD, precisa estruturar estudos técnicos |
| **TR** | Já tem ETP, precisa detalhar especificações |
| **EDITAL** | Tem minuta de edital para processar |
| **CONTRATO** | Tem minuta de contrato ou contrato de referência |

#### **Passo 4: Processar**

1. Clique no botão **"🚀 Processar e encaminhar para [destino]"**
2. Aguarde o processamento (~10-30 segundos)

**O que acontece nos bastidores:**
```
1. Sistema extrai texto do arquivo
2. Agente de IA analisa o conteúdo
3. Identifica campos estruturados
4. Salva em formato JSON
5. Redireciona para o módulo de destino
```

#### **Passo 5: Verificar Resultado**

Após o processamento:
```
✅ Insumo processado com sucesso!
📄 Arquivo: memorando_compras.pdf
🎯 Destino: DFD
📊 165 palavras extraídas
💾 Dados salvos em: exports/insumos/json/DFD_ultimo.json

[➡️ Ir para o módulo DFD]
```

### 2.5 Formatos de Arquivo Suportados

#### **PDF (.pdf)**
- ✅ PDFs com texto selecionável
- ✅ PDFs gerados por editores (Word, Google Docs)
- ⚠️ PDFs escaneados requerem OCR prévio
- ❌ PDFs protegidos por senha não são suportados

**Tecnologia:** PyMuPDF (fitz)

#### **DOCX (.docx)**
- ✅ Microsoft Word 2007 ou superior
- ✅ Google Docs exportado como DOCX
- ✅ LibreOffice Writer (.docx)

**Tecnologia:** docx2txt

#### **TXT (.txt)**
- ✅ Arquivos de texto puro
- ✅ Codificação UTF-8
- ✅ Qualquer editor de texto

### 2.6 Solução de Problemas

#### **Problema: "Erro ao extrair texto do PDF"**
**Solução:**
- Verifique se o PDF não está corrompido
- Tente abrir o PDF em um leitor (Adobe, Chrome)
- Se for escaneado, use software de OCR antes
- Converta para DOCX ou TXT

#### **Problema: "Arquivo muito grande"**
**Solução:**
- Divida o documento em partes menores
- Remova páginas desnecessárias
- Comprima o PDF usando ferramentas online

#### **Problema: "Nenhum conteúdo extraído"**
**Solução:**
- Confirme que há texto no documento
- Verifique se não é apenas imagens
- Teste com outro formato (DOCX em vez de PDF)

---

## 3. Módulo 02: DFD

### 3.1 O que é o DFD?

O **DFD (Documento de Formalização da Demanda)** é o primeiro documento oficial da fase interna da contratação. Ele registra:
- A necessidade institucional
- A justificativa para a contratação
- Informações preliminares sobre objeto e valor
- Fundamentação legal básica

**Base Legal:** Art. 18, §1º, Lei 14.133/2021

### 3.2 Estrutura do DFD

O DFD no Projeto SAAB-Tech possui **11 seções estruturadas**:

| Nº | Seção | Conteúdo |
|----|-------|----------|
| 1 | **Contexto Institucional** | Situação atual do órgão |
| 2 | **Diagnóstico da Situação Atual** | Problemas identificados |
| 3 | **Fundamentação da Necessidade** | Por que contratar? |
| 4 | **Objetivos da Contratação** | O que se espera alcançar |
| 5 | **Escopo Inicial da Demanda** | Descrição preliminar do objeto |
| 6 | **Resultados Esperados** | Metas e entregas |
| 7 | **Benefícios Institucionais** | Ganhos para o órgão |
| 8 | **Justificativa Legal** | Fundamento jurídico |
| 9 | **Riscos da Não Contratação** | Consequências de não contratar |
| 10 | **Requisitos Mínimos** | Especificações essenciais |
| 11 | **Critérios de Sucesso** | Como avaliar o resultado |

### 3.3 Como Acessar

1. Na barra lateral, clique em **📄 DFD – Formalização da Demanda**
2. A interface carregará automaticamente

### 3.4 Interface do Módulo

#### **Cabeçalho Informativo**
```
📄 Formalização da Demanda (DFD)
📌 DFD carregado a partir dos insumos processados no módulo 🔧 Insumos.

ℹ️ Status: Insumo detectado (DFD_ultimo.json)
```

#### **Botão de Processamento IA**
```
┌─────────────────────────────────────────────┐
│  [✨ Gerar Rascunho com IA Especializada]   │
└─────────────────────────────────────────────┘
```

#### **Formulário Estruturado**
```
┌─────────────────────────────────────────────┐
│  📋 Documento de Formalização da Demanda    │
│                                             │
│  ▼ 1. Contexto Institucional               │
│  [Text area - editável]                     │
│                                             │
│  ▼ 2. Diagnóstico da Situação Atual        │
│  [Text area - editável]                     │
│                                             │
│  ... (11 seções)                            │
└─────────────────────────────────────────────┘
```

### 3.5 Formas de Preencher o DFD

O sistema oferece **3 opções** para preencher o DFD:

#### **Opção 1: Processar Insumo com IA (Recomendado)**

**Pré-requisito:** Ter enviado um insumo no módulo 🔧 Insumos

**Passos:**
1. Acesse o módulo DFD
2. Verifique a mensagem de insumo detectado
3. Clique em **"✨ Gerar Rascunho com IA Especializada"**
4. Aguarde processamento (~15-30 segundos)

**Resultado:**
```
✅ Rascunho de DFD gerado com sucesso!
📊 11 seções preenchidas automaticamente
💾 Dados salvos em: exports/dfd_data.json
```

#### **Opção 2: Preencher Manualmente**

**Quando usar:** Não tem insumo ou prefere controle total

**Passos:**
1. Acesse o módulo DFD
2. Clique em cada seção expansível
3. Digite o conteúdo diretamente
4. Clique em **"💾 Salvar Formulário"**

#### **Opção 3: Híbrida (IA + Manual)**

**Melhor abordagem!**

1. Processe com IA primeiro
2. Revise seção por seção
3. Ajuste e complemente conforme necessário
4. Salve a versão final

### 3.6 Passo a Passo Completo

#### **Exemplo Prático: Contratação de Serviços de Limpeza**

**Contexto:**
- Unidade: Fórum da Comarca de Guarulhos
- Necessidade: Renovação do contrato de limpeza
- Valor estimado: R$ 850.000/ano

**Passo 1: Processar Insumo**
```
1. Já enviou memorando no módulo Insumos
2. Acessa módulo DFD
3. Vê mensagem: "Insumo detectado"
4. Clica em "Gerar Rascunho com IA"
```

**Passo 2: Revisar Seções Geradas**

**Seção 1 - Contexto Institucional (exemplo gerado):**
```
O Fórum da Comarca de Guarulhos possui 45.000m² de área 
construída, atendendo diariamente cerca de 3.500 pessoas 
entre servidores, magistrados, advogados e público em geral. 
A manutenção da higiene e limpeza é essencial para o 
funcionamento adequado das atividades jurisdicionais.
```

**Seção 2 - Diagnóstico (exemplo gerado):**
```
O contrato atual de limpeza vence em 30/03/2026. Sem a 
renovação ou nova contratação, haverá descontinuidade nos 
serviços essenciais, comprometendo a salubridade e a 
segurança sanitária das dependências do Fórum.
```

**Passo 3: Ajustar Informações**

Você pode clicar em qualquer seção e editar:
```
[ANTES]
Valor estimado: A definir

[DEPOIS - editado por você]
Valor estimado: R$ 850.000,00 anuais (estimativa baseada 
em contratos similares da região)
```

**Passo 4: Salvar**
```
Clique em: [💾 Salvar Formulário]

Feedback:
✅ DFD salvo com sucesso!
💾 Arquivo: exports/dfd_data.json
🕐 Última atualização: 10/12/2025 14:35
```

**Passo 5: Exportar DOCX**
```
Clique em: [📤 Gerar DOCX Institucional]

Sistema gera:
- Documento Word formatado
- Cabeçalho TJSP
- 11 seções estruturadas
- Rodapé com data e versão

Download automático: DFD_Guarulhos_Limpeza_20251210.docx
```

### 3.7 Campos Especiais do DFD

Além das 11 seções textuais, o DFD possui **campos administrativos**:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| **unidade_solicitante** | Órgão demandante | "Fórum de Guarulhos" |
| **responsavel** | Servidor responsável | "João Silva - Diretor" |
| **data_elaboracao** | Data de criação | "10/12/2025" |
| **valor_estimado** | Estimativa preliminar | "R$ 850.000,00" |
| **prazo_estimado** | Duração prevista | "12 meses" |

### 3.8 Dicas de Qualidade

✅ **Boas práticas:**
- Use parágrafos de 3-5 linhas para facilitar leitura
- Cite legislação aplicável (Lei 14.133/2021)
- Inclua dados concretos (áreas, quantidades, valores)
- Seja objetivo e técnico
- Evite linguagem informal

✅ **Checklist de Revisão:**
- [ ] Todas as 11 seções estão preenchidas?
- [ ] Valor estimado foi informado?
- [ ] Responsável está identificado?
- [ ] Justificativa está clara?
- [ ] Há fundamentação legal?

### 3.9 Validações Automáticas

O sistema valida automaticamente:

| Validação | Critério | Severidade |
|-----------|----------|------------|
| **Seção vazia** | Alguma das 11 seções sem texto | ⚠️ Média |
| **Texto muito curto** | Seção com menos de 50 caracteres | ⚠️ Média |
| **Valor ausente** | Campo "valor_estimado" vazio | 🚨 Alta |
| **Responsável ausente** | Campo "responsavel" vazio | 🚨 Crítica |

**Onde ver alertas?**
- Vá ao módulo **⚠️ Alertas**
- Filtre por "DFD"
- Corrija os itens apontados

---

## 4. Módulo 03: ETP

### 4.1 O que é o ETP?

O **ETP (Estudos Técnicos Preliminares)** é o documento que detalha tecnicamente a contratação. É **obrigatório** pela Lei 14.133/2021 para todas as contratações.

**Base Legal:** Art. 18, §1º, Lei 14.133/2021 + IN SEGES/ME 40/2020

### 4.2 Estrutura do ETP

O ETP possui **27 seções obrigatórias**:

#### **Grupo 1: Identificação (4 campos)**
1. Unidade Demandante
2. Responsável pela Elaboração
3. Equipe de Planejamento
4. Data de Elaboração

#### **Grupo 2: Necessidade (5 seções)**
5. Descrição da Necessidade
6. Área Requisitante
7. Descrição dos Requisitos da Contratação
8. Levantamento de Mercado
9. Descrição da Solução como um Todo

#### **Grupo 3: Contratação (7 seções)**
10. Justificativa da Contratação
11. Descrição do Objeto
12. Especificações Técnicas
13. Quantidade
14. Valor Estimado
15. Prazo de Execução
16. Modalidade de Licitação

#### **Grupo 4: Riscos e Sustentabilidade (5 seções)**
17. Análise de Riscos
18. Medidas de Mitigação de Riscos
19. Resultados Esperados
20. Providências a Serem Adotadas
21. Critérios de Sustentabilidade

#### **Grupo 5: Contratual (6 seções)**
22. Regime de Execução
23. Critério de Julgamento
24. Forma de Pagamento
25. Critérios de Habilitação
26. Estimativa de Impacto Econômico-Financeiro
27. Declarações Complementares

### 4.3 Como Acessar

1. Na barra lateral, clique em **📘 ETP – Estudo Técnico Preliminar**
2. Aguarde carregamento

### 4.4 Interface do Módulo

#### **Status de Carregamento**
```
ℹ️ Status ETP
📎 Campos do ETP carregados automaticamente do módulo INSUMOS
📊 Contexto detectado: DFD disponível
```

#### **Botão de Processamento IA**
```
┌──────────────────────────────────┬─────────────────┐
│  📊 Preencha as seções abaixo ou │ [✨ Processar   │
│  clique em 'Processar com IA'    │  com IA]        │
└──────────────────────────────────┴─────────────────┘
```

### 4.5 Formas de Preencher o ETP

#### **Opção 1: Processar com IA (Inteligente)**

**O que acontece:**
1. Sistema lê DFD já preenchido
2. Sistema lê insumo original (se houver)
3. ETPAgent estrutura as 27 seções
4. Enriquece com informações técnicas
5. Preenche formulário automaticamente

**Passos:**
```
1. Clique em [✨ Processar com IA]
2. Aguarde (~30-45 segundos)
3. Visualize métricas:
   - Unidade: Fórum de Guarulhos
   - Responsável: João Silva
   - Prazo: 12 meses
   - Valor: R$ 850.000,00
4. Veja: "Seções preenchidas: 27/27"
```

#### **Opção 2: Upload de Insumo Específico**

Se você tem um documento ETP existente:
```
1. Vá ao módulo 🔧 Insumos
2. Faça upload do arquivo
3. Selecione destino: "ETP"
4. Processe
5. Volte ao módulo ETP
6. Campos estarão preenchidos
```

#### **Opção 3: Preenchimento Manual**

Para controle total:
```
1. Role para baixo até o formulário
2. Preencha seção por seção
3. Use os campos de texto expandidos
4. Salve periodicamente
```

### 4.6 Passo a Passo Completo

#### **Continuando o exemplo: Serviços de Limpeza**

**Passo 1: Garantir que DFD está completo**
```
✅ DFD já foi preenchido e salvo
✅ Contém informações sobre limpeza do Fórum
✅ Valor estimado definido
```

**Passo 2: Acessar módulo ETP**
```
1. Clica em [📘 ETP] na barra lateral
2. Sistema detecta DFD automaticamente
3. Mostra: "Contexto detectado: DFD disponível"
```

**Passo 3: Processar com IA**
```
1. Clica em [✨ Processar com IA]
2. Aguarda processamento
3. Visualiza métricas preenchidas:
   ┌─────────────┬─────────────┬─────────────┬─────────────┐
   │ Unidade     │ Responsável │ Prazo       │ Valor       │
   │ Fórum Gua...│ João Silva  │ 12 meses    │ R$ 850k     │
   └─────────────┴─────────────┴─────────────┴─────────────┘
```

**Passo 4: Revisar Seções Críticas**

**Seção 5 - Descrição da Necessidade (gerada):**
```
O Fórum da Comarca de Guarulhos necessita contratar empresa 
especializada em serviços de limpeza, conservação e higienização 
para suas dependências, garantindo ambiente adequado para o 
desenvolvimento das atividades jurisdicionais e administrativas, 
conforme exigências da Vigilância Sanitária e normas da ANVISA.
```

**Seção 10 - Justificativa (gerada):**
```
A contratação justifica-se pela:
• Obrigatoriedade legal de manter condições salubres
• Vencimento do contrato atual em 30/03/2026
• Impossibilidade de execução direta pelo órgão
• Especialização técnica exigida para serviços de limpeza hospitalar
• Conformidade com Lei 14.133/2021, Art. 11, II
```

**Seção 14 - Valor Estimado (você ajusta):**
```
[GERADO]
R$ 850.000,00 anuais

[VOCÊ ADICIONA DETALHES]
R$ 850.000,00 anuais, sendo:
• Limpeza geral: R$ 600.000,00
• Limpeza especializada (banheiros, copas): R$ 150.000,00
• Produtos e equipamentos: R$ 100.000,00

Base: Pesquisa de preços realizada em 05/12/2025 com 3 fornecedores
```

**Passo 5: Salvar ETP**
```
Clique em: [💾 Salvar ETP]

✅ ETP salvo com sucesso!
💾 Arquivo: exports/etp_data.json
📊 27/27 seções preenchidas (100%)
```

**Passo 6: Exportar DOCX**
```
Clique em: [📤 Gerar DOCX do ETP]

Download: ETP_Guarulhos_Limpeza_20251210.docx
- 15-20 páginas
- Formatação institucional TJSP
- Todas as 27 seções estruturadas
- Tabelas e listas formatadas
```

### 4.7 Seções Mais Importantes

#### **⭐ Seção 12: Especificações Técnicas**

Esta é a seção **mais crítica** do ETP. Deve conter:

```markdown
**Exemplo de boa especificação:**

ESPECIFICAÇÕES TÉCNICAS DOS SERVIÇOS DE LIMPEZA

1. LIMPEZA GERAL (Áreas Administrativas)
   - Frequência: Diária (segunda a sexta)
   - Horário: 18h às 22h (após expediente)
   - Atividades:
     • Varrição e lavagem de pisos
     • Limpeza de vidros e janelas
     • Recolhimento de lixo
     • Limpeza de mobiliário

2. LIMPEZA ESPECIALIZADA (Sanitários)
   - Frequência: 3x ao dia (8h, 12h, 17h)
   - Produtos: Desinfetantes hospitalares aprovados ANVISA
   - Atividades:
     • Desinfecção de sanitários, pias, espelhos
     • Reposição de papel higiênico, sabonete, toalhas
     • Desobstrução de ralos

3. MATERIAIS E EQUIPAMENTOS
   - Fornecidos pela CONTRATADA
   - Produtos biodegradáveis (sustentabilidade)
   - Equipamentos de proteção individual (EPIs)
```

#### **⭐ Seção 17: Análise de Riscos**

Identifique potenciais problemas:

```markdown
| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Greve de funcionários | Média | Alto | Cláusula de continuidade no contrato |
| Falta de produtos | Baixa | Médio | Estoque mínimo obrigatório |
| Qualidade insatisfatória | Média | Alto | Fiscalização semanal + penalidades |
| Atraso no início | Baixa | Alto | Prazo de mobilização de 5 dias |
```

### 4.8 Validações do ETP

| Validação | Critério | Alerta |
|-----------|----------|--------|
| Seções vazias | Alguma das 27 não preenchida | 🚨 Crítico |
| Valor estimado ausente | Campo vazio ou "a definir" | 🚨 Crítico |
| Prazo indefinido | "A definir", "N/A" | ⚠️ Alto |
| Especificação curta | Seção 12 com menos de 200 caracteres | ⚠️ Médio |

---

## 5. Módulo 04: TR

### 5.1 O que é o TR?

O **TR (Termo de Referência)** é o documento técnico que detalha **minuciosamente** o objeto da contratação, especificações, obrigações, critérios de aceitação e condições contratuais.

**Base Legal:** Art. 6º, XXIII + Art. 40, Lei 14.133/2021

### 5.2 Estrutura do TR

O TR possui **9 seções principais**:

| Nº | Seção | Conteúdo |
|----|-------|----------|
| 1 | **Do Objeto** | Descrição detalhada do que será contratado |
| 2 | **Justificativa** | Fundamentação da necessidade (resumo DFD+ETP) |
| 3 | **Especificação Técnica** | Detalhamento técnico completo |
| 4 | **Quantitativo e Prazo** | Volumes, unidades, cronograma |
| 5 | **Critérios de Aceitação** | Como avaliar a entrega |
| 6 | **Obrigações da Contratada** | Deveres da empresa |
| 7 | **Obrigações da Contratante** | Deveres do TJSP |
| 8 | **Forma de Pagamento** | Condições e prazos de pagamento |
| 9 | **Sanções Administrativas** | Penalidades por descumprimento |

### 5.3 Como Acessar

1. Na barra lateral, clique em **📑 TR – Termo de Referência**
2. Aguarde carregamento

### 5.4 Interface do Módulo

#### **Detecção Automática de Contexto**
```
✅ Contexto detectado:
   • DFD: Disponível
   • ETP: Disponível
   📊 O TRAgent utilizará estes dados automaticamente
```

#### **Opções de Preenchimento**
```
┌──────────────────────────────────────────────┐
│ [🤖 Processar com IA]  [📄 Carregar Modelo] │
└──────────────────────────────────────────────┘
```

### 5.5 Passo a Passo Completo

#### **Continuando: Serviços de Limpeza**

**Passo 1: Verificar Contexto**
```
✅ DFD completo
✅ ETP completo (27 seções)
✅ Pronto para gerar TR
```

**Passo 2: Processar com TRAgent**
```
1. Clica em [🤖 Processar com IA]
2. Aguarda (~30-40 segundos)
3. Sistema:
   - Lê DFD inteiro
   - Lê ETP inteiro
   - Consolida informações
   - Estrutura TR nas 9 seções
```

**Passo 3: Revisar Seções do TR**

**Seção 1 - Do Objeto (exemplo gerado):**
```
Contratação de empresa especializada para prestação de serviços 
continuados de limpeza, conservação e higienização das dependências 
do Fórum da Comarca de Guarulhos/SP, com fornecimento de materiais, 
equipamentos e mão de obra especializada, pelo período de 12 (doze) 
meses, podendo ser prorrogado até 60 meses nos termos do Art. 107 
da Lei 14.133/2021.
```

**Seção 3 - Especificação Técnica (gerada do ETP):**
```
3.1 ROTINA DIÁRIA DE LIMPEZA
[Copia detalhes da Seção 12 do ETP]

3.2 PRODUTOS A SEREM UTILIZADOS
• Desinfetantes: Quaternário de amônio (ANVISA)
• Detergentes: Biodegradáveis, pH neutro
• Ceras: Líquidas incolores para pisos
[...]

3.3 MÃO DE OBRA
• Quantidade: 25 funcionários
• Turno diurno: 15 funcionários (7h-16h)
• Turno noturno: 10 funcionários (18h-22h)
• Uniformes: Padronizados, com identificação
• Capacitação: Treinamento inicial obrigatório
```

**Seção 5 - Critérios de Aceitação (crítico!):**
```
5.1 FISCALIZAÇÃO
A fiscalização será exercida por servidor designado, que verificará:
• Cumprimento do cronograma de limpeza
• Qualidade dos serviços prestados
• Presença dos funcionários
• Adequação dos produtos utilizados

5.2 CRITÉRIOS DE RECUSA
Serão recusados serviços que apresentarem:
• Áreas não limpas conforme especificação
• Produtos inadequados ou vencidos
• Ausência de funcionários sem justificativa
• Descumprimento de normas de segurança

5.3 INDICADORES DE QUALIDADE
• Meta: 95% de aprovação em fiscalizações mensais
• Método: Checklist com 20 itens de verificação
• Penalidade: Redução de 10% do pagamento por falha grave
```

**Passo 4: Ajustar Obrigações**

**Seção 6 - Obrigações da Contratada (você pode adicionar):**
```
[GERADO PELA IA]
6.1 Fornecer todos os materiais e equipamentos
6.2 Disponibilizar mão de obra qualificada
6.3 Cumprir legislação trabalhista
6.4 Manter seguro de responsabilidade civil

[VOCÊ ADICIONA]
6.5 Substituir funcionários faltosos em até 2 horas
6.6 Fornecer relatório mensal de atividades
6.7 Manter canal de atendimento 24h para emergências
6.8 Realizar inspeção mensal com gestor do contrato
```

**Passo 5: Salvar e Exportar**
```
1. Clica em [💾 Salvar TR]
   ✅ TR salvo em exports/tr_data.json

2. Clica em [📤 Gerar DOCX do TR]
   Download: TR_Guarulhos_Limpeza_20251210.docx
   - 20-25 páginas
   - Formatação oficial TJSP
   - 9 seções completas
```

### 5.6 Modelos Pré-definidos

O sistema oferece **modelos institucionais** para tipos comuns:

| Tipo | Modelo | Quando usar |
|------|--------|-------------|
| **Serviços Contínuos** | TR_Servicos_Continuos.docx | Limpeza, segurança, telefonia |
| **Materiais** | TR_Aquisicao_Materiais.docx | Compra de bens |
| **TI** | TR_Tecnologia_Informacao.docx | Software, hardware, suporte |
| **Obras** | TR_Obras_Reformas.docx | Construção, reforma |

**Como usar:**
```
1. No módulo TR, clique em [📄 Carregar Modelo]
2. Selecione o modelo adequado
3. Sistema preenche estrutura básica
4. Ajuste para sua necessidade específica
5. Salve
```

### 5.7 Checklist de Qualidade do TR

Antes de finalizar, verifique:

- [ ] **Objeto** está claro e completo?
- [ ] **Especificações técnicas** são mensuráveis?
- [ ] **Quantidades** estão definidas?
- [ ] **Prazo de execução** está especificado?
- [ ] **Critérios de aceitação** são objetivos?
- [ ] **Obrigações** de ambas as partes estão claras?
- [ ] **Forma de pagamento** está detalhada?
- [ ] **Sanções** estão proporcionais?
- [ ] **Referências legais** estão corretas?

---

## 6. Fluxo Integrado

### 6.1 Visão do Fluxo Completo

```
ETAPA 1: INSUMO
├─ Upload de memorando
├─ Processamento com DocumentAgent
└─ Salvamento: exports/insumos/json/DFD_ultimo.json
    ↓
ETAPA 2: DFD (11 seções)
├─ Leitura do insumo
├─ Processamento com DocumentAgent especializado
├─ Revisão manual
└─ Salvamento: exports/dfd_data.json
    ↓
ETAPA 3: ETP (27 seções)
├─ Leitura do DFD
├─ Leitura do insumo original
├─ Processamento com ETPAgent
├─ Enriquecimento técnico
└─ Salvamento: exports/etp_data.json
    ↓
ETAPA 4: TR (9 seções)
├─ Leitura do DFD + ETP
├─ Processamento com TRAgent
├─ Consolidação de especificações
├─ Ajustes manuais
└─ Salvamento: exports/tr_data.json
    ↓
PRÓXIMO: EDITAL
```

### 6.2 Integração Automática de Dados

O sistema **propaga automaticamente** informações entre módulos:

| Dado | Origem | Propagado para |
|------|--------|----------------|
| **Objeto** | DFD | ETP, TR, Edital, Contrato |
| **Valor estimado** | DFD/ETP | TR, Edital, Contrato |
| **Prazo** | ETP | TR, Edital, Contrato |
| **Especificações** | ETP → TR | Edital, Contrato |
| **Responsável** | DFD | Todos os módulos |

**Benefício:** Não precisa digitar a mesma informação múltiplas vezes!

### 6.3 Alertas de Inconsistência

O módulo **⚠️ Alertas** detecta:

```
🚨 INCONSISTÊNCIA DETECTADA

Módulo: ETP
Campo: valor_estimado
Valor: R$ 850.000,00

Módulo: TR
Campo: valor_global
Valor: R$ 900.000,00

❌ Os valores diferem em R$ 50.000,00

Ação recomendada: Uniformizar o valor ou justificar a diferença
```

---

## 7. Casos Práticos

### 7.1 Caso 1: Aquisição de Material de Expediente

**Contexto:**
- Tipo: Aquisição de materiais
- Valor: R$ 45.000,00
- Prazo: Entrega imediata

**Fluxo:**
```
1. INSUMO: Upload de lista de necessidades (Excel → PDF)
2. DFD: Gerado em 15 minutos (justificativa simples)
3. ETP: Preenchimento das 27 seções em 30 minutos
4. TR: Adaptado de modelo "Aquisição de Materiais"
5. TOTAL: ~1 hora (vs. 8 horas manual)
```

### 7.2 Caso 2: Desenvolvimento de Software

**Contexto:**
- Tipo: Serviço especializado de TI
- Valor: R$ 2.500.000,00
- Prazo: 18 meses

**Fluxo:**
```
1. INSUMO: Documento técnico de 50 páginas
2. DFD: IA processa e estrutura necessidade tecnológica
3. ETP: Seção de especificações técnicas revisada por TI
4. TR: Modelo especializado em TI + ajustes customizados
5. TOTAL: ~4 horas (vs. 40 horas manual)
```

### 7.3 Caso 3: Renovação de Contrato

**Contexto:**
- Tipo: Renovação de serviço contínuo
- Valor: R$ 1.200.000,00
- Situação: Contrato anterior como referência

**Fluxo:**
```
1. INSUMO: Upload do contrato atual (PDF 80 páginas)
2. DFD: Gerado com justificativa de continuidade
3. ETP: Sistema aproveita 70% das especificações anteriores
4. TR: Ajustes apenas em valores e prazos
5. TOTAL: ~2 horas (vs. 20 horas manual)
```

---

## 📚 Próximos Passos

Você completou o aprendizado dos **Módulos de Planejamento**! 

Continue para:
- **Manual 03** – Módulos de Licitação (Edital, Validador, Contrato)
- **Manual 04** – Módulos de Governança (Alertas, Painéis)

---

## 📞 Suporte Técnico

**Dúvidas sobre planejamento de contratações?**

📧 saab-tech@tjsp.jus.br  
☎️ (11) XXXX-XXXX  
🕐 Segunda a Sexta, 9h-18h

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Manual 02/06 – Módulos de Planejamento*
