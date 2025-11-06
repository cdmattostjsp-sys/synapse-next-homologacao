# ==========================================================
# utils/ai_client.py
# SynapseNext – Cliente Institucional OpenAI
# Revisão: Engenheiro Synapse – 2025-11-05 (versão compatível Streamlit)
# ==========================================================

import os
from openai import OpenAI
import json

class AIClient:
    """Cliente institucional padronizado para acesso à API OpenAI."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada no ambiente (.env).")
        self.client = OpenAI(api_key=api_key)

    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:
        """
        Envia um prompt para o modelo de linguagem institucional e retorna a resposta JSON.
        Aceita texto puro (str) ou binário (bytes). Compatível com Streamlit.
        """

        try:
            # Garante que conteudo é string legível
            if isinstance(conteudo, bytes):
                conteudo = conteudo.decode("utf-8", errors="ignore")
            elif not isinstance(conteudo, str):
                conteudo = str(conteudo)

            mensagem = (
                f"{prompt}\n\n"
                f"---\n"
                f"Conteúdo do documento:\n{conteudo[:4000]}\n"
                f"---\n"
                f"Responda no formato JSON estruturado para o artefato {artefato}."
            )

            resposta = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente técnico institucional do TJSP."},
                    {"role": "user", "content": mensagem},
                ],
                max_tokens=500,
            )

            texto = resposta.choices[0].message.content.strip()

            try:
                return json.loads(texto)
            except Exception:
                return {"resposta_texto": texto}

        except Exception as e:
            return {"erro": f"Falha na chamada OpenAI: {e}"}
