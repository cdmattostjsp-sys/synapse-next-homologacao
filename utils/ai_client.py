# -*- coding: utf-8 -*-
"""
AI Client – Wrapper institucional para OpenAI
Uso:
    from utils.ai_client import AIClient
    client = AIClient()
    result = client.chat([
        {"role": "system", "content": "Você é um redator técnico do TJSP."},
        {"role": "user", "content": "Gerar sumário do DFD para ..."}
    ])
Observações:
- Mantém compatibilidade com Streamlit (st.secrets) e variáveis de ambiente.
- Exige openai>=1.40 no requirements.txt.
"""
from __future__ import annotations
import os
from typing import List, Dict, Any, Optional

try:
    import streamlit as st  # opcional em execução de testes
except Exception:  # pragma: no cover
    st = None

try:
    from openai import OpenAI
except Exception as e:  # pragma: no cover
    OpenAI = None

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class AIClient:
    """Cliente institucional de IA (OpenAI) para o SynapseNext/SAAB-TJSP."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # Hierarquia de obtenção da chave: st.secrets -> env var
        self.api_key = api_key or (st.secrets.get("OPENAI_API_KEY") if st else None) or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY não configurada. Use st.secrets ou variável de ambiente.")
        if OpenAI is None:
            raise RuntimeError("Pacote openai não encontrado. Adicione `openai>=1.40` ao requirements.txt.")
        self.model = model or DEFAULT_MODEL
        self.client = OpenAI(api_key=self.api_key)

    def chat(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.2,
        response_format: Optional[Dict[str, Any]] = None,
        max_output_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Executa uma chamada de chat ao modelo configurado.
        Retorna dict com content, finish_reason e usage (quando disponível).
        """
        kwargs = dict(model=self.model, messages=messages, temperature=temperature)
        if response_format:
            kwargs["response_format"] = response_format
        if max_output_tokens:
            kwargs["max_output_tokens"] = max_output_tokens
        resp = self.client.chat.completions.create(**kwargs)
        choice = resp.choices[0]
        return {
            "content": choice.message.content,
            "finish_reason": choice.finish_reason,
            "usage": getattr(resp, "usage", None),
        }
