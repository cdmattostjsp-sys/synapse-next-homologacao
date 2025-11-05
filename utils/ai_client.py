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
- Mantém compatibilidade com Streamlit (st.secrets), .env e variáveis de ambiente.
- Exige openai>=2.7.1 (compatível com Streamlit 1.39.0).
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# 🔹 Carrega automaticamente variáveis do .env
from dotenv import load_dotenv
load_dotenv()

try:
    import streamlit as st  # opcional em execução de testes
except Exception:
    st = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class AIClient:
    """Cliente institucional de IA (OpenAI) para o SynapseNext/SAAB-TJSP."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # Hierarquia de obtenção da chave: .env → os.environ → st.secrets
        env_key = os.getenv("OPENAI_API_KEY")
        secrets_key = None

        if st is not None:
            try:
                if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
                    secrets_key = st.secrets["OPENAI_API_KEY"]
            except Exception:
                secrets_key = None

        self.api_key = api_key or env_key or secrets_key

        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não configurada. Verifique o arquivo .env ou st.secrets."
            )

        if OpenAI is None:
            raise RuntimeError(
                "Pacote openai não encontrado. Adicione `openai>=2.7.1` ao requirements.txt."
            )

        self.model = model or DEFAULT_MODEL
        self.client = OpenAI(api_key=self.api_key)
        print(f"[AIClient] ✅ Cliente OpenAI inicializado com modelo '{self.model}'")

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


# ===============================================================
# 🧾 Bloco de validação e log pós-ajuste de credenciais
# ===============================================================
if __name__ == "__main__":
    try:
        client = AIClient()
        log_dir = Path(__file__).resolve().parents[1] / "exports" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "ai_client_init_fix_20251105.txt"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.now().isoformat()}] OPENAI_API_KEY reconhecida: {bool(client.api_key)}\n"
            )

        print(f"🗂️ Log pós-ajuste gravado em {log_file}")
        print(f"✅ OPENAI_API_KEY reconhecida: {bool(client.api_key)}")

    except Exception as e:
        print(f"⚠️ Falha ao validar AIClient: {e}")
