# ==========================================================
# utils/ai_client.py — vNext_D2.1 (compatível com OpenAI Responses API)
# Cliente Institucional OpenAI – TJSP / SAAB
# TOTALMENTE COMPATÍVEL com DocumentAgent D2.1
# ==========================================================

from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI


class AIClient:
    """
    Cliente institucional padronizado para consultas à OpenAI usando o
    NOVO ENDPOINT 'responses.create', obrigatório nos modelos 4o e 4o-mini.

    Benefícios:
      ✓ Suporte nativo a JSON via response_format
      ✓ Retorno sempre limpo como string JSON
      ✓ Compatível com DocumentAgent D2.1
    """

    def __init__(self, model: str = None):

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada no ambiente.")

        # Cliente OpenAI oficial (novo SDK)
        self.client = OpenAI(api_key=api_key)

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")


    # ==========================================================
    # MÉTODO PRINCIPAL
    # ==========================================================
    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:

        # ------------------------------------------------------
        # Normalização do conteúdo enviado
        # ------------------------------------------------------
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        elif not isinstance(conteudo, str):
            conteudo = str(conteudo)

        conteudo = conteudo or ""
        trecho = conteudo[:8000]

        # ------------------------------------------------------
        # Montagem do bloco de mensagens
        # ------------------------------------------------------
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é o assistente institucional do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                    "Sua resposta deve ser EXCLUSIVAMENTE JSON válido, sem comentários."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{prompt}\n\n"
                    f"=== CONTEÚDO DO DOCUMENTO (INSUMO) ===\n"
                    f"{trecho}\n\n"
                    f"=== INSTRUÇÃO FINAL ===\n"
                    f"Responda APENAS com um JSON válido referente ao artefato: {artefato}."
                ),
            },
        ]

        # ------------------------------------------------------
        # CHAMADA COM O NOVO ENDPOINT
        # ------------------------------------------------------
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
            return {"erro": f"Falha grave ao consultar OpenAI: {e}"}

        # ------------------------------------------------------
        # LOG CURTO
        # ------------------------------------------------------
        print("\n===== AIClient DEBUG =====")
        print(f"[Modelo] {self.model}")
        print(f"[Trecho enviado] {len(trecho)} chars")
        print(f"[Resposta JSON bruta] {texto[:300]}...\n")

        # ------------------------------------------------------
        # 1) Tentativa direta de json.loads
        # ------------------------------------------------------
        try:
            return json.loads(texto)
        except Exception:
            print("[AIClient] JSON direto falhou — tentando limpeza.")

        # ------------------------------------------------------
        # 2) Limpeza de bloco markdown
        # ------------------------------------------------------
        try:
            texto_limpo = (
                texto.replace("```json", "")
                .replace("```", "")
                .strip()
            )
            return json.loads(texto_limpo)
        except Exception:
            print("[AIClient] JSON após limpeza falhou — fallback final.")

        # ------------------------------------------------------
        # 3) Fallback de segurança
        # ------------------------------------------------------
        return {"resposta_texto": texto}
