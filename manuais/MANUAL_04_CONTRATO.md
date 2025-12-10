# 📘 Manual do Usuário – Projeto SAAB-Tech


---

## 6. Cláusulas Contratuais

### 6.1 Estrutura das 15 Cláusulas

O DOCX gerado contém **15 cláusulas padronizadas**:

| Nº | Cláusula | Origem dos Dados | Obrigatória |
|----|----------|------------------|-------------|
| 1ª | DO OBJETO | Campo 5 (objeto) | ✅ Sim |
| 2ª | DA FUNDAMENTAÇÃO LEGAL | Campo 6 (fundamentacao_legal) | ✅ Sim |
| 3ª | DO VALOR | Campo 9 (valor_global) | ✅ Sim |
| 4ª | DA VIGÊNCIA | Campos 7 e 8 (vigencia, prazo_execucao) | ✅ Sim |
| 5ª | DA FORMA DE PAGAMENTO | Campo 10 (forma_pagamento) | ✅ Sim |
| 6ª | DAS OBRIGAÇÕES DA CONTRATADA | Campo 13 (obrigacoes_contratada) | ✅ Sim |
| 7ª | DAS OBRIGAÇÕES DO CONTRATANTE | Campo 14 (obrigacoes_contratante) | ✅ Sim |
| 8ª | DA FISCALIZAÇÃO | Campo 15 (fiscalizacao) | ✅ Sim |
| 9ª | DA GARANTIA CONTRATUAL | Campo 12 (garantia_contratual) | ✅ Sim |
| 10ª | DAS PENALIDADES | Campo 16 (penalidades) | ✅ Sim |
| 11ª | DA RESCISÃO | Campo 17 (rescisao) | ✅ Sim |
| 12ª | DAS ALTERAÇÕES CONTRATUAIS | Campo 18 (alteracoes) | ✅ Sim |
| 13ª | DO REAJUSTE | Campo 11 (reajuste) | ⚠️ Condicional |
| 14ª | DAS DISPOSIÇÕES GERAIS | Campo 20 (disposicoes_gerais) | ✅ Sim |
| 15ª | DO FORO | Campo 19 (foro) | ✅ Sim |

### 6.2 Formatação das Cláusulas

**Padrão TJSP:**
```
CLÁUSULA [NÚMERO]ª - [TÍTULO EM MAIÚSCULAS]

[Parágrafo 1º com texto justificado, fonte Arial 12, espaçamento 1,5]

§ 1º [Parágrafo primeiro]
§ 2º [Parágrafo segundo]
...

Subitens:
I - [item 1]
II - [item 2]
...

Alíneas:
a) [alínea a]
b) [alínea b]
...
```

---

## 7. Validações e Alertas

### 7.1 Validações Automáticas

O sistema valida os 20 campos antes de salvar:

| Validação | Critério | Severidade |
|-----------|----------|------------|
| **Número contrato vazio** | Campo obrigatório | 🚨 Crítico |
| **Data inválida** | Formato DD/MM/AAAA | 🚨 Crítico |
| **Objeto vazio** | Descrição obrigatória | 🚨 Crítico |
| **Partes incompletas** | CONTRATANTE e CONTRATADA | 🚨 Crítico |
| **Valor ausente** | Campo "valor_global" | 🚨 Crítico |
| **Vigência indefinida** | Não pode ser "a definir" | ⚠️ Alto |
| **Obrigações vazias** | Mínimo 5 obrigações cada parte | ⚠️ Alto |
| **Penalidades ausentes** | Pelo menos 2 tipos | ⚠️ Médio |

### 7.2 Alertas de Inconsistência

O módulo **⚠️ Alertas** detecta divergências:

```
🚨 INCONSISTÊNCIA DETECTADA

Documento 1: EDITAL
Campo: valor_estimado
Valor: R$ 850.000,00

Documento 2: CONTRATO
Campo: valor_global
Valor: R$ 820.000,00

❌ Valor do contrato (R$ 820k) é menor que o estimado no edital 
   (R$ 850k) - Diferença: R$ 30.000,00

ℹ️ Isso é NORMAL quando há economia na licitação.
   Certifique-se de que está correto e documente o motivo.
```

---

## 8. Casos Práticos

### 8.1 Caso 1: Contrato de Serviços Contínuos

**Cenário:**
- Limpeza do Fórum
- Valor: R$ 850.000,00/ano
- Prazo: 12 meses (prorrogável até 60)

**Tempo:**
- Geração: 30 segundos
- Revisão: 20 minutos
- TOTAL: ~25 minutos

**Vs. Manual:** ~8 horas

### 8.2 Caso 2: Contrato de Aquisição

**Cenário:**
- Material permanente (móveis)
- Valor: R$ 250.000,00
- Entrega: 30 dias

**Particularidades:**
- Garantia do produto: 12 meses
- Instalação incluída
- Pagamento em parcela única

**Tempo:** ~15 minutos

### 8.3 Caso 3: Renovação de Contrato

**Cenário:**
- Upload de contrato anterior
- Atualização de valores (reajuste)
- Novo prazo

**Fluxo:**
```
1. Upload do contrato atual (PDF)
2. Sistema extrai 20 campos
3. Você ajusta apenas:
   - Data nova
   - Valor reajustado
   - Nova vigência
4. Gera novo contrato
```

**Tempo:** ~10 minutos

---

## 📚 Próximos Passos

Você completou o aprendizado sobre **Contratos Administrativos**!

Continue para:
- **Manual 04** – Módulos de Governança (Alertas, Painéis)
- **Manual 05** – Módulos Avançados (Relatórios, Integração)

---

## 📞 Suporte Técnico

**Dúvidas sobre contratos?**

📧 saab-tech@tjsp.jus.br  
☎️ (11) XXXX-XXXX  
🕐 Segunda a Sexta, 9h-18h

**Suporte Jurídico:**  
📧 assessoria.juridica@tjsp.jus.br

---

**© 2025 – Tribunal de Justiça do Estado de São Paulo**  
**Projeto SAAB-Tech | Ecossistema SAAB 5.0**  
*Manual 04/07 – Módulo de Contrato Administrativo*
