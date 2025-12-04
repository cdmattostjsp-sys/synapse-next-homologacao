# Archive – Duplicatas Removidas

## Conteúdo

- **validator_engine_vNext_root.py**: Cópia anterior em `/validator_engine_vNext.py` (raiz)
- **validator_engine_vNext_utils.py**: Cópia anterior em `/utils/validator_engine_vNext.py`

## Motivo da Movimentação

Consolidação do engine de validação do projeto. As duplicatas foram removidas para evitar:
- Shadowing de módulos
- Imports conflitantes
- Divergência de comportamento entre versões

## Versão Oficial Atual

A versão canônica e operacional agora está centralizada em:
```
knowledge/validators/validator_engine_vNext.py
```

Todos os imports devem referenciar este caminho:
```python
from knowledge.validators.validator_engine_vNext import validate_document
```

## Arquivos Protegidos (NÃO movidos)

- `knowledge/validators/validator_engine_vNext.py` — **Engine oficial (canônico)**
- `knowledge/validators/validator_engine.py` — **Engine legado (POC)**
- `knowledge/validators/validator_engine_backup.py` — **Backup institucional**

## Referência Histórica

Se precisar consultar o histórico destas duplicatas, use:
```bash
git log --follow archive/validator_engine_vNext_*.py
```

## Próximos Passos Recomendados

1. ✅ Atualizar imports em `synapse_chat.py` e `synapse_chat_vNext.py`
2. ✅ Executar testes para validar imports consolidados
3. ✅ Fazer commit com mensagem: "refactor: consolidate validator_engine to knowledge/validators/"

## Data

Gerado em: 2025-12-04

---

**Projeto:** SynapseNext vNext (TJSP/SAAB 5.0)  
**Status:** Consolidação de arquitetura em progresso
