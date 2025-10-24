# -*- coding: utf-8 -*-
"""
DocumentAgent – Agente de construção de artefatos (DFD, ETP, TR, Edital, Contrato)

• Baseado em metadados fornecidos pelo usuário (session_state ou dict).
• Usa prompts padronizados em /prompts/*.json como base institucional.
• Produz saída estruturada (dict) com seções, pronto para export pipelines.

Integração:
    from agents.document_agent import DocumentAgent
    agent = DocumentAgent("DFD")
    result = agent.generate(metadata)
"""
from __future__ import annotations
import json
import os
from typing import Dict, Any

from utils.ai_client import AIClient

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

SYSTEM_BASE = (
    "Você opera como redator técnico da Secretaria de Administração e Abastecimento (SAAB/TJSP). "
    "Produza conteúdo objetivo, normativo, alinhado à Lei 14.133/2021 e aos padrões redacionais institucionais. "
    "Priorize metadados do formulário. Se faltarem dados, proponha perguntas claras ao final na seção 'Lacunas'."
)

SCHEMA_HINT = {
    "DFD": ["Contexto", "Necessidade", "Resultados Esperados", "Justificativa Legal", "Escopo", "Critérios de Sucesso"],
    "ETP": ["Objeto", "Soluções de Mercado", "Justificativa Técnica", "Requisitos", "Estimativa de Custos", "Riscos"],
    "TR":  ["Objeto", "Especificações Técnicas", "Critérios de Aceitação", "Prazos", "Garantias", "Gestão e Fiscalização"],
    "EDITAL": ["Disposições Gerais", "Condições de Participação", "Julgamento", "Prazos", "Sanções", "Anexos"],
    "CONTRATO": ["Cláusulas Gerais", "Objeto", "Vigência", "Preço e Reajuste", "Obrigações", "Fiscalização", "Penalidades"],
}


class DocumentAgent:
    def __init__(self, modulo: str, model: str | None = None):
        self.modulo = modulo.upper()
        self.client = AIClient(model=model)
        self.prompt_template = self._load_prompt(self.modulo)
        if self.modulo not in SCHEMA_HINT:
            raise ValueError(f"Módulo inválido: {self.modulo}")

    def _load_prompt(self, modulo: str) -> Dict[str, Any]:
        path = os.path.join(PROMPTS_DIR, f"{modulo}.json")
        if not os.path.exists(path):
            # fallback genérico
            return {"system": SYSTEM_BASE, "user": ""}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        system = data.get("system", SYSTEM_BASE)
        user = data.get("user", "")
        return {"system": system, "user": user}

    def build_messages(self, metadata: Dict[str, Any]) -> list[dict]:
        # Metadados priorizados
        md = json.dumps(metadata, ensure_ascii=False, indent=2)
        sections = ", ".join(SCHEMA_HINT[self.modulo])
        user_msg = (
            f"Gerar rascunho estruturado do módulo {self.modulo} em JSON com as seções: {sections}. "
            "Use linguagem institucional. Campos ausentes devem ser listados em 'Lacunas'.\n\n"
            f"METADADOS:\n{md}\n\n"
            "Responda em JSON com o seguinte formato: { 'modulo': str, 'secoes': {secao: texto}, 'lacunas': [..] }"
        )
        return [
            {"role": "system", "content": self.prompt_template.get("system", SYSTEM_BASE)},
            {"role": "user", "content": self.prompt_template.get("user", "") + "\n\n" + user_msg},
        ]

    def generate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        msgs = self.build_messages(metadata)
        result = self.client.chat(msgs, temperature=0.15)
        content = result["content"]
        # Tentar parsear JSON retornado
        try:
            parsed = json.loads(content)
        except Exception:
            parsed = {
                "modulo": self.modulo,
                "secoes": {"Conteúdo": content},
                "lacunas": ["Formato JSON não garantido pelo modelo – utilize o texto em 'Conteúdo'."],
            }
        parsed["_usage"] = result.get("usage")
        return parsed
