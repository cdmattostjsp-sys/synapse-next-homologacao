# -*- coding: utf-8 -*-
"""
DocumentAgent – SynapseNext / SAAB TJSP
Agente institucional de geração e estruturação de artefatos administrativos.
Compatível com Lei nº 14.133/2021 e padrões redacionais da SAAB.
Versão vNext 2025 – Homologada
"""

from __future__ import annotations
import os
import json
from typing import Dict, Any
from datetime import datetime

from utils.ai_client import AIClient

# Caminho base para os PROMPTs institucionais
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# Schema de seções por módulo
SCHEMA_HINT = {
    "DFD": ["Contexto", "Necessidade", "Resultados Esperados", "Justificativa Legal", "Escopo", "Critérios de Sucesso"],
    "ETP": ["Objeto", "Soluções de Mercado", "Justificativa Técnica", "Requisitos", "Estimativa de Custos", "Riscos"],
    "TR":  ["Objeto", "Especificações Técnicas", "Critérios de Aceitação", "Prazos", "Garantias", "Gestão e Fiscalização"],
    "EDITAL": ["Disposições Gerais", "Condições de Participação", "Julgamento", "Prazos", "Sanções", "Anexos"],
    "CONTRATO": ["Cláusulas Gerais", "Objeto", "Vigência", "Preço e Reajuste", "Obrigações", "Fiscalização", "Penalidades"]
}

SYSTEM_BASE = (
    "Você é um redator técnico da Secretaria de Administração e Abastecimento (SAAB/TJSP). "
    "Sua tarefa é elaborar artefatos administrativos conforme a Lei nº 14.133/2021, "
    "mantendo linguagem institucional, técnica e objetiva. "
    "Priorize as informações fornecidas pelos metadados do formulário e "
    "registre eventuais dados ausentes na seção 'Lacunas'."
)


class DocumentAgent:
    """Agente institucional de construção de artefatos administrativos."""

    def __init__(self, modulo: str, model: str | None = None):
        self.modulo = modulo.upper()
        if self.modulo not in SCHEMA_HINT:
            raise ValueError(f"Módulo inválido: {self.modulo}")
        self.client = AIClient(model=model)
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> Dict[str, Any]:
        """Carrega o prompt institucional correspondente ao módulo."""
        path = os.path.join(PROMPTS_DIR, f"{self.modulo}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                "system": data.get("system", SYSTEM_BASE),
                "user": data.get("user", "")
            }
        else:
            return {"system": SYSTEM_BASE, "user": ""}

    def _build_messages(self, metadata: Dict[str, Any]) -> list[dict]:
        """Monta o contexto para envio à IA."""
        md_json = json.dumps(metadata, ensure_ascii=False, indent=2)
        sections = ", ".join(SCHEMA_HINT[self.modulo])
        user_msg = (
            f"Gerar rascunho estruturado do módulo {self.modulo} em JSON com as seções: {sections}. "
            f"Use linguagem institucional. Campos ausentes devem ser listados em 'Lacunas'.\n\n"
            f"METADADOS:\n{md_json}\n\n"
            "Formato esperado de resposta:\n"
            "{ 'modulo': str, 'secoes': {secao: texto}, 'lacunas': [..] }"
        )
        return [
            {"role": "system", "content": self.prompt_template["system"]},
            {"role": "user", "content": self.prompt_template["user"] + "\n\n" + user_msg}
        ]

    def generate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a geração de conteúdo técnico baseado em metadados."""
        msgs = self._build_messages(metadata)
        result = self.client.chat(msgs, temperature=0.15)
        raw_content = result["content"]

        # Tenta decodificar como JSON
        try:
            parsed = json.loads(raw_content)
        except Exception:
            parsed = {
                "modulo": self.modulo,
                "secoes": {"Conteúdo": raw_content},
                "lacunas": ["Formato JSON não garantido pelo modelo – conteúdo bruto incluído."]
            }

        parsed["_usage"] = result.get("usage")
        parsed["_gerado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return parsed
