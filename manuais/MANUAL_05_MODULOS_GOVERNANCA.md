# 📘 Manual do Usuário – Projeto SAAB-Tech

## Manual 05: Módulos de Governança e Monitoramento

**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Tribunal de Justiça do Estado de São Paulo**  
**Secretaria de Administração e Abastecimento (SAAB)**

---


---

## 1. Visão Geral

### 1.1 O que são Módulos de Governança?

Os **Módulos de Governança** são ferramentas de **monitoramento, auditoria e análise** que garantem a qualidade e conformidade dos documentos gerados no Projeto SAAB-Tech.

```
MÓDULOS DE GOVERNANÇA:
├─ 09. ⚠️ Alertas (Detecção de pendências)
├─ 10. 💡 Análise de Desempenho (Métricas técnicas)
├─ 11. 📊 Painel de Governança (Consolidação institucional)
└─ 12. 📈 Painel Executivo (Visão estratégica)
```

### 1.2 Finalidade

| Módulo | Função | Público-Alvo |
|--------|--------|--------------|
| **Alertas** | Detectar inconsistências e campos vazios | Técnicos operacionais |
| **Análise Desempenho** | Métricas de qualidade documental | Analistas e gestores |
| **Painel Governança** | Auditoria consolidada | Equipe de governança |
| **Painel Executivo** | Indicadores estratégicos | Alta gestão/Direção |

### 1.3 Quando Usar

✅ **Use governança quando:**
- Finalizar documentos (DFD, ETP, TR, Edital, Contrato)
- Identificar problemas antes da submissão
- Avaliar qualidade da documentação
- Gerar relatórios para superiores
- Auditar processos de contratação

---

## 2. Módulo 09: Alertas

### 2.1 O que é o Módulo Alertas?

O **Módulo ⚠️ Alertas** realiza **validação automática em tempo real** de todos os documentos processados, detectando:
- Campos obrigatórios vazios
- Inconsistências entre módulos
- Dados faltantes ou incompletos
- Divergências de valores

### 2.2 Como Funciona

**Sistema de Validação:**
```
1. Sistema monitora 21 campos obrigatórios em 5 módulos
2. Detecta inconsistências automaticamente
3. Classifica por severidade (Crítico/Médio/Informativo)
4. Gera recomendações de correção
5. Mantém histórico de alertas
```

**Campos Validados:**

| Módulo | Campos Validados | Total |
|--------|------------------|-------|
| **DFD** | unidade, responsável, valor_estimado, prazo_estimado | 4 |
| **ETP** | unidade, responsável, valor_estimado, prazo_execução, modalidade | 5 |
| **TR** | objeto, especificacoes, valor_global, prazo_execução | 4 |
| **Edital** | numero_edital, objeto, valor_estimado, prazo_entrega | 4 |
| **Contrato** | numero_contrato, objeto, valor_global, vigencia | 4 |

### 2.3 Como Acessar

1. Na barra lateral, clique em **⚠️ Alertas**
2. Sistema carrega alertas automaticamente

### 2.4 Interface do Módulo

**Cards de Resumo:**
```
┌─────────────┬─────────────┬─────────────┐
│ 🚨 Críticos │ ⚠️ Médios   │ ℹ️ Informativos │
│     3       │     7       │     2        │
│ Graves      │ Atenção     │ Avisos       │
└─────────────┴─────────────┴─────────────┘
```

**Filtros:**
```
🔍 Filtros:
├─ Por Módulo: [DFD] [ETP] [TR] [Edital] [Contrato]
└─ Por Severidade: [Alto] [Médio] [Baixo]
```

### 2.5 Tipos de Alertas

#### **Alerta Crítico 🚨**

**Quando ocorre:** Campo obrigatório vazio ou dado essencial ausente

**Exemplo:**
```
🚨 ALERTA CRÍTICO
Módulo: ETP
Campo: valor_estimado
Mensagem: Campo obrigatório "valor_estimado" está vazio

💡 Recomendação: Preencha o valor estimado no módulo ETP. 
   Este campo é obrigatório pela IN SEGES/ME 40/2020.
```

#### **Alerta Médio ⚠️**

**Quando ocorre:** Inconsistência entre documentos ou texto muito curto

**Exemplo:**
```
⚠️ ALERTA MÉDIO
Módulo: TR
Campo: objeto
Mensagem: Divergência detectada no campo "objeto"

Detalhes:
• ETP: "Contratação de serviços de limpeza..."
• TR:  "Contratação de empresa de limpeza..."

💡 Recomendação: Uniformize a descrição do objeto em todos 
   os documentos para manter consistência.
```

#### **Alerta Informativo ℹ️**

**Quando ocorre:** Avisos gerais ou sugestões de melhoria

**Exemplo:**
```
ℹ️ ALERTA INFORMATIVO
Módulo: DFD
Campo: contexto_institucional
Mensagem: Texto curto detectado (85 caracteres)

💡 Recomendação: Expanda a seção com mais detalhes sobre 
   o contexto institucional (mínimo recomendado: 200 caracteres).
```

### 2.6 Passo a Passo

#### **Passo 1: Atualizar Alertas**

```
1. Acesse [⚠️ Alertas]
2. Clique em [🔄 Atualizar Alertas]
3. Sistema analisa todos os módulos
4. Aguarde ~10-15 segundos
5. Visualize resumo atualizado
```

#### **Passo 2: Filtrar Alertas**

```
1. Use sidebar para filtrar:
   - Módulos: Selecione quais deseja ver
   - Severidade: Foque em críticos primeiro
   
2. Lista é atualizada em tempo real
```

#### **Passo 3: Corrigir Problemas**

```
Para cada alerta:
1. Leia a mensagem e recomendação
2. Navegue até o módulo indicado
3. Corrija o campo problemático
4. Salve as alterações
5. Volte ao módulo Alertas
6. Clique em [🔄 Atualizar Alertas]
7. Verifique se o alerta foi resolvido
```

### 2.7 Histórico de Alertas

**Visualizar histórico:**
```
1. Role até "Histórico de Alertas Anteriores"
2. Veja evolução temporal
3. Compare alertas atuais vs. anteriores
4. Identifique melhorias ou reincidências
```

**Estatísticas históricas:**
- Total de alertas ao longo do tempo
- Taxa de resolução de problemas
- Módulos com mais alertas recorrentes
- Evolução da qualidade documental

---

## 3. Módulo 10: Análise de Desempenho

### 3.1 O que é o Módulo Análise de Desempenho?

O **Módulo 💡 Análise de Desempenho** oferece **métricas técnicas** sobre a qualidade e consistência da documentação:
- Contagem de palavras (word count)
- Coerência global entre documentos
- Conformidade legal
- Evolução temporal de métricas

### 3.2 Indicadores Principais

| Métrica | Descrição | Meta |
|---------|-----------|------|
| **Total Eventos** | Documentos processados | Crescimento contínuo |
| **Word Count Total** | Soma de palavras em todos os docs | > 50.000 palavras |
| **Conformidade Legal** | % de conformidade com Lei 14.133/2021 | > 95% |
| **Coerência Global** | Consistência entre módulos | > 85% |

### 3.3 Como Acessar

1. Na barra lateral, clique em **💡 Análise de Desempenho**
2. Sistema carrega métricas automaticamente

### 3.4 Interface do Módulo

**Cards de Indicadores:**
```
┌──────────┬──────────┬──────────┬──────────┐
│ 📄 Total │ 📝 Words │ ✅ Legal │ 🧩 Coer. │
│ Eventos  │ Count    │ Conform. │ Global   │
│   42     │ 68.450   │  96.2%   │  88.5%   │
└──────────┴──────────┴──────────┴──────────┘
```

**Filtros Temporais:**
```
⚙️ Configurações:
└─ Período: [7 dias] [15 dias] [30 dias] [60 dias]
```

### 3.5 Gráficos e Análises

#### **Gráfico 1: Evolução Temporal – Volume**

```
📈 Volume de eventos registrados (30 dias)

   40│                            ●
   35│                     ●
   30│              ●
   25│       ●
   20│ ●
    └─────────────────────────────────►
     Dia 1  Dia 7  Dia 15  Dia 22  Dia 30
```

**Interpretação:**
- Crescimento = Aumento de produtividade
- Estabilidade = Fluxo constante
- Queda = Possível problema operacional

#### **Gráfico 2: Distribuição por Artefato**

```
📁 Eventos por artefato (últimos 30 dias)

DFD      ████████████ 12
ETP      ██████████████████ 18
TR       ████████████ 12
EDITAL   ██████ 6
CONTRATO ████ 4
```

**Interpretação:**
- ETP tem mais processamentos (documento mais complexo)
- Contrato tem menos (etapa final)

#### **Gráfico 3: Coerência Global**

```
🧭 Tendência de coerência global (últimos 30 dias)

100%│                            ●
 90%│                     ●  ●
 80%│              ●  ●
 70%│       ●  ●
    └─────────────────────────────────►
     Semana 1  Semana 2  Semana 3  Semana 4
```

**Interpretação:**
- Acima 85% = Boa consistência
- Entre 70-85% = Revisão recomendada
- Abaixo 70% = Problemas graves de inconsistência

### 3.6 Modo Sintético vs. Real

**ℹ️ Modo Sintético:**
```
Sistema de auditoria não encontrado. Exibindo métricas 
baseadas nos documentos processados (word count básico).
```

**✅ Modo Real (com auditoria):**
```
Sistema de auditoria ativo. Métricas completas com timestamps, 
user_id, e análise detalhada de coerência.
```

### 3.7 Como Interpretar Métricas

**Conformidade Legal < 90%:**
```
⚠️ AÇÃO NECESSÁRIA:
- Revisar campos obrigatórios vazios
- Verificar fundamentação legal
- Consultar módulo Alertas para detalhes
```

**Coerência Global < 80%:**
```
⚠️ AÇÃO NECESSÁRIA:
- Verificar inconsistências entre DFD/ETP/TR
- Uniformizar valores e prazos
- Revisar descrições do objeto
```

---

## 4. Módulo 11: Painel de Governança

### 4.1 O que é o Painel de Governança?

O **Módulo 📊 Painel de Governança** consolida **auditorias e alertas institucionais** em uma visão unificada para equipes de compliance e governança.

### 4.2 Finalidade

- Consolidar alertas de todos os módulos
- Visualizar distribuição por severidade
- Identificar categorias de problemas mais frequentes
- Exportar dados para análise externa

### 4.3 Como Acessar

1. Na barra lateral, clique em **📊 Painel de Governança**
2. Sistema carrega dados consolidados

### 4.4 Interface do Módulo

**Indicadores Consolidados:**
```
┌──────────┬──────────┬──────────┬──────────┐
│ Total    │ Alta     │ Média    │ Baixa    │
│ Alertas  │ Severid. │ Severid. │ Severid. │
│   24     │    5     │    12    │    7     │
└──────────┴──────────┴──────────┴──────────┘
```

**Gráfico de Distribuição:**
```
📊 Distribuição de Alertas por Severidade

Alto   █████████████████████ 5
Médio  ████████████████████████████████████████████ 12
Baixo  ████████████████████ 7
```

### 4.5 Filtros Disponíveis

```
⚙️ Filtros de Visualização:
├─ Severidade: [Alto] [Médio] [Baixo]
└─ Categoria: [Campo vazio] [Inconsistência] [Texto curto] ...
```

### 4.6 Tabela Consolidada

**Colunas exibidas:**
- **Módulo**: Origem do alerta (DFD, ETP, TR, etc.)
- **Categoria**: Tipo do problema
- **Campo**: Campo problemático
- **Mensagem**: Descrição do alerta
- **Recomendação**: Ação sugerida
- **Timestamp**: Data/hora da detecção

**Exemplo de linha:**
```
DFD | Campo vazio | valor_estimado | Campo obrigatório vazio | 
Preencha o valor estimado | 2025-12-10 14:35:22
```

### 4.7 Exportação de Dados

**Exportar para JSON:**
```
1. Clique em [💾 Exportar Alertas Consolidados para JSON]
2. Sistema gera arquivo em /exports/analises/
3. Nome: alertas_consolidados_YYYYMMDD_HHMMSS.json
4. Use para:
   - Análise em ferramentas externas (Excel, Python)
   - Integração com sistemas de BI
   - Auditoria externa
```

**Estrutura do JSON:**
```json
{
  "alerts": [
    {
      "modulo": "DFD",
      "categoria": "campo_vazio",
      "severidade": "alto",
      "campo": "valor_estimado",
      "mensagem": "Campo obrigatório vazio",
      "recomendacao": "Preencha o campo...",
      "timestamp": "2025-12-10T14:35:22"
    }
  ],
  "totais": {
    "total": 24,
    "alto": 5,
    "medio": 12,
    "baixo": 7
  }
}
```

---

## 5. Módulo 12: Painel Executivo

### 5.1 O que é o Painel Executivo?

O **Módulo 📈 Painel Executivo** oferece uma **visão estratégica consolidada** para alta gestão, diretores e coordenadores, com:
- Indicadores executivos sintéticos
- Insights e recomendações estratégicas
- Distribuição institucional de alertas
- Relatório executivo em PDF (exportação)

### 5.2 Público-Alvo

- 🎯 Diretores e Coordenadores da SAAB
- 🎯 Desembargadores e Magistrados
- 🎯 Equipe de Planejamento Estratégico
- 🎯 Auditores institucionais

### 5.3 Como Acessar

1. Na barra lateral, clique em **📈 Painel Executivo**
2. Sistema carrega visão consolidada

### 5.4 Interface do Módulo

**Indicadores Executivos:**
```
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ Alertas  │ Alta     │ Média    │ Baixa    │ Módulos  │
│ Totais   │ Severid. │ Severid. │ Severid. │ Afetados │
│   24     │    5     │    12    │    7     │    5     │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

### 5.5 Insights Estratégicos

**Semáforo de Alertas:**

🔴 **Alto > 0:**
```
⚠️ CRÍTICO
Foram detectados alertas de alta severidade. 
Recomenda-se auditoria imediata dos documentos críticos.

AÇÃO EXECUTIVA:
→ Convocar reunião emergencial com equipe técnica
→ Revisar documentos com alertas críticos
→ Não submeter documentação até correção
```

🟡 **Médio > 0, Alto = 0:**
```
ℹ️ ATENÇÃO
A maioria dos alertas possui severidade média.
Recomenda-se revisão textual antes da submissão.

AÇÃO EXECUTIVA:
→ Agendar revisão com responsáveis
→ Prazo: 48 horas para correção
→ Re-análise após ajustes
```

🟢 **Baixo apenas:**
```
✅ CONFORMIDADE
Nenhum alerta crítico encontrado. 
A integridade documental está dentro dos parâmetros aceitáveis.

AÇÃO EXECUTIVA:
→ Documentação aprovada para prosseguir
→ Manter monitoramento contínuo
```

### 5.6 Distribuição Institucional

**Gráfico 1: Alertas por Módulo**
```
DFD       ██████████ 8
ETP       ████████ 6
TR        ██████ 4
EDITAL    ████ 3
CONTRATO  ██ 3
```

**Gráfico 2: Categorias Mais Frequentes**
```
Campo vazio          ████████████████ 10
Inconsistência       ████████████ 8
Texto curto          ██████ 4
Divergência de valor ██ 2
```

### 5.7 Relatório Executivo PDF

**Gerar relatório:**
```
1. Clique em [📘 Gerar Relatório Executivo em PDF]
2. Sistema processa (~10-15 segundos)
3. Download: relatorio_executivo_YYYYMMDD.pdf
```

**Conteúdo do PDF:**
- Capa institucional TJSP
- Resumo executivo (1 página)
- Indicadores consolidados
- Gráficos de distribuição
- Tabela de alertas críticos
- Recomendações estratégicas
- Assinatura digital (opcional)

**Quando usar:**
- Reuniões de diretoria
- Apresentações para desembargadores
- Auditorias externas (TCE, CGJ)
- Documentação de processos

---

## 6. Casos Práticos

### 6.1 Caso 1: Correção de Alertas Críticos

**Situação:**
```
Você finalizou ETP e TR, mas o módulo Alertas mostra:
🚨 3 alertas críticos
⚠️ 5 alertas médios
```

**Ação passo a passo:**
```
1. Acesse [⚠️ Alertas]
2. Filtre por "Severidade: Alto"
3. Identifique os 3 críticos:
   - ETP: valor_estimado vazio
   - TR: obrigacoes_contratada vazio
   - TR: forma_pagamento vazio

4. Corrija cada um:
   a) Vá ao [📘 ETP]
      - Preencha Seção 14: R$ 850.000,00
      - Salve
   
   b) Vá ao [📑 TR]
      - Preencha Seção 6: Obrigações (15 itens)
      - Preencha Seção 8: Forma de pagamento
      - Salve

5. Volte ao [⚠️ Alertas]
6. Clique [🔄 Atualizar Alertas]
7. Confirme: 0 alertas críticos ✅
```

**Tempo:** ~15 minutos

### 6.2 Caso 2: Análise de Desempenho Mensal

**Situação:**
```
Final do mês, precisa gerar relatório de desempenho 
para apresentar ao coordenador.
```

**Ação:**
```
1. Acesse [💡 Análise de Desempenho]
2. Selecione período: "30 dias"
3. Clique [🔄 Atualizar Métricas]
4. Analise indicadores:
   - 42 eventos processados
   - 68.450 palavras geradas
   - 96.2% conformidade legal
   - 88.5% coerência global

5. Capture screenshots dos gráficos:
   - Evolução temporal
   - Distribuição por artefato
   - Tendência de coerência

6. Monte apresentação com:
   - Indicadores principais
   - Gráficos de evolução
   - Conclusões e melhorias
```

**Tempo:** ~20 minutos

### 6.3 Caso 3: Auditoria Executiva

**Situação:**
```
Desembargador solicitou relatório consolidado de 
qualidade da documentação para reunião amanhã.
```

**Ação:**
```
1. Acesse [📈 Painel Executivo]
2. Verifique semáforo:
   - 5 alertas altos = 🔴 CRÍTICO
   
3. Leia insights estratégicos
4. Clique [📘 Gerar Relatório Executivo em PDF]
5. Download do PDF (15 páginas)

6. Revise o conteúdo:
   - Resumo executivo (página 2)
   - Alertas críticos (páginas 4-6)
   - Recomendações (página 14)

7. Envie por e-mail para o gabinete

Opcional: Se tempo permitir:
8. Corrija alertas críticos
9. Gere novo relatório atualizado
10. Envie versão corrigida
```

**Tempo:** ~10 minutos (relatório) + 30 minutos (correções)

### 6.4 Caso 4: Monitoramento Contínuo

**Situação:**
```
Estabelecer rotina semanal de governança da equipe.
```

**Rotina recomendada:**
```
SEGUNDA-FEIRA (15 min):
├─ Acessar [⚠️ Alertas]
├─ Atualizar alertas
├─ Distribuir correções para equipe
└─ Definir prazo: até quarta

QUARTA-FEIRA (10 min):
├─ Verificar se correções foram feitas
├─ Re-atualizar alertas
└─ Cobrar pendências

SEXTA-FEIRA (20 min):
├─ Acessar [💡 Análise de Desempenho]
├─ Gerar métricas da semana
├─ Comparar com semana anterior
├─ Documentar melhorias/problemas
└─ Apresentar em reunião de equipe
```

---

## 📚 Próximos Passos

Você completou o aprendizado dos **Módulos de Governança**!

Continue para:
- **Manual 05** – Módulos Avançados (Relatório, Comparador, Integração, Versão)
- **Manual 06** – FAQ e Troubleshooting

---

## 📞 Suporte Técnico

**Dúvidas sobre governança?**

📧 saab-tech@tjsp.jus.br  
☎️ (11) XXXX-XXXX  
🕐 Segunda a Sexta, 9h-18h

**Suporte de Auditoria:**  
📧 governanca@tjsp.jus.br

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Manual 05/07 – Módulos de Governança e Monitoramento*
