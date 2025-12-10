# 🧪 Guia de Testes - Refatoração Home.py v6

**Projeto:** SAAB-Tech  
**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Objetivo:** Validar refatoração modular e integração de documentação

---

## 📋 Checklist de Testes

### ✅ FASE 1: Verificação de Arquivos

**Status:** ✅ COMPLETO

- [x] `streamlit_app/Home.py` - Refatorado (83 linhas)
- [x] `streamlit_app/Home.py.backup` - Backup original (192 linhas)
- [x] `streamlit_app/utils/home_components.py` - Componentes modulares (221 linhas)
- [x] `streamlit_app/pages/99_📚_Documentação.py` - Nova página (375 linhas)
- [x] 7 manuais em `manuais/MANUAL_*.md` (184 KB total)

---

### ✅ FASE 2: Validação Técnica

**Status:** ✅ COMPLETO

#### Validações Executadas:

```bash
✓ Diretório manuais/ acessível
✓ 7 manuais encontrados (21-36 KB cada)
✓ Componentes modulares carregados
✓ Página de documentação criada
✓ Backup original preservado
✓ 3 botões de navegação configurados
✓ Todos apontam para pages/99_📚_Documentação.py
✓ 7 referências de manuais mapeadas
✓ Integração completa validada
```

---

### 🧪 FASE 3: Testes Funcionais (PARA VOCÊ EXECUTAR)

#### **Teste 1: Iniciar Aplicação**

```bash
cd /workspaces/synapse-next-homologacao
streamlit run streamlit_app/Home.py
```

**Resultado Esperado:**
- ✅ Aplicação inicia sem erros
- ✅ Porta padrão 8501 abre no navegador
- ✅ Página Home carrega em 2-3 segundos

---

#### **Teste 2: Validar Home.py Refatorado**

**Componentes a verificar:**

1. **Cabeçalho Institucional**
   - [ ] Logo TJSP visível
   - [ ] Título "Projeto SAAB-Tech"
   - [ ] Subtítulo "Secretaria de Administração e Abastecimento • TJSP"
   - [ ] Linha divisória horizontal

2. **Seção de Introdução**
   - [ ] Texto de boas-vindas exibido
   - [ ] 4 bullet points visíveis:
     - Insumos, DFD, ETP, TR
     - Relatórios técnicos personalizados
     - Painéis de governança
     - Interoperabilidade

3. **Cards de Navegação (Grid 5 colunas)**
   - [ ] Card "📁 Documentos Técnicos" - azul com hover
   - [ ] Card "📊 Painel Executivo" - azul com hover
   - [ ] Card "⚖️ Governança & Conformidade" - azul com hover
   - [ ] Card "🔗 Interoperabilidade" - azul com hover
   - [ ] Card "📈 Relatórios & Dashboards" - azul com hover
   - [ ] Animação de elevação ao passar o mouse

4. **Seção de Manuais (NOVA FUNCIONALIDADE)**
   - [ ] Título "📚 Consulte os Manuais do Sistema"
   - [ ] Subtítulo explicativo visível
   - [ ] 3 cards horizontais:
     - [ ] "📖 Manuais Básicos" (esquerda)
     - [ ] "🎓 Módulos Avançados" (centro)
     - [ ] "🆘 Suporte" (direita)
   - [ ] 3 botões azuis abaixo dos cards

5. **Rodapé**
   - [ ] Texto "TJSP • Secretaria de Administração..."
   - [ ] Timestamp de build atualizado
   - [ ] Logo TJSP no final da página

---

#### **Teste 3: Navegação para Documentação**

**Passo a Passo:**

1. Na Home, role até "📚 Consulte os Manuais do Sistema"
2. Clique no botão **"Acessar Manuais Básicos"**

**Resultado Esperado:**
- [ ] Sistema redireciona para `99_📚_Documentação.py`
- [ ] URL muda para `.../99_📚_Documentação`
- [ ] Página aparece na barra lateral com emoji 📚

3. Repita para os outros 2 botões:
   - [ ] "Acessar Módulos Avançados" → mesma página
   - [ ] "Acessar FAQ e Ajuda" → mesma página

---

#### **Teste 4: Interface de Documentação**

**Componentes a verificar:**

1. **Cabeçalho da Página**
   - [ ] Banner gradiente (azul → vermelho)
   - [ ] Título "📚 Documentação do Sistema"
   - [ ] Subtítulo "Central de Manuais do Projeto SAAB-Tech"

2. **Breadcrumb**
   - [ ] Texto "🏠 Home → 📚 Documentação"
   - [ ] Fundo cinza claro
   - [ ] Link "Home" funcional

3. **Estatísticas (4 boxes azuis)**
   - [ ] Box 1: "7 Manuais Disponíveis"
   - [ ] Box 2: "16 Módulos Documentados"
   - [ ] Box 3: "300+ Páginas de Conteúdo"
   - [ ] Box 4: "2025.1 Versão do Sistema"

4. **Seletor de Manual**
   - [ ] Dropdown com 7 opções:
     - 📘 Manual 01 - Introdução e Primeiros Passos
     - 📗 Manual 02 - Módulos de Planejamento
     - 📙 Manual 03A - Edital e Validador
     - 📕 Manual 03B - Contrato Administrativo
     - 📔 Manual 04 - Módulos de Governança
     - 📓 Manual 05 - Módulos Avançados
     - 📖 Manual 06 - FAQ e Troubleshooting

---

#### **Teste 5: Visualização de Manual**

**Passo a Passo:**

1. Selecione "📘 Manual 01 - Introdução e Primeiros Passos"

**Card Informativo:**
- [ ] Descrição exibida
- [ ] Campo "Páginas" preenchido
- [ ] Campo "Nível" exibido (Iniciante/Intermediário/Avançado)

2. Clique na aba **"👁️ Visualizar"**

**Conteúdo:**
- [ ] Markdown renderizado corretamente
- [ ] Títulos (# ## ###) formatados
- [ ] Listas numeradas e bullet points visíveis
- [ ] Tabelas renderizadas
- [ ] Blocos de código com syntax highlighting
- [ ] Scrollbox funcional (altura ~600px)
- [ ] Todo o conteúdo do manual visível

3. Clique na aba **"📥 Download"**

**Download:**
- [ ] Descrição do formato exibida
- [ ] Botão "⬇️ Baixar MANUAL_01_INTRODUCAO_PRIMEIROS_PASSOS.md"
- [ ] Botão azul com largura total
- [ ] Ao clicar: arquivo .md baixado (21-36 KB)
- [ ] Arquivo abre em editor Markdown

---

#### **Teste 6: Testar Todos os Manuais**

**Repetir Teste 5 para cada manual:**

| Manual | Arquivo | Tamanho | Status |
|--------|---------|---------|--------|
| Manual 01 | MANUAL_01_INTRODUCAO_PRIMEIROS_PASSOS.md | 21.4 KB | [ ] |
| Manual 02 | MANUAL_02_MODULOS_PLANEJAMENTO.md | 30.4 KB | [ ] |
| Manual 03A | MANUAL_03A_EDITAL_VALIDADOR.md | 29.6 KB | [ ] |
| Manual 03B | MANUAL_03B_CONTRATO.md | 36.6 KB | [ ] |
| Manual 04 | MANUAL_04_MODULOS_GOVERNANCA.md | 18.9 KB | [ ] |
| Manual 05 | MANUAL_05_MODULOS_AVANCADOS.md | 21.4 KB | [ ] |
| Manual 06 | MANUAL_06_FAQ_TROUBLESHOOTING.md | 25.9 KB | [ ] |

**Para cada manual, verificar:**
- [ ] Seleção no dropdown funciona
- [ ] Card informativo atualiza
- [ ] Conteúdo renderiza corretamente
- [ ] Download funciona

---

#### **Teste 7: Seção de Ajuda**

**Verificar na página de documentação:**

1. **Bloco "Precisa de Mais Ajuda?" (3 colunas)**
   - [ ] Coluna 1: "📧 Suporte Técnico"
     - Email: saab-tech@tjsp.jus.br
     - SLA: 4 horas
   - [ ] Coluna 2: "🎓 Treinamentos"
     - Modalidades disponíveis
     - Certificação mencionada
   - [ ] Coluna 3: "📞 Contato Direto"
     - Telefone exibido
     - Horário de atendimento

2. **Rodapé**
   - [ ] Copyright TJSP 2025
   - [ ] Texto "Projeto SAAB-Tech | Ecossistema SAAB 5.0"
   - [ ] Timestamp atualizado

---

#### **Teste 8: Navegação Reversa**

**Passo a Passo:**

1. Estando na página de Documentação
2. Clique no link **"Home"** no breadcrumb
3. OU use a barra lateral do Streamlit

**Resultado Esperado:**
- [ ] Retorna para Home.py
- [ ] Página Home carrega completa
- [ ] Sem erros no console
- [ ] Estado preservado (sem recarregamento desnecessário)

---

### 🐛 FASE 4: Testes de Erros

#### **Teste 9: Resiliência a Erros**

**Cenários de erro simulados:**

1. **Manual ausente**
   ```bash
   # Renomeie temporariamente um manual
   mv manuais/MANUAL_01_INTRODUCAO_PRIMEIROS_PASSOS.md manuais/TEMP.md
   
   # Recarregue a página de documentação
   # Selecione Manual 01
   ```
   
   **Resultado Esperado:**
   - [ ] Mensagem de erro: "❌ Manual não encontrado"
   - [ ] Orientação: "Entre em contato com o suporte"
   - [ ] Sistema não quebra
   
   ```bash
   # Restaure o arquivo
   mv manuais/TEMP.md manuais/MANUAL_01_INTRODUCAO_PRIMEIROS_PASSOS.md
   ```

2. **Página sem permissões**
   - [ ] Sistema trata graciosamente
   - [ ] Mensagem de erro clara

---

### 📊 FASE 5: Testes de Performance

#### **Teste 10: Tempo de Carregamento**

**Medir tempos:**

| Ação | Tempo Esperado | Tempo Real | Status |
|------|----------------|------------|--------|
| Iniciar app | < 5s | _____s | [ ] |
| Carregar Home.py | < 2s | _____s | [ ] |
| Navegar para Documentação | < 1s | _____s | [ ] |
| Renderizar Manual 01 (21 KB) | < 3s | _____s | [ ] |
| Renderizar Manual 03B (36 KB) | < 4s | _____s | [ ] |
| Trocar entre manuais | < 2s | _____s | [ ] |
| Download de manual | < 1s | _____s | [ ] |

**Métrica de Sucesso:** Todos os tempos dentro do esperado

---

### 🎨 FASE 6: Testes de UI/UX

#### **Teste 11: Responsividade**

**Testar em diferentes resoluções:**

1. **Desktop (1920x1080)**
   - [ ] Grid de 5 cards na Home
   - [ ] Layout não quebra
   - [ ] Espaçamentos corretos

2. **Laptop (1366x768)**
   - [ ] Grid ajusta automaticamente
   - [ ] Conteúdo legível
   - [ ] Botões acessíveis

3. **Tablet (768x1024)**
   - [ ] Cards empilham corretamente
   - [ ] Fontes escaláveis
   - [ ] Navegação intuitiva

**Como testar no navegador:**
- Pressione `F12` → Toggle Device Toolbar
- Teste resoluções diferentes

---

#### **Teste 12: Acessibilidade**

**Verificar:**

- [ ] Contraste de cores adequado (azul TJSP vs branco)
- [ ] Textos legíveis (tamanhos de fonte apropriados)
- [ ] Botões com áreas de clique suficientes
- [ ] Navegação por teclado funcional (Tab, Enter)
- [ ] Emoji não quebram em navegadores antigos

---

### 🔄 FASE 7: Teste de Rollback

#### **Teste 13: Restaurar Versão Original**

**Se necessário voltar à versão anterior:**

```bash
cd /workspaces/synapse-next-homologacao/streamlit_app

# Restaurar Home.py original
cp Home.py.backup Home.py

# Remover componentes modulares (opcional)
rm -f utils/home_components.py

# Remover página de documentação (opcional)
rm -f pages/99_📚_Documentação.py

# Reiniciar Streamlit
streamlit run Home.py
```

**Resultado Esperado:**
- [ ] Sistema volta à versão 192 linhas
- [ ] Funcionalidade preservada
- [ ] Seção de manuais desaparece
- [ ] Sem erros

**Para reverter o rollback:**
```bash
# Restaurar versão refatorada
git restore streamlit_app/Home.py
git restore streamlit_app/utils/home_components.py
git restore streamlit_app/pages/99_📚_Documentação.py
```

---

## 📈 Métricas de Sucesso

### Critérios de Aprovação:

| Categoria | Critério | Meta | Status |
|-----------|----------|------|--------|
| **Funcionalidade** | Todos os testes funcionais passam | 100% | [ ] |
| **Performance** | Carregamento < 5s | < 5s | [ ] |
| **Navegação** | Botões funcionam corretamente | 3/3 | [ ] |
| **Visualização** | Todos os 7 manuais renderizam | 7/7 | [ ] |
| **Download** | Todos os downloads funcionam | 7/7 | [ ] |
| **UI/UX** | Interface responsiva e acessível | ✅ | [ ] |
| **Resiliência** | Erros tratados graciosamente | ✅ | [ ] |

---

## 🚀 Próximos Passos Após Testes

### Se TODOS os testes passarem:

1. ✅ **Marcar refatoração como COMPLETA**
2. ✅ **Remover arquivo de backup** (opcional, após 30 dias)
3. ✅ **Documentar mudanças no changelog**
4. ✅ **Treinar usuários na nova interface**
5. ✅ **Monitorar feedback inicial** (primeiros 7 dias)

### Se houver falhas:

1. 🔍 **Documentar falhas específicas**
2. 🔧 **Priorizar correções críticas**
3. 🧪 **Re-testar após ajustes**
4. 🔄 **Considerar rollback se necessário**

---

## 📞 Suporte Durante Testes

**Encontrou problemas?**

1. **Verifique console do navegador** (F12 → Console)
2. **Verifique logs do Streamlit** (terminal onde rodou `streamlit run`)
3. **Capture screenshots** de erros
4. **Anote mensagens de erro completas**

**Contato:**
- 📧 saab-tech@tjsp.jus.br
- 📋 Abra issue no repositório (se aplicável)

---

## ✅ Assinatura de Conclusão

**Testes executados por:** _________________________  
**Data:** ___/___/2025  
**Resultado geral:** [ ] APROVADO [ ] APROVADO COM RESSALVAS [ ] REPROVADO  
**Observações:**

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Guia de Testes v1.0**
