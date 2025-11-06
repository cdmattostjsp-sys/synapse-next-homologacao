# -*- coding: utf-8 -*-
"""
Módulo de integração com IA para geração de artefatos (DFD, ETP, TR).
Chamada padronizada via wrapper institucional AIClient.
"""

import json
from typing import Dict, Any, Optional
from utils.ai_client import AIClient

# 🔧 Função principal de inferência IA
def processar_insumo(
    texto: str,
    tipo_artefato: str,
    metadados_form: Optional[Dict[str, Any]] = None,
    arquivo_nome: Optional[str] = None,
) -> Dict[str, Any]:
    metadados_form = metadados_form or {}
    modulo = tipo_artefato.upper()

    chaves_por_modulo = {
        "DFD": [
            "objeto", "justificativa", "resultados_esperados", "requisitos_minimos",
            "criterio_julgamento", "prazo_execucao", "base_legal"
        ],
        "ETP": [
            "objeto", "motivacao", "alternativas", "vantagem_da_solucao", "riscos",
            "estimativa_custos", "criterios_aceitacao", "base_legal"
        ],
        "TR": [
            "objeto", "escopo_detalhado", "requisitos_tecnicos", "condicoes_entrega",
            "indicadores_de_desempenho", "criterio_julgamento", "prazos", "garantias",
            "base_legal"
        ]
    }

    chaves = chaves_por_modulo.get(modulo, [])

    prompt = [
        {
            "role": "system",
            "content": (
                "Você é redator técnico do SAAB/TJSP, especialista na Lei 14.133/2021. "
                "Seu trabalho é inferir campos administrativos a partir de insumos fornecidos. "
                "Responda ESTRITAMENTE em JSON válido (um único objeto) conforme o schema solicitado. "
                "Se um campo não puder ser inferido, deixe-o vazio e liste em 'lacunas'. "
                "Não adicione comentários fora do JSON."
            )
        },
        {
            "role": "user",
            "content": (
                f"MÓDULO ALVO: {modulo}\n"
                f"METADADOS DO FORMULÁRIO:\n{json.dumps(metadados_form, ensure_ascii=False)}\n\n"
                f"EXTRATO DO INSUMO:\n{texto[:12000]}\n\n"
                f"RETORNE JSON COM AS CHAVES: {chaves}, incluindo 'lacunas' e 'evidencias'."
            )
        }
    ]

    ai = AIClient()
    try:
        # 🔍 DEBUG opcional – exibe prompt no terminal
        print("========== DEBUG PROMPT ==========")
        print(json.dumps(prompt, indent=2, ensure_ascii=False))
        print("===================================")

        resposta = ai.chat_as_json(messages=prompt)
    except Exception as e:
        resposta = {
            "modulo": modulo,
            "campos": {},
            "lacunas": [f"Erro IA: {str(e)}"],
            "evidencias": []
        }

    return {
        "modulo": modulo,
        "campos": resposta.get("campos", {}),
        "lacunas": resposta.get("lacunas", []),
        "inferido_de": {
            "arquivo": arquivo_nome,
            "bytes": bool(texto),
        }
    }
