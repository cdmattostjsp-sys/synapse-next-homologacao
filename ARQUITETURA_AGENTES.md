# 🏗️ Arquitetura de Agentes Especializados - SynapseNext

## 📋 Visão Geral

O SynapseNext implementa uma **arquitetura de agentes especializados**, onde cada tipo de documento (DFD, ETP, TR, Contrato, etc.) possui seu próprio agente otimizado.

### ❌ **Problema da Arquitetura Anterior**

- **Um único agente genérico** (`document_agent.py`) tentava processar todos os artefatos
- **Prompts genéricos** não capturavam as especificidades de cada documento
- **Mapeamento incorreto** entre campos extraídos e formulários
- **Extração incompleta** de dados administrativos

### ✅ **Solução: Agentes Especializados**

Cada agente:
- ✅ Conhece a **estrutura específica** do documento
- ✅ Tem **prompt otimizado** com instruções precisas
- ✅ Retorna **campos padronizados** mapeados para o formulário
- ✅ Extrai **dados administrativos** corretamente

---

## 🎯 Agentes Implementados

### 1️⃣ **DFDAgent** (`agents/document_agent.py`)

**Responsável por**: Documentos de Formalização de Demanda

**Estrutura**:
```python
{
  "unidade_demandante": str,
  "responsavel": str,
  "prazo_estimado": str,
  "valor_estimado": str,
  "descricao_necessidade": str,
  "motivacao": str,
  "texto_narrativo": str,
  "secoes": {
    "Contexto Institucional": str,
    "Diagnóstico da Situação Atual": str,
    "Fundamentação da Necessidade": str,
    "Objetivos da Contratação": str,
    "Escopo Inicial da Demanda": str,
    "Resultados Esperados": str,
    "Benefícios Institucionais": str,
    "Justificativa Legal": str,
    "Riscos da Não Contratação": str,
    "Requisitos Mínimos": str,
    "Critérios de Sucesso": str
  },
  "lacunas": list
}
```

**11 seções** organizadas para governança moderna

---

### 2️⃣ **ETPAgent** (`agents/etp_agent.py`) ✅ NOVO

**Responsável por**: Estudos Técnicos Preliminares (Lei 14.133/2021)

**Estrutura**:
```python
{
  "unidade_demandante": str,
  "responsavel": str,
  "prazo_estimado": str,
  "valor_estimado": str,
  "secoes": {
    "objeto": str,                          # Seção 1
    "descricao_necessidade": str,           # Seção 2
    "previsao_pca": str,                    # Seção 3
    "planejamento_estrategico": str,        # Seção 4
    "catalogo_padronizacao": str,           # Seção 5
    "requisitos_contratacao": str,          # Seção 6
    "condicoes_recebimento": str,           # Seção 7
    "condicoes_execucao_pagamento": str,    # Seção 8
    "garantias": str,                       # Seção 9
    "modalidade_licitacao": str,            # Seção 10
    "estimativa_quantidades": str,          # Seção 11
    "levantamento_mercado": str,            # Seção 12
    "estimativa_valor": str,                # Seção 13
    "descricao_solucao": str,               # Seção 14
    "justificativa_parcelamento": str,      # Seção 15
    "resultados_pretendidos": str,          # Seção 16
    "providencias_previas": str,            # Seção 17
    "contratacoes_correlatas": str,         # Seção 18
    "impactos_ambientais": str,             # Seção 19
    "possibilidade_compra_locacao": str,    # Seção 20
    "participacao_consorcio": str,          # Seção 21
    "vistoria_visita_tecnica": str,         # Seção 22
    "cumprimento_resolucoes_cnj": str,      # Seção 23
    "plano_riscos": str,                    # Seção 24
    "equipe_planejamento": str,             # Seção 25
    "estimativa_prazo_vigencia": str,       # Seção 26
    "avaliacao_conclusiva": str             # Seção 27
  },
  "lacunas": list
}
```

**27 seções obrigatórias** conforme Lei 14.133/2021, art. 18, §1º

**Prompt otimizado**:
- Instruções específicas para localizar seções numeradas
- Extração de dados administrativos da seção 25 (Equipe)
- Extração de valor da seção 13 (Estimativa)
- Extração de prazo da seção 26 (Vigência)

---

### 3️⃣ **TRAgent** (`agents/tr_agent.py`)

**Responsável por**: Termos de Referência

**Estrutura**:
```python
{
  "artefato": "TR",
  "timestamp": str,
  "TR": {
    "objeto": str,                      # Seção 1
    "justificativa_tecnica": str,       # Seção 2
    "especificacao_tecnica": str,       # Seção 3
    "criterios_julgamento": str,        # Seção 4
    "riscos": str,                      # Seção 5
    "observacoes_finais": str,          # Seção 6
    "prazo_execucao": str,              # Seção 7
    "estimativa_valor": str,            # Seção 8
    "fonte_recurso": str                # Seção 9
  }
}
```

**9 seções padronizadas** conforme padrão TJSP

**Prompt otimizado**:
- Instruções específicas para identificar seções 1-9
- Extração sintética para prazo, valor e fonte (seções 7-9)
- Mantém estrutura JSON simples e clara

**Teste local**: `test_tr_agent.py` (9/9 seções extraídas ✅)

---

### 4️⃣ **EditalAgent** (`agents/edital_agent.py`)

**Responsável por**: Editais de Licitação

**Estrutura**:
```python
{
  "artefato": "EDITAL",
  "timestamp": str,
  "EDITAL": {
    "objeto": str,                      # Campo 1
    "tipo_licitacao": str,             # Campo 2
    "criterio_julgamento": str,        # Campo 3
    "condicoes_participacao": str,     # Campo 4
    "exigencias_habilitacao": str,     # Campo 5
    "obrigacoes_contratada": str,      # Campo 6
    "prazo_execucao": str,             # Campo 7
    "fontes_recursos": str,            # Campo 8
    "gestor_fiscal": str,              # Campo 9
    "observacoes_gerais": str,         # Campo 10
    "numero_edital": str,              # Campo 11
    "data_publicacao": str             # Campo 12
  },
  "contexto_usado": list
}
```

**12 campos padronizados** conforme Lei 14.133/2021

**Prompt otimizado**:
- Instruções específicas para identificar campos 1-12
- Integração automática com contexto DFD/ETP/TR
- Enriquecimento inteligente de campos vazios usando dados de outros módulos
- Geração automática de número e data se não presentes no documento

**Teste local**: `test_edital_agent.py` (12/12 campos extraídos ✅)

---

## 🔄 Fluxo de Processamento

### Pipeline Completo

```
1. INSUMOS (Upload PDF)
   ↓
2. Extração PyMuPDF (texto bruto)
   ↓
3. Salvar em exports/insumos/json/{TIPO}_ultimo.json
   ↓
4. Módulo específico (DFD/ETP/TR)
   ↓
5. obter_{tipo}_da_sessao() carrega dados
   ↓
6. Formulário exibe dados brutos
   ↓
7. Botão "Processar com IA"
   ↓
8. gerar_{tipo}_com_ia()
   ↓
9. Agente especializado processa
   ↓
10. Mesclagem inteligente (preserva + enriquece)
   ↓
11. Atualizar formulário (st.rerun())
   ↓
12. Exportação DOCX/JSON
```

---

## 📁 Estrutura de Arquivos

### Agentes
```
agents/
├── document_agent.py       # DFDAgent (11 seções governança)
├── etp_agent.py           # ETPAgent (27 seções Lei 14.133)
├── tr_agent.py            # TRAgent (9 seções padrão TJSP)
├── edital_agent.py        # EditalAgent (12 campos licitação)
├── github_bridge.py       # Integrações GitHub
├── guide_agent.py         # Guias e documentação
└── stage_detector.py      # Detecção de fase do processo
```

### Integrações
```
utils/
├── integration_dfd.py     # Backend DFD + gerar_dfd_com_ia()
├── integration_etp.py     # Backend ETP + gerar_etp_com_ia()
├── integration_tr.py      # Backend TR + gerar_tr_com_ia()
├── integration_edital.py  # Backend Edital + gerar_edital_com_ia()
└── ai_client.py          # Cliente OpenAI centralizado
```

### Páginas Streamlit
```
streamlit_app/pages/
├── 02_📘 DFD – Documento de Formalização de Demanda.py
├── 03_📘 ETP – Estudo Técnico Preliminar.py
├── 05_📑 TR – Termo de Referência.py
└── ...
```

---

## 🛠️ Como Criar Novo Agente

### Template Básico

```python
# agents/{tipo}_agent.py

from utils.ai_client import AIClient
from datetime import datetime

# Definir seções específicas
SECOES_{TIPO} = [
    "secao1",
    "secao2",
    # ...
]

class {Tipo}Agent:
    """Agente especializado em {Tipo de Documento}"""
    
    def __init__(self):
        try:
            self.ai = AIClient()
        except Exception as e:
            print(f"[{Tipo}Agent] ERRO: {e}")
            self.ai = None
    
    def generate(self, conteudo_base: str) -> dict:
        """Processa documento e retorna estrutura completa"""
        
        if self.ai is None:
            return {
                "erro": "AIClient não disponível",
                "{TIPO}": self._get_template_vazio()
            }
        
        prompt = self._montar_prompt()
        resposta = self.ai.ask(prompt=prompt, conteudo=conteudo_base, artefato="{TIPO}")
        
        if "erro" in resposta:
            return resposta
        
        # Extrair e sanitizar
        d = resposta.get("{TIPO}", resposta)
        
        # Garantir todos os campos
        d.setdefault("campo1", "")
        # ...
        
        # Garantir todas as seções
        secoes = d.get("secoes", {})
        for s in SECOES_{TIPO}:
            secoes.setdefault(s, "")
        d["secoes"] = secoes
        
        d["gerado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d["origem"] = "{tipo}_agent_v1"
        
        return d
    
    def _get_template_vazio(self) -> dict:
        """Template vazio para fallback"""
        # ...
    
    def _montar_prompt(self) -> str:
        """Prompt otimizado para {TIPO}"""
        return (
            "Você é o agente especializado do TJSP em {Tipo de Documento}...\n\n"
            "INSTRUÇÕES ESPECÍFICAS:\n"
            "1. Localizar seções...\n"
            "2. Extrair dados...\n"
            # ...
        )

# Função wrapper
def processar_{tipo}_com_ia(conteudo_textual: str = "") -> dict:
    """Wrapper para integration_{tipo}.py"""
    # ...
```

---

## 📊 Status Atual (Dezembro 2025)

| Agente | Status | Campos/Seções | Testes | Deploy |
|--------|--------|---------------|--------|--------|
| DFDAgent | ✅ Produção | 11 seções | ✅ test_dfd_cli.py | ✅ |
| ETPAgent | ✅ Produção | 27 seções | ✅ test_etp_agent.py | ✅ |
| TRAgent | ✅ Produção | 9 seções | ✅ test_tr_agent.py | ✅ |
| EditalAgent | ✅ Produção | 12 campos | ✅ test_edital_agent.py | ✅ |
| ContratoAgent | 🟡 Planejado | ~20 seções | ⏳ | ⏳ |

---

## 🎯 Benefícios da Arquitetura

### Para o Desenvolvedor
- ✅ **Código modular**: Cada agente é independente
- ✅ **Manutenção facilitada**: Alterações isoladas
- ✅ **Testes específicos**: Cada agente tem seu teste
- ✅ **Escalável**: Novos agentes sem afetar existentes

### Para o Usuário
- ✅ **Extração precisa**: Agentes otimizados para cada documento
- ✅ **Formulários completos**: Todos os campos preenchidos
- ✅ **Dados estruturados**: Seções organizadas e numeradas
- ✅ **Menos edição manual**: Alta qualidade na extração

### Para o TJSP
- ✅ **Conformidade legal**: Estruturas seguem legislação (Lei 14.133/2021)
- ✅ **Padronização**: Documentos uniformes
- ✅ **Rastreabilidade**: Origem e timestamp dos dados
- ✅ **Auditoria**: Lacunas identificadas automaticamente

---

## 🔧 Troubleshooting

### Problema: Formulário não preenche
**Diagnóstico**: Estrutura do `defaults` incompatível com formulário

**Solução**:
1. Verificar se `defaults.get("secoes")` retorna dict
2. Confirmar que keys das seções correspondem ao formulário
3. Validar que `obter_{tipo}_da_sessao()` retorna estrutura correta

### Problema: Dados administrativos vazios
**Diagnóstico**: Agente não está extraindo da seção correta

**Solução**:
1. Revisar prompt do agente (instruções de extração)
2. Verificar se seção está numerada no documento
3. Testar com `test_{tipo}_agent.py` localmente

### Problema: Seções marcadas como vazias
**Diagnóstico**: Conteúdo textual insuficiente ou truncado

**Solução**:
1. Verificar tamanho do texto em `conteudo_textual`
2. Aumentar `max_tokens` no `ai_client.py` se necessário
3. Revisar extração PyMuPDF no módulo INSUMOS

---

## 📚 Referências

- **Lei 14.133/2021**: Nova Lei de Licitações e Contratos
- **OpenAI SDK 1.52.2**: `chat.completions.create()`
- **httpx 0.27.2**: Versão compatível (0.28+ remove `proxies`)
- **Streamlit 1.39.0**: Framework da aplicação

---

**Última atualização**: 2025-12-08  
**Autor**: Sistema SynapseNext TJSP  
**Versão**: 2.0 (Arquitetura de Agentes Especializados)
