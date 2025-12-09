# 📜 Guia do Módulo Contrato – SynapseNext v2025.1

## 🎯 Visão Geral

O **Módulo 08 – Contrato Administrativo** é o último estágio da jornada de contratação pública no SynapseNext. Ele consolida todos os dados dos módulos anteriores (DFD, ETP, TR, Edital) para gerar um **Contrato Administrativo** completo e robusto, alinhado à **Lei Federal nº 14.133/2021**.

---

## 🔧 Problemas Resolvidos nesta Implementação

### ❌ Antes (Versão Anterior)
1. **Defaults hardcoded** no formulário:
   - Vigência: "12 meses a contar da assinatura"
   - Reajuste: "Conforme índice oficial e cláusulas legais"
   - Foro: "Comarca de São Paulo/SP"
   
2. **Sem processamento robusto com IA**:
   - Prompt genérico direto (não especializado)
   - Não integrava contexto DFD/ETP/TR/Edital
   
3. **Sem integração com módulo Insumos**:
   - "Contrato" não aparecia como opção de destino
   
4. **DOCX simples**:
   - Sem formatação profissional
   - Sem cores institucionais TJSP
   - Sem estrutura de cláusulas

### ✅ Agora (v2025.1)
1. **Formulário limpo**: Campos vazios até processamento
2. **ContratoAgent especializado**: 20 campos com enriquecimento AGRESSIVO
3. **Integração completa**: Upload via Insumos + Processamento direto
4. **DOCX profissional**: 15 cláusulas, cores TJSP RGB(0,51,102), formatação institucional

---

## 🚀 Como Usar o Módulo Contrato

### **Opção 1: Processar Insumo com Upload**

1. Acesse **Módulo 08 – Contrato**
2. Na seção "📤 Upload de Insumo":
   - Clique em **"Browse files"** e selecione um arquivo (PDF/DOCX/TXT)
   - Arquivo pode ser: minuta de contrato, rascunho, contrato de referência
3. Clique no botão **"🤖 Processar Insumo com ContratoAgent"**
4. Aguarde o processamento (~10-30 segundos)
5. ✅ Os 20 campos serão preenchidos automaticamente
6. Revise os campos e ajuste manualmente se necessário
7. Clique em **"📤 Gerar DOCX Profissional"** para download

### **Opção 2: Gerar do Contexto (sem upload)**

**Pré-requisito**: Ter processado DFD, ETP, TR ou Edital anteriormente

1. Acesse **Módulo 08 – Contrato**
2. Observe a seção "🔗 Detecção automática de contexto":
   - Mostra quantos módulos anteriores estão disponíveis
   - Exemplo: "📎 **Contexto detectado**: 4/4 módulos anteriores disponíveis"
3. Clique no botão **"🧠 Gerar Contrato APENAS do Contexto"**
4. ✅ O ContratoAgent irá:
   - Extrair informações de DFD (objeto, valor, justificativa)
   - Extrair informações de ETP (prazos, resultados pretendidos)
   - Extrair informações de TR (especificações técnicas, fonte de recursos)
   - Extrair informações de Edital (obrigações, modalidade)
   - **Enriquecer AGRESSIVAMENTE** cada campo do contrato
5. Revise os campos e gere o DOCX

### **Opção 3: Upload via Módulo Insumos**

1. Acesse **Módulo 01 – Insumos**
2. Faça upload do arquivo de contrato
3. No selectbox "Selecione o módulo de destino", escolha **"CONTRATO"**
4. Clique em **"🚀 Processar e encaminhar para CONTRATO"**
5. O sistema irá:
   - Extrair o texto do arquivo
   - Salvar em `exports/insumos/json/CONTRATO_ultimo.json`
   - Disponibilizar para o Módulo 08
6. Acesse **Módulo 08 – Contrato** para visualizar os dados

### **Opção 4: Preencher Manualmente**

1. Acesse **Módulo 08 – Contrato**
2. Preencha os 20 campos do formulário manualmente:
   - **Identificação**: Número do Contrato, Data de Assinatura
   - **Valores e Prazos**: Vigência, Prazo de Execução, Valor Global, Forma de Pagamento, Reajuste, Garantia
   - **Partes**: Contratante, Contratada, Fundamentação Legal
   - **Objeto**: Descrição do objeto do contrato
   - **Obrigações**: Da Contratada, Da Contratante, Fiscalização
   - **Penalidades**: Penalidades, Rescisão
   - **Disposições Finais**: Alterações, Foro, Disposições Gerais
3. Clique em **"💾 Salvar Campos Editados Manualmente"**
4. Clique em **"📤 Gerar DOCX Profissional"**

---

## 📋 Estrutura dos 20 Campos do Contrato

| Campo | Descrição | Fonte de Enriquecimento |
|-------|-----------|-------------------------|
| `numero_contrato` | Número identificador do contrato | Manual ou insumo |
| `data_assinatura` | Data de assinatura do contrato | Manual ou insumo |
| `objeto` | Descrição do objeto contratual | **MERGE**: TR + Edital + ETP + DFD |
| `partes_contratante` | TJSP (hardcoded com CNPJ) | Padrão TJSP 51.174.001/0001-50 |
| `partes_contratada` | Empresa/fornecedor contratado | Edital ou insumo |
| `fundamentacao_legal` | Base legal (Lei 14.133/2021, etc.) | Edital ou padrão |
| `vigencia` | Período de vigência do contrato | TR > ETP > Edital |
| `prazo_execucao` | Prazo para execução dos serviços | TR > ETP > Edital |
| `valor_global` | Valor total do contrato | **PRIORIDADE**: DFD > ETP > Edital |
| `forma_pagamento` | Condições de pagamento | Edital ou TR |
| `reajuste` | Cláusula de reajuste de preços | Edital ou padrão Lei 14.133/2021 |
| `garantia_contratual` | Garantia exigida da contratada | Edital |
| `obrigacoes_contratada` | Obrigações da parte contratada | **MERGE**: Edital + TR |
| `obrigacoes_contratante` | Obrigações do TJSP | Edital |
| `fiscalizacao` | Regras de fiscalização do contrato | Edital > DFD |
| `penalidades` | Penalidades por descumprimento | Edital ou padrão Lei 14.133/2021 |
| `rescisao` | Condições de rescisão contratual | Edital ou padrão Lei 14.133/2021 |
| `alteracoes` | Regras para alterações contratuais | Padrão Lei 14.133/2021 |
| `foro` | Foro competente para disputas | **PADRÃO**: "Comarca de São Paulo/SP" |
| `disposicoes_gerais` | Cláusulas gerais adicionais | Edital ou insumo |

---

## 📄 Estrutura do DOCX Gerado

O documento DOCX profissional gerado possui a seguinte estrutura:

```
┌─────────────────────────────────────────────────┐
│   TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO   │
│          CONTRATO ADMINISTRATIVO Nº [XXX]       │
│              Data: [DD/MM/AAAA]                 │
└─────────────────────────────────────────────────┘

PREÂMBULO
O TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO...
e [CONTRATADA]... firmam o presente Contrato...

CLÁUSULA PRIMEIRA – DO OBJETO
[Descrição do objeto com merge de TR + Edital + ETP + DFD]

CLÁUSULA SEGUNDA – DA FUNDAMENTAÇÃO LEGAL
[Base legal: Lei 14.133/2021, Edital, etc.]

CLÁUSULA TERCEIRA – DA VIGÊNCIA
[Período de vigência do contrato]

CLÁUSULA QUARTA – DO VALOR GLOBAL
[Valor total em R$ com extenso]

CLÁUSULA QUINTA – DA FORMA DE PAGAMENTO
[Condições e prazos de pagamento]

CLÁUSULA SEXTA – DO REAJUSTE
[Índices e periodicidade de reajuste]

CLÁUSULA SÉTIMA – DA GARANTIA CONTRATUAL
[Tipo e valor da garantia exigida]

CLÁUSULA OITAVA – DAS OBRIGAÇÕES DA CONTRATADA
[Lista de obrigações da parte contratada]

CLÁUSULA NONA – DAS OBRIGAÇÕES DA CONTRATANTE
[Lista de obrigações do TJSP]

CLÁUSULA DÉCIMA – DA FISCALIZAÇÃO
[Regras de acompanhamento e fiscalização]

CLÁUSULA DÉCIMA PRIMEIRA – DAS PENALIDADES
[Sanções por descumprimento]

CLÁUSULA DÉCIMA SEGUNDA – DA RESCISÃO
[Condições para rescisão do contrato]

CLÁUSULA DÉCIMA TERCEIRA – DAS ALTERAÇÕES
[Regras para alterações contratuais]

CLÁUSULA DÉCIMA QUARTA – DO FORO
[Foro competente: Comarca de São Paulo/SP]

CLÁUSULA DÉCIMA QUINTA – DISPOSIÇÕES GERAIS
[Cláusulas gerais e complementares]

┌─────────────────────────────────────────────────┐
│                   ASSINATURAS                   │
│   São Paulo, [DD/MM/AAAA]                       │
│                                                 │
│   ___________________________________________   │
│              CONTRATANTE                        │
│   Tribunal de Justiça do Estado de São Paulo   │
│                                                 │
│   ___________________________________________   │
│              CONTRATADA                         │
└─────────────────────────────────────────────────┘
```

**Formatação Profissional**:
- ✅ Cores institucionais TJSP: RGB(0, 51, 102) nos headings
- ✅ Alinhamento justificado nos parágrafos
- ✅ Cabeçalho centralizado
- ✅ Quebras de página adequadas
- ✅ Espaçamento entre cláusulas
- ✅ Fonte profissional (Calibri padrão do DOCX)

---

## 🤖 Como o ContratoAgent Enriquece os Campos

### **Enriquecimento AGRESSIVO**

O ContratoAgent não apenas **copia** dados, ele **ELABORA** e **SINTETIZA**:

1. **Campo `objeto`**:
   ```python
   objeto = merge_values([
       tr_campos.get("especificacao_tecnica"),
       edital_campos.get("objeto"),
       etp_campos.get("objeto"),
       dfd_campos.get("objeto")
   ])
   # Resultado: texto de 300-600 caracteres consolidando todas as fontes
   ```

2. **Campo `valor_global`**:
   ```python
   valor_global = (
       dfd_campos.get("valor_estimado") or
       etp_campos.get("orcamento_previsto") or
       edital_campos.get("valor_estimado") or
       "A definir conforme proposta vencedora"
   )
   # Prioridade: DFD > ETP > Edital
   ```

3. **Campo `prazo_execucao`**:
   ```python
   prazo_execucao = (
       tr_campos.get("prazo_execucao") or
       etp_campos.get("prazo_estimado") or
       edital_campos.get("prazo_execucao") or
       ""
   )
   # Prioridade: TR > ETP > Edital
   ```

4. **Campo `obrigacoes_contratada`**:
   ```python
   obrigacoes_contratada = merge_values([
       edital_campos.get("obrigacoes_contratada"),
       tr_campos.get("obrigacoes_fornecedor")
   ])
   # Merge: Edital + TR
   ```

5. **Campo `foro`**:
   ```python
   foro = "Comarca de São Paulo/SP"
   # Padrão institucional TJSP (não enriquecido)
   ```

6. **Campo `partes_contratante`**:
   ```python
   partes_contratante = (
       "TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO, "
       "pessoa jurídica de direito público, "
       "inscrito no CNPJ sob o nº 51.174.001/0001-50, "
       "com sede na Praça da Sé, s/nº, São Paulo/SP"
   )
   # Hardcoded padrão TJSP
   ```

### **Contexto Visual para a IA**

O ContratoAgent prepara um contexto visual com emojis para ajudar a IA a priorizar informações:

```
📋 DFD (Documento de Formalização de Demanda):
- Objeto: [descrição]
- Justificativa: [texto]
- Valor estimado: [valor]

📐 ETP (Estudo Técnico Preliminar):
- Prazo estimado: [prazo]
- Resultados pretendidos: [texto]

📄 TR (Termo de Referência):
- Especificação técnica: [detalhes]
- Prazo de execução: [prazo]
- Fonte de recursos: [dotação]

📜 Edital de Licitação:
- Edital nº: [número]
- Modalidade: [pregão/concorrência]
- Obrigações da contratada: [lista]
```

---

## 🔍 Diagnóstico e Troubleshooting

### **Verificar Contexto Disponível**

No Módulo 08, expanda **"🔍 Informações de Diagnóstico"** para ver:
```json
{
  "modulos_anteriores_disponiveis": {
    "DFD": true,
    "ETP": true,
    "TR": true,
    "Edital": false
  },
  "campos_processados": 20,
  "timestamp_ultima_atualizacao": "2025-12-09T10:45:30",
  "buffer_docx_disponivel": true
}
```

### **Problemas Comuns**

#### ❌ "Campos vazios após processamento"
**Causa**: Insumo sem texto suficiente ou formato não suportado  
**Solução**:
1. Verifique se o arquivo tem pelo menos 50 caracteres de texto
2. PDFs escaneados sem OCR não funcionam (use PDF com texto selecionável)
3. Tente converter DOCX para TXT antes de enviar

#### ❌ "Erro ao gerar DOCX"
**Causa**: Biblioteca `python-docx` não disponível  
**Solução**:
1. O sistema usa fallback automático (versão simples)
2. Em Streamlit Cloud, a biblioteca deve estar em `requirements.txt`
3. Verifique logs: `[integration_contrato] python-docx não disponível`

#### ❌ "Contexto detectado: 0/4 módulos"
**Causa**: Nenhum módulo anterior foi processado nesta sessão  
**Solução**:
1. Processe ao menos um módulo antes (DFD, ETP, TR ou Edital)
2. Ou faça upload direto de um insumo de contrato
3. Ou preencha manualmente os campos

#### ❌ "Download button não aparece"
**Causa**: Buffer DOCX não foi criado  
**Solução**:
1. Verifique se clicou em "📤 Gerar DOCX Profissional"
2. Aguarde o spinner terminar
3. Verifique logs de erro na seção de diagnóstico

---

## 📊 Comparação: Antes vs Agora

| Aspecto | ❌ Antes (v2024) | ✅ Agora (v2025.1) |
|---------|------------------|-------------------|
| **Campos** | 13 campos básicos | **20 campos completos** |
| **Defaults** | Hardcoded ("12 meses...") | **Campos vazios** |
| **IA** | Prompt genérico direto | **ContratoAgent especializado** |
| **Contexto** | Não integrava DFD/ETP/TR | **Merge AGRESSIVO de 4 módulos** |
| **Insumos** | Não aparecia em Insumos | **Opção "CONTRATO" disponível** |
| **DOCX** | 13 seções simples | **15 cláusulas profissionais** |
| **Formatação** | Sem cores, sem alinhamento | **RGB(0,51,102), justificado, institucional** |
| **Buffer** | Download direto (erro Cloud) | **BytesIO buffer strategy** |
| **Enriquecimento** | Copia campos literalmente | **ELABORA + SINTETIZA + MERGE** |

---

## 🎓 Base Legal

Todos os contratos gerados seguem a **Lei Federal nº 14.133/2021** (Nova Lei de Licitações e Contratos Administrativos), incluindo:

- **Art. 92**: Formalização do contrato
- **Art. 93**: Cláusulas necessárias
- **Art. 104**: Alterações contratuais
- **Art. 137**: Rescisão contratual
- **Art. 156**: Penalidades administrativas

---

## 🚀 Próximos Passos

Após usar o Módulo Contrato, você pode:

1. **Validar o Contrato** (futuro): Usar o Validador de Contratos (similar ao Validador de Editais)
2. **Integrar com Sistema de Gestão**: Exportar JSON para integração com sistemas externos
3. **Arquivar**: Salvar DOCX e JSON em `exports/` para histórico
4. **Refinar**: Ajustar manualmente os campos e regerar o DOCX

---

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique os logs: `[integration_contrato]` no terminal
- Expanda "🔍 Informações de Diagnóstico" no Módulo 08
- Consulte este guia: `GUIA_MODULO_CONTRATO.md`

---

**Versão**: v2025.1  
**Última atualização**: 09/12/2024  
**Autor**: Engenheiro Synapse – SAAB/TJSP
