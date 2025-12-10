# 📘 Manual do Usuário – Projeto SAAB-Tech

## Manual 01: Introdução e Primeiros Passos

**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Tribunal de Justiça do Estado de São Paulo**  
**Secretaria de Administração e Abastecimento (SAAB)**

---


---

## 📑 Índice

1. Visão Geral do Sistema
2. Objetivos e Benefícios
3. Arquitetura Técnica
4. Requisitos de Acesso
5. Primeiro Acesso
6. Interface e Navegação
7. Conceitos Fundamentais
8. Fluxo Completo de Trabalho
9. Boas Práticas

---

## 1. Visão Geral do Sistema

### 1.1 O que é o Projeto SAAB-Tech?

O **Projeto SAAB-Tech** (anteriormente SynapseNext) é uma plataforma institucional de **inteligência artificial aplicada a contratações públicas**, desenvolvida especificamente para o Tribunal de Justiça do Estado de São Paulo (TJSP).

O sistema automatiza e guia todo o processo de elaboração dos documentos da **fase interna de licitação**, desde a identificação da necessidade até a formalização do contrato, seguindo rigorosamente a **Lei Federal nº 14.133/2021** (Nova Lei de Licitações).

### 1.2 Principais Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **🔧 Tutoria Guiada** | Jornada interativa passo a passo para preenchimento dos artefatos |
| **🤖 IA Semântica** | Agentes especializados para cada tipo de documento (DFD, ETP, TR, Edital, Contrato) |
| **✅ Validação em Tempo Real** | Análise automática de coerência, completude e conformidade legal |
| **📄 Exportação Institucional** | Geração de documentos DOCX e PDF padronizados TJSP |
| **📚 Base Normativa** | Integração com legislação, instruções normativas e jurisprudência do TJSP |
| **⚠️ Sistema de Alertas** | Monitoramento de pendências e inconsistências entre documentos |
| **📊 Painéis de Governança** | Indicadores de desempenho e conformidade para gestores |

### 1.3 Módulos do Sistema

O Projeto SAAB-Tech é composto por **16 módulos integrados**:

#### **Módulos de Planejamento (Fase Interna)**
1. **🔧 Insumos** – Upload e processamento de documentos de entrada
2. **📄 DFD** – Documento de Formalização da Demanda
3. **📘 ETP** – Estudos Técnicos Preliminares
4. **📑 TR** – Termo de Referência

#### **Módulos de Licitação**
5. **📜 Edital** – Minuta do Edital de Licitação
6. **🧩 Validador de Editais** – Conformidade com Lei 14.133/2021
7. **📜 Contrato** – Contrato Administrativo

#### **Módulos de Governança e Análise**
8. **⚠️ Alertas** – Painel de pendências e inconsistências
9. **💡 Análise de Desempenho** – Métricas técnicas e indicadores
10. **📊 Painel de Governança** – Consolidação de auditorias
11. **📈 Painel Executivo** – Visão gerencial estratégica

#### **Módulos Avançados**
12. **🧾 Relatório Técnico** – Documentação consolidada
13. **🔍 Comparador** – Análise comparativa entre versões
14. **🗂️ Registro de Versão** – Controle de histórico
15. **🔗 Integração** – Conectores com sistemas externos (SAJ ADM)

---

## 2. Objetivos e Benefícios

### 2.1 Objetivos Estratégicos

- ✅ **Reduzir tempo de elaboração** de documentos licitatórios (até 70%)
- ✅ **Aumentar conformidade legal** com a Lei 14.133/2021
- ✅ **Padronizar documentação** institucional do TJSP
- ✅ **Minimizar erros e inconsistências** entre documentos
- ✅ **Facilitar auditoria e fiscalização** com rastreabilidade completa
- ✅ **Capacitar servidores** através de tutoria inteligente

### 2.2 Benefícios para o Usuário

| Perfil | Benefícios |
|--------|-----------|
| **Servidor Operacional** | Interface guiada, preenchimento automático, sugestões inteligentes |
| **Gestor de Área** | Validação prévia, redução de retrabalho, documentos padronizados |
| **Assessor Jurídico** | Conformidade legal automatizada, checklist institucional |
| **Diretor/Secretário** | Painéis de governança, indicadores de desempenho, auditoria |

### 2.3 Conformidade Legal

O sistema está alinhado com:
- 📜 **Lei Federal nº 14.133/2021** (Nova Lei de Licitações)
- 📜 **Decreto Federal nº 11.462/2023** (Regulamentação)
- 📜 **Instruções Normativas TJSP** (SAAB/STI)
- 📜 **Jurisprudência do TCE-SP** (Tribunal de Contas)

---

## 3. Arquitetura Técnica

### 3.1 Tecnologias Utilizadas

```
┌─────────────────────────────────────────┐
│         INTERFACE DO USUÁRIO            │
│         Streamlit Web Interface         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        CAMADA DE AGENTES DE IA          │
│  • ContratoAgent  • EditalAgent         │
│  • ETPAgent       • TRAgent             │
│  • DocumentAgent  • GuideAgent          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      MOTOR DE PROCESSAMENTO             │
│  OpenAI GPT-4 + LangChain               │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       BASE DE CONHECIMENTO              │
│  • Legislação  • Modelos                │
│  • Checklists  • Jurisprudência         │
└─────────────────────────────────────────┘
```

### 3.2 Stack Tecnológico

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| **Frontend** | Streamlit | 1.28+ |
| **Backend** | Python | 3.11+ |
| **IA** | OpenAI GPT-4 | API v1 |
| **Framework IA** | LangChain | 0.1+ |
| **Processamento PDF** | PyMuPDF (fitz) | 1.23+ |
| **Processamento DOCX** | python-docx | 1.1+ |
| **Validação** | YAML + JSON Schema | - |
| **Exportação** | ReportLab + python-docx | - |

### 3.3 Arquitetura de Dados

```
exports/
├── insumos/
│   └── json/           # Arquivos brutos processados
├── dfd_data.json       # DFD estruturado
├── etp_data.json       # ETP estruturado
├── tr_data.json        # TR estruturado
├── edital_data.json    # Edital estruturado
├── contrato_data.json  # Contrato estruturado
└── backups/            # Versões anteriores
```

---

## 4. Requisitos de Acesso

### 4.1 Requisitos Técnicos

#### **Hardware Mínimo**
- **Processador:** Intel Core i3 / AMD Ryzen 3 ou superior
- **Memória RAM:** 4 GB (recomendado 8 GB)
- **Armazenamento:** 500 MB livres
- **Conexão:** Internet banda larga (mínimo 5 Mbps)

#### **Software**
- **Sistema Operacional:** Windows 10+, macOS 10.15+, ou Linux
- **Navegador:** Google Chrome 100+, Firefox 100+, Edge 100+, Safari 15+
- **Resolução:** Mínimo 1366x768 pixels (recomendado 1920x1080)

### 4.2 Requisitos Institucionais

- ✅ **Vínculo funcional** com o TJSP
- ✅ **Credenciais de acesso** fornecidas pela SAAB
- ✅ **Treinamento básico** em contratações públicas (desejável)
- ✅ **Conhecimento** da Lei 14.133/2021 (básico)

### 4.3 Permissões de Usuário

| Perfil | Permissões |
|--------|-----------|
| **Operador** | Criar/editar documentos, visualizar próprios registros |
| **Gestor** | Todas as anteriores + validar documentos, gerar relatórios |
| **Auditor** | Visualização completa, exportar dados, painéis de governança |
| **Administrador** | Acesso total, configurações de sistema, gestão de usuários |

---

## 5. Primeiro Acesso

### 5.1 Acessando o Sistema

1. **Abra seu navegador** (Chrome, Firefox ou Edge recomendados)

2. **Digite o endereço oficial:**
   ```
   https://saab-tech.tjsp.jus.br
   ```
   *(Endereço de exemplo - solicite o URL oficial à SAAB)*

3. **Aguarde o carregamento** da página inicial

### 5.2 Tela de Boas-Vindas

Ao acessar pela primeira vez, você verá:

```
╔════════════════════════════════════════════════╗
║                                                ║
║         🏛️ Projeto SAAB-Tech                  ║
║    Tribunal de Justiça de São Paulo           ║
║                                                ║
║  Sistema de Inteligência Artificial para      ║
║     Contratações Públicas (Lei 14.133/2021)   ║
║                                                ║
║           [🚀 Começar Nova Jornada]           ║
║                                                ║
╚════════════════════════════════════════════════╝
```

### 5.3 Configuração Inicial

**Não é necessária configuração manual!** O sistema está pré-configurado e pronto para uso.

#### **O que o Sistema Faz Automaticamente:**
- ✅ Cria diretórios de trabalho
- ✅ Carrega base normativa atualizada
- ✅ Inicializa agentes de IA
- ✅ Prepara validadores institucionais

---

## 6. Interface e Navegação

### 6.1 Estrutura da Interface

A interface é dividida em **3 áreas principais**:

```
┌─────────────────────────────────────────────────────────┐
│  🏛️ CABEÇALHO INSTITUCIONAL                             │
│  Projeto SAAB-Tech | TJSP                               │
└─────────────────────────────────────────────────────────┘
┌──────────────┬──────────────────────────────────────────┐
│              │                                          │
│   MENU       │     ÁREA DE TRABALHO PRINCIPAL          │
│  LATERAL     │                                          │
│              │  - Formulários                           │
│  • Home      │  - Botões de ação                        │
│  • Insumos   │  - Visualizações                         │
│  • DFD       │  - Resultados                            │
│  • ETP       │                                          │
│  • TR        │                                          │
│  • Edital    │                                          │
│  • Validador │                                          │
│  • Contrato  │                                          │
│  • Alertas   │                                          │
│  • ...       │                                          │
│              │                                          │
└──────────────┴──────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│  RODAPÉ INFORMATIVO                                     │
│  © 2025 TJSP - Projeto SAAB-Tech v2025.1               │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Menu Lateral (Sidebar)

O **menu lateral** contém todos os módulos do sistema organizados sequencialmente:

| Ícone | Módulo | Função |
|-------|--------|--------|
| 🏠 | **Home** | Página inicial e visão geral |
| 🔧 | **Insumos** | Upload de documentos |
| 📄 | **DFD** | Formalização da Demanda |
| 📘 | **ETP** | Estudos Técnicos Preliminares |
| 📑 | **TR** | Termo de Referência |
| 📜 | **Edital** | Minuta do Edital |
| 🧩 | **Validador de Editais** | Conformidade legal |
| 📜 | **Contrato** | Contrato Administrativo |
| ⚠️ | **Alertas** | Pendências e inconsistências |
| 💡 | **Análise de Desempenho** | Métricas técnicas |
| 📊 | **Painel de Governança** | Auditoria consolidada |
| 📈 | **Painel Executivo** | Visão gerencial |
| 🧾 | **Relatório Técnico** | Documentação completa |
| 🔍 | **Comparador** | Análise de versões |
| 🗂️ | **Registro de Versão** | Histórico |
| 🔗 | **Integração** | Sistemas externos |

### 6.3 Elementos da Interface

#### **Botões de Ação**
```css
🚀 Processar com IA      → Botão primário (azul TJSP)
💾 Salvar                → Botão secundário (verde)
📤 Exportar DOCX         → Botão de exportação (cinza)
🔄 Recarregar            → Botão de atualização
```

#### **Áreas de Formulário**
- **Text Input:** Campos de texto simples (1 linha)
- **Text Area:** Campos de texto expandido (múltiplas linhas)
- **Select Box:** Listas suspensas
- **Date Input:** Seleção de datas
- **File Uploader:** Upload de arquivos

#### **Feedback Visual**
```
✅ Mensagem de sucesso   → Fundo verde
⚠️ Aviso                 → Fundo amarelo
❌ Erro                  → Fundo vermelho
ℹ️ Informação            → Fundo azul claro
```

### 6.4 Navegação Eficiente

#### **Dica 1: Siga a Ordem dos Módulos**
Para uma contratação completa, siga esta sequência:
```
1️⃣ Insumos → 2️⃣ DFD → 3️⃣ ETP → 4️⃣ TR → 5️⃣ Edital → 6️⃣ Contrato
```

#### **Dica 2: Use Atalhos de Teclado**
- **Ctrl + S** – Salvar (quando aplicável)
- **F5** – Recarregar página
- **Ctrl + F** – Buscar na página

#### **Dica 3: Aproveite o Contexto Integrado**
O sistema **lembra automaticamente** dos dados preenchidos nos módulos anteriores!

---

## 7. Conceitos Fundamentais

### 7.1 O que são "Insumos"?

**Insumos** são documentos de entrada que você fornece ao sistema para iniciar o processamento. Podem ser:

- 📄 **PDF** – Documentos escaneados ou digitais
- 📄 **DOCX** – Arquivos do Microsoft Word
- 📄 **TXT** – Arquivos de texto simples

**Exemplos de insumos:**
- Memorandos de solicitação de compra
- Atas de reunião técnica
- Levantamentos de necessidades
- Minutas preliminares
- Contratos de referência

### 7.2 O que são "Agentes de IA"?

**Agentes** são módulos de inteligência artificial especializados em processar e estruturar cada tipo de documento:

| Agente | Especialização |
|--------|----------------|
| **DocumentAgent** | Extração genérica de texto e estruturação inicial |
| **ContratoAgent** | Extração de 20 campos de contratos administrativos |
| **EditalAgent** | Extração de 12 campos de editais de licitação |
| **ETPAgent** | Estruturação de 27 seções dos Estudos Técnicos |
| **TRAgent** | Estruturação de 9 seções do Termo de Referência |
| **GuideAgent** | Orientação e tutoria ao usuário |

### 7.3 Fluxo de Processamento

```mermaid
graph LR
    A[Upload Insumo] --> B[Extração de Texto]
    B --> C[Agente de IA]
    C --> D[Estruturação]
    D --> E[Validação]
    E --> F[Persistência JSON]
    F --> G[Exibição no Formulário]
```

1. **Upload:** Você envia um arquivo
2. **Extração:** Sistema lê o conteúdo
3. **Processamento IA:** Agente analisa e estrutura
4. **Validação:** Sistema verifica conformidade
5. **Armazenamento:** Dados salvos em JSON
6. **Exibição:** Campos preenchidos no formulário

### 7.4 Persistência de Dados

**Todos os dados são salvos automaticamente!**

Os arquivos ficam armazenados em:
```
exports/
├── dfd_data.json        ← Seus dados do DFD
├── etp_data.json        ← Seus dados do ETP
├── tr_data.json         ← Seus dados do TR
├── edital_data.json     ← Seus dados do Edital
└── contrato_data.json   ← Seus dados do Contrato
```

**Você pode:**
- ✅ Fechar o navegador sem perder dados
- ✅ Continuar o trabalho depois
- ✅ Recuperar versões anteriores (backups automáticos)

---

## 8. Fluxo Completo de Trabalho

### 8.1 Jornada Típica de Contratação

#### **Cenário: Contratação de Serviços de Manutenção Predial**

**Passo 1: Preparar Insumo**
- Reunir informações sobre a necessidade
- Ter em mãos: memorando, levantamento técnico, orçamentos

**Passo 2: Módulo Insumos (🔧)**
```
1. Acessar módulo "Insumos"
2. Clicar em "Browse files"
3. Selecionar arquivo PDF/DOCX
4. Escolher destino: "DFD"
5. Clicar em "🚀 Processar"
6. Aguardar (~10-30 segundos)
```

**Passo 3: Módulo DFD (📄)**
```
1. Acessar módulo "DFD"
2. Ver campos pré-preenchidos pela IA
3. Revisar e ajustar conforme necessário
4. Clicar em "💾 Salvar"
5. Clicar em "📤 Gerar DOCX"
6. Baixar documento padronizado
```

**Passo 4: Módulo ETP (📘)**
```
1. Acessar módulo "ETP"
2. Sistema detecta DFD automaticamente
3. Clicar em "✨ Processar com IA"
4. Revisar 27 seções estruturadas
5. Ajustar campos se necessário
6. Salvar e exportar DOCX
```

**Passo 5: Módulo TR (📑)**
```
1. Acessar módulo "TR"
2. Sistema integra DFD + ETP
3. Processar ou preencher manualmente
4. Revisar 9 seções técnicas
5. Exportar DOCX institucional
```

**Passo 6: Módulo Edital (📜)**
```
1. Acessar módulo "Edital"
2. Sistema consolida DFD + ETP + TR
3. Processar minuta com IA
4. Revisar 12 campos obrigatórios
5. Exportar minuta do edital
```

**Passo 7: Validador de Editais (🧩)**
```
1. Acessar "Validador de Editais"
2. Clicar em "Usar Edital Gerado"
3. Selecionar tipo de contratação
4. Executar validação completa
5. Analisar score de conformidade
6. Exportar relatório de validação
```

**Passo 8: Módulo Contrato (📜)**
```
1. Acessar módulo "Contrato"
2. Sistema integra todos os módulos anteriores
3. Gerar contrato com contexto completo
4. Revisar 20 campos do contrato
5. Exportar contrato final em DOCX
```

**Passo 9: Monitoramento (⚠️)**
```
1. Acessar módulo "Alertas"
2. Verificar pendências detectadas
3. Corrigir inconsistências
4. Atualizar documentos conforme necessário
```

### 8.2 Tempo Estimado por Etapa

| Etapa | Sem Sistema | Com SAAB-Tech | Economia |
|-------|-------------|---------------|----------|
| DFD | 3-4 horas | 30-45 minutos | **75%** |
| ETP | 8-12 horas | 1-2 horas | **85%** |
| TR | 6-8 horas | 1-1,5 horas | **80%** |
| Edital | 4-6 horas | 45-60 minutos | **80%** |
| Validação | 2-3 horas | 10-15 minutos | **90%** |
| Contrato | 3-4 horas | 30-45 minutos | **80%** |
| **TOTAL** | **26-37 horas** | **4-6 horas** | **~80%** |

---

## 9. Boas Práticas

### 9.1 Preparação de Insumos

✅ **FAÇA:**
- Use documentos com texto pesquisável (não imagens escaneadas)
- Organize informações antes do upload
- Prefira arquivos DOCX ou PDF com OCR
- Inclua dados completos (valores, prazos, responsáveis)

❌ **EVITE:**
- PDFs com páginas em branco
- Arquivos corrompidos ou com erro
- Textos excessivamente técnicos sem contexto
- Informações contraditórias no mesmo documento

### 9.2 Revisão de Conteúdo Gerado

✅ **SEMPRE REVISE:**
- Valores monetários e datas
- Nomes de pessoas e órgãos
- Fundamentação legal
- Especificações técnicas críticas

⚠️ **A IA é uma assistente, não substitui análise humana!**

### 9.3 Organização do Trabalho

📁 **Mantenha backups externos:**
- Faça download dos DOCX gerados
- Guarde em pasta compartilhada da equipe
- Mantenha controle de versões

📅 **Respeite a sequência:**
- Complete um módulo antes de avançar
- Não pule etapas obrigatórias (DFD → ETP → TR)
- Use o validador antes de finalizar

### 9.4 Segurança da Informação

🔒 **Dados Sensíveis:**
- Não compartilhe credenciais de acesso
- Não divulgue documentos antes da publicação oficial
- Feche a sessão ao finalizar o trabalho
- Respeite as políticas de segurança do TJSP

### 9.5 Quando Solicitar Suporte

📞 **Entre em contato com SAAB se:**
- Sistema apresentar erro técnico persistente
- Dúvidas sobre conformidade legal
- Necessidade de treinamento adicional
- Sugestões de melhoria

---

## 📞 Suporte e Contato

**Secretaria de Administração e Abastecimento (SAAB)**  
Tribunal de Justiça do Estado de São Paulo

📧 **E-mail:** saab-tech@tjsp.jus.br  
☎️ **Telefone:** (11) XXXX-XXXX  
🌐 **Portal:** https://saab.tjsp.jus.br  

**Horário de Atendimento:**  
Segunda a Sexta, das 9h às 18h

---

## 📚 Próximos Passos

Agora que você conhece o básico do sistema, consulte os manuais específicos:

- 📘 **Manual 02** – Módulos de Planejamento (Insumos, DFD, ETP, TR)
- 📘 **Manual 03** – Módulos de Licitação (Edital, Validador, Contrato)
- 📘 **Manual 04** – Módulos de Governança (Alertas, Painéis)
- 📘 **Manual 05** – Módulos Avançados (Relatórios, Comparador, Integração)
- 📘 **Manual 06** – FAQ e Troubleshooting

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Uso restrito ao TJSP. Distribuição não autorizada é proibida.*
