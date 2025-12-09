# 🚨 Sistema de Alertas v2025.1 - Guia Completo

## 📋 Visão Geral

O **Sistema de Alertas** do SynapseNext é responsável por monitorar automaticamente todos os documentos processados (DFD, ETP, TR, EDITAL, CONTRATO) e detectar:

- ✅ **Campos obrigatórios vazios ou incompletos**
- ✅ **Validações de formato e tamanho mínimo**
- ✅ **Inconsistências entre documentos** (divergência de valores, objetos diferentes)
- ✅ **Arquivos ausentes no diretório exports/**

---

## 🎯 Funcionalidades Principais

### 1. **Coleta de Estado do Sistema**
- Varre o diretório `exports/` buscando arquivos `*_data.json`
- Extrai campos de cada documento processado
- Identifica arquivos ausentes
- Retorna estado completo com timestamps

### 2. **Validações por Módulo**

#### 📄 DFD (Documento de Formalização da Demanda)
| Campo | Validação | Severidade | Limite |
|-------|-----------|------------|--------|
| `objeto` | Tamanho mínimo | Médio | 100 caracteres |
| `justificativa` | Tamanho mínimo | Médio | 150 caracteres |
| `valor_estimado` | Formato monetário (R$ + dígitos) | Alto | Obrigatório |
| `responsavel` | Preenchimento | Crítico | Não vazio |

#### 📋 ETP (Estudos Técnicos Preliminares)
| Campo | Validação | Severidade | Limite |
|-------|-----------|------------|--------|
| `prazo_execucao` | Não indefinido | Alto | Não pode ser "a definir", "n/a" |
| `orcamento_previsto` | Definido | Alto | Não pode conter "definir" |

#### 📝 TR (Termo de Referência)
| Campo | Validação | Severidade | Limite |
|-------|-----------|------------|--------|
| `especificacao_tecnica` | Tamanho mínimo | Médio | 200 caracteres |
| `criterio_aceitacao` | Tamanho mínimo | Alto | 50 caracteres |

#### 📢 EDITAL
| Campo | Validação | Severidade | Limite |
|-------|-----------|------------|--------|
| `numero_edital` | Formato válido | Alto | Não pode ser "N/A" ou "XXX/YYYY" |
| `obrigacoes_contratada` | Mínimo de obrigações | Médio | 5 obrigações (separadas por `;`) |

#### 📑 CONTRATO
| Campo | Validação | Severidade | Limite |
|-------|-----------|------------|--------|
| `numero_contrato` | Formato válido | Alto | Não pode conter "XXX" |
| `partes_contratada` | Completude | Alto | Mínimo 50 caracteres |
| `obrigacoes_contratada` | Tamanho mínimo | Médio | 500 caracteres |

### 3. **Validações de Consistência Cross-Documento**

#### Divergência de Valores
- Compara `valor_estimado` (DFD), `valor_global` (EDITAL), `orcamento_previsto` (ETP)
- **Threshold**: divergência máxima de **20%**
- **Severidade**: Alto

#### Similaridade de Objetos
- Compara descrições de `objeto` entre todos os documentos
- **Método**: Similaridade de Jaccard (palavras em comum / palavras totais)
- **Threshold**: similaridade mínima de **30%**
- **Severidade**: Médio

---

## 🖥️ Interface (Página 09_Alertas.py)

### Componentes da Interface

1. **📊 Cards de Resumo**
   - 🚨 Críticos: pendências graves
   - ⚠️ Médios: atenção necessária
   - ℹ️ Informativos: avisos gerais

2. **🔄 Botão Atualizar**
   - Re-scan completo do sistema
   - Salva novo registro no histórico
   - Atualiza interface automaticamente

3. **🔍 Filtros na Sidebar**
   - **Por Módulo**: DFD, ETP, TR, EDITAL, CONTRATO, SISTEMA
   - **Por Severidade**: alto, medio, baixo
   - Aplicação em tempo real

4. **📈 Gráfico de Distribuição**
   - Visualização por tipo de alerta
   - Atualiza conforme filtros selecionados

5. **🔍 Detalhamento dos Alertas**
   - Lista completa com badges coloridos por módulo
   - Mensagem descritiva do problema
   - 💡 Recomendação de ação
   - Timestamp de detecção

6. **📜 Histórico de Execuções**
   - Últimas 10 execuções do sistema
   - Totais por execução
   - Resumo textual

7. **📊 Estatísticas do Sistema**
   - Total de execuções registradas
   - Média de alertas críticos
   - Média de alertas totais
   - Primeira e última execução

---

## 🔧 Backend (utils/alertas_pipeline.py)

### Funções Principais

#### `gerar_alertas_reais(salvar_historico=True)`
**Função orquestradora principal**
- Coleta estado do sistema
- Analisa cada documento
- Valida consistência cross-doc
- Calcula totais por severidade
- Salva no histórico (opcional)

**Retorno:**
```python
{
    "gerado_em": "09/12/2025 12:06:48",
    "timestamp": "2025-12-09T12:06:48",
    "totais": {
        "total": 20,
        "critico": 18,
        "medio": 1,
        "informativo": 1,
        "alto": 18,
        "medio_sev": 1,
        "baixo": 1
    },
    "alerts": [
        {
            "id": "dfd_objeto_curto",
            "modulo": "DFD",
            "campo": "objeto",
            "tipo": "Médio",
            "severidade": "medio",
            "categoria": "Validação",
            "mensagem": "Campo 'objeto' tem menos de 100 caracteres no DFD",
            "recomendacao": "Expandir descrição do objeto contratado",
            "timestamp": "09/12/2025 12:06:48"
        }
    ],
    "resumo": "20 alertas – 18 críticos, 1 médios, 1 informativos",
    "estado_sistema": {...}
}
```

#### `carregar_historico(limit=10)`
**Carrega histórico de execuções anteriores**
- Lista últimos N arquivos JSON
- Retorna resumos ordenados por data (mais recente primeiro)

**Retorno:**
```python
[
    {
        "arquivo": "alertas_20251209_120648.json",
        "timestamp": "09/12/2025 12:06:48",
        "totais": {"total": 20, "critico": 18, "medio": 1, "informativo": 1},
        "resumo": "20 alertas – 18 críticos, 1 médios, 1 informativos"
    }
]
```

#### `obter_estatisticas_historico()`
**Calcula estatísticas agregadas do histórico**
- Total de execuções
- Médias de alertas críticos/totais
- Primeira e última execução
- Evolução temporal

**Retorno:**
```python
{
    "total_execucoes": 15,
    "primeira_execucao": "20251201_140030",
    "ultima_execucao": "20251209_120648",
    "media_alertas_criticos": 12.3,
    "media_alertas_total": 18.7,
    "evolucao": [...]
}
```

#### `gerar_alertas(snapshot=None)`
**Wrapper de compatibilidade**
- Usado pelo Painel de Governança (página 11)
- Chama `gerar_alertas_reais()` internamente
- Retorna apenas lista de alertas (sem totais)

---

## 📂 Estrutura de Arquivos

```
exports/
└── analises/
    └── historico_alertas/
        ├── alertas_20251209_120648.json  # Registro mais recente
        ├── alertas_20251208_153022.json
        └── alertas_20251207_091545.json
```

Cada arquivo JSON contém:
- `gerado_em`: timestamp legível
- `totais`: contadores por tipo/severidade
- `alerts`: lista completa de alertas
- `resumo`: texto descritivo
- `estado_sistema`: snapshot completo dos documentos

---

## 🧪 Como Testar

### 1. **Teste Manual via Terminal**
```bash
cd /workspaces/synapse-next-homologacao

# Gerar alertas reais
python3 -c "
from utils.alertas_pipeline import gerar_alertas_reais
resultado = gerar_alertas_reais(salvar_historico=True)
print(f'Total: {resultado[\"totais\"][\"total\"]} alertas')
print(f'Críticos: {resultado[\"totais\"][\"critico\"]}')
print(f'Histórico salvo: {resultado.get(\"historico_salvo\")}')
"

# Carregar histórico
python3 -c "
from utils.alertas_pipeline import carregar_historico
historico = carregar_historico(limit=5)
for h in historico:
    print(f'{h[\"timestamp\"]}: {h[\"resumo\"]}')
"
```

### 2. **Teste via Interface Streamlit**
1. Iniciar aplicação: `streamlit run streamlit_app/Home.py`
2. Navegar para: **⚠️ Alertas** (página 09)
3. Observar contadores nos cards
4. Clicar **🔄 Atualizar Alertas**
5. Testar filtros na sidebar
6. Verificar detalhamento dos alertas
7. Expandir histórico e estatísticas

### 3. **Teste de Integração com Módulos**
1. Processar um DFD com campo obrigatório vazio
2. Abrir página 09_Alertas
3. Verificar se alerta crítico aparece
4. Corrigir o campo no DFD
5. Clicar **🔄 Atualizar**
6. Verificar se alerta desaparece

---

## 🐛 Troubleshooting

### Problema: "Nenhum alerta detectado"
**Causa**: Nenhum arquivo `*_data.json` em `exports/`  
**Solução**: Processar pelo menos um documento (DFD, ETP, TR, EDITAL ou CONTRATO)

### Problema: "Erro ao ler arquivo JSON"
**Causa**: Arquivo corrompido ou formato inválido  
**Solução**: Deletar arquivo corrompido e reprocessar documento

### Problema: "Histórico vazio"
**Causa**: Primeira execução ou `salvar_historico=False`  
**Solução**: Clicar **🔄 Atualizar Alertas** para gerar primeiro registro

### Problema: "Muitos alertas críticos"
**Causa**: Documentos com campos obrigatórios vazios  
**Solução**: 
1. Verificar detalhamento dos alertas
2. Identificar campos problemáticos
3. Reprocessar documentos corrigindo os campos
4. Atualizar alertas

---

## 📊 Interpretação de Alertas

### Severidade: **Alto (Crítico)**
🚨 **Ação Imediata Necessária**
- Campos obrigatórios vazios
- Formatos inválidos que impedem processamento
- Inconsistências graves entre documentos

### Severidade: **Médio**
⚠️ **Atenção Necessária**
- Campos com tamanho abaixo do recomendado
- Formatos válidos mas não ideais
- Divergências moderadas entre documentos

### Severidade: **Baixo (Informativo)**
ℹ️ **Avisos Gerais**
- Arquivos ausentes (ainda não processados)
- Sugestões de melhorias
- Notificações de sistema

---

## 🔄 Fluxo de Trabalho Recomendado

1. **Processar Documentos**
   - Página 02: DFD
   - Página 03: ETP
   - Página 05: TR
   - Página 06: EDITAL
   - Página 08: CONTRATO

2. **Verificar Alertas**
   - Abrir Página 09: Alertas
   - Clicar **🔄 Atualizar Alertas**
   - Revisar alertas críticos

3. **Corrigir Problemas**
   - Identificar campos problemáticos
   - Voltar às páginas específicas
   - Reprocessar com correções

4. **Validar Correções**
   - Voltar à Página 09
   - Atualizar alertas
   - Confirmar redução de alertas críticos

5. **Monitorar Evolução**
   - Verificar histórico
   - Acompanhar estatísticas
   - Manter alertas críticos = 0

---

## 📝 Notas Técnicas

- **Persistência**: Todos os alertas são salvos em JSON com encoding UTF-8
- **Performance**: Scan completo leva ~1-2 segundos para 5 documentos
- **Concorrência**: Sistema é thread-safe para leitura
- **Cache**: Interface usa `st.session_state` para evitar re-scans desnecessários
- **Compatibilidade**: Mantida com Painel de Governança via wrapper `gerar_alertas()`

---

## 🎯 Próximas Melhorias (Futuro)

- [ ] Integração automática com hooks nas páginas de processamento
- [ ] Badge de notificação na sidebar com contador de críticos
- [ ] Toast warnings ao salvar documento com problemas
- [ ] Export de alertas para Excel/PDF
- [ ] Dashboard de evolução temporal dos alertas
- [ ] Alertas por e-mail para stakeholders

---

**Versão**: 2025.1  
**Data**: Dezembro/2025  
**Autor**: Sistema SynapseNext TJSP  
**Homologação**: ✅ Completa
