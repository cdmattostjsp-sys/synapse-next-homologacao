# Documentação de Referência SAAB-Tech

> **Propósito**: Kit de referência arquitetural para projetos satélite do TJSP  
> **Versão**: 2025.1-homolog  
> **Última atualização**: 16/12/2025

---

## 📚 ÍNDICE DE DOCUMENTOS

### 1. [ARCHITECTURE_PATTERNS.md](ARCHITECTURE_PATTERNS.md)
**Padrões arquiteturais do SAAB-Tech**

Conteúdo:
- ✅ Estrutura de diretórios completa
- ✅ Separação de responsabilidades (UI/Agentes/Serviços)
- ✅ Padrão de módulos (Pages)
- ✅ Padrão de agentes (BaseAgent)
- ✅ Gerenciamento de Session State
- ✅ Integração entre módulos
- ✅ Exportação de dados (JSON/DOCX)
- ✅ Escalabilidade futura

**Use quando**: Criar estrutura inicial de novo projeto

---

### 2. [DESIGN_SYSTEM_TJSP.md](DESIGN_SYSTEM_TJSP.md)
**CSS institucional e padrões visuais PJe-inspired**

Conteúdo:
- ✅ Paleta de cores oficial
- ✅ CSS completo copiável
- ✅ Tipografia (hierarquia de títulos)
- ✅ Componentes visuais (botões, expanders, tabs)
- ✅ Layouts de colunas
- ✅ Ícones funcionais
- ✅ Responsividade
- ✅ Acessibilidade

**Use quando**: Aplicar design institucional em páginas

---

### 3. [INTEGRATION_BLUEPRINT.md](INTEGRATION_BLUEPRINT.md)
**Blueprint para integração entre sistemas**

Conteúdo:
- ✅ Arquitetura de integração
- ✅ Opções: API REST / Shared Storage / Database
- ✅ Schema de dados compartilhada
- ✅ Fluxo de integração (SAAB-Tech ↔ Satélite)
- ✅ Autenticação e segurança
- ✅ Monitoramento e auditoria
- ✅ Roadmap de implementação

**Use quando**: Conectar sistemas do ecossistema TJSP

---

### 4. [CODE_STANDARDS.md](CODE_STANDARDS.md)
**Convenções de código e boas práticas**

Conteúdo:
- ✅ Estrutura de imports
- ✅ Nomenclatura (arquivos, variáveis, funções, classes)
- ✅ Formatação de código
- ✅ Docstrings e comentários
- ✅ Type hints
- ✅ Tratamento de erros
- ✅ Streamlit best practices
- ✅ Versionamento Git
- ✅ Testes
- ✅ Segurança

**Use quando**: Escrever código Python/Streamlit institucional

---

## 🎯 COMO USAR ESTA REFERÊNCIA

### Cenário 1: Criar Novo Projeto do Zero

```bash
# 1. Consultar estrutura de diretórios
cat ARCHITECTURE_PATTERNS.md  # Seção 1

# 2. Criar estrutura básica
mkdir -p streamlit_app/pages agents utils prompts knowledge

# 3. Copiar CSS institucional
cat DESIGN_SYSTEM_TJSP.md     # Seção 2 (CSS completo)

# 4. Aplicar convenções de código
cat CODE_STANDARDS.md          # Durante desenvolvimento
```

---

### Cenário 2: Aplicar Design Institucional

```python
# 1. Abrir DESIGN_SYSTEM_TJSP.md
# 2. Copiar CSS da Seção 2 (completo)
# 3. Colar no topo da página:

st.markdown("""
<style>
/* [COLAR CSS AQUI] */
</style>
""", unsafe_allow_html=True)

# 4. Usar padrões de componentes (Seção 4)
st.markdown("<h1>Título</h1>", unsafe_allow_html=True)
st.markdown("### Seção")
st.button("Ação", type="primary", use_container_width=True)
```

---

### Cenário 3: Integrar com SAAB-Tech

```bash
# 1. Ler INTEGRATION_BLUEPRINT.md completo
# 2. Escolher opção de integração (Seção 2)
# 3. Implementar schema de dados (Seção 3)
# 4. Seguir fluxo de integração (Seção 4)
# 5. Adicionar logs de auditoria (Seção 7)
```

---

### Cenário 4: Code Review / Onboarding

```bash
# Novos desenvolvedores devem ler (nesta ordem):
1. CODE_STANDARDS.md          # Convenções básicas
2. ARCHITECTURE_PATTERNS.md   # Estrutura do projeto
3. DESIGN_SYSTEM_TJSP.md      # Padrões visuais
4. INTEGRATION_BLUEPRINT.md   # (se aplicável)
```

---

## 📦 PROJETOS QUE USAM ESTA REFERÊNCIA

### 1. SAAB-Tech (Origem)
- **Repositório**: `synapse-next-homologacao`
- **Status**: ✅ Homologado
- **Escopo**: Fase Interna de Licitação
- **Módulos**: INSUMOS, DFD, ETP, TR, Edital, Contrato, Validador

### 2. Contrato-Regional-IA (Satélite)
- **Repositório**: `contrato-regional-ia` (em desenvolvimento)
- **Status**: 🟡 MVP Q1/2025
- **Escopo**: Fiscalização de contratos regionais
- **Módulos**: Dashboard, Contrato Individual, Copilot, Notificações, Orientações
- **Integração**: JSON Shared Storage (MVP) → API REST (Q2/2025)

---

## 🔄 VERSIONAMENTO

### Política de Atualização:

**Versão Atual**: 2025.1-homolog (16/12/2025)

**Quando atualizar**:
- ✅ Novos padrões aprovados institucionalmente
- ✅ Mudanças arquiteturais validadas em produção
- ✅ Feedback de múltiplos projetos satélite
- ✅ Atualizações de legislação/normativas

**Processo**:
1. Proposta de mudança via Issue GitHub
2. Revisão técnica (Engenheiro Synapse)
3. Aprovação institucional (SAAB/TJSP)
4. Atualização de documentos
5. Notificação aos projetos satélite

---

## 📞 CONTATO E SUPORTE

### Responsáveis:

**Técnico**:
- Engenheiro Synapse
- GitHub: @engenheiro-synapse
- Email: synapse@tjsp.jus.br

**Institucional**:
- SAAB - Secretaria de Administração e Abastecimento
- Email: saab-tech@tjsp.jus.br

### Canais:

- 🐛 **Bugs/Issues**: GitHub Issues (técnico)
- 📧 **Dúvidas**: Email institucional
- 📚 **Documentação**: Este diretório
- 💬 **Reuniões**: Quinzenais (alinhamento de projetos)

---

## 🎓 RECURSOS ADICIONAIS

### Documentação Externa:

- [Streamlit Docs](https://docs.streamlit.io/)
- [PEP 8 - Python Style Guide](https://peps.python.org/pep-0008/)
- [FastAPI Docs](https://fastapi.tiangolo.com/) (para APIs futuras)
- [Lei 14.133/2021](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm)

### Documentação Interna:

- `/GUIA_PADRAO_VISUAL_PJe.md` (raiz do projeto)
- `/ARQUITETURA_AGENTES.md` (detalhamento de agentes)
- `/knowledge/` (base de conhecimento institucional)

---

## ⚠️ AVISOS IMPORTANTES

### 🔒 Segurança:

- **NUNCA** commitar secrets/credenciais
- **SEMPRE** usar `.env` ou Streamlit secrets
- **VALIDAR** inputs do usuário
- **AUDITAR** integrações entre sistemas

### 🏛️ Conformidade:

- Seguir Lei 14.133/2021
- Respeitar normativas TJSP
- Manter rastreabilidade de decisões
- Documentar integrações

### 📝 Licenciamento:

- Código institucional TJSP
- Uso restrito a projetos autorizados
- Consultar SAAB antes de compartilhar externamente

---

## 🗺️ ROADMAP DESTA DOCUMENTAÇÃO

### Q1/2025 (Atual):
- ✅ 4 documentos de referência
- ✅ Kit completo para MVP
- ✅ Exemplos de código copiáveis

### Q2/2025:
- ⏳ Templates de código (`.py` prontos)
- ⏳ Scripts de scaffolding
- ⏳ Testes automatizados de conformidade

### Q3/2025:
- ⏳ CLI para gerar projetos
- ⏳ Biblioteca compartilhada `tjsp-commons`
- ⏳ Portal de documentação interativo

### Q4/2025:
- ⏳ Certificação de projetos satélite
- ⏳ Marketplace de componentes
- ⏳ Governança de integração

---

## 📊 MÉTRICAS DE ADOÇÃO

**Projetos Ativos**: 2  
**Linhas de Código Documentadas**: ~500 (exemplos)  
**Padrões Definidos**: 47  
**Última Revisão**: 16/12/2025

---

## 🙏 AGRADECIMENTOS

Este kit de referência foi desenvolvido com base na experiência prática do **Projeto SAAB-Tech** e feedback de múltiplas equipes do TJSP.

Agradecimentos especiais a:
- Equipe SAAB/TJSP
- Desenvolvedores dos projetos satélite
- Usuários finais (fiscais, gestores, administradores)

---

**Mantido com ❤️ pelo time SAAB-Tech | TJSP**

