# 📘 Manual do Usuário – Projeto SAAB-Tech

## Manual 03B: Módulo de Contrato Administrativo

**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Tribunal de Justiça do Estado de São Paulo**  
**Secretaria de Administração e Abastecimento (SAAB)**

---

## 📑 Índice

1. [Visão Geral do Módulo Contrato](#1-visão-geral)
2. [Estrutura do Contrato (20 Campos)](#2-estrutura-do-contrato)
3. [Como Usar o Módulo](#3-como-usar-o-módulo)
4. [Formas de Gerar o Contrato](#4-formas-de-gerar)
5. [Passo a Passo Completo](#5-passo-a-passo-completo)
6. [Cláusulas Contratuais](#6-cláusulas-contratuais)
7. [Validações e Alertas](#7-validações-e-alertas)
8. [Casos Práticos](#8-casos-práticos)

---

## 1. Visão Geral

### 1.1 O que é o Módulo Contrato?

O **Módulo 08 - Contrato Administrativo** é o **estágio final** da jornada de contratação pública no Projeto SAAB-Tech. Ele consolida **todos os dados** dos módulos anteriores para gerar um contrato administrativo completo e robusto.

**Base Legal:** Art. 89 a 111, Lei 14.133/2021

### 1.2 Integração Total

O módulo de Contrato **integra automaticamente** dados de:

```
DFD + ETP + TR + EDITAL  →  CONTRATO
```

**O que é integrado:**
- ✅ **Objeto** (do DFD/ETP/TR)
- ✅ **Valor global** (do ETP/TR/Edital)
- ✅ **Prazo de execução** (do ETP/TR)
- ✅ **Especificações técnicas** (do TR)
- ✅ **Obrigações** (do TR/Edital)
- ✅ **Forma de pagamento** (do TR)
- ✅ **Sanções** (do TR/Edital)
- ✅ **Responsáveis** (de todos os módulos)

### 1.3 ContratoAgent Especializado

O **ContratoAgent** é o agente de IA mais avançado do sistema:

```python
CAPACIDADES DO CONTRATOAGENT:
├─ Extração de 20 campos estruturados
├─ Enriquecimento AGRESSIVO de dados
├─ Integração com contexto completo (DFD+ETP+TR+Edital)
├─ Geração de 15 cláusulas contratuais
├─ Formatação institucional TJSP
└─ Exportação DOCX profissional
```

### 1.4 Diferencial da Versão 2025.1

**❌ Versão Anterior:**
- Campos com defaults hardcoded
- Prompt genérico para IA
- Formulário com valores pré-preenchidos
- DOCX simples sem formatação

**✅ Versão 2025.1:**
- Campos limpos até processamento
- ContratoAgent especializado
- Enriquecimento agressivo com contexto
- DOCX profissional (cores TJSP, 15 cláusulas)
- Integração completa com Insumos

---

## 2. Estrutura do Contrato

### 2.1 Os 20 Campos Obrigatórios

O contrato administrativo possui **20 campos padronizados**:

#### **Grupo 1: Identificação (5 campos)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 1 | **numero_contrato** | Número identificador | "CONT-001/2026" |
| 2 | **data_assinatura** | Data de formalização | "15/02/2026" |
| 3 | **partes_contratante** | CONTRATANTE (TJSP) | "Tribunal de Justiça de SP" |
| 4 | **partes_contratada** | CONTRATADA (empresa) | "Empresa XYZ Ltda, CNPJ..." |
| 5 | **objeto** | O que será contratado | "Serviços de limpeza..." |

#### **Grupo 2: Fundamentação Legal (1 campo)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 6 | **fundamentacao_legal** | Base jurídica | "Lei 14.133/2021, Art. 89..." |

#### **Grupo 3: Prazos e Vigência (2 campos)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 7 | **vigencia** | Período de validade | "12 meses a contar da assinatura" |
| 8 | **prazo_execucao** | Tempo para conclusão | "Início imediato, 12 meses" |

#### **Grupo 4: Valores e Pagamento (3 campos)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 9 | **valor_global** | Valor total | "R$ 850.000,00" |
| 10 | **forma_pagamento** | Condições de pagamento | "Mensal, até 5º dia útil..." |
| 11 | **reajuste** | Regras de reajuste | "Após 12 meses, IPCA..." |

#### **Grupo 5: Garantias e Seguros (1 campo)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 12 | **garantia_contratual** | Garantia exigida | "5% do valor, caução ou seguro" |

#### **Grupo 6: Obrigações (2 campos)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 13 | **obrigacoes_contratada** | Deveres da empresa | "15 obrigações detalhadas" |
| 14 | **obrigacoes_contratante** | Deveres do TJSP | "8 obrigações detalhadas" |

#### **Grupo 7: Gestão Contratual (1 campo)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 15 | **fiscalizacao** | Responsável e regras | "Servidor designado, inspeções..." |

#### **Grupo 8: Penalidades e Rescisão (2 campos)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 16 | **penalidades** | Sanções aplicáveis | "Advertência, multa, suspensão..." |
| 17 | **rescisao** | Causas de rescisão | "Motivos dos Arts. 137 e 138" |

#### **Grupo 9: Alterações e Disposições Finais (3 campos)**

| Nº | Campo | Descrição | Exemplo |
|----|-------|-----------|---------|
| 18 | **alteracoes** | Possibilidade de aditivos | "Acréscimo até 25%..." |
| 19 | **foro** | Jurisdição competente | "Comarca de São Paulo/SP" |
| 20 | **disposicoes_gerais** | Cláusulas complementares | "Legislação aplicável, publicação..." |

### 2.2 Campos vs. Cláusulas

**Importante distinguir:**

```
CAMPOS (20)           →  Dados estruturados para processamento
                          (salvos em JSON)
                          
CLÁUSULAS (15)        →  Seções do contrato DOCX
                          (geradas a partir dos campos)
```

**Mapeamento:**
```
Campo "objeto"               → Cláusula 1ª (DO OBJETO)
Campo "valor_global"         → Cláusula 3ª (DO VALOR)
Campo "obrigacoes_contratada" → Cláusula 6ª (DAS OBRIGAÇÕES DA CONTRATADA)
```

---

## 3. Como Usar o Módulo

### 3.1 Como Acessar

1. Na barra lateral, clique em **📜 Contrato**
2. Aguarde carregamento da interface

### 3.2 Interface do Módulo

#### **Detecção Automática de Contexto**

```
┌────────────────────────────────────────────┐
│  📎 CONTEXTO DETECTADO                     │
├────────────────────────────────────────────┤
│  ✅ DFD: Disponível                        │
│  ✅ ETP: Disponível                        │
│  ✅ TR: Disponível                         │
│  ✅ Edital: Disponível                     │
├────────────────────────────────────────────┤
│  📊 4/4 módulos anteriores disponíveis     │
│                                            │
│  💡 O ContratoAgent utilizará todos estes  │
│     dados para enriquecer o contrato       │
└────────────────────────────────────────────┘
```

#### **Métricas do Contexto**

```
┌──────────┬──────────┬──────────┬──────────┐
│   DFD    │   ETP    │   TR     │  Edital  │
│  ✅ OK   │  ✅ OK   │  ✅ OK   │  ✅ OK   │
└──────────┴──────────┴──────────┴──────────┘
```

#### **Seções de Entrada**

**Seção 1: Upload de Insumo (opcional)**
```
┌────────────────────────────────────────────┐
│  📤 Upload de Insumo (opcional)            │
│                                            │
│  Opções:                                   │
│  • Upload direto de minuta (PDF/DOCX/TXT) │
│  • Processar apenas com contexto           │
│  • Preencher manualmente                   │
│                                            │
│  [📁 Envie um arquivo de referência...]   │
└────────────────────────────────────────────┘
```

**Seção 2: Botões de Processamento**
```
┌────────────────────────┬───────────────────┐
│  [🤖 Processar Insumo  │  [🧠 Gerar do    │
│   com ContratoAgent]   │   Contexto]       │
└────────────────────────┴───────────────────┘
```

**Seção 3: Formulário com 20 Campos**
```
┌────────────────────────────────────────────┐
│  📋 CAMPOS DO CONTRATO                     │
│                                            │
│  1. Número do Contrato: [____________]     │
│  2. Data de Assinatura: [__/__/____]       │
│  3. Objeto: [________________________]     │
│  ...                                       │
│  20. Disposições Gerais: [___________]     │
└────────────────────────────────────────────┘
```

---

## 4. Formas de Gerar

### 4.1 Opção 1: Processar com Contexto Completo (Recomendado)

**Quando usar:**
- Você completou DFD, ETP, TR e Edital
- Quer aproveitar todos os dados já preenchidos
- Contratação padrão (não tem minuta de referência)

**Pré-requisitos:**
```
✅ DFD salvo
✅ ETP salvo
✅ TR salvo
✅ Edital salvo (opcional, mas recomendado)
```

**Passos:**
```
1. Acesse módulo Contrato
2. Verifique detecção de contexto (4/4 módulos)
3. Clique em [🧠 Gerar Contrato do Contexto]
4. Aguarde processamento (~30-40 segundos)
5. Revise os 20 campos preenchidos
6. Ajuste conforme necessário
7. Salve e exporte DOCX
```

**O que o ContratoAgent faz:**
```
1. Lê dfd_data.json completo
2. Lê etp_data.json completo
3. Lê tr_data.json completo
4. Lê edital_data.json completo
5. Consolida todas as informações
6. Enriquece cada campo com dados integrados
7. Gera estrutura contratual completa
8. Preenche os 20 campos automaticamente
```

### 4.2 Opção 2: Upload de Minuta + Contexto

**Quando usar:**
- Tem minuta de contrato de referência
- Quer usar modelo de contrato anterior
- Renovação de contrato existente

**Passos:**
```
1. Acesse módulo Contrato
2. Faça upload do arquivo de referência
3. Clique em [🤖 Processar Insumo com ContratoAgent]
4. Sistema:
   - Extrai dados do arquivo
   - Integra com contexto (DFD/ETP/TR/Edital)
   - Enriquece com dados dos módulos anteriores
5. Revise e ajuste
6. Salve e exporte
```

**Vantagem:**
- Aproveita estrutura de contrato existente
- Enriquece com dados atualizados dos módulos
- Combina o melhor dos dois mundos

### 4.3 Opção 3: Upload via Insumos

**Quando usar:**
- Tem arquivo de contrato para processar primeiro
- Quer processar separadamente antes de ajustar

**Passos:**
```
1. Vá ao módulo 🔧 Insumos
2. Faça upload do arquivo de contrato
3. Selecione destino: "CONTRATO"
4. Processe
5. Volte ao módulo Contrato
6. Campos estarão preenchidos
7. Revise e exporte
```

### 4.4 Opção 4: Preenchimento Manual

**Quando usar:**
- Contrato muito específico
- Não tem documentos anteriores
- Quer controle total

**Passos:**
```
1. Acesse módulo Contrato
2. Role até o formulário
3. Preencha os 20 campos manualmente
4. Use campos de texto expandidos
5. Salve periodicamente
6. Clique em [💾 Salvar Campos Editados Manualmente]
7. Exporte DOCX
```

---

## 5. Passo a Passo Completo

### 5.1 Cenário: Finalizando Contratação de Limpeza

**Contexto Atual:**
```
✅ DFD completo (Fórum Guarulhos)
✅ ETP completo (27 seções, R$ 850k)
✅ TR completo (9 seções, especificações detalhadas)
✅ Edital validado (Score 92/100)
✅ Licitação homologada
📋 Vencedor: Empresa Clean Tech Ltda, CNPJ 12.345.678/0001-90
```

### 5.2 Passo 1: Acessar Módulo Contrato

```
1. Clica em [📜 Contrato] na barra lateral
2. Sistema carrega interface
3. Detecta automaticamente:

┌────────────────────────────────────────────┐
│  📎 Contexto integrado: DFD, ETP, TR, Edital│
│  📊 4/4 módulos disponíveis                │
│                                            │
│  Dados detectados:                         │
│  • Objeto: Serviços de limpeza            │
│  • Valor: R$ 850.000,00                   │
│  • Prazo: 12 meses                        │
│  • Unidade: Fórum de Guarulhos            │
└────────────────────────────────────────────┘
```

### 5.3 Passo 2: Gerar com Contexto Completo

```
1. Clica em [🧠 Gerar Contrato do Contexto]

2. Sistema exibe progresso:
   [████████████████░░░░] 80%
   Processando com ContratoAgent...
   
3. Aguarda ~35 segundos

4. Resultado:
   ✅ Contrato processado com sucesso!
   📊 20 campos extraídos e estruturados
   💾 Salvo em: exports/contrato_data.json
```

### 5.4 Passo 3: Revisar Campos Gerados

#### **Grupo 1: Identificação**

**Campo 1 - Número do Contrato (gerado):**
```
[SISTEMA SUGERE]
CONT-001/2026

[VOCÊ AJUSTA PARA PADRÃO TJSP]
Contrato SAAB-TJSP nº 090207/2026
Processo Administrativo nº 2025.00.123456-7
```

**Campo 2 - Data de Assinatura:**
```
[GERADO]
15/02/2026

[CONFIRMADO]
✅ Data prevista para assinatura
```

**Campo 3 - Partes Contratante:**
```
[GERADO AUTOMATICAMENTE]
TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO
CNPJ: 51.357.770/0001-50
Representado por: Desembargador [Nome]
Cargo: Presidente do Tribunal de Justiça
Endereço: Praça da Sé, s/nº - Centro - São Paulo/SP
CEP: 01018-010
```

**Campo 4 - Partes Contratada (você preenche após licitação):**
```
[VOCÊ ADICIONA DADOS DO VENCEDOR]
CLEAN TECH SERVIÇOS DE LIMPEZA LTDA
CNPJ: 12.345.678/0001-90
Representante Legal: João da Silva
CPF: 123.456.789-00
Endereço: Rua das Flores, 1000 - Guarulhos/SP
CEP: 07010-000
Telefone: (11) 1234-5678
E-mail: contato@cleantech.com.br
```

**Campo 5 - Objeto (consolidado de DFD/ETP/TR):**
```
[GERADO COM INTEGRAÇÃO COMPLETA]
Contratação de empresa especializada para prestação de serviços 
continuados de limpeza, conservação e higienização das dependências 
do Fórum da Comarca de Guarulhos/SP, com fornecimento de todos os 
materiais, equipamentos, produtos e mão de obra especializada 
necessários, pelo período de 12 (doze) meses, com possibilidade de 
prorrogação por até 60 (sessenta) meses, nos termos do Art. 107 da 
Lei Federal nº 14.133/2021.

Área de abrangência: 45.000m² (quarenta e cinco mil metros quadrados)
Frequência: Diária (segunda a sexta-feira)
Turnos: Diurno (7h-16h) e noturno (18h-22h)
```

#### **Grupo 2: Fundamentação Legal**

**Campo 6 - Fundamentação Legal (gerado automaticamente):**
```
[COMPLETO E PRECISO]
O presente contrato é regido pela Lei Federal nº 14.133, de 1º de 
abril de 2021 (Lei de Licitações e Contratos Administrativos), 
Decreto Federal nº 11.462/2023, Lei Complementar nº 123/2006 
(Estatuto da Micro e Pequena Empresa), além das disposições 
estabelecidas no Edital de Pregão Eletrônico nº 123/2025, seus 
anexos, proposta da CONTRATADA e demais normas aplicáveis.

Amparo Licitatório:
• Pregão Eletrônico nº 123/2025
• Processo Administrativo nº 2025.00.123456-7
• Homologação em: 05/02/2026
• Adjudicação em: 06/02/2026
```

#### **Grupo 3: Prazos e Vigência**

**Campo 7 - Vigência:**
```
[GERADO DO ETP/TR]
12 (doze) meses, contados a partir da data de assinatura deste 
contrato, com possibilidade de prorrogação por iguais e sucessivos 
períodos, até o limite de 60 (sessenta) meses, mediante interesse 
das partes e desde que observadas as disposições do Art. 107 da 
Lei nº 14.133/2021.

Início da vigência: 15/02/2026
Término previsto: 14/02/2027
Prorrogação máxima até: 14/02/2031
```

**Campo 8 - Prazo de Execução:**
```
[DETALHADO]
Prazo de mobilização: 5 (cinco) dias úteis a contar da assinatura
Início efetivo dos serviços: 20/02/2026
Execução: Contínua durante toda a vigência contratual
Horários: Conforme especificado no Termo de Referência (Anexo I)
```

#### **Grupo 4: Valores e Pagamento**

**Campo 9 - Valor Global:**
```
[DO ETP/TR/EDITAL]
R$ 850.000,00 (oitocentos e cinquenta mil reais) anuais

Detalhamento:
• Valor mensal: R$ 70.833,33
• Valor diário: R$ 2.361,11

Composição de custos:
├─ Mão de obra (25 funcionários): R$ 600.000,00 (70,6%)
├─ Materiais e produtos: R$ 150.000,00 (17,6%)
├─ Equipamentos e uniformes: R$ 80.000,00 (9,4%)
└─ Despesas administrativas: R$ 20.000,00 (2,4%)

Reajuste: Após 12 meses, conforme cláusula de reajuste
```

**Campo 10 - Forma de Pagamento (do TR):**
```
[DETALHADO COM INTEGRAÇÃO]
Pagamento mensal, mediante apresentação de Nota Fiscal eletrônica, 
em até 5 (cinco) dias úteis após o atestado de execução dos serviços 
pelo fiscal do contrato.

Condições:
• Emissão de NF-e até o 3º dia útil do mês subsequente
• Comprovação de regularidade fiscal e trabalhista
• Apresentação de relatório mensal de atividades
• Atestado do fiscal em até 2 dias úteis
• Pagamento via ordem bancária eletrônica

Glosa de pagamento:
• Falhas graves: redução de até 10% do valor mensal
• Falhas médias: redução de até 5%
• Falhas leves: advertência sem desconto

Dotação orçamentária:
• Unidade: 02.01 - TJSP
• Elemento: 33.90.37 - Locação de Mão de Obra
• Fonte: 01 - Recursos Ordinários
```

**Campo 11 - Reajuste (conforme Lei 14.133/2021):**
```
[GERADO CONFORME LEGISLAÇÃO]
Os preços poderão ser reajustados após 12 (doze) meses, contados da 
data de apresentação da proposta, mediante aplicação do Índice Nacional 
de Preços ao Consumidor Amplo - IPCA, apurado pelo IBGE, ou outro 
índice que venha a substituí-lo, conforme Art. 92, §1º, da Lei nº 
14.133/2021.

Fórmula de reajuste:
R = V x (I₁ / I₀)

Onde:
R = Valor reajustado
V = Valor contratual a reajustar
I₁ = Índice relativo ao mês de reajuste
I₀ = Índice do mês de apresentação da proposta

Data base: 01/01/2026 (proposta)
Primeiro reajuste possível: 01/01/2027
```

#### **Grupo 5: Garantias**

**Campo 12 - Garantia Contratual:**
```
[CONFORME ART. 96, LEI 14.133/2021]
A CONTRATADA prestará garantia de 5% (cinco por cento) do valor total 
do contrato, no prazo de 10 (dez) dias úteis após a assinatura, em 
uma das seguintes modalidades:

a) Caução em dinheiro;
b) Seguro-garantia;
c) Fiança bancária.

Valor da garantia: R$ 42.500,00

Finalidade:
• Assegurar o fiel cumprimento das obrigações
• Responder por danos causados ao patrimônio público
• Cobrir multas aplicadas

Liberação da garantia:
• Após término da vigência contratual
• Cumpridas todas as obrigações
• Quitadas eventuais multas ou indenizações
• Prazo: até 30 dias após termo final
```

#### **Grupo 6: Obrigações**

**Campo 13 - Obrigações da Contratada (15 obrigações do TR):**
```
[CONSOLIDADO DE TR + EDITAL]

SÃO OBRIGAÇÕES DA CONTRATADA:

1. EXECUÇÃO DOS SERVIÇOS
   1.1 Executar os serviços conforme especificações do Termo de Referência
   1.2 Cumprir rigorosamente cronograma e horários estabelecidos
   1.3 Manter padrão de qualidade durante toda a vigência

2. MÃO DE OBRA
   2.1 Disponibilizar 25 funcionários qualificados e treinados
   2.2 Substituir funcionários faltosos em até 2 (duas) horas
   2.3 Fornecer uniformes padronizados e crachás de identificação
   2.4 Realizar treinamentos periódicos (mínimo trimestral)
   2.5 Manter preposto em tempo integral nas dependências

3. MATERIAIS E EQUIPAMENTOS
   3.1 Fornecer todos os materiais, produtos e equipamentos necessários
   3.2 Utilizar produtos biodegradáveis e aprovados pela ANVISA
   3.3 Manter estoque mínimo de 15 dias de materiais
   3.4 Substituir produtos vencidos ou inadequados imediatamente

4. OBRIGAÇÕES TRABALHISTAS
   4.1 Cumprir toda legislação trabalhista, previdenciária e tributária
   4.2 Efetuar pagamento de salários até o 5º dia útil
   4.3 Recolher encargos sociais nos prazos legais
   4.4 Fornecer vale-transporte e alimentação aos funcionários
   4.5 Manter regularidade fiscal e trabalhista comprovada mensalmente

5. SEGUROS E GARANTIAS
   5.1 Manter seguro de responsabilidade civil vigente (mínimo R$ 500k)
   5.2 Manter garantia contratual durante toda vigência
   5.3 Responder por danos ao patrimônio ou terceiros

6. FISCALIZAÇÃO E RELATÓRIOS
   6.1 Aceitar fiscalização a qualquer tempo, sem aviso prévio
   6.2 Apresentar relatório mensal de atividades até dia 3
   6.3 Atender solicitações do fiscal em até 24 horas
   6.4 Manter canal de comunicação 24h (telefone/WhatsApp)

7. EMERGÊNCIAS
   7.1 Atender chamados de emergência em até 2 (duas) horas
   7.2 Disponibilizar equipe de sobreaviso
   7.3 Executar serviços extras quando solicitado (com pagamento adicional)

8. CONFORMIDADE
   8.1 Cumprir normas de segurança do trabalho (NRs do MTE)
   8.2 Observar políticas de segurança da informação do TJSP
   8.3 Respeitar código de ética e conduta do servidor público
```

**Campo 14 - Obrigações da Contratante (8 obrigações):**
```
[GERADO AUTOMATICAMENTE]

SÃO OBRIGAÇÕES DO CONTRATANTE (TJSP):

1. PAGAMENTO
   1.1 Efetuar pagamentos nos prazos estabelecidos
   1.2 Fornecer dotação orçamentária suficiente

2. FISCALIZAÇÃO
   2.1 Designar servidor para fiscalização do contrato
   2.2 Notificar a CONTRATADA sobre falhas ou irregularidades
   2.3 Atestar execução dos serviços mensalmente

3. INFRAESTRUTURA
   3.1 Fornecer acesso às dependências do Fórum
   3.2 Disponibilizar pontos de água e energia
   3.3 Fornecer local para guarda de materiais e equipamentos

4. INFORMAÇÕES
   4.1 Prestar esclarecimentos necessários à execução
   4.2 Comunicar alterações de horários ou necessidades especiais

5. ACOMPANHAMENTO
   5.1 Avaliar qualidade dos serviços periodicamente
   5.2 Aplicar penalidades quando cabíveis

6. COLABORAÇÃO
   6.1 Facilitar execução dos serviços
   6.2 Resolver questões administrativas prontamente

7. SEGURANÇA
   7.1 Garantir segurança dos funcionários da CONTRATADA
   7.2 Comunicar riscos ou situações de perigo

8. DOCUMENTAÇÃO
   8.1 Fornecer cópia do contrato e anexos
   8.2 Manter registro de ocorrências e atestados
```

#### **Grupo 7: Gestão Contratual**

**Campo 15 - Fiscalização:**
```
[CONFORME TR E LEGISLAÇÃO]

FISCALIZAÇÃO DO CONTRATO

Fiscal designado: [Nome do servidor]
Matrícula: [número]
Cargo: Diretor Administrativo
Portaria de nomeação: [número/ano]

Atribuições do fiscal:
• Acompanhar e fiscalizar execução diária dos serviços
• Realizar inspeções periódicas (mínimo semanal)
• Atestar notas fiscais mensalmente
• Aplicar checklist de qualidade com 20 itens
• Registrar ocorrências em livro próprio
• Notificar a CONTRATADA sobre falhas
• Propor aplicação de penalidades
• Solicitar documentação comprovató ria de regularidade

Metodologia de fiscalização:
• Inspeção visual diária
• Checklist semanal de qualidade (score mínimo 95%)
• Reunião mensal com preposto da CONTRATADA
• Avaliação trimestral de desempenho

A fiscalização do CONTRATANTE não exclui nem reduz a responsabilidade 
da CONTRATADA pela qualidade, correção e segurança dos serviços 
prestados.
```

#### **Grupo 8: Penalidades**

**Campo 16 - Penalidades (Art. 156, Lei 14.133/2021):**
```
[COMPLETO E PROPORCIONAL]

SANÇÕES ADMINISTRATIVAS

Pela inexecução total ou parcial do contrato, a CONTRATADA poderá 
sofrer as seguintes penalidades:

1. ADVERTÊNCIA
   Aplicação: Falhas leves e ocasionais
   Exemplos:
   • Atraso leve no início dos serviços
   • Falha pontual sem reincidência
   • Descumprimento de obrigação secundária

2. MULTAS
   2.1 Multa de Mora (atraso):
       • 0,3% ao dia sobre valor mensal, até 30 dias
       • Máximo de 10% do valor mensal
   
   2.2 Multa por Inexecução Parcial:
       • 5% sobre valor do serviço não executado
   
   2.3 Multa por Inexecução Total:
       • 10% sobre o valor total do contrato
   
   2.4 Multas Específicas:
       • Falta de funcionário sem substituição: R$ 500,00/dia
       • Falta de material: R$ 300,00/ocorrência
       • Descumprimento de horário: R$ 200,00/ocorrência
       • Ausência do preposto: R$ 1.000,00/dia

3. SUSPENSÃO TEMPORÁRIA
   Prazo: Até 2 anos
   Motivos:
   • Reincidência em faltas graves
   • Descumprimento reiterado de obrigações
   • Fraude ou má-fé comprovada

4. DECLARAÇÃO DE INIDONEIDADE
   Motivos:
   • Fraude grave na execução
   • Apresentação de documentação falsa
   • Comportamento inidôneo

Processo de aplicação:
• Notificação prévia com prazo de defesa (5 dias úteis)
• Análise da defesa
• Decisão fundamentada
• Possibilidade de recurso

As multas poderão ser descontadas:
• Dos pagamentos devidos
• Da garantia contratual
• Mediante cobrança judicial
```

**Campo 17 - Rescisão (Art. 137 e 138, Lei 14.133/2021):**
```
[CAUSAS LEGAIS]

RESCISÃO CONTRATUAL

O contrato poderá ser rescindido nas seguintes hipóteses:

1. RESCISÃO UNILATERAL PELO CONTRATANTE (Art. 137):
   
   a) Por razões de interesse público:
      • Necessidade de adequação administrativa
      • Mudança de prioridades institucionais
   
   b) Por inadimplemento da CONTRATADA:
      • Não cumprimento de cláusulas contratuais
      • Cumprimento irregular de obrigações
      • Lentidão que comprometa o prazo
      • Atraso injustificado no início
      • Paralisação sem justa causa
      • Subcontratação não autorizada
      • Desatendimento às determinações do fiscal
      • Cometimento reiterado de faltas
      • Decretação de falência ou insolvência
      • Dissolução da sociedade
      • Alteração social sem anuência
   
   c) Por razões de segurança nacional ou ordem pública

2. RESCISÃO AMIGÁVEL (Art. 138, I):
   • Consenso entre as partes
   • Formalização por apostilamento
   • Sem aplicação de penalidades

3. RESCISÃO JUDICIAL (Art. 138, II):
   • Por qualquer das partes
   • Em caso de impasse ou litígio

Efeitos da rescisão:
• Assunção imediata do objeto pela Administração
• Ocupação e utilização de equipamentos e materiais
• Retenção de créditos até apuração de danos
• Execução da garantia contratual
• Pagamento apenas pelos serviços efetivamente executados

Direitos da CONTRATADA em caso de rescisão:
• Devolução de garantia (se não houver débitos)
• Pagamento proporcional aos serviços executados
• Indenização por prejuízos comprovados (se rescisão por interesse público)
```

#### **Grupo 9: Disposições Finais**

**Campo 18 - Alterações:**
```
[CONFORME ART. 124 E 125, LEI 14.133/2021]

ALTERAÇÕES CONTRATUAIS

O contrato poderá ser alterado mediante termo aditivo, nas seguintes 
situações:

1. ALTERAÇÕES UNILATERAIS PELA ADMINISTRAÇÃO:
   
   a) Modificação do projeto ou especificações para melhor adequação
   b) Alteração do regime de execução por fato superveniente
   c) Modificação da forma de pagamento por interesse público

2. ALTERAÇÕES POR ACORDO DAS PARTES:
   
   a) Acréscimos ou supressões quantitativas:
      • Limite: até 25% do valor inicial atualizado
      • Excepcionalmente até 50% para reforma de edifício/equipamento
      • Supressão acima de 25% se houver acordo
   
   b) Substituição de garantia contratual
   
   c) Alteração qualitativa do objeto por fato superveniente
   
   d) Prorrogação de prazos
   
   e) Recomposição de preços (equilíbrio econômico-financeiro)

Procedimento:
• Justificativa fundamentada
• Proposta formal da parte interessada
• Análise técnica e jurídica
• Aprovação pela autoridade competente
• Formalização por termo aditivo
• Publicação no Diário de Justiça Eletrônico

Limites para aditivos:
• Acréscimo: Até 25% (regra) ou 50% (exceção)
• Supressão: Até 25% sem acordo; sem limite com acordo
• Prorrogação: Até 60 meses total (Art. 107)
```

**Campo 19 - Foro:**
```
[PADRÃO TJSP]
Fica eleito o Foro da Comarca de São Paulo, Capital do Estado de 
São Paulo, para dirimir quaisquer dúvidas ou controvérsias oriundas 
do presente contrato, com renúncia expressa a qualquer outro, por 
mais privilegiado que seja.
```

**Campo 20 - Disposições Gerais:**
```
[CLÁUSULAS COMPLEMENTARES]

DISPOSIÇÕES GERAIS

1. LEGISLAÇÃO APLICÁVEL
   O presente contrato rege-se pela Lei Federal nº 14.133/2021 e suas 
   alterações, Decreto Federal nº 11.462/2023, Lei Complementar nº 
   123/2006, demais normas pertinentes e, subsidiariamente, pelos 
   princípios da teoria geral dos contratos e disposições de direito 
   privado.

2. VINCULAÇÃO AO EDITAL
   Integram o presente contrato, independentemente de transcrição:
   • Edital de Pregão Eletrônico nº 123/2025
   • Termo de Referência (Anexo I)
   • Proposta da CONTRATADA
   • Ata de julgamento e homologação

3. PUBLICAÇÃO
   O resumo do contrato será publicado no Diário de Justiça Eletrônico 
   - DJE, conforme Art. 94 da Lei nº 14.133/2021.

4. ASSINATURA ELETRÔNICA
   O contrato será assinado eletronicamente por ambas as partes, com 
   certificado digital ICP-Brasil.

5. CONTROLE INTERNO
   O contrato está sujeito a fiscalização pelos órgãos de controle 
   interno e externo.

6. CASOS OMISSOS
   Os casos omissos serão resolvidos pela CONTRATANTE, com base na 
   legislação aplicável e princípios gerais de direito.

7. COMUNICAÇÕES
   Todas as comunicações entre as partes deverão ser formais, por escrito, 
   protocoladas ou por meio eletrônico oficial.

8. GARANTIA CONTRA VÍCIOS
   A CONTRATADA responde por vícios ou defeitos dos serviços prestados, 
   mesmo após o término da vigência contratual.

9. PROPRIEDADE INTELECTUAL
   Não há cessão de direitos de propriedade intelectual no presente contrato.

10. ANTICORRUPÇÃO
    A CONTRATADA declara conhecer as normas de prevenção à corrupção 
    previstas na legislação brasileira (Lei nº 12.846/2013) e se compromete 
    a cumpri-las fielmente.
```

### 5.5 Passo 4: Salvar Contrato

```
1. Clica em [💾 Salvar Contrato]

2. Sistema salva:
   ✅ Dados salvos em: exports/contrato_data.json
   ✅ Backup automático em: exports/backups/
   🕐 Última atualização: 10/12/2025 16:45
   
3. Confirmação:
   ✅ Contrato salvo com sucesso!
   📊 20/20 campos preenchidos (100%)
```

### 5.6 Passo 5: Gerar DOCX Profissional

```
1. Clica em [📤 Gerar DOCX Profissional]

2. Sistema processa (~5-10 segundos)

3. DOCX gerado com:
   📄 Nome: Contrato_SAAB_090207_2026_CleanTech.docx
   📏 Páginas: 35-40
   🎨 Formatação: Institucional TJSP
   🏛️ Cores: RGB(0, 51, 102) - Azul TJSP
   
4. Estrutura do documento:
   ├─ CAPA INSTITUCIONAL
   │  ├─ Brasão TJSP
   │  ├─ Título centralizado
   │  ├─ Número do contrato
   │  └─ Data
   │
   ├─ PREÂMBULO
   │  ├─ Identificação das partes
   │  ├─ Fundamentação legal
   │  └─ Objeto resumido
   │
   ├─ 15 CLÁUSULAS CONTRATUAIS
   │  ├─ Cláusula 1ª - DO OBJETO
   │  ├─ Cláusula 2ª - DA FUNDAMENTAÇÃO LEGAL
   │  ├─ Cláusula 3ª - DO VALOR
   │  ├─ Cláusula 4ª - DA VIGÊNCIA
   │  ├─ Cláusula 5ª - DA FORMA DE PAGAMENTO
   │  ├─ Cláusula 6ª - DAS OBRIGAÇÕES DA CONTRATADA
   │  ├─ Cláusula 7ª - DAS OBRIGAÇÕES DO CONTRATANTE
   │  ├─ Cláusula 8ª - DA FISCALIZAÇÃO
   │  ├─ Cláusula 9ª - DA GARANTIA CONTRATUAL
   │  ├─ Cláusula 10ª - DAS PENALIDADES
   │  ├─ Cláusula 11ª - DA RESCISÃO
   │  ├─ Cláusula 12ª - DAS ALTERAÇÕES CONTRATUAIS
   │  ├─ Cláusula 13ª - DO REAJUSTE
   │  ├─ Cláusula 14ª - DAS DISPOSIÇÕES GERAIS
   │  └─ Cláusula 15ª - DO FORO
   │
   ├─ LOCAL, DATA E ASSINATURAS
   │  ├─ São Paulo, [data]
   │  ├─ Assinatura CONTRATANTE
   │  └─ Assinatura CONTRATADA
   │
   ├─ ANEXOS
   │  ├─ Anexo I - Termo de Referência
   │  ├─ Anexo II - Proposta da CONTRATADA
   │  └─ Anexo III - Documentação da licitação
   │
   └─ RODAPÉ INSTITUCIONAL
      └─ © TJSP - Projeto SAAB-Tech

5. Download automático inicia
```

---

## 6. Cláusulas Contratuais

### 6.1 Estrutura das 15 Cláusulas

O DOCX gerado contém **15 cláusulas padronizadas**:

| Nº | Cláusula | Origem dos Dados | Obrigatória |
|----|----------|------------------|-------------|
| 1ª | DO OBJETO | Campo 5 (objeto) | ✅ Sim |
| 2ª | DA FUNDAMENTAÇÃO LEGAL | Campo 6 (fundamentacao_legal) | ✅ Sim |
| 3ª | DO VALOR | Campo 9 (valor_global) | ✅ Sim |
| 4ª | DA VIGÊNCIA | Campos 7 e 8 (vigencia, prazo_execucao) | ✅ Sim |
| 5ª | DA FORMA DE PAGAMENTO | Campo 10 (forma_pagamento) | ✅ Sim |
| 6ª | DAS OBRIGAÇÕES DA CONTRATADA | Campo 13 (obrigacoes_contratada) | ✅ Sim |
| 7ª | DAS OBRIGAÇÕES DO CONTRATANTE | Campo 14 (obrigacoes_contratante) | ✅ Sim |
| 8ª | DA FISCALIZAÇÃO | Campo 15 (fiscalizacao) | ✅ Sim |
| 9ª | DA GARANTIA CONTRATUAL | Campo 12 (garantia_contratual) | ✅ Sim |
| 10ª | DAS PENALIDADES | Campo 16 (penalidades) | ✅ Sim |
| 11ª | DA RESCISÃO | Campo 17 (rescisao) | ✅ Sim |
| 12ª | DAS ALTERAÇÕES CONTRATUAIS | Campo 18 (alteracoes) | ✅ Sim |
| 13ª | DO REAJUSTE | Campo 11 (reajuste) | ⚠️ Condicional |
| 14ª | DAS DISPOSIÇÕES GERAIS | Campo 20 (disposicoes_gerais) | ✅ Sim |
| 15ª | DO FORO | Campo 19 (foro) | ✅ Sim |

### 6.2 Formatação das Cláusulas

**Padrão TJSP:**
```
CLÁUSULA [NÚMERO]ª - [TÍTULO EM MAIÚSCULAS]

[Parágrafo 1º com texto justificado, fonte Arial 12, espaçamento 1,5]

§ 1º [Parágrafo primeiro]
§ 2º [Parágrafo segundo]
...

Subitens:
I - [item 1]
II - [item 2]
...

Alíneas:
a) [alínea a]
b) [alínea b]
...
```

---

## 7. Validações e Alertas

### 7.1 Validações Automáticas

O sistema valida os 20 campos antes de salvar:

| Validação | Critério | Severidade |
|-----------|----------|------------|
| **Número contrato vazio** | Campo obrigatório | 🚨 Crítico |
| **Data inválida** | Formato DD/MM/AAAA | 🚨 Crítico |
| **Objeto vazio** | Descrição obrigatória | 🚨 Crítico |
| **Partes incompletas** | CONTRATANTE e CONTRATADA | 🚨 Crítico |
| **Valor ausente** | Campo "valor_global" | 🚨 Crítico |
| **Vigência indefinida** | Não pode ser "a definir" | ⚠️ Alto |
| **Obrigações vazias** | Mínimo 5 obrigações cada parte | ⚠️ Alto |
| **Penalidades ausentes** | Pelo menos 2 tipos | ⚠️ Médio |

### 7.2 Alertas de Inconsistência

O módulo **⚠️ Alertas** detecta divergências:

```
🚨 INCONSISTÊNCIA DETECTADA

Documento 1: EDITAL
Campo: valor_estimado
Valor: R$ 850.000,00

Documento 2: CONTRATO
Campo: valor_global
Valor: R$ 820.000,00

❌ Valor do contrato (R$ 820k) é menor que o estimado no edital 
   (R$ 850k) - Diferença: R$ 30.000,00

ℹ️ Isso é NORMAL quando há economia na licitação.
   Certifique-se de que está correto e documente o motivo.
```

---

## 8. Casos Práticos

### 8.1 Caso 1: Contrato de Serviços Contínuos

**Cenário:**
- Limpeza do Fórum
- Valor: R$ 850.000,00/ano
- Prazo: 12 meses (prorrogável até 60)

**Tempo:**
- Geração: 30 segundos
- Revisão: 20 minutos
- TOTAL: ~25 minutos

**Vs. Manual:** ~8 horas

### 8.2 Caso 2: Contrato de Aquisição

**Cenário:**
- Material permanente (móveis)
- Valor: R$ 250.000,00
- Entrega: 30 dias

**Particularidades:**
- Garantia do produto: 12 meses
- Instalação incluída
- Pagamento em parcela única

**Tempo:** ~15 minutos

### 8.3 Caso 3: Renovação de Contrato

**Cenário:**
- Upload de contrato anterior
- Atualização de valores (reajuste)
- Novo prazo

**Fluxo:**
```
1. Upload do contrato atual (PDF)
2. Sistema extrai 20 campos
3. Você ajusta apenas:
   - Data nova
   - Valor reajustado
   - Nova vigência
4. Gera novo contrato
```

**Tempo:** ~10 minutos

---

## 📚 Próximos Passos

Você completou o aprendizado sobre **Contratos Administrativos**!

Continue para:
- **Manual 04** – Módulos de Governança (Alertas, Painéis)
- **Manual 05** – Módulos Avançados (Relatórios, Integração)

---

## 📞 Suporte Técnico

**Dúvidas sobre contratos?**

📧 saab-tech@tjsp.jus.br  
☎️ (11) XXXX-XXXX  
🕐 Segunda a Sexta, 9h-18h

**Suporte Jurídico:**  
📧 assessoria.juridica@tjsp.jus.br

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Manual 03B/07 – Módulo de Contrato Administrativo*
