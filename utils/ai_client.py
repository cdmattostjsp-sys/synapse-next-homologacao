# ==========================================================
# utils/ai_client.py — vNext_D2 (robusto + anti-alucinação)
# Cliente Institucional OpenAI – TJSP / SAAB
# Compatível com DocumentAgent Moderno-Governança (D2)
# ==========================================================

from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI


class AIClient:
    """
    Cliente institucional padronizado para consultas à OpenAI, com:
      ✓ Logs de diagnóstico controlados
      ✓ Estrutura system/user consistente
      ✓ Força JSON válido via response_format
      ✓ Limpeza de blocos ```json
      ✓ Fallback seguro sem quebrar o pipeline
    """

    def __init__(self, model: str = None):

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada no ambiente.")

        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # ==========================================================
    # MÉTODO PRINCIPAL
    # ==========================================================
    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:

        # Normalização
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        elif not isinstance(conteudo, str):
            conteudo = str(conteudo)

        conteudo = conteudo or ""
        trecho = conteudo[:8000]

        mensagens = [
            {
                "role": "system",
                "content": (
                    "Você é o assistente institucional do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                    "Produza respostas formais, administrativas e SEMPRE em JSON válido."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{prompt}\n\n"
                    f"=== CONTEÚDO DO DOCUMENTO (INSUMO) ===\n"
                    f"{trecho}\n\n"
                    f"=== INSTRUÇÃO FINAL ===\n"
                    f"Responda exclusivamente com JSON válido para o artefato: {artefato}."
                ),
            },
        ]

        # CHAMADA OFICIAL
        try:
            resposta = self.client.chat.completions.create(
                model=self.model,
                messages=mensagens,
                temperature=0.10,
                max_tokens=5000,
                response_format={"type": "json_object"},  # força JSON
            )
            texto = resposta.choices[0].message.content.strip()

        except Exception as e:
            print(f"[AIClient][ERRO FATAL] {e}")
            return {
                "erro": f"❌ Falha grave ao consultar OpenAI: {e}",
                "modelo_utilizado": self.model,
            }

        # Logs curtos
        try:
            print("\n===== AIClient DEBUG =====")
            print(f"[Modelo] {self.model} | [Artefato] {artefato}")
            print(f"[Trecho enviado] {len(trecho)} chars")
            print(f"[Resposta JSON bruta] {texto[:500]}...\n")
        except:
            pass

        # 1) JSON direto
        try:
            return json.loads(texto)
        except Exception:
            print("[AIClient] JSON direto falhou — tentando limpeza.")

        # 2) limpeza geral
        try:
            texto_limpo = (
                texto.replace("```json", "")
                .replace("```", "")
                .replace("“", '"')
                .replace("”", '"')
                .strip()
            )
            return json.loads(texto_limpo)
        except Exception:
            print("[AIClient] JSON após limpeza falhou — fallback.")

        # 3) fallback seguro
        return {"resposta_texto": texto}
