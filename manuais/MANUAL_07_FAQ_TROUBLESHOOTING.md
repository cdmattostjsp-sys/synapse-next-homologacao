# 📘 Manual do Usuário – Projeto SAAB-Tech

## Manual 07: FAQ e Troubleshooting

**Versão:** 2025.1  
**Data:** Dezembro/2025  
**Tribunal de Justiça do Estado de São Paulo**  
**Secretaria de Administração e Abastecimento (SAAB)**

---


---

## 📑 Índice

1. Perguntas Frequentes (FAQ)
2. Problemas Comuns e Soluções
3. Dicas de Otimização
4. Recuperação de Dados
5. Canais de Suporte
6. Recursos de Treinamento

---

## 1. Perguntas Frequentes

### 1.1 Uso Geral

**Q1: Como iniciar um novo processo de contratação?**
```
R: 1. Acesse módulo 🔧 Insumos
   2. Descreva a necessidade (texto ou upload)
   3. Processe com IA
   4. Dados propagam automaticamente para DFD
   5. Continue a jornada: DFD → ETP → TR → Edital → Contrato
```

**Q2: Posso pular etapas do processo?**
```
R: NÃO recomendado. A jornada foi projetada para:
   - Garantir conformidade legal
   - Manter rastreabilidade
   - Evitar dados faltantes
   
   Sequência obrigatória:
   Insumos → DFD → ETP → TR → Edital → Contrato
```

**Q3: Como salvar meu trabalho parcial?**
```
R: Em cada módulo:
   1. Preencha os campos desejados
   2. Clique [💾 Salvar]
   3. Dados salvos automaticamente em exports/[modulo]_data.json
   4. Backup automático criado em exports/backups/
```

**Q4: Posso trabalhar offline?**
```
R: NÃO. O sistema requer:
   - Conexão com internet (APIs OpenAI)
   - Acesso ao servidor Streamlit
   - Autenticação contínua
   
   Em caso de perda de conexão:
   - Dados em memória podem ser perdidos
   - Salve frequentemente (a cada 15-20 minutos)
```

**Q5: Quantos processos posso gerenciar simultaneamente?**
```
R: Ilimitado, mas com organização:
   - Use nomenclatura clara nos arquivos
   - Exporte JSONs com identificação
   - Mantenha estrutura de pastas:
     exports/
     ├─ processo_123456/
     │  ├─ dfd_data.json
     │  ├─ etp_data.json
     │  └─ tr_data.json
     └─ processo_789012/
        └─ ...
```

### 1.2 Módulo DFD

**Q6: Quantas seções o DFD tem?**
```
R: 11 seções obrigatórias (Lei 14.133/2021):
   1. Necessidade
   2. Objeto
   3. Alinhamento Estratégico
   4. Equipe de Planejamento
   5. Requisitos Necessidade
   6. Análise Mercado
   7. Estimativa Valor
   8. Estimativa Prazo
   9. Solução Adotada
   10. Justificativa
   11. Efeitos Não Contratação
```

**Q7: Posso usar DFD de outro processo como template?**
```
R: SIM, duas formas:
   1. Upload direto no módulo Insumos (destino: DFD)
   2. Copiar JSON de exports/ e editar manualmente
   
   Sempre revise e ajuste para o novo contexto!
```

**Q8: O que fazer se o DFDAgent gerar dados incorretos?**
```
R: 1. Revise o campo com erro
   2. Edite manualmente no formulário
   3. Salve novamente
   4. Se erro persistir, processe novamente com insumo mais detalhado
   5. Alternativa: preencha manualmente sem IA
```

### 1.3 Módulo ETP

**Q9: Quantas seções tem o ETP?**
```
R: 27 seções obrigatórias (IN SEGES/ME 40/2020):
   Seções 1-6: Objeto e contexto
   Seções 7-12: Análises de mercado
   Seções 13-18: Estimativas e contratação
   Seções 19-24: Gestão e riscos
   Seções 25-27: Sustentabilidade e declarações
```

**Q10: Como o ETP usa dados do DFD?**
```
R: Integração automática:
   DFD → ETP
   ├─ Objeto → Seção 1 (Definição Objeto)
   ├─ Necessidade → Seção 3 (Descrição Necessidade)
   ├─ Valor estimado → Seção 13 (Estimativa Valor)
   ├─ Prazo → Seção 14 (Estimativa Prazo)
   └─ Justificativa → Seção 5 (Requisitos Solução)
```

**Q11: ETP pode ser gerado sem DFD?**
```
R: Tecnicamente SIM, mas NÃO recomendado:
   - Perda de rastreabilidade
   - Dados incompletos ou inconsistentes
   - Violação da jornada de governança
   
   Exceção: Processos legados em migração
```

### 1.4 Módulo TR

**Q12: Quantas seções tem o Termo de Referência?**
```
R: 9 seções consolidadas (Lei 14.133/2021, Art. 6º):
   1. Objeto (do ETP)
   2. Especificações Técnicas (detalhadas)
   3. Justificativa (do DFD/ETP)
   4. Valor Estimado (do ETP)
   5. Prazo de Execução (do ETP)
   6. Forma de Pagamento
   7. Obrigações Contratante/Contratada
   8. Sanções Administrativas
   9. Critérios Aceitação/Fiscalização
```

**Q13: Como adicionar especificações técnicas detalhadas?**
```
R: 1. Acesse seção 2 (Especificações Técnicas)
   2. Use o editor de texto expandido
   3. Adicione tabelas, listas, medidas
   4. Para materiais/serviços complexos:
      - Crie planilhas em Excel
      - Faça upload no módulo Insumos
      - Referencie no TR: "conforme Anexo A"
```

**Q14: Posso gerar TR sem ETP?**
```
R: NÃO. O TR é dependente do ETP:
   - ETP fornece análises obrigatórias (IN 40/2020)
   - TR usa dados consolidados do ETP
   - Sem ETP = TR incompleto e não conforme
   
   Sempre complete: DFD → ETP → TR
```

### 1.5 Módulo Edital

**Q15: Quantos campos tem o Edital?**
```
R: 12 campos estruturados:
   1. Número Edital
   2. Modalidade Licitação
   3. Objeto
   4. Valor Estimado
   5. Prazo Execução
   6. Critério Julgamento
   7. Exigências Habilitação
   8. Forma Pagamento
   9. Prazos Recursos
   10. Garantia Contratual
   11. Sanções Administrativas
   12. Anexos e Referências
```

**Q16: O que é o score de validação?**
```
R: Score de 0-100 que avalia conformidade legal:
   
   90-100: ✅ Excelente (pronto para publicação)
   70-89:  ⚠️ Bom (ajustes recomendados)
   50-69:  ⚠️ Aceitável (requer melhorias)
   0-49:   ❌ Inadequado (revisão obrigatória)
   
   Baseado em 12 critérios da Lei 14.133/2021
```

**Q17: Como melhorar o score de validação?**
```
R: 1. Execute [⚙️ Validar Edital]
   2. Veja detalhamento dos critérios
   3. Identifique itens com ❌ ou ⚠️
   4. Corrija campos específicos:
      - Adicione detalhes faltantes
      - Complete especificações
      - Ajuste valores/prazos
   5. Re-valide até score > 85
```

### 1.6 Módulo Contrato

**Q18: Quantos campos tem o Contrato?**
```
R: 20 campos obrigatórios (9 grupos):
   Identificação: 5 campos
   Legal: 1 campo
   Prazos: 2 campos
   Valores: 3 campos
   Garantias: 1 campo
   Obrigações: 2 campos
   Gestão: 1 campo
   Penalidades: 2 campos
   Disposições: 3 campos
```

**Q19: Quantas cláusulas tem o DOCX gerado?**
```
R: 15 cláusulas padronizadas TJSP:
   1ª - DO OBJETO
   2ª - DA FUNDAMENTAÇÃO LEGAL
   3ª - DO VALOR
   ... (até 15ª - DO FORO)
   
   Formatação institucional RGB(0,51,102)
```

**Q20: Como adicionar dados da empresa vencedora?**
```
R: Após licitação:
   1. Acesse módulo Contrato
   2. Localize campo "Partes Contratada"
   3. Preencha:
      - Razão social
      - CNPJ
      - Representante legal
      - Endereço completo
      - Contatos
   4. Salve e gere DOCX
```

---

## 2. Problemas Comuns

### 2.1 Erros de Upload

**ERRO: "Falha ao processar arquivo PDF"**
```
Causa: PDF corrompido, protegido ou com OCR ruim

Solução:
1. Verifique se PDF abre corretamente
2. Remova proteção de senha:
   - Adobe Acrobat: "Remover segurança"
   - Online: ilovepdf.com/pt/desbloquear-pdf
3. Para PDFs escaneados:
   - Reprocesse com OCR (Adobe Acrobat)
   - Ou converta para DOCX antes de upload
4. Tamanho máximo: 10 MB
   - Comprima PDFs grandes (smallpdf.com)
```

**ERRO: "Formato de arquivo não suportado"**
```
Causa: Arquivo em formato não aceito

Formatos aceitos:
✅ PDF (.pdf)
✅ Word (.docx, .doc)
✅ Texto (.txt)
❌ Excel (.xlsx) - use módulo específico
❌ Imagens (.jpg, .png) - converta para PDF com OCR

Solução:
1. Converta para formato aceito
2. Use conversores online (CloudConvert)
3. Para Excel: copie texto para Word
```

**ERRO: "Timeout no processamento"**
```
Causa: Documento muito longo ou API lenta

Solução:
1. Reduza tamanho do documento:
   - Divida em seções menores
   - Remova imagens pesadas
2. Tente novamente em horário diferente
3. Se persistir, preencha manualmente
4. Contate suporte para ajuste de timeout
```

### 2.2 Erros de IA/Processamento

**ERRO: "OpenAI API Error: Rate limit exceeded"**
```
Causa: Limite de requisições à API OpenAI excedido

Solução:
1. Aguarde 1-2 minutos
2. Tente novamente
3. Em horários de pico (10h-16h):
   - Aguarde até 5 minutos
   - Ou processe fora do horário de pico
4. Para emergências: preencha manualmente
```

**ERRO: "Dados extraídos estão vazios ou incompletos"**
```
Causa: Documento mal formatado ou texto ilegível

Solução:
1. Verifique qualidade do documento fonte
2. Para textos genéricos:
   - Adicione mais detalhes ao insumo
   - Seja específico sobre valores, prazos
3. Para uploads:
   - Use documentos bem formatados
   - Evite PDFs escaneados de baixa qualidade
4. Alternativa: preencha campos manualmente
```

**ERRO: "Agent timeout após 60 segundos"**
```
Causa: Processamento complexo excedeu tempo limite

Solução:
1. Simplifique o insumo:
   - Remova informações redundantes
   - Foque no essencial
2. Divida em etapas:
   - Processe DFD primeiro
   - Depois ETP separadamente
3. Ajuste configuração (admin):
   - Aumente timeout em config.yaml
4. Para documentos enormes (>50 páginas):
   - Resuma manualmente antes de processar
```

### 2.3 Erros de Exportação DOCX

**ERRO: "Falha ao gerar DOCX"**
```
Causa: Biblioteca python-docx com problema

Solução:
1. Recarregue a página (F5)
2. Tente gerar novamente
3. Verifique se todos os campos estão preenchidos
4. Se persistir:
   - Limpe cache do navegador
   - Reinicie aplicação Streamlit
   - Contate suporte TI
```

**ERRO: "DOCX gerado sem formatação"**
```
Causa: Template de formatação não carregado

Solução:
1. Verifique arquivo: utils/docx_templates/
2. Reinstale dependências:
   pip install --upgrade python-docx
3. Baixe templates atualizados do repositório
4. Temporariamente: use exportação PDF
```

**ERRO: "Caracteres especiais aparecem como '?'"**
```
Causa: Problema de encoding (UTF-8)

Solução:
1. Evite caracteres especiais raros:
   ❌ ™ ® © € £
   ✅ Use texto simples
2. Para caracteres necessários:
   - Digite no próprio Word após exportação
3. Reporte ao suporte para correção permanente
```

### 2.4 Problemas de Navegação

**ERRO: "Página em branco ao clicar em módulo"**
```
Causa: Cache do navegador ou sessão expirada

Solução:
1. Recarregue página (F5 ou Ctrl+R)
2. Limpe cache:
   - Chrome: Ctrl+Shift+Del
   - Selecione "Imagens e arquivos em cache"
   - Limpe último 1 hora
3. Se não resolver:
   - Feche todas as abas do SAAB-Tech
   - Abra nova janela anônima
   - Faça login novamente
```

**ERRO: "Dados não aparecem após salvar"**
```
Causa: Dados não persistidos corretamente

Solução:
1. Verifique se viu mensagem "✅ Salvo com sucesso"
2. Se não viu:
   - Clique [💾 Salvar] novamente
   - Aguarde até 5 segundos
3. Verifique arquivo JSON:
   - Baixe exports/[modulo]_data.json
   - Abra com editor texto
   - Confirme se dados estão lá
4. Se JSON vazio:
   - Preencha novamente
   - Salve em horário de menor uso
```

**ERRO: "Botão não responde ao clicar"**
```
Causa: JavaScript não carregado ou conflito

Solução:
1. Aguarde 5 segundos (pode estar processando)
2. Verifique se há mensagem de erro no topo
3. Recarregue página (F5)
4. Teste em navegador diferente:
   ✅ Chrome (recomendado)
   ✅ Edge
   ⚠️ Firefox (pode ter lentidão)
   ❌ Internet Explorer (não suportado)
```

### 2.5 Alertas e Validações

**ERRO: "Muitos alertas críticos (🚨)"**
```
Causa: Dados incompletos ou inconsistentes

Solução:
1. Acesse módulo ⚠️ Alertas
2. Filtre por: Severidade = Crítico
3. Para cada alerta:
   - Leia descrição
   - Vá ao módulo indicado
   - Corrija campo específico
4. Priorize alertas de:
   - Valores faltantes
   - Datas inválidas
   - Obrigações vazias
5. Re-valide até ter 0 alertas críticos
```

**ERRO: "Validador retorna score baixo (<70)"**
```
Causa: Edital com campos obrigatórios vazios

Solução:
1. Execute validação detalhada
2. Identifique critérios com ❌
3. Complete campos obrigatórios:
   - Objeto (descrição > 100 caracteres)
   - Valor estimado (numérico)
   - Prazo execução (definido)
   - Critério julgamento (claro)
   - Forma pagamento (detalhada)
4. Re-valide
5. Meta: score > 85 para publicação
```

---

## 3. Otimização

### 3.1 Performance

**Dica 1: Limpe cache regularmente**
```
Frequência: A cada 2 semanas

Como fazer:
1. Chrome: Configurações > Privacidade > Limpar dados
2. Selecione:
   ☑ Cookies e dados de sites
   ☑ Imagens e arquivos em cache
   ☐ Histórico de navegação (opcional)
3. Período: Última semana
4. Clique [Limpar dados]
5. Reabra SAAB-Tech
```

**Dica 2: Use navegador recomendado**
```
Performance por navegador (testes internos):

Chrome 120+:     ⭐⭐⭐⭐⭐ (recomendado)
Edge 120+:       ⭐⭐⭐⭐⭐ (recomendado)
Firefox 120+:    ⭐⭐⭐⭐ (lentidão ocasional)
Safari 17+:      ⭐⭐⭐ (alguns bugs)
IE 11:           ❌ Não suportado
```

**Dica 3: Feche abas não utilizadas**
```
Streamlit consome memória por sessão:
- 1 aba aberta: ~200 MB RAM
- 5 abas abertas: ~1 GB RAM
- 10+ abas: Lentidão garantida

Recomendação:
- Mantenha máximo 2-3 abas abertas
- Feche abas inativas
- Use função "Duplicar aba" com moderação
```

### 3.2 Gestão de Dados

**Dica 4: Organize exports por processo**
```
Estrutura recomendada:

exports/
├─ 2025_001_limpeza_guarulhos/
│  ├─ dfd_data.json
│  ├─ etp_data.json
│  ├─ tr_data.json
│  ├─ edital_data.json
│  └─ contrato_data.json
│
├─ 2025_002_aquisicao_moveis/
│  └─ ...
│
└─ backups/
   └─ [backups automáticos]
```

**Dica 5: Faça backup manual semanal**
```
1. Baixe todos os JSONs:
   - dfd_data.json
   - etp_data.json
   - tr_data.json
   - edital_data.json
   - contrato_data.json

2. Salve em pasta local:
   C:\SAAB_Tech_Backups\YYYYMMDD\

3. Ou na nuvem:
   - OneDrive
   - Google Drive
   - SharePoint TJSP

4. Mantenha últimas 4 semanas
```

**Dica 6: Limpe dados de teste**
```
Periodicamente (mensal):
1. Identifique processos de teste
2. Delete JSONs antigos de exports/
3. Mantenha apenas:
   - Processos ativos (últimos 30 dias)
   - Processos arquivados importantes
4. Não delete backups/ automáticos
```

### 3.3 Boas Práticas

**Dica 7: Salve frequentemente**
```
Regra de ouro: SALVE A CADA 15 MINUTOS

Por quê:
- Sessão Streamlit expira após inatividade
- Quedas de conexão podem perder dados
- Não há "salvamento automático"

Como lembrar:
- Configure alarme no celular (timer 15 min)
- Use checklist mental: "Preenchi 3 campos → Salvo"
```

**Dica 8: Use nomenclatura padronizada**
```
Para números de processo:
❌ "processo novo"
❌ "teste123"
✅ "2025.00.123456-7" (formato TJSP)

Para descrições:
❌ "limpeza"
❌ "material"
✅ "Serviços de limpeza - Fórum Guarulhos"
✅ "Aquisição de móveis - Prédio Central"

Benefícios:
- Fácil localização
- Rastreabilidade
- Conformidade documental
```

**Dica 9: Revise antes de exportar**
```
Checklist pré-exportação:

☐ Todos os campos obrigatórios preenchidos
☐ Valores numéricos corretos (sem "R$" extra)
☐ Datas no formato DD/MM/AAAA
☐ Nomes completos (sem abreviações)
☐ Revisão ortográfica (F7 no navegador)
☐ Score de validação > 85 (para Edital)
☐ 0 alertas críticos (módulo Alertas)
☐ Backup do JSON salvo localmente
```

---

## 4. Recuperação de Dados

### 4.1 Restaurar de Backup Automático

**Cenário: Dados perdidos após crash**
```
Solução:
1. Acesse: exports/backups/
2. Identifique arquivo mais recente:
   [modulo]_data_backup_YYYYMMDD_HHMMSS.json
3. Renomeie para: [modulo]_data.json
4. Mova para: exports/
5. Recarregue módulo no SAAB-Tech
6. Dados restaurados!
```

**Nota:** Backups automáticos são criados a cada salvamento

### 4.2 Recuperar de Export Manual

**Cenário: Precisa voltar para versão de ontem**
```
Solução:
1. Localize backup manual em sua pasta local
2. Copie arquivo JSON desejado
3. No SAAB-Tech:
   - Acesse módulo correspondente
   - Delete dados atuais (se necessário)
4. Upload do JSON:
   - Use módulo Insumos
   - Destino: módulo correspondente
   - Processe
5. Ou substitua diretamente em exports/
```

### 4.3 Reconstruir Dados Manualmente

**Cenário: Sem backups disponíveis**
```
Solução (último recurso):
1. Acesse módulo com dados perdidos
2. Preencha formulário manualmente:
   - Consulte documentos originais
   - Use informações de módulos anteriores
   - Aproveite dados propagados automaticamente
3. Salve múltiplas vezes durante preenchimento
4. Valide com módulo Alertas
5. Documente o motivo da reconstrução
```

---

## 5. Suporte

### 5.1 Canais de Atendimento

**Suporte Técnico Geral**
```
📧 E-mail: saab-tech@tjsp.jus.br
☎️ Telefone: (11) XXXX-XXXX
🕐 Horário: Segunda a Sexta, 9h-18h
⏱️ SLA Resposta: 4 horas úteis
```

**Suporte Especializado**

```
JURÍDICO (dúvidas legais, conformidade)
📧 assessoria.juridica@tjsp.jus.br
📋 Temas: Interpretação legal, validação editais

TI/INTEGRAÇÃO (problemas técnicos, APIs)
📧 ti.integracao@tjsp.jus.br
🔧 Temas: Erros sistema, integrações SAJ ADM

SAJ ADM (integração, sincronização)
📧 saj.suporte@tjsp.jus.br
🔗 Temas: Conexão SAJ, exportação processos

TREINAMENTO (capacitação, workshops)
📧 capacitacao.saab@tjsp.jus.br
📚 Temas: Cursos, tutoriais, certificação
```

### 5.2 Como Abrir Chamado

**Informações necessárias:**
```
1. IDENTIFICAÇÃO
   - Nome completo
   - Matrícula
   - Unidade/Fórum
   - E-mail institucional
   - Telefone

2. PROBLEMA
   - Módulo afetado
   - Descrição detalhada do erro
   - Mensagem de erro (print screen)
   - Quando ocorreu
   - Já tentou soluções do manual?

3. CONTEXTO
   - Navegador e versão
   - Sistema operacional
   - Número do processo (se aplicável)
   - Última ação realizada antes do erro

4. URGÊNCIA
   - Baixa: Dúvida geral
   - Média: Erro que tem workaround
   - Alta: Sistema travado, prazo próximo
   - Crítica: Perda de dados, publicação iminente
```

**Template de e-mail:**
```
Assunto: [SAAB-Tech] Erro no módulo [NOME] - [URGÊNCIA]

Prezados,

Nome: [Seu nome]
Matrícula: [número]
Unidade: [Fórum/Vara]

PROBLEMA:
Ao tentar [ação realizada], recebi o seguinte erro:
"[mensagem de erro completa]"

CONTEXTO:
- Módulo: [DFD/ETP/TR/Edital/Contrato]
- Navegador: Chrome 120
- Processo: 2025.00.123456-7
- Data/Hora: 10/12/2025 14:30

TENTATIVAS:
Já tentei:
1. Recarregar página (F5)
2. Limpar cache
3. [outras tentativas]

O erro persiste.

Solicito orientação.

Atenciosamente,
[Nome]
```

### 5.3 Níveis de Suporte

```
NÍVEL 1 - SUPORTE BÁSICO (Help Desk)
├─ Dúvidas sobre uso
├─ Problemas de login
├─ Orientação de navegação
└─ SLA: 4 horas

NÍVEL 2 - SUPORTE TÉCNICO
├─ Erros de sistema
├─ Problemas de integração
├─ Recuperação de dados
└─ SLA: 8 horas

NÍVEL 3 - SUPORTE ESPECIALIZADO
├─ Bugs complexos
├─ Customizações
├─ Análise de logs
└─ SLA: 24 horas

NÍVEL 4 - DESENVOLVIMENTO
├─ Novas funcionalidades
├─ Correções de código
├─ Atualizações de versão
└─ SLA: Conforme priorização
```

---

## 6. Recursos de Treinamento

### 6.1 Documentação Disponível

**Manuais Completos (7 documentos):**
```
✅ Manual 01 - Introdução e Primeiros Passos
✅ Manual 02 - Módulos de Planejamento (Insumos, DFD, ETP, TR)
✅ Manual 03A - Edital e Validador
✅ Manual 03B - Contrato Administrativo
✅ Manual 04 - Módulos de Governança (Alertas, Painéis)
✅ Manual 05 - Módulos Avançados (Relatórios, Integração)
✅ Manual 07 - FAQ e Troubleshooting (este documento)

📁 Local: /manuais/ no repositório
📥 Download: Portal SAAB-Tech > Documentação
```

### 6.2 Vídeos Tutoriais

**Biblioteca de vídeos (em produção):**
```
🎥 BÁSICO
├─ Introdução ao SAAB-Tech (10 min)
├─ Como criar seu primeiro DFD (15 min)
├─ Jornada completa: Insumo até Contrato (30 min)
└─ Exportando documentos (8 min)

🎥 INTERMEDIÁRIO
├─ Otimizando uso dos Agents de IA (20 min)
├─ Sistema de Alertas e Validações (15 min)
├─ Comparador e Controle de Versão (18 min)
└─ Integração com SAJ ADM (25 min)

🎥 AVANÇADO
├─ Troubleshooting comum (22 min)
├─ Administração e configuração (35 min)
├─ Boas práticas de governança (28 min)
└─ Casos de uso complexos (40 min)
```

**Acesso:**
```
🌐 Portal: https://capacitacao.tjsp.jus.br/saab-tech
📺 YouTube: Canal TJSP (playlist "SAAB-Tech")
💿 DVD: Solicite à Divisão de Capacitação
```

### 6.3 Workshops e Treinamentos

**Modalidades:**
```
PRESENCIAL
├─ Turmas de 15-20 pessoas
├─ Laboratório com computadores
├─ Duração: 4 horas
├─ Certificado de participação
└─ Agendamento: capacitacao.saab@tjsp.jus.br

ONLINE (AO VIVO)
├─ Turmas de até 50 pessoas
├─ Via Microsoft Teams
├─ Duração: 2 horas
├─ Gravação disponibilizada
└─ Agendamento: Mensal (última sexta)

EAD (ASSÍNCRONO)
├─ Curso completo (8 módulos)
├─ Duração: 12 horas (ritmo próprio)
├─ Avaliação final obrigatória
├─ Certificado digital
└─ Plataforma: Moodle TJSP
```

**Cronograma 2026:**
```
JANEIRO
├─ 24/01 (Sex) - Workshop Online - Módulos Básicos
└─ 31/01 (Sex) - Workshop Presencial - Fórum Central

FEVEREIRO
├─ 14/02 (Sex) - Workshop Online - Governança
└─ 28/02 (Sex) - Workshop Presencial - Interior

MARÇO
├─ 21/03 (Sex) - Workshop Online - Integração
└─ 28/03 (Sex) - Workshop Presencial - Capital

[Cronograma completo no Portal]
```

### 6.4 Comunidade e Fóruns

**Grupos de Discussão:**
```
TEAMS - Canal "SAAB-Tech Usuários"
├─ Tire dúvidas com colegas
├─ Compartilhe boas práticas
├─ Receba atualizações oficiais
└─ Acesso: Solicite ao administrador

E-MAIL - Lista "saab-tech-usuarios@tjsp.jus.br"
├─ Discussões técnicas
├─ Avisos de manutenção
├─ Novidades e releases
└─ Inscrição: Automática após primeiro login

WIKI INTERNA
├─ Base de conhecimento colaborativa
├─ Artigos de usuários experientes
├─ FAQ dinâmico
└─ Acesso: https://wiki.tjsp.jus.br/saab-tech
```

### 6.5 Certificação

**Programa de Certificação SAAB-Tech:**
```
NÍVEL 1 - USUÁRIO
├─ Requisitos:
│  ☐ Conclusão do curso EAD (12h)
│  ☐ Avaliação teórica (nota mín 7.0)
│  ☐ Processou 3 contratações completas
├─ Validade: 2 anos
└─ Benefício: Suporte prioritário

NÍVEL 2 - ESPECIALISTA
├─ Requisitos:
│  ☐ Certificação Nível 1 válida
│  ☐ Workshop avançado presencial (8h)
│  ☐ Processou 10+ contratações
│  ☐ Projeto prático (estudo de caso)
├─ Validade: 3 anos
└─ Benefício: Pode ministrar treinamentos internos

NÍVEL 3 - INSTRUTOR
├─ Requisitos:
│  ☐ Certificação Nível 2 válida
│  ☐ Curso de formação de instrutores (24h)
│  ☐ 50+ contratações processadas
│  ☐ Aprovação da banca examinadora
├─ Validade: Permanente (renovação anual simples)
└─ Benefício: Ministra treinamentos oficiais
```

**Como se inscrever:**
```
1. Acesse: https://capacitacao.tjsp.jus.br/certificacao
2. Preencha formulário de interesse
3. Aguarde convocação (por e-mail)
4. Realize o curso/avaliações
5. Receba certificado digital
```

---

## 📊 Indicadores de Qualidade

### Tempo Médio de Resolução

```
AUTOCONSULTA (Manual FAQ):      ~5 minutos
SUPORTE NÍVEL 1 (Help Desk):    4 horas
SUPORTE NÍVEL 2 (Técnico):      8 horas
SUPORTE NÍVEL 3 (Especialista): 24 horas
SUPORTE NÍVEL 4 (Dev):          Conforme sprint
```

### Taxa de Resolução

```
PRIMEIRO CONTATO:     78%
ATÉ SEGUNDO CONTATO:  94%
ATÉ TERCEIRO CONTATO: 99%
ESCALONADO PARA DEV:  1%
```

---

## 📞 Contatos Rápidos

```
📧 GERAL:        saab-tech@tjsp.jus.br
📧 JURÍDICO:     assessoria.juridica@tjsp.jus.br
📧 TI:           ti.integracao@tjsp.jus.br
📧 SAJ ADM:      saj.suporte@tjsp.jus.br
📧 TREINAMENTO:  capacitacao.saab@tjsp.jus.br

☎️ TELEFONE:     (11) XXXX-XXXX
🕐 HORÁRIO:      Segunda a Sexta, 9h-18h

🌐 PORTAL:       https://saab-tech.tjsp.jus.br
📚 WIKI:         https://wiki.tjsp.jus.br/saab-tech
🎥 VÍDEOS:       https://capacitacao.tjsp.jus.br/saab-tech
```

---

## ✅ Conclusão

**Parabéns! Você completou todos os 7 manuais do Projeto SAAB-Tech!**

### Jornada Completa:
```
✅ Manual 01 - Introdução e Primeiros Passos
✅ Manual 02 - Módulos de Planejamento
✅ Manual 03A - Edital e Validador
✅ Manual 03B - Contrato Administrativo
✅ Manual 04 - Módulos de Governança
✅ Manual 05 - Módulos Avançados
✅ Manual 07 - FAQ e Troubleshooting
```

### Agora você está pronto para:
- ✅ Processar contratações completas com IA
- ✅ Garantir conformidade legal (Lei 14.133/2021)
- ✅ Gerar documentação profissional
- ✅ Monitorar governança e qualidade
- ✅ Integrar com sistemas TJSP
- ✅ Resolver problemas autonomamente
- ✅ Apoiar colegas como referência técnica

### Próximos passos:
1. **Pratique:** Processe uma contratação real do início ao fim
2. **Certifique-se:** Inscreva-se no programa de certificação
3. **Contribua:** Compartilhe experiências na comunidade
4. **Aprimore:** Sugira melhorias ao suporte

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Manual 07/07 – FAQ e Troubleshooting*  
*Versão 2025.1 – Dezembro/2025*

---

## 📖 Índice Geral da Série

Para consulta rápida, localize o manual desejado:

| Manual | Tema | Arquivo |
|--------|------|---------|
| 01 | Introdução e Primeiros Passos | MANUAL_01_INTRODUCAO.md |
| 02 | Módulos de Planejamento | MANUAL_02_PLANEJAMENTO.md |
| 03A | Edital e Validador | MANUAL_03A_EDITAL.md |
| 03B | Contrato Administrativo | MANUAL_03B_CONTRATO.md |
| 04 | Módulos de Governança | MANUAL_04_MODULOS_GOVERNANCA.md |
| 05 | Módulos Avançados | MANUAL_05_MODULOS_AVANCADOS.md |
| 06 | FAQ e Troubleshooting | MANUAL_06_FAQ_TROUBLESHOOTING.md |

**Boa sorte e bom trabalho com o Projeto SAAB-Tech! 🚀**
