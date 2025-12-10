# 📘 Manual do Usuário – Projeto SAAB-Tech

## Manual 03: Módulos de Licitação - Edital e Validador

**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Tribunal de Justiça do Estado de São Paulo**  
**Secretaria de Administração e Abastecimento (SAAB)**

---


---

## 1. Visão Geral

### 1.1 O que são Módulos de Licitação?

Os **Módulos de Licitação** representam a **fase externa** da contratação pública, onde os documentos da fase interna são consolidados em **instrumentos convocatórios** (editais) e posteriormente em **contratos administrativos**.

```
📜 EDITAL → 🧩 VALIDADOR → 📜 CONTRATO
```

### 1.2 Integração com Fase Interna

Os módulos de licitação **herdam automaticamente** todos os dados da fase de planejamento:

```
DFD + ETP + TR  →  EDITAL  →  CONTRATO
```

**Benefícios:**
- ✅ Não precisa redigitar informações
- ✅ Consistência automática entre documentos
- ✅ Rastreabilidade completa
- ✅ Conformidade legal verificada

### 1.3 Base Legal

- **Lei Federal nº 14.133/2021** (Art. 40 a 57 - Licitações)
- **Decreto Federal nº 11.462/2023** (Regulamentação)
- **IN SEGES/ME nº 65/2021** (Minutas Padronizadas)
- **Jurisprudência TCE-SP** (Editais)

---

## 2. Módulo 05: Edital

### 2.1 O que é o Módulo Edital?

O **Módulo 06 - Edital** gera a **minuta do edital de licitação**, documento que convoca interessados e estabelece as regras da disputa. Ele consolida:
- Objeto da contratação (do DFD/ETP/TR)
- Especificações técnicas (do TR)
- Condições de participação
- Critérios de julgamento
- Obrigações contratuais

**Base Legal:** Art. 40, Lei 14.133/2021

### 2.2 Estrutura do Edital

O Edital no Projeto SAAB-Tech possui **12 campos estruturados**:

| Nº | Campo | Conteúdo |
|----|-------|----------|
| 1 | **Número do Edital** | Identificação oficial (Ex: 001/2025) |
| 2 | **Data de Publicação** | Data prevista para publicação |
| 3 | **Objeto** | Descrição do que será licitado |
| 4 | **Tipo de Licitação** | Pregão, Concorrência, etc. |
| 5 | **Critério de Julgamento** | Menor preço, melhor técnica, etc. |
| 6 | **Condições de Participação** | Quem pode participar |
| 7 | **Exigências de Habilitação** | Documentos obrigatórios |
| 8 | **Obrigações da Contratada** | Deveres da empresa vencedora |
| 9 | **Prazo de Execução** | Tempo para conclusão |
| 10 | **Fontes de Recursos** | Origem do orçamento |
| 11 | **Gestor/Fiscal** | Responsável pela fiscalização |
| 12 | **Observações Gerais** | Informações complementares |

### 2.3 Como Acessar

1. Na barra lateral, clique em **📜 Edital – Minuta do Edital**
2. Aguarde carregamento da interface

### 2.4 Interface do Módulo

#### **Detecção de Contexto**
```
✅ Contexto integrado detectado:
   • DFD: Disponível
   • ETP: Disponível
   • TR: Disponível
   
📊 O EditalAgent utilizará automaticamente estes dados
```

#### **Opções de Processamento**
```
┌────────────────────────────────────────────────┐
│ [🤖 Processar Edital com IA Especializada]    │
│ [📄 Carregar Insumo de Edital]                │
└────────────────────────────────────────────────┘
```

### 2.5 Formas de Gerar o Edital

#### **Opção 1: Processar com Contexto (Recomendado)**

**Pré-requisito:** Ter completado DFD, ETP e TR

**Passos:**
```
1. Acesse o módulo Edital
2. Sistema detecta contexto automaticamente
3. Clique em "🤖 Processar Edital com IA"
4. Aguarde processamento (~30-45 segundos)
5. Revise os 12 campos gerados
6. Ajuste conforme necessário
7. Salve e exporte
```

**Resultado:**
```
✅ Edital processado com sucesso!
📊 12 campos estruturados
💾 Salvo em: exports/edital_data.json
```

#### **Opção 2: Upload de Minuta Existente**

Se você tem uma minuta de edital de referência:

**Passos:**
```
1. Vá ao módulo 🔧 Insumos
2. Faça upload do arquivo (PDF/DOCX)
3. Selecione destino: "EDITAL"
4. Processe
5. Volte ao módulo Edital
6. Campos estarão preenchidos
7. Ajuste e complemente
```

#### **Opção 3: Preenchimento Manual**

Para controle total:
```
1. Acesse o módulo Edital
2. Role até o formulário
3. Preencha campo por campo
4. Use os campos de texto expandidos
5. Salve periodicamente
```

### 2.6 Passo a Passo Completo

#### **Exemplo: Continuando Serviços de Limpeza**

**Contexto Atual:**
```
✅ DFD completo (11 seções)
✅ ETP completo (27 seções)
✅ TR completo (9 seções)
📋 Objeto: Serviços de limpeza
💰 Valor: R$ 850.000,00/ano
⏱️ Prazo: 12 meses
```

**Passo 1: Verificar Contexto Integrado**
```
Ao acessar módulo Edital:

✅ Contexto detectado: DFD, ETP, TR

Sistema exibe resumo:
┌────────────────────────────────────────┐
│ Objeto: Serviços de limpeza           │
│ Valor Estimado: R$ 850.000,00         │
│ Prazo: 12 meses                       │
│ Unidade: Fórum de Guarulhos           │
└────────────────────────────────────────┘
```

**Passo 2: Processar com EditalAgent**
```
1. Clica em [🤖 Processar Edital com IA]
2. Aguarda processamento
3. Sistema:
   - Lê todos os dados de DFD/ETP/TR
   - Estrutura os 12 campos do edital
   - Aplica legislação (Lei 14.133/2021)
   - Inclui cláusulas obrigatórias
```

**Passo 3: Revisar Campos Gerados**

**Campo 1 - Número do Edital (gerado):**
```
[Sistema sugere]
Edital nº 001/2025 - Pregão Eletrônico

[Você ajusta]
Edital nº 090207/2025 - Pregão Eletrônico nº 123/2025
```

**Campo 3 - Objeto (consolidado do TR):**
```
Contratação de empresa especializada para prestação de serviços 
continuados de limpeza, conservação e higienização das dependências 
do Fórum da Comarca de Guarulhos/SP, incluindo fornecimento de 
materiais, equipamentos e mão de obra qualificada, pelo período 
de 12 (doze) meses, podendo ser prorrogado por até 60 (sessenta) 
meses, nos termos do Art. 107 da Lei Federal nº 14.133/2021.
```

**Campo 4 - Tipo de Licitação (você define):**
```
Modalidade: Pregão Eletrônico
Tipo: Menor Preço Global Anual
Amparo Legal: Art. 6º, L, e Art. 17, II, Lei 14.133/2021
Regime de Execução: Empreitada por Preço Global
```

**Campo 5 - Critério de Julgamento:**
```
MENOR PREÇO GLOBAL ANUAL

Será vencedora a proposta que apresentar o MENOR VALOR GLOBAL 
ANUAL para a totalidade dos serviços especificados no Termo de 
Referência, observados os padrões de qualidade e desempenho 
estabelecidos.

Critérios de desempate:
1º. Bens/serviços produzidos no Brasil
2º. Bens/serviços produzidos por empresas brasileiras
3º. Bens/serviços produzidos por ME/EPP
4º. Sorteio público
```

**Campo 7 - Exigências de Habilitação (crítico!):**
```
DOCUMENTAÇÃO OBRIGATÓRIA:

A) HABILITAÇÃO JURÍDICA:
   • Ato constitutivo, estatuto ou contrato social
   • Prova de inscrição no CNPJ
   • Decreto de autorização (se empresa estrangeira)

B) REGULARIDADE FISCAL E TRABALHISTA:
   • Certidão Negativa de Débitos Federais (RFB)
   • Certidão Negativa de Débitos Estaduais
   • Certidão Negativa de Débitos Municipais
   • CND INSS
   • FGTS - CRF
   • Certidão Negativa de Débitos Trabalhistas (TST)

C) QUALIFICAÇÃO TÉCNICA:
   • Atestado de capacidade técnica (mínimo 3 atestados)
   • Comprovação de execução de serviços similares
   • Prova de inscrição no CREA/CAU (se aplicável)

D) QUALIFICAÇÃO ECONÔMICO-FINANCEIRA:
   • Balanço patrimonial do último exercício
   • Certidão negativa de falência e recuperação judicial
   • Capital social mínimo de 10% do valor estimado

E) OUTRAS EXIGÊNCIAS:
   • Declaração de inexistência de fato impeditivo
   • Declaração de cumprimento do disposto no Art. 7º, XXXIII, CF
   • Declaração de elaboração independente de proposta
```

**Campo 8 - Obrigações da Contratada (do TR):**
```
SÃO OBRIGAÇÕES DA CONTRATADA:

1. Executar os serviços conforme especificações do Termo de Referência
2. Fornecer todos os materiais, equipamentos e produtos necessários
3. Disponibilizar mão de obra qualificada e em quantidade suficiente
4. Cumprir rigorosamente o cronograma estabelecido
5. Substituir funcionários faltosos em até 2 (duas) horas
6. Manter seguro de responsabilidade civil vigente
7. Cumprir toda a legislação trabalhista, previdenciária e tributária
8. Fornecer uniformes e EPIs aos funcionários
9. Realizar treinamentos periódicos da equipe
10. Atender chamados de emergência em até 2 (duas) horas
11. Apresentar relatório mensal de atividades
12. Manter preposto em tempo integral nas dependências
13. Reparar danos causados por seus funcionários
14. Manter canal de comunicação 24h (telefone/WhatsApp)
15. Aceitar fiscalização a qualquer tempo
```

**Campo 10 - Fontes de Recursos:**
```
DOTAÇÃO ORÇAMENTÁRIA:

Unidade Orçamentária: 02.01 - Poder Judiciário - TJSP
Programa de Trabalho: 02.122.0571.4256
Elemento de Despesa: 33.90.37 - Locação de Mão de Obra
Fonte de Recursos: 01 - Recursos Ordinários

Valor Orçado: R$ 850.000,00 (exercício 2026)

Observação: A despesa será empenhada conforme a execução dos 
serviços e disponibilidade orçamentária, em parcelas mensais.
```

**Passo 4: Ajustar Cronograma**

Você pode adicionar seção customizada:
```
CRONOGRAMA DO CERTAME:

• Publicação do Edital: 15/01/2026
• Prazo para impugnações: até 13/01/2026 (3 dias úteis antes)
• Sessão pública do Pregão: 20/01/2026 às 10h00
• Envio de propostas: até 20/01/2026 às 09h00
• Análise de habilitação: 20 a 22/01/2026
• Homologação: até 27/01/2026
• Assinatura do contrato: até 10/02/2026
• Início da execução: 17/02/2026
```

**Passo 5: Salvar e Exportar**
```
1. Clica em [💾 Salvar Edital]
   ✅ Edital salvo em exports/edital_data.json

2. Clica em [📤 Gerar DOCX do Edital]
   Download: Edital_090207_2025_Limpeza.docx
   
Estrutura do DOCX:
   - Capa institucional TJSP
   - Preâmbulo legal
   - 12 campos estruturados
   - Modelos de anexos (proposta, declarações)
   - 30-40 páginas formatadas
```

### 2.7 Modelos de Edital

O sistema oferece **modelos pré-configurados** por tipo de contratação:

| Tipo | Modelo | Características |
|------|--------|-----------------|
| **Serviços Contínuos** | Edital_Servicos_Continuos.docx | Limpeza, segurança, vigilância |
| **Materiais Permanentes** | Edital_Materiais.docx | Móveis, equipamentos |
| **Materiais de Consumo** | Edital_Consumo.docx | Material de expediente |
| **Tecnologia** | Edital_TI.docx | Software, hardware, suporte |
| **Obras** | Edital_Obras.docx | Construção, reforma |
| **Serviços Especializados** | Edital_Servicos_Especializados.docx | Consultoria, engenharia |

**Como usar modelos:**
```
1. No campo "Tipo de Licitação"
2. Sistema sugere modelo adequado
3. Aceita sugestão ou escolhe manualmente
4. Campos adaptam-se automaticamente
```

### 2.8 Cláusulas Obrigatórias (Lei 14.133/2021)

O EditalAgent **inclui automaticamente** todas as cláusulas obrigatórias:

#### **Cláusulas Essenciais (Art. 40):**
```
✅ Objeto da licitação
✅ Prazo e condições de execução
✅ Condições de participação
✅ Critérios de julgamento
✅ Sanções aplicáveis
✅ Prazos de pagamento
✅ Condições de garantia
✅ Critérios de aceitabilidade de preços
✅ Legislação aplicável
✅ Foro competente
```

#### **Cláusulas de Sustentabilidade:**
```
✅ Uso de produtos biodegradáveis (quando aplicável)
✅ Coleta seletiva de resíduos
✅ Economia de água e energia
✅ Gestão de resíduos
✅ Responsabilidade socioambiental
```

#### **Cláusulas Trabalhistas:**
```
✅ Cumprimento de legislação trabalhista
✅ Pagamento de salários em dia
✅ Recolhimento de encargos
✅ Fornecimento de EPIs
✅ Segurança do trabalho
```

### 2.9 Validações do Edital

O sistema verifica automaticamente:

| Validação | Critério | Alerta |
|-----------|----------|--------|
| **Número do edital** | Não pode ser "N/A" ou genérico | 🚨 Crítico |
| **Objeto vazio** | Campo obrigatório | 🚨 Crítico |
| **Tipo de licitação** | Deve ser válido (Pregão, Concorrência, etc.) | 🚨 Alto |
| **Critério de julgamento** | Deve estar definido | 🚨 Alto |
| **Exigências habilitação** | Mínimo 5 itens | ⚠️ Médio |
| **Obrigações contratada** | Mínimo 5 obrigações | ⚠️ Médio |
| **Prazo execução** | Não pode ser indefinido | ⚠️ Alto |

### 2.10 Checklist Pré-Publicação

Antes de publicar o edital, verifique:

- [ ] **Número do edital** está correto e único?
- [ ] **Objeto** está claro e específico?
- [ ] **Valor estimado** está atualizado? (pode ser sigiloso)
- [ ] **Tipo de licitação** é adequado ao objeto?
- [ ] **Prazo** para propostas é suficiente (mínimo 8 dias úteis)?
- [ ] **Habilitação** não é restritiva demais?
- [ ] **Especificações** não direcionam para marca específica?
- [ ] **Recursos orçamentários** estão empenhados?
- [ ] **Minuta de contrato** está anexada?
- [ ] **Modelos** de declarações estão anexados?
- [ ] **Revisão jurídica** foi realizada?

---

## 3. Módulo 06: Validador

### 3.1 O que é o Validador de Editais?

O **Módulo 07 - Validador de Editais** realiza **análise automática de conformidade legal** da minuta do edital contra:
- Lei Federal nº 14.133/2021
- Checklist institucional TJSP
- Jurisprudência do TCE-SP
- Boas práticas de licitação

**Resultado:** Score de conformidade + relatório detalhado

### 3.2 O que o Validador Analisa?

#### **Análise Estrutural**
```
✅ Presença de cláusulas obrigatórias
✅ Sequência lógica das seções
✅ Completude dos campos
✅ Formatação adequada
```

#### **Análise de Conformidade Legal**
```
✅ Tipo de licitação adequado ao objeto
✅ Critério de julgamento correto
✅ Prazos mínimos respeitados
✅ Exigências de habilitação legais
✅ Sanções proporcionais
```

#### **Análise de Riscos**
```
⚠️ Especificações excessivamente restritivas
⚠️ Exigências desproporcionais
⚠️ Direcionamento para fornecedor específico
⚠️ Prazos inadequados
⚠️ Valores incompatíveis com mercado
```

### 3.3 Como Acessar

1. Na barra lateral, clique em **🧩 Validador de Editais**
2. Aguarde carregamento da interface

### 3.4 Interface do Módulo

#### **Abas de Entrada**
```
┌─────────────────────────────────────────┐
│  📎 Edital Gerado  │  📄 Upload        │
└─────────────────────────────────────────┘
```

**Aba 1: Edital Gerado (Recomendado)**
- Usa o edital processado no Módulo 06
- Integração automática

**Aba 2: Upload de Arquivo**
- Para editais externos (PDF/DOCX/TXT)
- Processar editais de terceiros

### 3.5 Formas de Validar

#### **Opção 1: Validar Edital Gerado (Automático)**

**Pré-requisito:** Ter processado edital no Módulo 06

**Passos:**
```
1. Acesse o módulo Validador
2. Clique na aba "📎 Edital Gerado"
3. Sistema detecta edital automaticamente:
   ✅ Edital detectado: Nº 090207/2025
4. Selecione tipo de contratação:
   [▼ Serviços Contínuos        ]
5. Clique em "🔍 EXECUTAR VALIDAÇÃO COMPLETA"
6. Aguarde análise (~15-30 segundos)
```

**Resultado:**
```
✅ VALIDAÇÃO CONCLUÍDA

SCORE DE CONFORMIDADE: 87/100 (BOM)

┌─────────────────────────────────────────┐
│ 📊 RESUMO DA VALIDAÇÃO                  │
├─────────────────────────────────────────┤
│ ✅ Aprovado: 24 itens                   │
│ ⚠️ Alertas: 3 itens                     │
│ ❌ Críticos: 0 itens                    │
└─────────────────────────────────────────┘
```

#### **Opção 2: Upload de Arquivo Externo**

Para validar edital existente (de outra unidade, edital antigo, etc.):

**Passos:**
```
1. Acesse Validador
2. Clique na aba "📄 Upload de Arquivo"
3. Clique em "Browse files"
4. Selecione o arquivo (PDF/DOCX/TXT)
5. Aguarde extração de texto
6. Selecione tipo de contratação
7. Clique em "🔍 EXECUTAR VALIDAÇÃO"
```

### 3.6 Passo a Passo Completo

#### **Exemplo: Validando Edital de Limpeza**

**Passo 1: Acessar Validador com Edital Gerado**
```
1. Acessa módulo 🧩 Validador
2. Sistema detecta edital:
   ✅ Edital Nº 090207/2025
   📄 Objeto: Serviços de limpeza
   💰 Valor: R$ 850.000,00
```

**Passo 2: Selecionar Tipo de Contratação**
```
Tipo de contratação:
[▼ Serviços Contínuos        ]

Opções:
• Serviços Contínuos
• Materiais (Consumo)
• Materiais (Permanentes)
• Tecnologia da Informação
• Obras e Reformas
• Consultoria/Serviços Especializados
```

**Passo 3: Executar Validação**
```
Clica em: [🔍 EXECUTAR VALIDAÇÃO COMPLETA]

Sistema processa:
[████████████████░░░░] 80%
Analisando cláusulas obrigatórias...
```

**Passo 4: Analisar Resultado Geral**
```
═══════════════════════════════════════
   RELATÓRIO DE VALIDAÇÃO DE EDITAL
═══════════════════════════════════════

Edital: 090207/2025 - Pregão Eletrônico
Objeto: Serviços de limpeza - Fórum Guarulhos
Data da Validação: 10/12/2025 15:42

───────────────────────────────────────
📊 SCORE DE CONFORMIDADE: 87/100
───────────────────────────────────────

Classificação: BOM ✅
Status: APTO para publicação com ressalvas

┌───────────────────────────────────┐
│ DISTRIBUIÇÃO DOS RESULTADOS       │
├───────────────────────────────────┤
│ ✅ Conformes: 24 itens (80%)      │
│ ⚠️ Alertas: 3 itens (10%)         │
│ ❌ Críticos: 0 itens (0%)         │
│ ℹ️ Informativos: 3 itens (10%)    │
└───────────────────────────────────┘
```

**Passo 5: Revisar Itens Detalhados**

**✅ ITENS CONFORMES (exemplos):**
```
✅ Objeto da licitação claramente definido
   → Descrição completa e precisa
   
✅ Tipo de licitação adequado ao objeto
   → Pregão Eletrônico (Lei 14.133/2021, Art. 17, II)
   
✅ Critério de julgamento especificado
   → Menor preço global anual
   
✅ Prazo para propostas adequado
   → 8 dias úteis (atende mínimo legal)
   
✅ Exigências de habilitação legais
   → Todas previstas na Lei 14.133/2021
   
✅ Recursos administrativos previstos
   → Prazos e procedimentos conformes
```

**⚠️ ALERTAS (requerem atenção):**
```
⚠️ ALERTA #1: Exigência de atestados técnicos
   Categoria: Habilitação
   Severidade: MÉDIA
   
   Problema detectado:
   O edital exige "mínimo de 3 atestados de capacidade 
   técnica". Isso pode ser considerado restritivo.
   
   Recomendação:
   Considere aceitar 1 atestado que comprove execução de 
   50% do valor estimado, conforme Art. 67, II, Lei 14.133/2021.
   
   Base Legal:
   Lei 14.133/2021, Art. 67, §2º - As exigências de 
   habilitação não devem restringir a competitividade.
   
───────────────────────────────────────

⚠️ ALERTA #2: Prazo de execução
   Categoria: Prazo
   Severidade: MÉDIA
   
   Problema detectado:
   Prazo de execução de 12 meses pode ser curto considerando
   o porte do Fórum (45.000m²).
   
   Recomendação:
   Verifique se 12 meses é adequado ou considere estender
   para 24 meses com opção de prorrogação.
   
───────────────────────────────────────

⚠️ ALERTA #3: Garantia contratual
   Categoria: Garantia
   Severidade: BAIXA
   
   Problema detectado:
   Percentual de garantia não foi especificado.
   
   Recomendação:
   Defina percentual entre 2% e 5% do valor contratual
   conforme Art. 96, Lei 14.133/2021.
```

**ℹ️ INFORMATIVOS:**
```
ℹ️ Cláusula de sustentabilidade presente
   O edital inclui critérios de sustentabilidade ambiental
   conforme Art. 11, II, d, Lei 14.133/2021.
   
ℹ️ Preferência para ME/EPP configurada
   Margem de preferência e cota reservada estão previstas.
   
ℹ️ Minuta de contrato anexada
   A minuta de contrato está presente como anexo do edital.
```

**Passo 6: Exportar Relatório**
```
Opções de exportação:

[📄 Exportar PDF]  [📊 Exportar Excel]  [📋 Copiar Resumo]

Download: Relatorio_Validacao_Edital_090207_2025.pdf

Conteúdo do PDF:
• Capa institucional TJSP
• Score e resumo executivo
• Análise item por item (30+ verificações)
• Recomendações detalhadas
• Base legal de cada item
• Checklist de correções
• 10-15 páginas
```

### 3.7 Tipos de Validação

O Validador realiza **4 tipos de análise**:

#### **1. Validação Estrutural**
```
CHECKLIST ESTRUTURAL (12 itens)

✅ Preâmbulo com identificação do órgão
✅ Número e modalidade do edital
✅ Objeto claramente definido
✅ Condições de participação
✅ Documentação de habilitação
✅ Proposta de preços
✅ Critério de julgamento
✅ Recursos administrativos
✅ Sanções administrativas
✅ Anexos obrigatórios (minuta contrato, modelos)
✅ Local, data e assinatura
✅ Foro competente
```

#### **2. Validação Legal (Lei 14.133/2021)**
```
CONFORMIDADE COM LEI 14.133/2021 (15 itens)

✅ Modalidade adequada ao objeto (Art. 17)
✅ Critério de julgamento legal (Art. 33 a 35)
✅ Prazos mínimos respeitados (Art. 54 a 57)
✅ Exigências de habilitação legais (Art. 62 a 70)
✅ Garantia contratual conforme (Art. 96)
✅ Sanções previstas em lei (Art. 155 a 163)
✅ Recursos cabíveis (Art. 165 a 168)
✅ Condições de participação (Art. 14 a 16)
✅ Critérios de aceitabilidade (Art. 59)
✅ Prazo de pagamento (Art. 98)
⚠️ Critérios de sustentabilidade (Art. 11, II, d)
✅ Preferência ME/EPP (LC 123/2006)
✅ Reserva de cota (Art. 48 a 50)
✅ Julgamento objetivo (Art. 33, §1º)
✅ Publicidade e transparência (Art. 52)
```

#### **3. Validação de Riscos**
```
ANÁLISE DE RISCOS JURÍDICOS (8 categorias)

✅ Especificações técnicas
   → Não direcionam para marca/fornecedor específico
   
⚠️ Exigências de habilitação
   → 3 atestados pode ser restritivo
   
✅ Prazos e condições
   → Adequados e razoáveis
   
✅ Sanções
   → Proporcionais e legais
   
✅ Critério de julgamento
   → Objetivo e mensurável
   
✅ Valores de referência
   → Compatíveis com pesquisa de preços
   
⚠️ Garantias exigidas
   → Percentual não especificado
   
✅ Condições de pagamento
   → Adequadas
```

#### **4. Validação Institucional (TJSP)**
```
CHECKLIST INSTITUCIONAL TJSP (10 itens)

✅ Numeração conforme padrão TJSP
✅ Referência a normas internas SAAB
✅ Dotação orçamentária especificada
✅ Gestor/Fiscal nomeado
✅ Formatação conforme manual TJSP
✅ Cláusulas trabalhistas incluídas
✅ Critérios de sustentabilidade
✅ Acessibilidade (se aplicável)
✅ Assinatura digital prevista
✅ Publicação no DJE prevista
```

### 3.8 Scores de Conformidade

O sistema classifica o edital em **5 níveis**:

| Score | Classificação | Status | Ação Recomendada |
|-------|---------------|--------|------------------|
| **90-100** | 🟢 EXCELENTE | Apto para publicação | Publicar imediatamente |
| **80-89** | 🟡 BOM | Apto com ressalvas | Corrigir alertas menores |
| **70-79** | 🟠 REGULAR | Necessita ajustes | Corrigir antes de publicar |
| **60-69** | 🔴 INSUFICIENTE | Não recomendado | Revisar completamente |
| **0-59** | ⛔ CRÍTICO | Não apto | Refazer o edital |

### 3.9 Checklist Institucional TJSP

O sistema usa checklist específico do TJSP com **50+ itens**:

```yaml
# Trecho do arquivo: knowledge/edital_checklist.yml

categorias:
  identificacao:
    - item: Órgão licitante identificado
      peso: critico
    - item: Número do edital único e sequencial
      peso: critico
    - item: Modalidade de licitação especificada
      peso: critico
      
  objeto:
    - item: Objeto claro e preciso
      peso: critico
    - item: Não direciona para marca específica
      peso: alto
    - item: Especificações mensuráveis
      peso: alto
      
  habilitacao:
    - item: Exigências previstas em lei
      peso: critico
    - item: Não são excessivamente restritivas
      peso: alto
    - item: Documentos listados claramente
      peso: medio
```

### 3.10 Casos Especiais de Validação

#### **Dispensa de Licitação**
```
Para editais de dispensa (Art. 75, Lei 14.133/2021):

• Valida se o valor está dentro do limite legal
• Verifica se a justificativa é adequada
• Confirma publicação no Portal Nacional
• Analisa fundamentação legal
```

#### **Licitações Internacionais**
```
Verificações adicionais:

• Conversão de moeda estrangeira
• Regras de importação
• Garantias internacionais
• Idioma dos documentos
```

#### **Pregão Eletrônico**
```
Itens específicos de pregão:

• Plataforma oficial (Comprasnet)
• Horário da sessão pública
• Tempo para lances
• Critérios de desempate
```

---

## 4. Fluxo Integrado

### 4.1 Visão do Fluxo Edital + Validação

```
MÓDULO EDITAL
├─ Processa contexto (DFD+ETP+TR)
├─ EditalAgent estrutura 12 campos
├─ Inclusão de cláusulas obrigatórias
├─ Geração de minuta DOCX
└─ Salva em exports/edital_data.json
      ↓
MÓDULO VALIDADOR
├─ Lê edital_data.json
├─ Executa 4 tipos de validação
├─ Gera score de conformidade
├─ Identifica alertas e riscos
└─ Exporta relatório PDF
      ↓
CORREÇÕES (se necessário)
├─ Volta ao Módulo Edital
├─ Ajusta campos conforme alertas
├─ Salva nova versão
└─ Valida novamente
      ↓
PUBLICAÇÃO
```

### 4.2 Iteração de Melhorias

**Ciclo recomendado:**
```
1. Gera edital no Módulo 06
2. Valida no Módulo 07
3. Analisa score e alertas
4. Volta ao Módulo 06 e corrige
5. Salva e valida novamente
6. Repete até score ≥ 85
7. Publica
```

**Exemplo de iteração:**
```
ITERAÇÃO 1:
Score: 78/100 (REGULAR)
Alertas: 5 itens
Ação: Corrigir exigências de habilitação

ITERAÇÃO 2:
Score: 85/100 (BOM)
Alertas: 2 itens
Ação: Especificar garantia contratual

ITERAÇÃO 3:
Score: 92/100 (EXCELENTE)
Alertas: 0 itens críticos
Ação: PUBLICAR ✅
```

---

## 5. Casos Práticos

### 5.1 Caso 1: Pregão Eletrônico - Material de Expediente

**Contexto:**
- Tipo: Aquisição
- Valor: R$ 85.000,00
- Modalidade: Pregão Eletrônico

**Fluxo:**
```
1. EDITAL:
   • Processa DFD+ETP+TR (1 hora total)
   • Gera edital em 10 minutos
   • 12 campos preenchidos automaticamente

2. VALIDADOR:
   • Score inicial: 81/100
   • Alerta: Especificações muito detalhadas
   • Correção: Simplifica especificações
   • Score final: 89/100 ✅

3. RESULTADO:
   • Tempo total: ~2 horas
   • Vs. manual: ~12 horas
   • Economia: 83%
```

### 5.2 Caso 2: Concorrência - Obra de Reforma

**Contexto:**
- Tipo: Obra pública
- Valor: R$ 3.500.000,00
- Modalidade: Concorrência

**Fluxo:**
```
1. EDITAL:
   • Usa modelo "Obras e Reformas"
   • Inclui projetos técnicos como anexos
   • Adiciona cláusulas específicas de engenharia
   
2. VALIDADOR:
   • Score inicial: 74/100
   • Alertas: 4 críticos
     - Prazo insuficiente para propostas
     - Exigência de CAU não fundamentada
     - Falta orçamento analítico
     - Garantia contratual acima do limite
   • Correções realizadas
   • Score final: 91/100 ✅

3. REVISÃO JURÍDICA:
   • Exporta relatório do validador
   • Assessor jurídico revisa
   • Aprova publicação
```

### 5.3 Caso 3: Dispensa de Licitação - Emergência

**Contexto:**
- Tipo: Serviço emergencial
- Valor: R$ 180.000,00
- Fundamento: Art. 75, VIII (emergência)

**Fluxo:**
```
1. EDITAL SIMPLIFICADO:
   • Justificativa de emergência detalhada
   • Prazo reduzido
   • Menor número de exigências
   
2. VALIDADOR:
   • Valida fundamentação legal
   • Confirma valor dentro do limite
   • Verifica urgência comprovada
   • Score: 87/100 ✅
   
3. PUBLICAÇÃO IMEDIATA:
   • Portal Nacional de Contratações
   • DJE (Diário de Justiça Eletrônico)
   • Site TJSP
```

---

## 📚 Próximos Passos

Continue sua jornada de aprendizado:

- **Manual 04** – Módulo de Contrato Administrativo
- **Manual 04** – Módulos de Governança (Alertas, Painéis)
- **Manual 05** – Módulos Avançados

---

## 📞 Suporte Técnico

**Dúvidas sobre editais e validação?**

📧 saab-tech@tjsp.jus.br  
☎️ (11) XXXX-XXXX  
🕐 Segunda a Sexta, 9h-18h

**Suporte Jurídico:**  
📧 assessoria.juridica@tjsp.jus.br

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Manual 03/07 – Módulos de Licitação: Edital e Validador*
