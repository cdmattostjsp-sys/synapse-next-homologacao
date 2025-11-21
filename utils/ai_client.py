# ==========================================================
# utils/ai_client.py — vNext_r3 (AJUSTE DEFINITIVO)
# SynapseNext – Cliente Institucional OpenAI (TJSP)
# ==========================================================

from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI


class AIClient:
    """
    Cliente institucional padronizado para uso interno dos agentes IA.
    Agora com arquitetura system/user correta para priorização do prompt.
    """

    def __init__(self, model: str = None):

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada em ambiente.")

        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # ==========================================================
    # MÉTODO PRINCIPAL
    # ==========================================================
    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:

        # ---------------------------------------------
        # Normalização do conteúdo recebido
        # ---------------------------------------------
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        elif not isinstance(conteudo, str):
            conteudo = str(conteudo)

        # Apenas um trecho do documento é necessário
        trecho_documento = conteudo[:8000]

        try:

            # ======================================================
            # 🔥 ESTRUTURA CORRIGIDA (system + user)
            # ======================================================
            mensagens = [
                {
                    "role": "system",
                    "content": (
                        "Você é o assistente institucional do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                        "Sua função é gerar documentos administrativos formais (DFD, ETP, TR, Edital, Contrato) "
                        "seguindo integralmente o prompt institucional fornecido."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"{prompt}\n\n"
                        f"=== CONTEÚDO DO DOCUMENTO (INSUMO) ===\n"
                        f"{trecho_documento}\n\n"
                        f"=== INSTRUÇÃO FINAL ===\n"
                        f"Responda EXCLUSIVAMENTE em JSON válido para o artefato institucional: {artefato}."
                    ),
                },
            ]

            # ======================================================
            # Chamada ao modelo (OpenAI oficial)
            # ======================================================
            resposta = self.client.chat.completions.create(
                model=self.model,
                messages=mensagens,
                temperature=0.25,
                max_tokens=3000,
            )

            texto = resposta.choices[0].message.content.strip()

            # TENTAR JSON DIRETO
            try:
                return json.loads(texto)

            except Exception:
                # Limpando formatação de código se vier com blocos
                if texto.startswith("```"):
                    texto = texto.replace("```json", "").replace("```", "").strip()

                try:
                    return json.loads(texto)
                except Exception:
                    return {"resposta_texto": texto}

        except Exception as e:
            return {
                "erro": f"❌ Falha na chamada OpenAI: {e}",
                "modelo_utilizado": self.model,
            }
