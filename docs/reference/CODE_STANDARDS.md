# Padrões e Convenções de Código TJSP (Referência)

> **Propósito**: Convenções de código, nomenclatura e boas práticas para projetos Python/Streamlit do TJSP  
> **Versão**: 2025.1-homolog  
> **Baseado em**: PEP 8 + Convenções Institucionais SAAB-Tech  
> **Data**: Dezembro 2025

---

## 1. ESTRUTURA DE IMPORTS

### Ordem Padrão:

```python
# ==========================================================
# pages/XX_Nome_Modulo.py – Descrição institucional
# ==========================================================

# 1. Correção de PATH (sempre primeiro)
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 2. Imports da biblioteca padrão (ordenados alfabeticamente)
import json
import os
from datetime import datetime
from io import BytesIO

# 3. Imports de terceiros (ordenados alfabeticamente)
import streamlit as st
from docx import Document

# 4. Imports locais - Utils
from utils.integration_xxx import processar_xxx
from utils.docx_generator import gerar_docx

# 5. Imports locais - Agentes
from agents.xxx_agent import XXXAgent

# 6. Imports locais - Home Utils
from home_utils.sidebar_organizer import apply_sidebar_grouping
from home_utils.refinamento_ia import render_refinamento_iterativo
```

---

## 2. NOMENCLATURA

### 2.1 Arquivos e Diretórios:

```python
# Arquivos Python (snake_case)
integration_contrato.py  ✅
IntegrationContrato.py   ❌
integration-contrato.py  ❌

# Diretórios (snake_case)
home_utils/              ✅
homeUtils/               ❌
home-utils/              ❌

# Pages Streamlit (numeração + título)
01_🔧 Insumos.py         ✅
insumos.py               ❌
1_insumos.py             ❌
```

### 2.2 Variáveis e Funções:

```python
# Variáveis (snake_case)
numero_contrato = "123/2025"     ✅
numeroContrato = "123/2025"      ❌
NumeroContrato = "123/2025"      ❌

# Funções (snake_case, verbos descritivos)
def processar_contrato(dados):   ✅
def ProcessarContrato(dados):    ❌
def contrato(dados):             ❌ (não descreve ação)

# Constantes (UPPER_SNAKE_CASE)
CAMPOS_OBRIGATORIOS = [...]      ✅
campos_obrigatorios = [...]      ❌
CamposObrigatorios = [...]       ❌
```

### 2.3 Classes:

```python
# Classes (PascalCase)
class ContratoAgent:             ✅
class contratoAgent:             ❌
class contrato_agent:            ❌

# Métodos de classe (snake_case)
class ContratoAgent:
    def processar_contrato(self):  ✅
    def ProcessarContrato(self):   ❌
```

### 2.4 Session State (Convenção SAAB-Tech):

```python
# Dados de módulos (sufixo _campos_ai)
st.session_state["dfd_campos_ai"]        ✅
st.session_state["etp_campos_ai"]        ✅
st.session_state["DFD_campos"]           ❌

# Buffers de exportação (sufixo _buffer)
st.session_state["contrato_docx_buffer"] ✅
st.session_state["contrato_docx_nome"]   ✅
st.session_state["contratoBuffer"]       ❌

# Flags (booleanos descritivos)
st.session_state["processing"]           ✅
st.session_state["show_refinamento"]     ✅
st.session_state["flag"]                 ❌ (não descritivo)
```

---

## 3. FORMATAÇÃO DE CÓDIGO

### 3.1 Indentação:

```python
# 4 espaços (NUNCA tabs)
def funcao():
    if condicao:
        fazer_algo()  # 4 espaços
    else:
        fazer_outra_coisa()  # 4 espaços
```

### 3.2 Linhas em Branco:

```python
# 2 linhas entre funções/classes de topo
def funcao1():
    pass


def funcao2():  # 2 linhas acima
    pass


# 1 linha entre métodos dentro de classe
class MinhaClasse:
    def metodo1(self):
        pass
    
    def metodo2(self):  # 1 linha acima
        pass
```

### 3.3 Comprimento de Linha:

```python
# Máximo 100 caracteres (PEP 8 adaptado)

# Quebra de linha em listas
CAMPOS = [
    "numero_contrato",
    "data_assinatura",
    "objeto",
    "vigencia"
]

# Quebra de linha em chamadas de função
resultado = processar_contrato(
    numero="123/2025",
    data="2025-12-01",
    objeto="Serviços de..."
)

# Strings longas
texto = (
    "Este é um texto muito longo que precisa ser quebrado "
    "em múltiplas linhas para manter a legibilidade do código"
)
```

---

## 4. DOCSTRINGS

### 4.1 Funções:

```python
def processar_contrato(dados: dict, contexto: dict = None) -> dict:
    """
    Processa dados de contrato com validação e enriquecimento.
    
    Args:
        dados: Dicionário com campos do contrato
        contexto: Dados de módulos anteriores (opcional)
        
    Returns:
        dict: Contrato processado com campos validados
        
    Raises:
        ValueError: Se dados obrigatórios estiverem ausentes
        
    Example:
        >>> dados = {"numero_contrato": "123/2025"}
        >>> resultado = processar_contrato(dados)
        >>> resultado["status"]
        'processado'
    """
    pass
```

### 4.2 Classes:

```python
class ContratoAgent:
    """
    Agente especializado em processamento de contratos administrativos.
    
    Responsabilidades:
        - Validar campos obrigatórios
        - Enriquecer com legislação aplicável
        - Gerar cláusulas padronizadas
        
    Attributes:
        model (str): Modelo de LLM utilizado
        prompts_dir (Path): Diretório de prompts
        
    Example:
        >>> agent = ContratoAgent(model="gpt-4")
        >>> resultado = agent.processar(dados)
    """
    
    def __init__(self, model: str = "gpt-4"):
        """Inicializa agente com modelo especificado."""
        self.model = model
```

### 4.3 Módulos (topo do arquivo):

```python
"""
Módulo de integração para contratos administrativos.

Este módulo fornece funções para:
- Processamento de contratos com IA
- Exportação em DOCX profissional
- Integração com módulos anteriores (DFD, ETP, TR, Edital)

Versão: 2025.1-homolog
Mantido por: Engenheiro Synapse | SAAB/TJSP
"""
```

---

## 5. COMENTÁRIOS

### 5.1 Comentários Inline:

```python
# Bom: Explicar "por quê", não "o quê"
numero_processado = numero.replace("/", "_")  # URLs não aceitam /

# Ruim: Descrever o óbvio
numero_processado = numero.replace("/", "_")  # Substitui / por _
```

### 5.2 Blocos de Comentários:

```python
# ==========================================================
# 📊 Processamento de Dados
# ==========================================================

# [CORREÇÃO CRÍTICA]: Adicionado tratamento de None
# para evitar erro quando campo está vazio (Issue #123)
if valor is not None:
    processar(valor)
```

### 5.3 TODO/FIXME:

```python
# TODO: Implementar validação de CPF/CNPJ
# FIXME: Corrigir bug de encoding em UTF-8
# DEPRECATED: Usar nova função processar_v2()
```

---

## 6. TYPE HINTS

### 6.1 Funções:

```python
from typing import Dict, List, Optional, Union

def processar_dados(
    entrada: Dict[str, str],
    opcoes: Optional[List[str]] = None
) -> Dict[str, Union[str, int]]:
    """Processa dados com type hints claros."""
    return {"status": "ok", "count": 1}
```

### 6.2 Variáveis (quando não óbvio):

```python
# Tipo óbvio (opcional)
numero: int = 42

# Tipo não óbvio (recomendado)
resultado: Dict[str, Any] = processar()

# Lista de objetos complexos
contratos: List[Dict[str, str]] = []
```

---

## 7. TRATAMENTO DE ERROS

### 7.1 Padrão Try-Except:

```python
try:
    resultado = processar_com_ia(dados)
    
    if resultado and "erro" not in resultado:
        st.success("✅ Processamento concluído!")
        return resultado
    else:
        st.warning("⚠️ Nenhum resultado retornado")
        return None
        
except FileNotFoundError as e:
    st.error(f"❌ Arquivo não encontrado: {e}")
    return None
    
except ValueError as e:
    st.error(f"❌ Erro de validação: {e}")
    return None
    
except Exception as e:
    st.error(f"❌ Erro inesperado: {e}")
    import traceback
    with st.expander("🔍 Detalhes técnicos"):
        st.code(traceback.format_exc())
    return None
```

### 7.2 Logging:

```python
import logging

logger = logging.getLogger(__name__)

def funcao_critica():
    try:
        processar()
    except Exception as e:
        logger.error(f"Erro em funcao_critica: {e}", exc_info=True)
        raise
```

---

## 8. STREAMLIT BEST PRACTICES

### 8.1 Session State:

```python
# Inicialização defensiva
if "campos_ai" not in st.session_state:
    st.session_state["campos_ai"] = {}

# Acesso seguro
campos = st.session_state.get("campos_ai", {})

# Evitar race conditions
def processar():
    # Copiar dados antes de processar
    dados_local = st.session_state["campos_ai"].copy()
    resultado = processar_dados(dados_local)
    st.session_state["campos_ai"] = resultado
```

### 8.2 Performance:

```python
# Cache de funções custosas
@st.cache_data(ttl=3600)
def carregar_legislacao():
    """Cache por 1 hora"""
    return ler_arquivo_grande()

# Cache de recursos
@st.cache_resource
def inicializar_agente():
    """Cache persistente (não expira)"""
    return ContratoAgent(model="gpt-4")
```

### 8.3 Componentes:

```python
# Usar use_container_width para responsividade
st.button("Processar", use_container_width=True)  ✅
st.button("Processar")                             ❌

# Sempre fornecer key em loops
for i, item in enumerate(lista):
    st.button(f"Item {i}", key=f"btn_{i}")  ✅
    st.button(f"Item {i}")                  ❌ (gera erro)
```

---

## 9. ESTRUTURA DE FUNÇÃO

### Padrão Recomendado:

```python
def funcao_principal(arg1: str, arg2: Optional[int] = None) -> Dict[str, Any]:
    """
    Docstring clara e completa.
    
    Args:
        arg1: Descrição do argumento
        arg2: Argumento opcional
        
    Returns:
        Dicionário com resultado estruturado
    """
    
    # 1. Validação de entrada
    if not arg1:
        raise ValueError("arg1 não pode ser vazio")
    
    # 2. Inicialização de variáveis
    resultado = {}
    dados_processados = []
    
    # 3. Lógica principal
    try:
        for item in processar_items(arg1):
            dados_processados.append(transformar(item))
            
        resultado = {
            "status": "sucesso",
            "dados": dados_processados,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        resultado = {
            "status": "erro",
            "mensagem": str(e)
        }
    
    # 4. Retorno estruturado
    return resultado
```

---

## 10. VERSIONAMENTO E GIT

### 10.1 Mensagens de Commit:

```bash
# Formato: <tipo>(<escopo>): <mensagem>

# Tipos válidos:
feat:     # Nova funcionalidade
fix:      # Correção de bug
refactor: # Refatoração (sem nova feature ou bug)
docs:     # Apenas documentação
style:    # Formatação, ponto-e-vírgula, etc
test:     # Adicionar testes
chore:    # Manutenção, deps, config

# Exemplos:
feat(contrato): Adiciona exportação DOCX profissional
fix(dfd): Corrige erro de encoding em UTF-8
refactor(ux): Aplica padrão PJe-inspired em todos os módulos
docs(api): Atualiza documentação de integração
```

### 10.2 Branches:

```bash
# Branch principal
main            # Código homologado

# Branches de trabalho
feature/nome-feature
fix/nome-bug
refactor/nome-refactor

# Exemplos:
feature/integracao-fiscal
fix/upload-race-condition
refactor/pje-design-system
```

---

## 11. TESTES

### 11.1 Nomenclatura:

```python
# Arquivo de teste
tests/test_contrato_agent.py  ✅
tests/contratoTest.py         ❌

# Função de teste
def test_processar_contrato_com_sucesso():  ✅
def testProcessarContrato():                ❌
def test1():                                ❌
```

### 11.2 Estrutura de Teste:

```python
import pytest
from agents.contrato_agent import ContratoAgent

def test_processar_contrato_com_dados_validos():
    """Deve processar contrato com dados válidos."""
    # Arrange
    agent = ContratoAgent()
    dados = {
        "numero_contrato": "123/2025",
        "objeto": "Serviços de..."
    }
    
    # Act
    resultado = agent.processar(dados)
    
    # Assert
    assert resultado["status"] == "processado"
    assert "numero_contrato" in resultado["CONTRATO"]
    assert resultado["CONTRATO"]["numero_contrato"] == "123/2025"

def test_processar_contrato_sem_dados_obrigatorios():
    """Deve levantar ValueError quando dados obrigatórios faltam."""
    # Arrange
    agent = ContratoAgent()
    dados = {}
    
    # Act & Assert
    with pytest.raises(ValueError):
        agent.processar(dados)
```

---

## 12. SEGURANÇA

### 12.1 Secrets e Credenciais:

```python
# NUNCA no código
api_key = "sk-abc123..."  ❌

# Sempre via ambiente ou Streamlit secrets
import os
api_key = os.getenv("OPENAI_API_KEY")  ✅

# Ou Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]  ✅
```

### 12.2 Validação de Entrada:

```python
def processar_arquivo(arquivo_upload):
    """Valida arquivo antes de processar."""
    
    # Validar extensão
    extensoes_validas = [".pdf", ".docx", ".txt"]
    if not any(arquivo_upload.name.endswith(ext) for ext in extensoes_validas):
        raise ValueError(f"Extensão inválida. Use: {extensoes_validas}")
    
    # Validar tamanho (10MB max)
    max_size = 10 * 1024 * 1024  # 10MB
    if arquivo_upload.size > max_size:
        raise ValueError("Arquivo muito grande (máx: 10MB)")
    
    # Processar com segurança
    return processar(arquivo_upload)
```

---

## 13. CHECKLIST DE QUALIDADE

Antes de fazer commit:

```
□ Código segue PEP 8 (verificar com flake8/black)
□ Type hints em funções públicas
□ Docstrings em funções/classes complexas
□ Comentários explicam "por quê", não "o quê"
□ Nomes descritivos (não abreviações obscuras)
□ Sem código comentado (remover ou justificar)
□ Sem prints de debug (usar logging)
□ Tratamento de erros adequado
□ Testes passando (se aplicável)
□ Sem secrets hardcoded
□ Imports organizados corretamente
□ Session state inicializado no topo
□ Mensagem de commit descritiva
```

---

## 14. FERRAMENTAS RECOMENDADAS

### Formatação Automática:

```bash
# Black (formatador)
pip install black
black streamlit_app/

# isort (organizar imports)
pip install isort
isort streamlit_app/

# flake8 (linter)
pip install flake8
flake8 streamlit_app/ --max-line-length=100
```

### Type Checking:

```bash
# mypy
pip install mypy
mypy streamlit_app/
```

---

## 15. REFERÊNCIAS

- **PEP 8**: https://peps.python.org/pep-0008/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html
- **Streamlit Best Practices**: https://docs.streamlit.io/develop/concepts/architecture
- **SAAB-Tech Patterns**: Ver `ARCHITECTURE_PATTERNS.md`
- **Design System**: Ver `DESIGN_SYSTEM_TJSP.md`

---

**Última atualização**: 16/12/2025  
**Mantido por**: Engenheiro Synapse | SAAB/TJSP  
**Aplicável a**: Todos os projetos Python/Streamlit do TJSP
