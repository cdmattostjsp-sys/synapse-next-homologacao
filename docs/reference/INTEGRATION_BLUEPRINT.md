# Blueprint de Integração entre Sistemas TJSP (Referência)

> **Propósito**: Guia para integração entre SAAB-Tech e projetos satélite  
> **Versão**: 2025.1-homolog  
> **Cenário**: SAAB-Tech (Contratos) ↔ Contrato-Regional-IA (Fiscalização)  
> **Data**: Dezembro 2025

---

## 1. VISÃO GERAL DA ARQUITETURA

### Sistemas no Ecossistema:

```
┌─────────────────────────────────────────────────────────────┐
│                    ECOSSISTEMA TJSP                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐          ┌────────────────────┐       │
│  │   SAAB-Tech      │◄────────►│ Contrato-Regional  │       │
│  │  (Homologado)    │   API    │   -IA (Piloto)     │       │
│  │                  │          │                    │       │
│  │ • DFD            │          │ • Dashboard        │       │
│  │ • ETP            │          │ • Fiscalização     │       │
│  │ • TR             │          │ • Notificações     │       │
│  │ • Edital         │          │ • Orientações      │       │
│  │ • Contrato       │◄─────────┤ • RAJ 10.1         │       │
│  └──────────────────┘  Dados   └────────────────────┘       │
│         │                              │                     │
│         │                              │                     │
│         ▼                              ▼                     │
│  ┌─────────────────────────────────────────────┐            │
│  │    Base de Conhecimento Compartilhada       │            │
│  │  • Legislação (Lei 14.133/2021)             │            │
│  │  • Modelos TJSP                             │            │
│  │  • Jurisprudência                           │            │
│  └─────────────────────────────────────────────┘            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. OPÇÕES DE INTEGRAÇÃO

### 2.1 Opção A: API REST (RECOMENDADO)

**Vantagens**:
- ✅ Desacoplamento total
- ✅ Escalabilidade
- ✅ Versionamento de API
- ✅ Autenticação/Autorização
- ✅ Múltiplos consumidores

**Stack Sugerida**:
```python
# SAAB-Tech: FastAPI endpoint
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ContratoOutput(BaseModel):
    numero_contrato: str
    data_assinatura: str
    objeto: str
    # ... outros campos

@app.get("/api/v1/contratos/{numero}")
async def get_contrato(numero: str) -> ContratoOutput:
    """Retorna dados de contrato para fiscalização"""
    # Buscar do session_state ou DB
    contrato = buscar_contrato(numero)
    return ContratoOutput(**contrato)

# Contrato-Regional: Consumidor
import httpx

async def carregar_contrato(numero: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://saab-tech.tjsp.gov.br/api/v1/contratos/{numero}"
        )
        return response.json()
```

---

### 2.2 Opção B: Shared Storage (JSON/Exports)

**Vantagens**:
- ✅ Simples de implementar
- ✅ Sem dependência de rede
- ✅ Auditável (arquivos versionados)

**Desvantagens**:
- ⚠️ Não é tempo real
- ⚠️ Sincronização manual
- ⚠️ Escalabilidade limitada

**Implementação**:

```python
# SAAB-Tech: Exporta contrato assinado
import json
from datetime import datetime

def exportar_contrato_para_fiscalizacao(contrato: dict):
    """Salva contrato em formato compartilhado"""
    
    dados_exportacao = {
        "sistema_origem": "SAAB-Tech",
        "timestamp_export": datetime.now().isoformat(),
        "versao": "2025.1",
        "contrato": contrato
    }
    
    # Salvar em diretório compartilhado
    arquivo = f"/shared/contratos/{contrato['numero_contrato']}.json"
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados_exportacao, f, ensure_ascii=False, indent=2)

# Contrato-Regional: Importa contrato
def importar_contrato_para_fiscalizacao(numero: str):
    """Carrega contrato do SAAB-Tech"""
    
    arquivo = f"/shared/contratos/{numero}.json"
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    return dados["contrato"]
```

---

### 2.3 Opção C: Database Compartilhado

**Vantagens**:
- ✅ Tempo real
- ✅ Consultas complexas
- ✅ Transações ACID
- ✅ Auditoria built-in

**Desvantagens**:
- ⚠️ Maior complexidade
- ⚠️ Requer infraestrutura
- ⚠️ Acoplamento de dados

**Stack Sugerida**:
```python
# SQLAlchemy + PostgreSQL
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Contrato(Base):
    __tablename__ = "contratos"
    
    numero_contrato = Column(String, primary_key=True)
    data_assinatura = Column(DateTime)
    objeto = Column(String)
    campos_estruturados = Column(JSON)
    sistema_origem = Column(String, default="SAAB-Tech")

# SAAB-Tech: Salva contrato
def salvar_contrato_db(contrato: dict):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    novo_contrato = Contrato(**contrato)
    session.add(novo_contrato)
    session.commit()

# Contrato-Regional: Lê contrato
def buscar_contrato_db(numero: str):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    contrato = session.query(Contrato).filter_by(numero_contrato=numero).first()
    return contrato
```

---

## 3. ESTRUTURA DE DADOS COMPARTILHADA

### Schema de Contrato (JSON):

```json
{
  "schema_version": "1.0",
  "sistema_origem": "SAAB-Tech",
  "timestamp_geracao": "2025-12-16T10:30:00",
  "metadata": {
    "usuario_responsavel": "user@tjsp.jus.br",
    "unidade": "SAAB",
    "status_workflow": "contrato_assinado"
  },
  "contrato": {
    "numero_contrato": "123/2025",
    "data_assinatura": "2025-12-01",
    "vigencia": "12 meses",
    "valor_global": "R$ 500.000,00",
    "objeto": "Prestação de serviços de...",
    "partes": {
      "contratante": "TJSP - Comarca de...",
      "contratada": "Empresa XYZ Ltda"
    },
    "gestores": {
      "gestor": "Nome do Gestor",
      "fiscal": "Nome do Fiscal"
    },
    "clausulas": {
      "obrigacoes_contratada": "...",
      "penalidades": "...",
      "rescisao": "..."
    }
  },
  "documentos_anexos": [
    {
      "tipo": "contrato_assinado",
      "url": "https://storage.tjsp/contratos/123_2025.pdf",
      "hash": "sha256:abc123..."
    }
  ],
  "integracao_fiscal": {
    "habilitada": true,
    "raj": "RAJ 10.1",
    "fiscal_designado": "fiscal@tjsp.jus.br"
  }
}
```

---

## 4. FLUXO DE INTEGRAÇÃO (CENÁRIO PILOTO)

### Fase 1: Contrato Gerado no SAAB-Tech

```
1. Usuário finaliza Contrato no módulo 08_Contrato
2. Clica "Salvar Contrato"
   └─> SAAB-Tech exporta JSON para /exports/contratos/
   └─> (Futuro) Dispara webhook para Contrato-Regional-IA
3. JSON fica disponível para importação
```

### Fase 2: Importação no Contrato-Regional-IA

```
1. Fiscal acessa Dashboard no Contrato-Regional-IA
2. Clica "Importar Contrato do SAAB-Tech"
3. Sistema lista contratos disponíveis em /exports/contratos/
4. Fiscal seleciona contrato RAJ 10.1
5. Sistema carrega dados estruturados
6. Inicia módulo de fiscalização
```

### Fase 3: Fiscalização e Notificações

```
1. Copilot responde perguntas com base no contrato carregado
2. Sistema gera notificações contratuais automaticamente
3. "Como proceder" exibe orientações contextuais
4. (Futuro) Feedback retorna ao SAAB-Tech via API
```

---

## 5. IMPLEMENTAÇÃO PRÁTICA

### 5.1 No SAAB-Tech (Módulo Contrato)

Adicionar botão de exportação para fiscalização:

```python
# streamlit_app/pages/08_Contrato.py

st.divider()
st.markdown("### 🔗 Integração com Fiscalização")

col1, col2 = st.columns(2)

with col1:
    st.info("📤 Enviar contrato para módulo de fiscalização regional")
    
with col2:
    if st.button("📤 Habilitar para Fiscalização", use_container_width=True):
        # Exportar com flag de integração
        dados_integracao = {
            "schema_version": "1.0",
            "sistema_origem": "SAAB-Tech",
            "timestamp_geracao": datetime.now().isoformat(),
            "integracao_fiscal": {
                "habilitada": True,
                "raj": st.selectbox("Selecione RAJ:", ["RAJ 10.1", "RAJ 10.2"]),
                "fiscal_designado": st.text_input("Email do Fiscal:")
            },
            "contrato": campos_formulario  # Dados já existentes
        }
        
        # Salvar em diretório de integração
        arquivo = f"exports/integracao_fiscal/contrato_{numero_contrato}.json"
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_integracao, f, ensure_ascii=False, indent=2)
        
        st.success("✅ Contrato habilitado para fiscalização!")
        st.info(f"📁 Arquivo disponível em: `{arquivo}`")
```

---

### 5.2 No Contrato-Regional-IA (Dashboard)

Botão de importação:

```python
# pages/01_Dashboard.py

st.markdown("### 📥 Importar Contrato do SAAB-Tech")

# Listar contratos disponíveis
contratos_disponiveis = listar_contratos_integracao()

if contratos_disponiveis:
    contrato_selecionado = st.selectbox(
        "Selecione o contrato:",
        contratos_disponiveis,
        format_func=lambda x: f"{x['numero_contrato']} - {x['objeto'][:50]}..."
    )
    
    if st.button("📥 Importar e Iniciar Fiscalização", type="primary"):
        # Carregar dados completos
        dados_contrato = carregar_contrato_integracao(contrato_selecionado['arquivo'])
        
        # Salvar em session_state
        st.session_state["contrato_fiscal"] = dados_contrato["contrato"]
        st.session_state["metadata_origem"] = dados_contrato["metadata"]
        
        st.success("✅ Contrato importado com sucesso!")
        st.switch_page("pages/02_Contrato_Individual.py")
else:
    st.info("Nenhum contrato disponível para importação")
```

---

## 6. AUTENTICAÇÃO E SEGURANÇA

### 6.1 API REST (Quando Implementada)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Valida token JWT do sistema consumidor"""
    token = credentials.credentials
    
    if not validar_token_tjsp(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    return token

@app.get("/api/v1/contratos/{numero}")
async def get_contrato(
    numero: str, 
    token: str = Depends(verificar_token)
):
    """Endpoint protegido por autenticação"""
    contrato = buscar_contrato(numero)
    
    # Log de auditoria
    registrar_acesso(token, "get_contrato", numero)
    
    return contrato
```

### 6.2 Shared Storage (Permissões)

```bash
# Permissões do diretório compartilhado
chown -R saab-tech:fiscal-regional /shared/contratos/
chmod 750 /shared/contratos/
chmod 640 /shared/contratos/*.json

# Apenas SAAB-Tech pode escrever
# Fiscal-Regional pode apenas ler
```

---

## 7. MONITORAMENTO E AUDITORIA

### Log de Integrações:

```python
import logging
from datetime import datetime

logger = logging.getLogger("integracao_tjsp")

def registrar_integracao(
    sistema_origem: str,
    sistema_destino: str,
    acao: str,
    dados: dict
):
    """Registra evento de integração para auditoria"""
    
    evento = {
        "timestamp": datetime.now().isoformat(),
        "sistema_origem": sistema_origem,
        "sistema_destino": sistema_destino,
        "acao": acao,
        "usuario": get_current_user(),
        "dados_resumo": {
            "numero_contrato": dados.get("numero_contrato"),
            "tipo_operacao": acao
        }
    }
    
    # Log estruturado
    logger.info(f"INTEGRACAO: {evento}")
    
    # Salvar em banco de auditoria (futuro)
    # salvar_log_auditoria(evento)
```

---

## 8. ROADMAP DE INTEGRAÇÃO

### MVP (Fase Atual - Q1 2025):
```
□ Exportação JSON manual (SAAB-Tech → arquivo)
□ Importação JSON manual (arquivo → Contrato-Regional-IA)
□ Schema de dados v1.0 definido
□ Documentação de integração
```

### Fase 2 (Q2 2025):
```
□ API REST no SAAB-Tech (endpoints básicos)
□ Autenticação JWT
□ Webhooks de notificação
□ Dashboard de integrações ativas
```

### Fase 3 (Q3 2025):
```
□ Database compartilhado (PostgreSQL)
□ Sincronização bidirecional
□ Feedback de fiscalização → SAAB-Tech
□ Relatórios consolidados
```

### Fase 4 (Q4 2025):
```
□ Microserviços escaláveis
□ Message Queue (RabbitMQ/Kafka)
□ Integração com outros sistemas TJSP
□ Portal unificado de gestão
```

---

## 9. CHECKLIST DE INTEGRAÇÃO

Ao implementar integração entre sistemas:

```
□ Schema de dados definido e versionado
□ Logs de auditoria implementados
□ Tratamento de erros robusto
□ Validação de dados em ambas as pontas
□ Documentação de API (se aplicável)
□ Testes de integração end-to-end
□ Plano de rollback em caso de falha
□ Monitoramento de saúde da integração
□ Controle de acesso e permissões
□ Backup de dados críticos
```

---

## 10. CONTATOS E SUPORTE

### Responsáveis pela Integração:

**SAAB-Tech**:
- Engenheiro Synapse
- saab-tech@tjsp.jus.br

**Contrato-Regional-IA**:
- Equipe RAJ 10.1
- fiscal-regional@tjsp.jus.br

### Canais de Comunicação:
- Issues GitHub (técnico)
- Email institucional (administrativo)
- Reuniões quinzenais de alinhamento

---

## 11. REFERÊNCIAS

- **Arquitetura SAAB-Tech**: Ver `ARCHITECTURE_PATTERNS.md`
- **Design System**: Ver `DESIGN_SYSTEM_TJSP.md`
- **Padrões de Código**: Ver `CODE_STANDARDS.md`
- **API Docs**: (Futuro) `https://saab-tech.tjsp.gov.br/api/docs`

---

**Última atualização**: 16/12/2025  
**Mantido por**: Engenheiro Synapse | SAAB/TJSP  
**Status**: 🟡 MVP em implementação (Q1 2025)
