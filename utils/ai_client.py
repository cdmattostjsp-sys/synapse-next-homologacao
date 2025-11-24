# ==========================================================
# utils/ai_client.py — vNext_r4 (com diagnóstico em logs)
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
    Agora com diagnóstico detalhado via logs (prints no Streamlit).
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
        """
        Envia prompt institucional + conteúdo de documento para o modelo
        e retorna a resposta já tratada (dict ou texto cru).

        Também registra informações de diagnóstico via prints
        (visíveis nos logs do Streamlit Cloud).
        """

        # ---------------------------------------------
        # Normalização do conteúdo recebido
        # ---------------------------------------------
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        elif not isinstance(conteudo, str):
            conteudo = str(conteudo)

        conteudo = conteudo or ""
        trecho_documento = conteudo[:8000]  # recorte para evitar excesso de contexto

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

            # ======================================================
            # 🔎 BLOCO DE DIAGNÓSTICO (LOGS STREAMLIT)
            # ======================================================
            try:
                print("===== IA DEBUG START =====")
                print(f"[Modelo] {self.model} | [Artefato] {artefato}")
                print(f"[Conteúdo] tamanho_total={len(conteudo)} | trecho_enviado={len(trecho_documento)}")
                print("----- PROMPT (início) -----")
                print(prompt[:1000])
                print("----- DOCUMENTO (início) -----")
                print(trecho_documento[:1000])
                print("----- RESPOSTA BRUTA (início) -----")
                print(texto[:2000])
                print("===== IA DEBUG END =====")
            except Exception as log_err:
                print(f"[IA DEBUG] Falha ao imprimir diagnóstico: {log_err}")

            # ======================================================
            # Tentativa de conversão direta para JSON
            # ======================================================
            try:
                parsed = json.loads(texto)
                print("[IA DEBUG] json.loads(texto) OK (resposta já era JSON).")
                return parsed

            except Exception:
                print("[IA DEBUG] json.loads(texto) FALHOU – tentando limpar blocos ```json ... ```.")

                # Limpando formatação de código se vier com blocos
                if texto.startswith("```"):
                    texto_limpo = texto.replace("```json", "").replace("```", "").strip()
                else:
                    texto_limpo = texto

                try:
                    parsed = json.loads(texto_limpo)
                    print("[IA DEBUG] json.loads(texto_limpo) OK após limpeza.")
                    return parsed
                except Exception:
                    print("[IA DEBUG] Falha final ao interpretar JSON – devolvendo texto cru em 'resposta_texto'.")
                    return {"resposta_texto": texto}

        except Exception as e:
            print(f"[IA DEBUG] EXCEÇÃO NA CHAMADA OPENAI: {e}")
            return {
                "erro": f"❌ Falha na chamada OpenAI: {e}",
                "modelo_utilizado": self.model,
            }
