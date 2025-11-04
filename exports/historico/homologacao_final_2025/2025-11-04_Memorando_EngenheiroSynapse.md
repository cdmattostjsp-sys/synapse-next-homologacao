# 🧩 **Memorando Técnico – Acionamento do Engenheiro Synapse**

📅 **Data:** 04/11/2025
📁 **Referência:** Pós-Homologação – Persistência Semântica vNext
👤 **Responsável:** Engenheiro Synapse
🏢 **Projeto:** SynapseNext – Secretaria de Administração e Abastecimento (TJSP)

---

## 🎯 **Objetivo**

Executar correções estruturais e semânticas de alinhamento pós-homologação, garantindo coerência entre **schemas JSON**, **validadores Python**, e a configuração unificada da API OpenAI.

---

## 🔹 **Escopo da Ação**

| Nº  | Área                   | Tarefa                                                                                                                                                          | Status Esperado                           |
| --- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 1️⃣ | Validação Semântica    | Reexecutar `validator_engine_vNext.py` com flag `--sync-schema` para alinhar `etp.min.json` e `tr.min.json`.                                                    | Schemas atualizados em `journey/schemas/` |
| 2️⃣ | Integração OpenAI      | Unificar acesso à chave `OPENAI_API_KEY` via `utils/ai_client.py`, eliminando referências duplicadas em `integration_ai_engine.py` e `integration_contrato.py`. | Configuração única, via `.env`            |
| 3️⃣ | Logs de Diagnóstico    | Inserir chamada `registrar_log("diagnostic_post_homologacao")` no final da função principal de `diagnostic_pipeline.py`.                                        | Log exportado automaticamente             |
| 4️⃣ | Auditoria de Metadados | Regenerar `docs/tamanho_arquivos.txt` com:  \n`python generate_auditoria_tecnica_vNext.py --refresh`                                                            | Metadados atualizados                     |
| 5️⃣ | Limpeza Estrutural     | Remover duplicatas de checklists, mantendo apenas `knowledge/validators/*.yml`.                                                                                 | Estrutura limpa e única                   |

---

## 🔹 **Comandos de Execução Sugeridos**

```bash
# 1. Sincronizar schemas semânticos
python knowledge/validators/validator_engine_vNext.py --sync-schema

# 2. Atualizar variáveis de ambiente
# (Certificar-se que .env contém a linha abaixo)
OPENAI_API_KEY="sua_chave_oficial_tjsp"

# 3. Corrigir logs
python diagnostic_pipeline.py --phase=post_homologacao

# 4. Regenerar auditoria técnica
python generate_auditoria_tecnica_vNext.py --refresh
```

---

## 🔹 **Entregáveis Esperados**

* `exports/analises/diagnostic_persistencia_vNext.txt`
* `exports/relatorios/Relatorio_Persistencia_Semantica_vNext.docx`

Ambos deverão ser entregues ao **Orchestrator Synapse** para consolidação e registro final da homologação.

---

## 📎 **Anexos de Referência**

* `/exports/historico/homologacao_final_2025/2025-11-04_Relatorio_Executivo_SynapseNext.md`
* `/docs/Plano_Homologacao_SynapseNext.md`
* `/knowledge/validators/validator_engine_vNext.py`

---

📄 **Assinatura Digital:**
*Orchestrator Synapse*
Supervisor de Homologação – Projeto SynapseNext (TJSP)

