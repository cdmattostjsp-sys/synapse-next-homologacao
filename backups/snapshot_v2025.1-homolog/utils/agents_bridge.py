# -*- coding: utf-8 -*-
"""
AgentsBridge – SynapseNext / SAAB TJSP
Ponte única de integração entre módulos Streamlit e agentes cognitivos.
Versão vNext 2025 – Homologada
"""

from __future__ import annotations
from typing import Dict, Any

from agents.document_agent import DocumentAgent

SUPPORTED = {"DFD", "ETP", "TR", "EDITAL", "CONTRATO"}


class AgentsBridge:
    """Gerencia e executa agentes de IA de forma unificada."""

    def __init__(self, modulo: str):
        modulo = modulo.upper()
        if modulo not in SUPPORTED:
            raise ValueError(f"Módulo não suportado: {modulo}")
        self.modulo = modulo
        self.agent = DocumentAgent(modulo)

    def generate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a geração institucional padronizada."""
        return self.agent.generate(metadata)

