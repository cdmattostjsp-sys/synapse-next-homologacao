# ==========================================================
# utils/ai_client.py — vNext_D4 (2025)
# Compatível com OpenAI Responses API + DocumentAgent D3
# SEM proxies — SEM parâmetros legados — 100% estável
# ==========================================================

from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI


class AIClient:
    """
    Cliente institucional padronizado para o TJSP.
    Compatível com a API oficial OpenAI (responses.create).
    """

    def __init__(self, model: str = None):

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada.")

        # Cliente oficial — sem proxies / sem parâmetros legados
        self.client = OpenAI(api_key=api_key)

        # Modelo institucional padrão
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")


    # ==========================================================
    # CHAMADA PRINCIPAL — JSON SEMPRE VÁLIDO
    # ==========================================================
    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:

        # Normalização
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        elif not isinstance(conteudo, str):
            conteudo = str(conteudo)

        conteudo = conteudo.strip()
        trecho = conteudo[:8000]  # limite seguro

        # Mensagens
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é o assistente institucional oficial do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                    "Sua resposta deve ser EXCLUSIVAMENTE um JSON válido."
                )
            },
            {
                "role": "user",
                "content": (
                    f"{prompt}\n\n"
                    f"=== CONTEÚDO DO DOCUMENTO ===\n"
                    f"{trecho}\n\n"
                    f"=== INSTRUÇÃO FINAL ===\n"
                    f"Responda APENAS com JSON para o artefato {artefato}."
                )
            }
        ]

        # Chamada à API
        try:
            resposta = self.client.responses.create(
                model=self.model,
                messages=messages,
                temperature=0.0,
                max_output_tokens=6000,
                response_format={"type": "json_object"},
            )

            texto = resposta.output_text.strip()

        except Exception as e:
            print(f"[AIClient][ERRO FATAL] {e}")
            return {"erro": f"Falha ao consultar a OpenAI: {e}"}

        # Log curto
        print("\n===== AIClient DEBUG =====")
        print(f"Modelo: {self.model}")
        print(f"Trecho enviado: {len(trecho)} caracteres")
        print(f"Início da resposta: {texto[:200]}")
        print("===== FIM DEBUG =====\n")

        # Tentativa de decodificação
        try:
            return json.loads(texto)
        except Exception:
            pass

        # Remover markdown, se existir
        try:
            txt = (
                texto.replace("```json", "")
                .replace("```", "")
                .strip()
            )
            return json.loads(txt)
        except Exception:
            return {"resposta_texto": texto}
