# 📘 Manual do Usuário – Projeto SAAB-Tech

## Manual 06: Módulos Avançados

**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Tribunal de Justiça do Estado de São Paulo**  
**Secretaria de Administração e Abastecimento (SAAB)**

---


---

## 1. Visão Geral

### 1.1 O que são Módulos Avançados?

Os **Módulos Avançados** são ferramentas especializadas para **consolidação, comparação, versionamento e integração** da documentação gerada.

```
MÓDULOS AVANÇADOS:
├─ 13. 🧾 Relatório Técnico (Consolidação documental)
├─ 14. 🔍 Comparador (Análise de diferenças)
├─ 15. 🗂️ Registro de Versão (Controle de versões)
└─ 16. 🔗 Integração (SAJ ADM e sistemas externos)
```

### 1.2 Público-Alvo

| Módulo | Usuários | Finalidade |
|--------|----------|------------|
| **Relatório Técnico** | Todos | Exportar documentação completa |
| **Comparador** | Analistas/Gestores | Comparar versões de documentos |
| **Registro Versão** | Equipe técnica | Manter histórico de alterações |
| **Integração** | Administradores | Conectar com sistemas TJSP |

### 1.3 Quando Usar

✅ **Use módulos avançados quando:**
- Finalizar processo completo de contratação
- Comparar propostas ou versões de documentos
- Manter histórico formal de alterações
- Integrar com SAJ ADM ou outros sistemas
- Gerar documentação para auditoria externa

---

## 2. Módulo 13: Relatório Técnico

### 2.1 O que é o Relatório Técnico?

O **Módulo 🧾 Relatório Técnico** gera um **documento consolidado** contendo toda a documentação da contratação em um único arquivo profissional.

**Conteúdo:**
- Capa institucional TJSP
- Sumário executivo
- DFD completo
- ETP completo (27 seções)
- TR completo (9 seções)
- Edital completo
- Contrato completo
- Anexos e apêndices

### 2.2 Como Acessar

1. Na barra lateral, clique em **🧾 Relatório Técnico**
2. Sistema carrega interface de geração

### 2.3 Interface do Módulo

**Seleção de Conteúdo:**
```
┌────────────────────────────────────────────┐
│ 📋 Selecione documentos para incluir:      │
│                                            │
│ ☑ DFD - Formalização da Demanda           │
│ ☑ ETP - Estudos Técnicos Preliminares     │
│ ☑ TR - Termo de Referência                │
│ ☑ Edital - Minuta do Edital               │
│ ☑ Contrato - Minuta do Contrato           │
│ ☐ Anexos técnicos                         │
│ ☐ Pareceres jurídicos                     │
└────────────────────────────────────────────┘
```

**Opções de Formatação:**
```
⚙️ Configurações:
├─ Formato: [PDF] [DOCX] [Ambos]
├─ Incluir capa: [Sim] [Não]
├─ Incluir sumário: [Sim] [Não]
├─ Numeração de páginas: [Sim] [Não]
└─ Marca d'água: [Sim] [Não]
```

### 2.4 Passo a Passo

#### **Passo 1: Selecionar Documentos**

```
1. Marque os documentos desejados
2. Recomendado: Todos (DFD, ETP, TR, Edital, Contrato)
3. Para processo completo: 5 documentos principais
```

#### **Passo 2: Configurar Formatação**

```
1. Formato: AMBOS (PDF + DOCX)
2. Incluir capa: SIM
3. Incluir sumário: SIM
4. Numeração: SIM
5. Marca d'água: NÃO (ou "MINUTA" se não finalizado)
```

#### **Passo 3: Gerar Relatório**

```
1. Clique em [📤 Gerar Relatório Técnico Consolidado]
2. Sistema processa (~30-60 segundos)
3. Aguarde barra de progresso
```

#### **Passo 4: Download**

```
Sistema gera 2 arquivos:

1. relatorio_tecnico_[processo]_YYYYMMDD.pdf
   - 80-120 páginas
   - Não editável
   - Para impressão/auditoria

2. relatorio_tecnico_[processo]_YYYYMMDD.docx
   - Editável
   - Para ajustes finais
   - Mantém formatação
```

### 2.5 Estrutura do Relatório

**Seções do documento consolidado:**

```
RELATÓRIO TÉCNICO CONSOLIDADO
├─ CAPA (Brasão TJSP, processo, data)
├─ SUMÁRIO EXECUTIVO (2 páginas)
│  ├─ Objeto da contratação
│  ├─ Valor total
│  ├─ Prazo
│  └─ Resumo das etapas
│
├─ PARTE I - PLANEJAMENTO (40-50 páginas)
│  ├─ DFD (11 seções)
│  ├─ ETP (27 seções)
│  └─ TR (9 seções)
│
├─ PARTE II - LICITAÇÃO (30-40 páginas)
│  ├─ Edital (12 campos + cláusulas)
│  └─ Resultado da validação
│
├─ PARTE III - CONTRATAÇÃO (35-45 páginas)
│  ├─ Contrato (20 campos + 15 cláusulas)
│  └─ Anexos contratuais
│
├─ ANEXOS
│  ├─ Planilhas de custos
│  ├─ Pesquisas de preço
│  └─ Pareceres técnicos
│
└─ ASSINATURAS
   ├─ Responsável técnico
   ├─ Aprovação jurídica
   └─ Autorização superior
```

### 2.6 Quando Usar

**Use o Relatório Técnico para:**
- ✅ Submissão completa do processo
- ✅ Auditoria TCE/CGJ
- ✅ Arquivo permanente da contratação
- ✅ Apresentações para diretoria
- ✅ Documentação de processos complexos

---

## 3. Módulo 14: Comparador

### 3.1 O que é o Comparador?

O **Módulo 🔍 Comparador** permite **comparar duas versões** de um mesmo documento, identificando:
- Textos adicionados (verde)
- Textos removidos (vermelho)
- Textos modificados (amarelo)
- Estatísticas de alterações

### 3.2 Como Acessar

1. Na barra lateral, clique em **🔍 Comparador**
2. Sistema carrega interface de comparação

### 3.3 Interface do Módulo

**Upload de Arquivos:**
```
┌────────────────────────────────────────────┐
│ 📄 VERSÃO ORIGINAL (Antes)                 │
│ [📁 Selecionar arquivo...]                 │
│ Arquivo: TR_versao_1.docx                  │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ 📄 VERSÃO NOVA (Depois)                    │
│ [📁 Selecionar arquivo...]                 │
│ Arquivo: TR_versao_2.docx                  │
└────────────────────────────────────────────┘

[🔍 Comparar Documentos]
```

**Tipo de Comparação:**
```
⚙️ Opções:
├─ Modo: [Texto] [Estrutural] [Completo]
├─ Sensibilidade: [Alta] [Média] [Baixa]
└─ Ignorar: [Formatação] [Espaços] [Pontuação]
```

### 3.4 Resultado da Comparação

**Estatísticas:**
```
📊 RESUMO DAS ALTERAÇÕES

┌──────────────┬──────────┐
│ Adições      │    45    │
│ Remoções     │    12    │
│ Modificações │    28    │
│ Total        │    85    │
└──────────────┴──────────┘

Taxa de alteração: 15,3%
Similaridade: 84,7%
```

**Visualização Side-by-Side:**
```
┌─────────────────────┬─────────────────────┐
│  VERSÃO ORIGINAL    │   VERSÃO NOVA       │
├─────────────────────┼─────────────────────┤
│ Valor estimado:     │ Valor estimado:     │
│ R$ 800.000,00       │ R$ 850.000,00       │
│ ❌ removido          │ ✅ adicionado        │
│                     │                     │
│ Prazo: 10 meses     │ Prazo: 12 meses     │
│ 🔄 modificado        │ 🔄 modificado        │
└─────────────────────┴─────────────────────┘
```

**Visualização Inline:**
```
Valor estimado: R$ ❌800.000,00✅850.000,00
Prazo de execução: 🔄10→12 meses
```

### 3.5 Casos de Uso

**Caso 1: Comparar Propostas de Licitação**
```
Cenário: Empresa ajustou proposta técnica
1. Upload proposta_original.pdf
2. Upload proposta_revisada.pdf
3. Compare
4. Identifique alterações críticas
5. Valide conformidade
```

**Caso 2: Auditar Alterações no TR**
```
Cenário: TR foi revisado pela assessoria jurídica
1. Upload TR_versao_1.docx (original)
2. Upload TR_versao_2_juridico.docx (revisado)
3. Compare com sensibilidade ALTA
4. Exporte relatório de alterações
5. Aprove ou solicite ajustes
```

**Caso 3: Verificar Aditivo Contratual**
```
Cenário: Precisa verificar o que mudou no termo aditivo
1. Upload contrato_original.pdf
2. Upload termo_aditivo_1.pdf
3. Compare
4. Identifique cláusulas alteradas
5. Documente justificativas
```

### 3.6 Exportação

**Gerar Relatório de Comparação:**
```
1. Após comparação, clique em [📤 Exportar Relatório]
2. Escolha formato:
   - PDF (não editável, para auditoria)
   - DOCX (editável, com marcações track changes)
   - HTML (visualização web)
3. Sistema gera: comparacao_[data].pdf
```

**Conteúdo do relatório:**
- Resumo estatístico de alterações
- Lista detalhada de mudanças
- Visualização lado a lado
- Conclusões e recomendações

---

## 4. Módulo 15: Registro de Versão

### 4.1 O que é o Registro de Versão?

O **Módulo 🗂️ Registro de Versão** mantém **histórico completo** de todas as versões dos documentos, permitindo:
- Rastreamento de alterações
- Rollback para versões anteriores
- Auditoria de modificações
- Identificação de responsáveis

### 4.2 Como Acessar

1. Na barra lateral, clique em **🗂️ Gerar Registro de Versão**
2. Sistema carrega interface de versionamento

### 4.3 Interface do Módulo

**Seleção de Documento:**
```
┌────────────────────────────────────────────┐
│ 📄 Selecione o documento:                  │
│ ▼ [DFD                                 ]   │
│   ETP                                      │
│   TR                                       │
│   Edital                                   │
│   Contrato                                 │
└────────────────────────────────────────────┘
```

**Histórico de Versões:**
```
📋 HISTÓRICO - Termo de Referência

┌─────┬────────────┬──────────┬───────────┐
│ Ver │ Data       │ Usuário  │ Alteração │
├─────┼────────────┼──────────┼───────────┤
│ 5.0 │ 10/12/2025 │ Ana S.   │ Aprovação │
│ 4.2 │ 09/12/2025 │ João M.  │ Ajuste    │
│ 4.1 │ 08/12/2025 │ Maria L. │ Revisão   │
│ 4.0 │ 07/12/2025 │ Pedro C. │ Refator.  │
│ 3.0 │ 05/12/2025 │ Ana S.   │ Atualiz.  │
└─────┴────────────┴──────────┴───────────┘
```

**Ações Disponíveis:**
```
Para cada versão:
├─ [👁️ Visualizar] - Ver conteúdo
├─ [📥 Baixar] - Download do arquivo
├─ [🔄 Restaurar] - Voltar para esta versão
├─ [🔍 Comparar] - Comparar com outra versão
└─ [📝 Detalhes] - Ver metadados completos
```

### 4.4 Sistema de Versionamento

**Nomenclatura de Versões:**
```
FORMATO: X.Y

X = Versão principal (mudanças estruturais)
Y = Versão secundária (ajustes menores)

Exemplos:
1.0 → Primeira versão
1.1 → Ajuste pequeno
2.0 → Revisão completa
2.1 → Correção pontual
3.0 → Nova estrutura
```

**Regras de Incremento:**
```
Incremento PRINCIPAL (X):
- Mudança estrutural no documento
- Adição/remoção de seções
- Alteração de valores críticos
- Aprovação por superior

Incremento SECUNDÁRIO (Y):
- Correção de texto
- Ajuste de formatação
- Atualização de datas
- Complemento de informações
```

### 4.5 Metadados de Versão

**Informações registradas:**
```json
{
  "versao": "4.2",
  "data": "2025-12-09T14:35:22",
  "usuario": "João Marcos Silva",
  "matricula": "123456",
  "tipo_alteracao": "ajuste",
  "resumo": "Atualização do valor estimado conforme nova pesquisa de preços",
  "campos_alterados": ["valor_global", "composicao_custos"],
  "hash_md5": "a3c5f8d2...",
  "tamanho_bytes": 45620,
  "aprovacao": {
    "status": "pendente",
    "aprovador": "Maria Lucia Santos",
    "data_aprovacao": null
  }
}
```

### 4.6 Operações Avançadas

#### **Restaurar Versão Anterior**

```
Cenário: Erro grave na versão atual, precisa voltar

1. Acesse [🗂️ Registro de Versão]
2. Selecione documento: TR
3. Identifique última versão boa: 4.1
4. Clique em [🔄 Restaurar] na linha 4.1
5. Confirme ação:
   ⚠️ "Versão atual (5.0) será arquivada.
       Versão 4.1 se tornará 5.1.
       Continuar?"
6. Confirme
7. Sistema restaura e cria nova entrada
```

**Resultado:**
```
Novo histórico:
5.1 - 10/12/2025 - Restauração da v4.1
5.0 - 10/12/2025 - (arquivada)
4.2 - 09/12/2025
4.1 - 08/12/2025 ← restaurada como 5.1
```

#### **Comparar Duas Versões**

```
1. Selecione versão base: 4.0
2. Selecione versão comparação: 5.0
3. Clique em [🔍 Comparar]
4. Sistema abre Módulo Comparador automaticamente
5. Visualize diferenças
```

### 4.7 Exportação de Histórico

**Gerar Relatório de Auditoria:**
```
1. Clique em [📤 Exportar Histórico Completo]
2. Escolha período:
   - Última semana
   - Último mês
   - Últimos 3 meses
   - Todo o histórico
3. Formato: PDF
4. Download: historico_versoes_TR_YYYYMMDD.pdf
```

**Conteúdo:**
- Linha do tempo de alterações
- Estatísticas (total de versões, frequência)
- Principais contribuidores
- Gráfico de evolução do documento
- Lista detalhada de cada versão

---

## 5. Módulo 16: Integração

### 5.1 O que é o Módulo Integração?

O **Módulo 🔗 Integração** conecta o Projeto SAAB-Tech com **sistemas externos** do TJSP:
- SAJ ADM (Sistema de Automação da Justiça - Administrativo)
- Portal de Compras TJSP
- Sistema de Protocolo
- APIs externas

### 5.2 Como Acessar

1. Na barra lateral, clique em **🔗 Integração**
2. Sistema carrega interface de conexão

### 5.3 Interface do Módulo

**Status de Conexões:**
```
🔗 INTEGRAÇÕES ATIVAS

┌────────────────┬──────────┬─────────────┐
│ Sistema        │ Status   │ Última Sinc │
├────────────────┼──────────┼─────────────┤
│ SAJ ADM        │ ✅ Ativo │ 10/12 14:30 │
│ Portal Compras │ ⚠️ Config │ N/A         │
│ Protocolo TJSP │ ✅ Ativo │ 10/12 09:15 │
│ API Externa    │ ❌ Inativo│ N/A         │
└────────────────┴──────────┴─────────────┘
```

**Ações Disponíveis:**
```
Para cada integração:
├─ [⚙️ Configurar] - Definir parâmetros
├─ [🔄 Sincronizar] - Forçar sincronização
├─ [📊 Logs] - Ver histórico de operações
└─ [❌ Desativar] - Desconectar temporariamente
```

### 5.4 Integração com SAJ ADM

**O que é sincronizado:**

**Exportação (SAAB-Tech → SAJ ADM):**
- ✅ Dados do processo administrativo
- ✅ Documentos gerados (DFD, ETP, TR)
- ✅ Status da contratação
- ✅ Valores e prazos

**Importação (SAJ ADM → SAAB-Tech):**
- ✅ Número do processo
- ✅ Dados da unidade solicitante
- ✅ Histórico de tramitação
- ✅ Pareceres anexados

**Como Configurar:**

```
1. Clique em [⚙️ Configurar] na linha SAJ ADM
2. Preencha credenciais:
   - URL do servidor: https://saj.tjsp.jus.br/api
   - Usuário: [seu_usuario]
   - Senha: [sua_senha]
   - Token API: [token_gerado]
3. Teste conexão: [🧪 Testar]
4. Se sucesso: "✅ Conexão estabelecida"
5. Salve configuração
```

**Como Sincronizar:**

```
Cenário: Finalizar TR e enviar para SAJ ADM

1. Finalize TR no SAAB-Tech
2. Acesse [🔗 Integração]
3. Na linha SAJ ADM, clique [🔄 Sincronizar]
4. Selecione dados:
   ☑ TR completo
   ☑ Anexos técnicos
   ☐ Histórico de versões
5. Clique [📤 Enviar para SAJ ADM]
6. Aguarde (~10-20 segundos)
7. Confirmação:
   "✅ TR sincronizado com SAJ ADM
    Processo: 2025.00.123456-7
    Protocolo: 98765/2025"
```

### 5.5 Integração com Portal de Compras

**Funcionalidades:**
- Publicação automática de editais
- Importação de propostas recebidas
- Atualização de status da licitação
- Notificações automáticas

**Como Publicar Edital:**

```
1. Finalize Edital no SAAB-Tech
2. Acesse [🔗 Integração]
3. Clique [⚙️ Configurar] no Portal Compras
4. Configure:
   - Modalidade: Pregão Eletrônico
   - Data abertura: 15/01/2026 10:00
   - Prazo propostas: 10 dias
5. Clique [📤 Publicar Edital]
6. Sistema:
   - Valida edital
   - Envia para Portal
   - Retorna número do pregão
7. Confirmação:
   "✅ Edital publicado
    Pregão nº 123/2026
    Link: https://compras.tjsp.jus.br/pregao/123"
```

### 5.6 Logs de Integração

**Visualizar histórico:**
```
1. Clique em [📊 Logs] de qualquer integração
2. Veja eventos:

┌────────────────┬─────────┬────────────┐
│ Data/Hora      │ Ação    │ Resultado  │
├────────────────┼─────────┼────────────┤
│ 10/12 14:30:15 │ Exportar│ ✅ Sucesso │
│ 10/12 09:15:42 │ Importar│ ✅ Sucesso │
│ 09/12 16:45:03 │ Exportar│ ❌ Erro    │
│ 09/12 16:50:12 │ Exportar│ ✅ Sucesso │
└────────────────┴─────────┴────────────┘
```

**Detalhes de erro:**
```
Clique em linha com erro:

❌ ERRO DE INTEGRAÇÃO
Data: 09/12/2025 16:45:03
Sistema: SAJ ADM
Operação: Exportar TR

Mensagem:
"Timeout na conexão com servidor SAJ ADM.
 Servidor não respondeu em 30 segundos."

Ação sugerida:
1. Verificar conexão de rede
2. Tentar novamente em alguns minutos
3. Se persistir, contatar suporte TI
```

### 5.7 Segurança

**Autenticação:**
- OAuth 2.0 para APIs externas
- Credenciais criptografadas
- Tokens com expiração automática
- Renovação automática de tokens

**Auditoria:**
- Registro de todas as operações
- Identificação do usuário responsável
- Timestamp de cada ação
- IP de origem das requisições

---

## 6. Casos Práticos

### 6.1 Caso 1: Documentação Completa para TCE

**Situação:**
```
Tribunal de Contas solicita documentação completa 
do processo de contratação de limpeza.
```

**Ação:**
```
1. Acesse [🧾 Relatório Técnico]
2. Marque TODOS os documentos:
   ☑ DFD
   ☑ ETP
   ☑ TR
   ☑ Edital
   ☑ Contrato
   ☑ Anexos técnicos
3. Configure:
   - Formato: PDF
   - Capa: Sim
   - Sumário: Sim
   - Marca d'água: Não
4. Gere relatório
5. Resultado: 115 páginas PDF
6. Envie ao TCE
```

**Tempo:** ~5 minutos

### 6.2 Caso 2: Auditoria de Alterações

**Situação:**
```
Assessoria jurídica questiona alterações feitas 
no TR entre versões 3.0 e 5.0.
```

**Ação:**
```
1. Acesse [🗂️ Registro de Versão]
2. Selecione: TR
3. Identifique versões:
   - 3.0: 05/12/2025
   - 5.0: 10/12/2025
4. Clique [🔍 Comparar] na v3.0
5. Selecione v5.0 para comparação
6. Sistema mostra:
   - 23 adições
   - 8 remoções
   - 15 modificações
7. Exporte relatório PDF
8. Envie à assessoria com justificativas
```

**Tempo:** ~10 minutos

### 6.3 Caso 3: Publicação de Edital

**Situação:**
```
Edital finalizado e validado, pronto para 
publicação no Portal de Compras.
```

**Ação:**
```
1. Valide edital: score > 85
2. Acesse [🔗 Integração]
3. Configure Portal de Compras:
   - Data abertura: 20/01/2026 10:00
   - Prazo: 15 dias
4. Clique [📤 Publicar Edital]
5. Aguarde sincronização
6. Confirmação:
   "✅ Pregão nº 134/2026 publicado"
7. Sistema envia notificações automáticas
```

**Tempo:** ~3 minutos

### 6.4 Caso 4: Rollback de Versão

**Situação:**
```
Versão 6.0 do Contrato tem erro grave.
Precisa voltar para v5.2 (última boa).
```

**Ação:**
```
1. Acesse [🗂️ Registro de Versão]
2. Selecione: Contrato
3. Identifique v5.2 (08/12/2025)
4. Clique [🔄 Restaurar]
5. Confirme:
   "⚠️ v6.0 será arquivada.
       v5.2 se tornará v6.1"
6. Confirme
7. Sistema restaura
8. Nova versão: 6.1 (baseada em 5.2)
9. Revise e corrija o problema
10. Salve como v6.2
```

**Tempo:** ~5 minutos

---

## 📚 Próximos Passos

Você completou o aprendizado dos **Módulos Avançados**!

Continue para:
- **Manual 07** – FAQ e Troubleshooting (guia de problemas comuns e suporte)

---

## 📞 Suporte Técnico

**Dúvidas sobre módulos avançados?**

📧 saab-tech@tjsp.jus.br  
☎️ (11) XXXX-XXXX  
🕐 Segunda a Sexta, 9h-18h

**Suporte de Integração:**  
📧 ti.integracao@tjsp.jus.br

**Suporte SAJ ADM:**  
📧 saj.suporte@tjsp.jus.br

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Manual 06/07 – Módulos Avançados*
