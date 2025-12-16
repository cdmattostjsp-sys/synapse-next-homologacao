# Padrões Arquiteturais SAAB-Tech (Referência)

> **Propósito**: Documentação de referência para projetos satélite do TJSP  
> **Versão**: 2025.1-homolog  
> **Data**: Dezembro 2025

---

## 1. ESTRUTURA DE DIRETÓRIOS (Padrão SAAB-Tech)

```
projeto/
├── streamlit_app/              # Aplicação principal
│   ├── Home.py                 # Página inicial (navegação)
│   ├── pages/                  # Módulos funcionais
│   │   ├── 01_Nome.py          # Numeração sequencial
│   │   ├── 02_Nome.py
│   │   └── 99_Documentação.py  # Sempre por último
│   └── home_utils/             # Componentes compartilhados UI
│       ├── sidebar_organizer.py
│       └── refinamento_ia.py
├── agents/                     # Agentes inteligentes
│   ├── base_agent.py           # Classe abstrata
│   ├── dfd_agent.py            # Agentes específicos
│   └── contrato_agent.py
├── utils/                      # Serviços e integrações
│   ├── ui_components.py        # (DEPRECATED - migrar para home_utils)
│   ├── integration_*.py        # Integrações por módulo
│   └── docx_generator.py       # Serviços de exportação
├── prompts/                    # Prompts estruturados
│   ├── system/                 # Prompts de sistema
│   └── user/                   # Templates de usuário
├── knowledge/                  # Base de conhecimento
│   ├── leis/                   # Legislação
│   ├── modelos/                # Templates TJSP
│   └── *.yml                   # Checklists estruturados
├── exports/                    # Dados gerados (git-ignored)
│   ├── json/                   # Dados estruturados
│   └── docx/                   # Documentos finais
├── tests/                      # Testes automatizados
├── requirements.txt            # Dependências Python
├── runtime.txt                 # Versão Python (Streamlit Cloud)
└── README.md                   # Documentação principal
```

---

## 2. PRINCÍPIOS ARQUITETURAIS

### 2.1 Separação de Responsabilidades

**UI (Streamlit Pages)**
- Apenas interface e interação
- Chama agentes/serviços
- Gerencia session_state
- Renderiza resultados

**Agentes (agents/)**
- Lógica de IA especializada
- Processamento de contexto
- Interação com LLM (OpenAI)
- Retorna dados estruturados

**Serviços (utils/)**
- Integrações externas
- Exportação de documentos
- Validações e conversões
- I/O de arquivos

**Knowledge Base**
- Dados estáticos (leis, modelos)
- Versionado no Git
- Formato YAML/Markdown/PDF

---

## 3. PADRÃO DE MÓDULOS (Pages)

### Estrutura Típica de uma Página:

```python
# ==========================================================
# pages/XX_Titulo.py – Descrição
# ==========================================================

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import streamlit as st
from utils.integration_xxx import processar_xxx
from agents.xxx_agent import XXXAgent
from home_utils.sidebar_organizer import apply_sidebar_grouping

# Configuração
st.set_page_config(page_title="Título", layout="wide")
apply_sidebar_grouping()

# CSS institucional (ver DESIGN_SYSTEM_TJSP.md)
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1>Título do Módulo</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Descrição</p>", unsafe_allow_html=True)

# Interface principal
# ... código do módulo ...

# Rodapé
st.caption("Informações institucionais")
```

---

## 4. PADRÃO DE AGENTES

### Classe Base (Conceitual):

```python
class BaseAgent:
    """
    Agente base para processamento com IA
    
    Responsabilidades:
    - Gerenciar prompts
    - Interagir com LLM
    - Validar respostas
    - Estruturar saída
    """
    
    def __init__(self, model="gpt-4"):
        self.model = model
        
    def processar(self, contexto: dict) -> dict:
        """
        Método principal de processamento
        
        Args:
            contexto: Dados de entrada estruturados
            
        Returns:
            dict: Resultado estruturado
        """
        pass
```

### Especialização:

```python
class ContratoAgent(BaseAgent):
    """Especializado em contratos administrativos"""
    
    def processar(self, contexto: dict) -> dict:
        # 1. Carregar prompt do sistema
        system_prompt = self._load_system_prompt()
        
        # 2. Construir mensagens
        messages = self._build_messages(contexto)
        
        # 3. Chamar LLM
        response = self._call_llm(messages)
        
        # 4. Validar e estruturar
        return self._parse_response(response)
```

---

## 5. GERENCIAMENTO DE ESTADO (Session State)

### Convenções de Nomenclatura:

```python
# Dados de módulos (campos processados pela IA)
st.session_state["dfd_campos_ai"]
st.session_state["etp_campos_ai"]
st.session_state["contrato_campos_ai"]

# Dados brutos (uploads)
st.session_state["upload_buffer"]

# Flags de controle
st.session_state["processing"]
st.session_state["show_refinamento"]

# Buffers de exportação (DOCX)
st.session_state["contrato_docx_buffer"]
st.session_state["contrato_docx_nome"]
```

### Inicialização Padrão:

```python
if "modulo_campos_ai" not in st.session_state:
    st.session_state["modulo_campos_ai"] = {}
```

---

## 6. INTEGRAÇÃO ENTRE MÓDULOS

### Padrão de Transferência de Dados:

```python
# Módulo A (origem)
if st.button("📤 Enviar para Módulo B"):
    dados = {"campo1": valor1, "campo2": valor2}
    st.session_state["moduloB_campos_ai"] = dados
    st.success("Dados transferidos!")
    
# Módulo B (destino)
dados_anteriores = st.session_state.get("moduloA_campos_ai", {})
if dados_anteriores:
    st.info(f"Contexto detectado de Módulo A")
```

### Função de Integração de Contexto:

```python
def integrar_com_contexto(session_state) -> dict:
    """Consolida dados de módulos anteriores"""
    contexto = {}
    
    if "dfd_campos_ai" in session_state:
        contexto["DFD"] = session_state["dfd_campos_ai"]
    if "etp_campos_ai" in session_state:
        contexto["ETP"] = session_state["etp_campos_ai"]
    # ... outros módulos
    
    return contexto
```

---

## 7. EXPORTAÇÃO DE DADOS

### JSON (Persistência):

```python
import json
from datetime import datetime

def export_to_json(dados: dict, modulo: str):
    """Salva dados estruturados em JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    resultado = {
        "artefato": modulo,
        "timestamp": datetime.now().isoformat(),
        "status": "processado",
        modulo: dados
    }
    
    arquivo = f"exports/json/{modulo}_{timestamp}.json"
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
```

### DOCX (Documentos):

```python
from docx import Document

def gerar_docx(campos: dict) -> BytesIO:
    """Gera documento DOCX profissional"""
    doc = Document()
    
    # Adicionar conteúdo
    doc.add_heading("Título", 0)
    for campo, valor in campos.items():
        doc.add_heading(campo.replace("_", " ").title(), 1)
        doc.add_paragraph(valor)
    
    # Salvar em buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
```

---

## 8. TRATAMENTO DE ERROS

### Padrão de Try-Except:

```python
try:
    resultado = processar_com_ia(dados)
    
    if resultado and "erro" not in resultado:
        st.success("✅ Processamento concluído!")
        st.session_state["dados"] = resultado
    else:
        st.warning("⚠️ Processamento retornou vazio")
        
except Exception as e:
    st.error(f"❌ Erro: {e}")
    import traceback
    with st.expander("🔍 Detalhes técnicos"):
        st.code(traceback.format_exc())
```

---

## 9. BOAS PRÁTICAS

### ✅ FAZER:
- Comentários em português institucional
- Docstrings em funções públicas
- Validação de entrada de dados
- Mensagens de feedback ao usuário
- Logs estruturados (quando aplicável)
- Session state inicializado no topo

### ❌ EVITAR:
- Código hardcoded (usar constantes)
- Imports relativos complexos
- State mutations sem controle
- Processamento síncrono longo (usar spinner)
- Secrets no código (usar .env ou Streamlit secrets)

---

## 10. ESCALABILIDADE FUTURA

### Preparar para:

**API REST** (FastAPI):
```python
# Futuro endpoint de integração
@app.post("/api/v1/processar-contrato")
async def processar_contrato(dados: ContratoInput):
    resultado = ContratoAgent().processar(dados.dict())
    return resultado
```

**Message Queue** (Celery/RabbitMQ):
```python
# Processamento assíncrono de tarefas pesadas
@celery.task
def processar_etp_async(contexto: dict):
    return ETPAgent().processar(contexto)
```

**Database** (PostgreSQL/MongoDB):
```python
# Migração de JSON para DB
def salvar_contrato_db(dados: dict):
    contrato = Contrato(**dados)
    db.session.add(contrato)
    db.session.commit()
```

---

## 11. REFERÊNCIAS CRUZADAS

- **Design Visual**: Ver `DESIGN_SYSTEM_TJSP.md`
- **Integração entre Sistemas**: Ver `INTEGRATION_BLUEPRINT.md`
- **Convenções de Código**: Ver `CODE_STANDARDS.md`
- **Guia Visual PJe**: Ver `/GUIA_PADRAO_VISUAL_PJe.md` (raiz do projeto)

---

**Última atualização**: 16/12/2025  
**Mantido por**: Engenheiro Synapse | SAAB/TJSP
