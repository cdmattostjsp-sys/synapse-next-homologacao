# -*- coding: utf-8 -*-
"""
AgentsBridge – Bridge único para criação/uso de agentes pelos módulos Streamlit.
Mantém a padronização institucional entre páginas e agentes.
"""
from __future__ import annotations
from typing import Dict, Any

from agents.document_agent import DocumentAgent

SUPPORTED = {"DFD", "ETP", "TR", "EDITAL", "CONTRATO"}


class AgentsBridge:
    def __init__(self, modulo: str):
        modulo = modulo.upper()
        if modulo not in SUPPORTED:
            raise ValueError(f"Módulo não suportado: {modulo}")
        self._agent = DocumentAgent(modulo)

    def generate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        return self._agent.generate(metadata)
